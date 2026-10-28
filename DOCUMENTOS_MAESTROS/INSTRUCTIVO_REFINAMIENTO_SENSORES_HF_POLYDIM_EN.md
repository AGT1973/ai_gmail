# CANONICAL INSTRUCTION: REFINEMENT & DISTILLATION OF SENSORIAL CAPABILITIES IN POLYDIM-EINSOF MODELS (HUGGING FACE / ATLAS ROADMAP)

> **Author:** Ariel García Traba — POLYDIM-EinsofOS Research Initiative  
> **Scope:** High-Performance Atlas Supercomputing Preparation | Fleet of 14 Hugging Face Models (`polydim-einsof`)  
> **Constitution:** Strict compliance with Rule 16, Rule 22, Rule 26, and Rule 38 (Silicon Certification with Exit Code 0).

---

## 1. Strategic Vision and Purpose

The purpose of this guide is to endow the canonical fleet of 14 POLYDIM models (hosted in `hf_export/` and in the `polydim-einsof` Hugging Face Hub organization) with the capability for zero-copy ingestion, isometric alignment, and direct geometric reasoning over **high-dimensional continuous physical sensory fields**:

1. **3D Radar (SAR / Phased Array Chirp):** $d_{\text{sensor}} = 4096$.
2. **Acoustic Sonar (Multibeam / Side-Scan):** $d_{\text{sensor}} = 2048$.
3. **3D LiDAR (Point Cloud / Time-of-Flight):** $d_{\text{sensor}} = 3072$.
4. **Medical Ultrasound / RF Doppler (Envelopes / I/Q):** $d_{\text{sensor}} = 2048$.
5. **Multispectral & Thermal Satellite (VIIRS / Sentinel-2):** $d_{\text{sensor}} = 4096$.

This procedure eliminates discrete 1D tokenization (BPE/WordPiece) for raw physical inputs, allowing direct zero-copy shared memory transfer (`PmtpShmBus`) with microsecond latency and 0 billed tokens.

---

## 2. Canonical Fleet of 14 POLYDIM Models (`hf_export/`)

| # | Model Identifier | Base Architecture | $d_{\text{model}}$ | Stiefel Adapter Dimension |
|---|---|---|---|---|
| 1 | `llama-3.1-8b-pmtp` | Meta LLaMA 3.1 | $4096$ | $\mathrm{St}(d_{\text{sensor}}, 4096)$ |
| 2 | `llama-3.2-3b-pmtp` | Meta LLaMA 3.2 | $3072$ | $\mathrm{St}(d_{\text{sensor}}, 3072)$ |
| 3 | `qwen2.5-coder-0.5b-pmtp` | Alibaba Qwen 2.5 | $896$ | $\mathrm{St}(d_{\text{sensor}}, 1024) \to 896$ |
| 4 | `qwen2.5-coder-1.5b-pmtp` | Alibaba Qwen 2.5 | $1536$ | $\mathrm{St}(d_{\text{sensor}}, 1536)$ |
| 5 | `deepseek-r1-1.5b-pmtp` | DeepSeek Distill | $1536$ | $\mathrm{St}(d_{\text{sensor}}, 1536)$ |
| 6 | `deepseek-r1-7b-pmtp` | DeepSeek Distill | $3584$ | $\mathrm{St}(d_{\text{sensor}}, 3584)$ |
| 7 | `gemma-2-2b-pmtp` | Google Gemma 2 | $2304$ | $\mathrm{St}(d_{\text{sensor}}, 2304)$ |
| 8 | `gemma-2-9b-pmtp` | Google Gemma 2 | $3584$ | $\mathrm{St}(d_{\text{sensor}}, 3584)$ |
| 9 | `phi-4-14b-pmtp` | Microsoft Phi-4 | $5120$ | $\mathrm{St}(d_{\text{sensor}}, 5120)$ |
| 10 | `phi-4-mini-3.8b-pmtp` | Microsoft Phi-4 | $3072$ | $\mathrm{St}(d_{\text{sensor}}, 3072)$ |
| 11 | `glm-4-9b-pmtp` | Zhipu AI GLM-4 | $4096$ | $\mathrm{St}(d_{\text{sensor}}, 4096)$ |
| 12 | `glm-5.3-prime-pmtp` | Zhipu AI GLM-5 | $4096$ | $\mathrm{St}(d_{\text{sensor}}, 4096)$ |
| 13 | `xiaomi-mimo-9b-pmtp` | Xiaomi MiMo | $4096$ | $\mathrm{St}(d_{\text{sensor}}, 4096)$ |
| 14 | `pplx-decider-27b-pmtp` | Perplexity Decider | $5120$ | $\mathrm{St}(d_{\text{sensor}}, 5120)$ |

---

## 3. PMTP Header Descriptor (`Wire 26505` — 64 Bytes)

Every sensory input is framed with the canonical 64-byte C-ABI header before entering the Stiefel projection layer:

```c
#include <stdint.h>

#pragma pack(push, 1)
typedef struct {
    uint32_t magic_header;       // 0x504D5450 ("PMTP")
    uint16_t sensor_type;        // 0x01: RADAR_3D, 0x02: SONAR, 0x03: LIDAR_3D,
                                 // 0x04: ULTRASOUND_MED, 0x05: SATELLITE_MS
    uint16_t dim_sensor;         // Input physical dimension d_sensor
    uint32_t sampling_rate_hz;   // Physical sampling frequency
    float    spatial_res_m;      // Spatial resolution per cell in meters
    uint64_t timestamp_ns;       // Silicon hardware timestamp (anti-replay)
    uint8_t  manifold_id;        // 0x01: Stiefel St(d_sensor, d_model)
    uint8_t  flags;              // Bit 0: FP64_HIGH_PREC, Bit 1: NEUMAIER_COMPENSATED
    uint8_t  reserved[38];       // Strict alignment to 64 bytes
} PmtpSensorDescriptor_t;
#pragma pack(pop)
```

---

## 4. Silicon Retraction & Loss Protocol

### 4.1 Strict Geometric Principles
1. **White Noise Veto:** Training on synthetic Gaussian noise is forbidden. Target latent states $\mathbf{y}_{\text{target}}$ must be extracted from verified teacher model activations (`output_hidden_states=True`) or analytical geodesic manifolds on $S^{d-1}$.
2. **Polar/QR Retraction:** The projection matrix $U$ stays orthonormal on the Stiefel manifold $\mathrm{St}(d_{\text{sensor}}, d_{\text{model}})$ via QR retraction at each optimizer step:
   $$U_{k+1} = \mathrm{qf}(U_k - \eta \nabla_{U} \mathcal{L})$$
3. **Geodesic Loss in $S^{D-1}$:**
   $$\mathcal{L}_{\text{geod}} = 1 - \frac{\langle \mathbf{z}_{\text{out}}, \mathbf{y}_{\text{target}} \rangle}{\lVert \mathbf{z}_{\text{out}} \rVert_2 \lVert \mathbf{y}_{\text{target}} \rVert_2} + \lambda \lVert U^\top U - I \rVert_F$$

---

## 5. Hugging Face Deployment & Ollama Integration

The resulting adapters are exported to `.safetensors` format with compensated Neumaier verification ($\lVert U^T U - I \rVert \le 10^{-15}$) and published to `https://huggingface.co/Polydim-Einsof`.
