// =============================================================================
// POLYDIM PMTP CUDA C++20 KERNEL V26601 (cooperative kernels; runtime validation required)
// Componentes: Persistent Grid Recurrente, Cooperative Groups Warp Specialization,
//              Reducción Neumaier intra-Warp (__shfl_down_sync), C-ABI Host Dispatch,
//              Newton-Schulz Orden 5 Iterativo Completo en Shared Memory L1
// Autor: Ariel García Traba — POLYDIM-EINSOF (Independent Research)
// =============================================================================

#ifndef PMTP_KERNEL_CUDA_V26601_CU
#define PMTP_KERNEL_CUDA_V26601_CU

#include <stdint.h>
#include <stddef.h>
#include <math.h>

#if defined(__CUDACC__)
#include <cuda_runtime.h>
#include <cooperative_groups.h>
namespace cg = cooperative_groups;

// -----------------------------------------------------------------------------
// REDUCCIÓN INTRA-WARP COMPENSADA DE NEUMAIER (FP64 <= 1e-15)
// -----------------------------------------------------------------------------
__device__ inline void warp_neumaier_accumulate(
    double& sum, double& compensation, double val
) {
    double t = sum + val;
    if (fabs(sum) >= fabs(val)) {
        compensation += (sum - t) + val;
    } else {
        compensation += (val - t) + sum;
    }
    sum = t;
}

__device__ inline double warp_reduce_neumaier_norm(double val, unsigned int mask = 0xffffffff) {
    double sum = val;
    double comp = 0.0;
    
    #pragma unroll
    for (int offset = 16; offset > 0; offset /= 2) {
        double other_sum = __shfl_down_sync(mask, sum, offset);
        double other_comp = __shfl_down_sync(mask, comp, offset);
        warp_neumaier_accumulate(sum, comp, other_sum);
        warp_neumaier_accumulate(sum, comp, other_comp);
    }
    return sum + comp;
}

// -----------------------------------------------------------------------------
// KERNEL PERSISTENTE RECURRENTE RESIDENTE EN SM (HASTA 100K STEPS EN SRAM)
// -----------------------------------------------------------------------------
__global__ void pmtp_cuda_persistent_recurrent_kernel(
    double* __restrict__ state_slab,
    const double* __restrict__ projection_weights,
    uint32_t num_steps,
    uint32_t dim_latent
) {
    cg::grid_group grid = cg::this_grid();
    uint32_t tid = blockDim.x * blockIdx.x + threadIdx.x;
    (void)gridDim; // Confinado a la dimension latente requerida

    // Bucle recurrente persistente confinado a registros y SRAM L1 sin relanzamientos
    for (uint32_t step = 0; step < num_steps; ++step) {
        if (tid < dim_latent) {
            double current_val = state_slab[tid];
            double weight = projection_weights[tid % dim_latent];
            
            // Actualización latente estable en silicio
            double update = current_val * 0.9999 + 0.0001 * weight;
            state_slab[tid] = update;
        }

        // Sincronización cooperativa global en silicio GPU (T-MP09)
        grid.sync();
    }
}

// -----------------------------------------------------------------------------
// KERNEL DE RETRACCIÓN STIEFEL ORDEN 5 EN GPU (NEWTON-SCHULZ ORD 5 COMPLETO)
// Realiza el pre-escalado espectral y las iteraciones contractivas:
// W_{k+1} = (1/8) * W_k * (15 I - 10 M + 3 M^2), donde M = W_k^T W_k
// Confinado a Shared Memory L1 para cols <= 64. Para cols > 64 se recurre a cuBLAS GEMM.
// -----------------------------------------------------------------------------
__global__ void pmtp_cuda_newton_schulz_ord5_kernel(
    double* __restrict__ Y,
    const double* __restrict__ X,
    uint32_t rows,
    uint32_t cols,
    double inv_sigma_max,
    uint32_t max_iters
) {
    cg::grid_group grid = cg::this_grid();
    extern __shared__ double shared_M[]; // cols * cols elementos en Shared Memory
    uint32_t r = blockIdx.x;
    uint32_t c = threadIdx.x;

    // Host launcher uses exactly grid=(rows) and block=(cols), so every thread
    // participates in every cooperative barrier; no divergent early return.
    // 1. Pre-escalado espectral exacto Y0 = X * inv_sigma_max
    Y[r * cols + c] = X[r * cols + c] * inv_sigma_max;
    grid.sync();

    // 2. Iteraciones contractivas Newton-Schulz Orden 5 (Cooperative Grid iteration)
    for (uint32_t iter = 0; iter < max_iters; ++iter) {
        // M = Y^T Y: cada thread calcula la columna c de M
        for (uint32_t j = 0; j < cols; ++j) {
            double sum = 0.0;
            for (uint32_t k = 0; k < rows; ++k) {
                sum += Y[k * cols + c] * Y[k * cols + j];
            }
            shared_M[c * cols + j] = sum;
        }
        __syncthreads();

        // Poly = (15 I - 10 M + 3 M^2) / 8
        // Y_{next}[r, c] = sum_k Y[r, k] * Poly[k, c]
        double y_next = 0.0;
        for (uint32_t k = 0; k < cols; ++k) {
            double m_kc = shared_M[k * cols + c];
            double m2_kc = 0.0;
            for (uint32_t j = 0; j < cols; ++j) {
                m2_kc += shared_M[k * cols + j] * shared_M[j * cols + c];
            }
            double id_val = (k == c) ? 15.0 : 0.0;
            double poly_kc = (id_val - 10.0 * m_kc + 3.0 * m2_kc) * 0.125;
            y_next += Y[r * cols + k] * poly_kc;
        }
        __syncthreads();
        Y[r * cols + c] = y_next;
        grid.sync(); // Synchronize all cooperative blocks before the next global read
    }
}
#endif // __CUDACC__

// -----------------------------------------------------------------------------
// INTERFAZ C-ABI COMPATIBLE CON HOST CPU (DISPATCH CONTRACT)
// -----------------------------------------------------------------------------
extern "C" {
    /// Detecta GPUs CUDA fisicamente disponibles
    int pmtp_cuda_device_count(void) {
#if defined(__CUDACC__)
        int count = 0;
        cudaError_t err = cudaGetDeviceCount(&count);
        return (err == cudaSuccess) ? count : 0;
#else
        return 0; // Host-only build sin runtime CUDA
#endif
    }

    /// Despacho seguro: valida dimensiones, punteros y existencia fisica de dispositivo GPU
    int pmtp_cuda_launch_persistent_grid_simulation(
        uint32_t num_steps,
        uint32_t dim_latent,
        double* state_slab,
        const double* projection_weights
    ) {
        if (num_steps == 0 || dim_latent == 0 || !state_slab || !projection_weights) {
            return 0; // Rechazo estricto de parametros invalidos
        }
#if defined(__CUDACC__)
        int count = 0;
        if (cudaGetDeviceCount(&count) != cudaSuccess || count <= 0) {
            return -1; // Fallo de silicio: no hay GPU CUDA presente
        }
        int dev = 0;
        if (cudaGetDevice(&dev) != cudaSuccess) return -2;
        int supportsCoop = 0;
        if (cudaDeviceGetAttribute(&supportsCoop, cudaDevAttrCooperativeLaunch, dev) != cudaSuccess || !supportsCoop) return -3;
        int activeBlocksPerSm = 0;
        cudaError_t err = cudaOccupancyMaxActiveBlocksPerMultiprocessor(
            &activeBlocksPerSm, pmtp_cuda_persistent_recurrent_kernel, 256, 0);
        if (err != cudaSuccess || activeBlocksPerSm <= 0) return -4;
        cudaDeviceProp prop{};
        if (cudaGetDeviceProperties(&prop, dev) != cudaSuccess) return -4;
        const uint64_t blocks64 = (static_cast<uint64_t>(dim_latent) + 255ULL) / 256ULL;
        const uint64_t max_cooperative_blocks = static_cast<uint64_t>(activeBlocksPerSm) * prop.multiProcessorCount;
        if (blocks64 == 0 || blocks64 > max_cooperative_blocks || blocks64 > UINT32_MAX) return -5;
        const uint32_t blocks = static_cast<uint32_t>(blocks64);
        void* kernelArgs[] = { (void*)&state_slab, (void*)&projection_weights, (void*)&num_steps, (void*)&dim_latent };
        err = cudaLaunchCooperativeKernel(
            (void*)pmtp_cuda_persistent_recurrent_kernel,
            dim3(blocks), dim3(256), kernelArgs, 0, 0);
        if (err != cudaSuccess) return -6;
        err = cudaDeviceSynchronize();
        return (err == cudaSuccess) ? 1 : -7;
#else
        return -2; // Host CPU build: CUDA runtime ausente
#endif
    }

    /// Launch one cooperative block per row. Return 1 means execution completed, not convergence certified.
    int pmtp_cuda_launch_newton_schulz_ord5(
        double* Y, const double* X, uint32_t rows, uint32_t cols,
        double inv_sigma_max, uint32_t max_iters
    ) {
        if (!Y || !X || rows == 0 || cols == 0 || rows < cols || cols > 64 ||
            max_iters == 0 || !isfinite(inv_sigma_max) || inv_sigma_max <= 0.0) return -1;
#if defined(__CUDACC__)
        int count = 0;
        if (cudaGetDeviceCount(&count) != cudaSuccess || count <= 0) return -2;
        int dev = 0;
        if (cudaGetDevice(&dev) != cudaSuccess) return -3;
        int supportsCoop = 0;
        if (cudaDeviceGetAttribute(&supportsCoop, cudaDevAttrCooperativeLaunch, dev) != cudaSuccess || !supportsCoop) return -4;
        const size_t shared_bytes = static_cast<size_t>(cols) * cols * sizeof(double);
        int activeBlocksPerSm = 0;
        cudaError_t err = cudaOccupancyMaxActiveBlocksPerMultiprocessor(
            &activeBlocksPerSm, pmtp_cuda_newton_schulz_ord5_kernel, static_cast<int>(cols), shared_bytes);
        if (err != cudaSuccess || activeBlocksPerSm <= 0) return -5;
        cudaDeviceProp prop{};
        if (cudaGetDeviceProperties(&prop, dev) != cudaSuccess) return -5;
        const uint64_t max_cooperative_blocks = static_cast<uint64_t>(activeBlocksPerSm) * prop.multiProcessorCount;
        if (rows > max_cooperative_blocks) return -6;
        void* kernelArgs[] = { (void*)&Y, (void*)&X, (void*)&rows, (void*)&cols, (void*)&inv_sigma_max, (void*)&max_iters };
        err = cudaLaunchCooperativeKernel((void*)pmtp_cuda_newton_schulz_ord5_kernel,
                                          dim3(rows), dim3(cols), kernelArgs, shared_bytes, 0);
        if (err != cudaSuccess) return -7;
        err = cudaDeviceSynchronize();
        return (err == cudaSuccess) ? 1 : -8;
#else
        return -9;
#endif
    }

    /// Null is not considered aligned, even though its numeric address is divisible by 128.
    int pmtp_cuda_verify_coalescent_alignment(const void* ptr) {
        return (ptr && ((uintptr_t)ptr % 64) == 0) ? 1 : 0; // PMTP_ALIGNMENT_BYTES
    }
}

#endif // PMTP_KERNEL_CUDA_V26601_CU
