"""POLYDIM — transporte de tensores y pre-escalado FP64.

Alcance:
- transfer(): copia de datos dentro de un dispositivo (NO es zero-copy),
  sin cambio implícito de dispositivo o dtype, sin solapamiento parcial.
- spectral_scale(): producto escalar, NO calcula sigma_max ni retrae a Stiefel.
- GPU Triton: implementaciones contiguas FP32/FP64 para copia y FP64
  para escalado. La ejecución GPU exige pruebas sobre el hardware objetivo.

Esta revisión conserva las firmas públicas V_TURING_004 y hace explícitas
las precondiciones y las rutas de fallback.
"""

from __future__ import annotations

import math
import struct
import sys
from typing import Any

import numpy as np

try:
    import torch
except ImportError:
    torch = None

try:
    if torch is not None and torch.cuda.is_available():
        import triton
        import triton.language as tl
    else:
        triton = None
except ImportError:
    triton = None

HAS_TORCH = torch is not None
HAS_TRITON = triton is not None

if HAS_TRITON:

    @triton.jit
    def pmtp_triton_coalescent_copy_kernel(
        src_ptr, dest_ptr, n_elements, BLOCK_SIZE: tl.constexpr
    ):
        """Copia 1:1. Solo para regiones CONTIGUAS y NO solapadas."""
        offsets = tl.program_id(0) * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)
        active = offsets < n_elements
        values = tl.load(src_ptr + offsets, mask=active, other=0)
        tl.store(dest_ptr + offsets, values, mask=active)

    @triton.jit
    def pmtp_triton_stiefel_scale_kernel(
        x_ptr, y_ptr, n_elements, scale_fp64_bits, BLOCK_SIZE: tl.constexpr
    ):
        """Escala FP64; bits de la constante preservados sin conversión FP32.

        En Triton una constante escalar Python float puede convertirse a FP32
        por inferencia de tipos. Se transmite su patrón IEEE-754 en int64,
        se convierte a tensor int64 y se reinterpreta bitwise como FP64.
        """
        offsets = tl.program_id(0) * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)
        active = offsets < n_elements
        scale_i64 = tl.full((), scale_fp64_bits, tl.int64)
        scale = scale_i64.to(tl.float64, bitcast=True)
        values = tl.load(x_ptr + offsets, mask=active, other=0)
        tl.store(y_ptr + offsets, values * scale, mask=active)


def _same_torch_view(a: Any, b: Any) -> bool:
    """Identidad lógica exacta; NO significa que una superposición sea segura."""
    return (
        a.data_ptr() == b.data_ptr()
        and a.shape == b.shape
        and a.stride() == b.stride()
        and a.dtype == b.dtype
        and a.device == b.device
    )


def _torch_shared_storage(a: Any, b: Any) -> bool:
    """Comprobación conservadora; puede rechazar slices disjuntas del mismo storage."""
    return a.untyped_storage().data_ptr() == b.untyped_storage().data_ptr()


def _same_numpy_view(a: np.ndarray, b: np.ndarray) -> bool:
    return (
        a.ctypes.data == b.ctypes.data
        and a.shape == b.shape
        and a.strides == b.strides
        and a.dtype == b.dtype
    )


def _provably_nonoverlapping(shape, strides, itemsize: int) -> bool:
    """Condición suficiente, conservadora, de inyectividad del índice físico.

    Ordena dimensiones por valor absoluto del stride en bytes y exige que
    cada dimensión comience fuera del span cubierto por las anteriores.
    Puede rechazar vistas no solapadas de strides exóticos; no las acepta
    sin poder demostrar inyectividad local.
    """
    if any(n == 0 for n in shape):
        return True
    pairs = sorted((abs(st), int(n)) for n, st in zip(shape, strides) if n > 1)
    span = itemsize
    for stride, dim in pairs:
        if stride < span:
            return False
        span += (dim - 1) * stride
    return True


def _valid_fp32_scale(scale: float) -> bool:
    with np.errstate(over="ignore", under="ignore", invalid="ignore"):
        converted = np.float32(scale)
    return bool(np.isfinite(converted) and converted > 0.0)


def _checked_scale(inv_sigma: float) -> float:
    try:
        scale = float(inv_sigma)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("inv_sigma debe ser un escalar real finito") from exc
    if not math.isfinite(scale) or scale <= 0.0:
        raise ValueError("inv_sigma debe ser finito y estrictamente positivo")
    return scale


class PolydimTritonSlabEngine:
    """Copia 1:1 y escalado escalar; no implementa un bus zero-copy.

    Política transfer(): False en entradas incompatibles, dispositivos
    cruzados, memoria solo lectura o solapamiento parcial; sin escrituras
    parciales cuando se rechaza por precondiciones verificables.
    """

    def __init__(self, block_size: int = 256):
        if type(block_size) is not int or not (128 <= block_size <= 1024):
            raise ValueError("block_size entero debe estar entre 128 y 1024")
        if block_size & (block_size - 1):
            raise ValueError("block_size debe ser potencia de dos")
        self.block_size = block_size
        self.num_warps = 8 if block_size == 1024 else 4
        self.is_gpu = HAS_TRITON

    def transfer(self, src: Any, dest: Any) -> bool:
        """Copia conservadora de elementos (no zero-copy, no reinterpreta dtype)."""
        if HAS_TORCH and isinstance(src, torch.Tensor) and isinstance(dest, torch.Tensor):
            if (
                src.shape != dest.shape
                or src.dtype != dest.dtype
                or src.device != dest.device
                or src.layout != torch.strided
                or dest.layout != torch.strided
                or src.device.type not in ("cpu", "cuda")
            ):
                return False
            if src.numel() == 0:
                return True
            if not _provably_nonoverlapping(
                dest.shape, tuple(st * dest.element_size() for st in dest.stride()),
                dest.element_size(),
            ):
                return False
            if _same_torch_view(src, dest):
                return True
            if _torch_shared_storage(src, dest):
                return False
            if (
                self.is_gpu
                and src.is_cuda
                and dest.is_cuda
                and src.is_contiguous()
                and dest.is_contiguous()
                and src.dtype in (torch.float32, torch.float64)
            ):
                blocks = triton.cdiv(src.numel(), self.block_size)
                pmtp_triton_coalescent_copy_kernel[(blocks,)](
                    src, dest, src.numel(), BLOCK_SIZE=self.block_size,
                    num_warps=self.num_warps,
                )
            else:
                dest.copy_(src)
            return True

        if isinstance(src, np.ndarray) and isinstance(dest, np.ndarray):
            if (
                src.shape != dest.shape
                or src.dtype != dest.dtype
                or src.dtype.hasobject
                or not dest.flags.writeable
            ):
                return False
            if not _provably_nonoverlapping(dest.shape, dest.strides, dest.itemsize):
                return False
            if src.size == 0 or _same_numpy_view(src, dest):
                return True
            if np.may_share_memory(src, dest):
                return False
            np.copyto(dest, src, casting="no")
            return True
        return False

    def spectral_scale(self, x: Any, inv_sigma: float):
        """Multiplica por inv_sigma; no calcula norma/espectro ni certifica Stiefel."""
        scale = _checked_scale(inv_sigma)
        if HAS_TORCH and isinstance(x, torch.Tensor):
            if x.layout != torch.strided or x.dtype not in (torch.float32, torch.float64):
                raise TypeError("spectral_scale requiere tensor torch strided FP32/FP64")
            if x.device.type not in ("cpu", "cuda"):
                raise TypeError("dispositivo torch no soportado")
            if x.dtype == torch.float32 and not _valid_fp32_scale(scale):
                raise ValueError("inv_sigma no representable como FP32 positivo")
            if x.numel() == 0:
                return torch.empty_like(x)
            if self.is_gpu and x.is_cuda and x.dtype == torch.float64 and x.is_contiguous():
                y = torch.empty_like(x)
                bits = struct.unpack("<q", struct.pack("<d", scale))[0]
                blocks = triton.cdiv(x.numel(), self.block_size)
                pmtp_triton_stiefel_scale_kernel[(blocks,)](
                    x, y, x.numel(), bits, BLOCK_SIZE=self.block_size,
                    num_warps=self.num_warps,
                )
                return y
            return x * scale

        if isinstance(x, np.ndarray):
            if x.dtype not in (np.dtype("float32"), np.dtype("float64")):
                raise TypeError("spectral_scale requiere NumPy FP32/FP64 nativo")
            if x.dtype == np.dtype("float32") and not _valid_fp32_scale(scale):
                raise ValueError("inv_sigma no representable como FP32 positivo")
            return x * scale
        raise TypeError(f"Tipo no soportado: {type(x)!r}")


def self_test():
    """Pruebas sin assert: se mantienen también bajo python -O."""
    engine = PolydimTritonSlabEngine(block_size=128)
    a = np.array([0., 42., -42., 1e-300], dtype=np.float64)
    b = np.zeros_like(a)
    if not engine.transfer(a, b) or not np.array_equal(a, b):
        raise RuntimeError("Transferencia NumPy incorrecta")
    if not np.array_equal(engine.spectral_scale(b, 0.5), b * 0.5):
        raise RuntimeError("Escalado NumPy incorrecto")
    scalar_src = np.array(12.0)
    scalar_dst = np.array(0.0)
    if not engine.transfer(scalar_src, scalar_dst) or scalar_dst.item() != 12.0:
        raise RuntimeError("Copia NumPy 0D incorrecta")
    if HAS_TORCH:
        device = "cuda" if engine.is_gpu else "cpu"
        t = torch.tensor([0., 42., -42., 1e-300], dtype=torch.float64, device=device)
        d = torch.zeros_like(t)
        if not engine.transfer(t, d) or not torch.equal(t, d):
            raise RuntimeError("Transferencia PyTorch incorrecta")
        if not torch.allclose(engine.spectral_scale(t, 0.5), t * 0.5, rtol=0, atol=0):
            raise RuntimeError("Escalado PyTorch incorrecto")
    if not engine.is_gpu:
        print("[CPU PASS / GPU BLOCKED] GPU Triton no ejecutada en este entorno")
        return None
    print("[GPU PASS provisional] autoprueba GPU ejecutada; faltan regresiones extensas")
    return True


if __name__ == "__main__":
    result = self_test()
    sys.exit(2 if result is None else (0 if result else 1))
