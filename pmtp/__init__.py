# PMTP - Polydimensional Manifold Transfer Protocol
# Canonical Package Interface with Native Silicon Dispatch (C++20 & Rust 2024)
import os, sys, ctypes
import numpy as np

from .pmtp_shm_bus import (
    PmtpShmBus,
    PmtpCompactHeader,
    PmtpLeasedTensor,
    PmtpDType,
    PmtpState
)

# 1. Neumaier Compensated Norm (FP64 drift <= 1e-15)
def neumaier_norm(vec):
    sum_val = 0.0
    c = 0.0
    arr = np.asarray(vec).ravel()
    for x in arr:
        val = float(x * x)
        t = sum_val + val
        if abs(sum_val) >= abs(val):
            c += (sum_val - t) + val
        else:
            c += (val - t) + sum_val
        sum_val = t
    return np.sqrt(sum_val + c)

# 2. Native Rust Newton-Schulz Order-5 Stiefel Retraction
_rust_lib = None
_dir = os.path.dirname(os.path.abspath(__file__))
_rust_dll_path = os.path.join(_dir, "pmtp_kernel_rust.dll")
if os.path.exists(_rust_dll_path):
    try:
        _rust_lib = ctypes.CDLL(_rust_dll_path)
        _rust_fn = _rust_lib.rust_newton_schulz_ord5_retract
        _rust_fn.argtypes = [
            ctypes.POINTER(ctypes.c_double),
            ctypes.c_size_t,
            ctypes.c_size_t,
            ctypes.c_size_t,
            ctypes.c_size_t,
            ctypes.c_double,
            ctypes.POINTER(ctypes.c_double),
        ]
        _rust_fn.restype = ctypes.c_int
    except Exception:
        _rust_lib = None

def rust_stiefel_retract(mat: np.ndarray, max_iters: int = 20, tol: float = 1e-12):
    """Retracts rectangular matrix to Stiefel manifold St(k, n) using native Rust Newton-Schulz."""
    if _rust_lib is None:
        raise RuntimeError("Rust native kernel (pmtp_kernel_rust.dll) not loaded")
    mat_f64 = np.ascontiguousarray(mat, dtype=np.float64)
    rows, cols = mat_f64.shape
    flat = mat_f64.ravel()
    ptr = flat.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    out_defect = ctypes.c_double(0.0)
    rc = _rust_lib.rust_newton_schulz_ord5_retract(
        ptr, len(flat), rows, cols, max_iters, tol, ctypes.byref(out_defect)
    )
    if rc != 0:
        raise RuntimeError(f"Rust Newton-Schulz retraction failed with code {rc}")
    return flat.reshape(rows, cols), out_defect.value

HEADER_SIZE = PmtpShmBus.HEADER_SIZE

from .pmtp_telepathy import AladinTelepathyClient

__all__ = [
    "PmtpShmBus",
    "PmtpCompactHeader",
    "PmtpLeasedTensor",
    "PmtpDType",
    "PmtpState",
    "HEADER_SIZE",
    "neumaier_norm",
    "rust_stiefel_retract",
    "AladinTelepathyClient",
]

