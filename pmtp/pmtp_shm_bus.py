# =============================================================================

# PMTP SHMBUS PYTHON ENGINE (RED TEAM PATCHSET; native atomics required)

# Componentes: PmtpCompactHeader, PmtpShmBus, DLPack Zero-Copy, Leases Atómicos

# =============================================================================



# ============================================================================

# PMTP TYPE DEFINITIONS & BINARY ABI (PYTHON 3.12+ CONTRACT)

# Proyecto: PMTP (Polydim Memory Tensor Protocol)

# Autor: Ariel García Traba (Investigador Independiente / EinsofOS)

# Base Teórica: Teoremas T-MP12, T-MP15, T-MP17, T-MP20, Enmienda E24-1, C11-1

# ============================================================================



import os

import sys

import time

import struct

import ctypes

import threading

import weakref

import secrets

import re

import gc

from enum import IntEnum

from typing import NamedTuple, Dict, Any, Tuple, Optional

from multiprocessing import shared_memory

import numpy as np

import hashlib

import hmac

import json

import tempfile



def _is_pid_alive(pid: int) -> bool:

    """Verifica fisicamente si un proceso esta vivo en el OS sin efectos secundarios."""

    if pid <= 0:

        return False

    if sys.platform == "win32":

        try:

            k32 = ctypes.windll.kernel32
            k32.OpenProcess.argtypes = [ctypes.c_uint32, ctypes.c_int, ctypes.c_uint32]
            k32.OpenProcess.restype = ctypes.c_void_p
            k32.GetExitCodeProcess.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong)]
            k32.GetExitCodeProcess.restype = ctypes.c_int
            k32.CloseHandle.argtypes = [ctypes.c_void_p]
            k32.CloseHandle.restype = ctypes.c_int

            h = k32.OpenProcess(0x1000, False, int(pid))

            if not h:

                return False

            exit_code = ctypes.c_ulong()

            res = k32.GetExitCodeProcess(h, ctypes.byref(exit_code))

            k32.CloseHandle(h)

            return bool(res) and (exit_code.value == 259)

        except Exception:

            return False

    else:

        try:

            os.kill(pid, 0)

            return True

        except ProcessLookupError:

            return False

        except PermissionError:

            return True

        except Exception:

            return False



# Carga transparente del C-ABI de silicio para operaciones atómicas hardware (CAS/fetch_add)

_NATIVE_LIB = None

try:

    _dir = os.path.dirname(os.path.abspath(__file__))

    _native_name = ("pmtp_kernel_cpp.dll" if os.name == "nt" else

                    "pmtp_kernel_cpp.dylib" if sys.platform == "darwin" else

                    "pmtp_kernel_cpp.so")

    _dll = os.path.join(_dir, _native_name)

    if os.path.exists(_dll):

        _NATIVE_LIB = ctypes.CDLL(_dll)

        _NATIVE_LIB.pmtp_shm_acquire_lease_raw.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint64)]

        _NATIVE_LIB.pmtp_shm_acquire_lease_raw.restype = ctypes.c_int

        _NATIVE_LIB.pmtp_shm_release_lease_raw.argtypes = [ctypes.c_void_p, ctypes.c_uint32]

        _NATIVE_LIB.pmtp_shm_release_lease_raw.restype = ctypes.c_int

        if hasattr(_NATIVE_LIB, "pmtp_shm_publish_raw"):

            _NATIVE_LIB.pmtp_shm_publish_raw.argtypes = [ctypes.c_void_p, ctypes.c_uint64, ctypes.c_void_p, ctypes.c_uint64, ctypes.c_uint16, ctypes.c_double, ctypes.POINTER(ctypes.c_uint32)]

            _NATIVE_LIB.pmtp_shm_publish_raw.restype = ctypes.c_int

        if hasattr(_NATIVE_LIB, "pmtp_shm_read_header_raw"):

            _NATIVE_LIB.pmtp_shm_read_header_raw.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

            _NATIVE_LIB.pmtp_shm_read_header_raw.restype = ctypes.c_int

        if hasattr(_NATIVE_LIB, "pmtp_shm_mark_destroying_raw"):

            _NATIVE_LIB.pmtp_shm_mark_destroying_raw.argtypes = [ctypes.c_void_p]

            _NATIVE_LIB.pmtp_shm_mark_destroying_raw.restype = ctypes.c_int

        if hasattr(_NATIVE_LIB, "pmtp_shm_commit_header_raw"):

            _NATIVE_LIB.pmtp_shm_commit_header_raw.argtypes = [ctypes.c_void_p]

            _NATIVE_LIB.pmtp_shm_commit_header_raw.restype = ctypes.c_int

        if hasattr(_NATIVE_LIB, "pmtp_shm_acquire_consistent_raw"):

            _NATIVE_LIB.pmtp_shm_acquire_consistent_raw.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint64)]

            _NATIVE_LIB.pmtp_shm_acquire_consistent_raw.restype = ctypes.c_int

except Exception:

    _NATIVE_LIB = None





def _attach_shared_memory(name: str):

    """Attach without registering an independent resource tracker when supported."""

    try:

        return shared_memory.SharedMemory(name=name, create=False, track=False)

    except TypeError as exc:  # No reliable independent-consumer tracker mode.

        raise RuntimeError(

            "Attach seguro requiere Python >=3.13 con SharedMemory(track=False); "

            "no se modifica el tracker compartido mediante API privada"

        ) from exc



PMTP_MAGIC_NUMBER = 0x504D5450  # ASCII "PMTP"

PMTP_VERSION_V1 = 0x0001

HEADER_COMPACT_SIZE = 64

WIRE_DESCRIPTOR_120B_SIZE = 120



class PmtpDType(IntEnum):

    FP32 = 0

    FP64 = 1

    FP16 = 2

    BF16 = 3

    INT32 = 4

    INT64 = 5

    INT16 = 6

    INT8 = 7

    UINT64 = 8

    UINT32 = 9

    UINT16 = 10

    UINT8 = 11



def numpy_to_pmtp_dtype(dtype) -> PmtpDType:

    dt = np.dtype(dtype)

    if dt == np.float32: return PmtpDType.FP32

    if dt == np.float64: return PmtpDType.FP64

    if dt == np.float16: return PmtpDType.FP16

    if dt == np.int32: return PmtpDType.INT32

    if dt == np.int64: return PmtpDType.INT64

    if dt == np.int16: return PmtpDType.INT16

    if dt == np.int8: return PmtpDType.INT8

    if dt == np.uint64: return PmtpDType.UINT64

    if dt == np.uint32: return PmtpDType.UINT32

    if dt == np.uint16: return PmtpDType.UINT16

    if dt == np.uint8: return PmtpDType.UINT8

    raise TypeError(f"DType no numérico o no soportado por PMTP C-ABI: {dtype}")



class PmtpState(IntEnum):

    IDLE = 0

    WRITING = 1

    COMMITTED = 2

    READING = 3



PMTP_DESTROYING_BIT = 1 << 63

PMTP_READERS_MASK = ~PMTP_DESTROYING_BIT



# Formato de cabecera compacta 64B; sincronización mediante primitivas nativas coordinadas:

# magic(4B I), version(2B H), dtype_id(2B H), active_slot(4B I), slab_id(4B I),

# num_elements(8B Q), timestamp_ns(8B Q), scale(8B d), generation(4B I),

# retired_slot0(1B ?), retired_slot1(1B ?), reserved_flags(2B H),

# state_and_readers(8B Q: Bit 63=DESTROYING_BIT, Bits 0-62=readers), reserved(8B 8s)

# Total = 4 + 2 + 2 + 4 + 4 + 8 + 8 + 8 + 4 + 1 + 1 + 2 + 8 + 8 = 64 bytes.

HEADER_COMPACT_FORMAT = "<IHHIIQQdI??HQ8s"

HEADER_COMPACT_STRUCT = struct.Struct(HEADER_COMPACT_FORMAT)

if HEADER_COMPACT_STRUCT.size != HEADER_COMPACT_SIZE:

    raise RuntimeError(f"Tamaño inválido: {HEADER_COMPACT_STRUCT.size}")



# Formato PolydimWireHeader 128B (canónico unificado C++ / Rust / Python - ABI-016):

# magic(4B I), version_major(2B H), version_minor(2B H), slab_uuid(16B 16s),

# num_elements(8B Q), payload_bytes(8B Q), timestamp_ns(8B Q), dtype(4B I),

# _pad_dtype(4B I), stiefel_defect(8B d), signature_blake2s(32B 32s), reserved(32B 32s)

# Total = 4 + 2 + 2 + 16 + 8 + 8 + 8 + 4 + 4 + 8 + 32 + 32 = 128 bytes.

WIRE_HEADER_128B_SIZE = 128

WIRE_HEADER_128B_FORMAT = "<IHH16sQQQIId32s32s"

WIRE_HEADER_128B_STRUCT = struct.Struct(WIRE_HEADER_128B_FORMAT)

if WIRE_HEADER_128B_STRUCT.size != WIRE_HEADER_128B_SIZE:

    raise RuntimeError(f"Tamaño inválido: {WIRE_HEADER_128B_STRUCT.size}")



# Formato descriptor wire extendido 120B (Enmienda E24-1):

# Descriptor extendido independiente de la cabecera compacta: campos explícitos

# con offsets little-endian definidos por WIRE_DESCRIPTOR_FORMAT (120 bytes).

# No debe interpretarse como los primeros 120 bytes de PmtpCompactHeader.

WIRE_DESCRIPTOR_FORMAT = "<IHHIIQQdIHH??HIIIIIQ32s8s"

WIRE_DESCRIPTOR_STRUCT = struct.Struct(WIRE_DESCRIPTOR_FORMAT)

if WIRE_DESCRIPTOR_STRUCT.size != WIRE_DESCRIPTOR_120B_SIZE:

    raise RuntimeError(f"Tamaño inválido: {WIRE_DESCRIPTOR_STRUCT.size}")





class PmtpCompactHeader(NamedTuple):

    magic: int

    version: int

    dtype_id: int

    active_slot: int

    slab_id: int

    num_elements: int

    timestamp_ns: int

    scale: float

    generation: int

    retired_slot0: bool

    retired_slot1: bool

    reserved_flags: int

    state_and_readers: int

    reserved: bytes



    @classmethod

    def unpack(cls, buffer: bytes) -> "PmtpCompactHeader":

        raw = HEADER_COMPACT_STRUCT.unpack(buffer[:HEADER_COMPACT_SIZE])

        return cls(*raw)



    def pack(self) -> bytes:

        return HEADER_COMPACT_STRUCT.pack(

            self.magic,

            self.version,

            self.dtype_id,

            self.active_slot,

            self.slab_id,

            self.num_elements,

            self.timestamp_ns,

            self.scale,

            self.generation,

            self.retired_slot0,

            self.retired_slot1,

            self.reserved_flags,

            self.state_and_readers,

            self.reserved

        )



    def to_dict(self) -> Dict[str, Any]:

        return {

            "magic": hex(self.magic),

            "version": self.version,

            "dtype": PmtpDType(self.dtype_id).name,

            "active_slot": self.active_slot,

            "slab_id": hex(self.slab_id),

            "num_elements": self.num_elements,

            "timestamp_ns": self.timestamp_ns,

            "scale": self.scale,

            "generation": self.generation,

            "retired_slot0": self.retired_slot0,

            "retired_slot1": self.retired_slot1,

            "active_readers": (self.state_and_readers & 0xFFFFFFFF) + ((self.state_and_readers >> 32) & 0x7FFFFFFF),

            "readers_slot0": self.state_and_readers & 0xFFFFFFFF,

            "readers_slot1": (self.state_and_readers >> 32) & 0x7FFFFFFF,

            "destroying": bool(self.state_and_readers & PMTP_DESTROYING_BIT),

        }





# ============================================================================

# PMTP SHM BUS V1.0 PRODUCTION ENGINE (ATOMIC-MONITOR-PROTECTED)

# Proyecto: PMTP (Polydim Memory Tensor Protocol)

# Autor: Ariel García Traba (Independent Research)

# Base Teórica: Teoremas T-MP12, T-MP15, T-MP17, T-MP20 (MP-55)

# ============================================================================



import os

import sys

import time

import struct

import threading

import weakref

import secrets

import re

import gc

from multiprocessing import shared_memory

from typing import Tuple, Dict, Any, Optional

import numpy as np





class _LeasedArray(np.ndarray):

    """NumPy view marker; the ctypes storage root, not this subclass, owns the lease."""

    _lease_owner = None



    def __array_finalize__(self, parent):

        # CR-3 FIX: Copies or slice views in Python heap do NOT retain the SHM lease!

        self._lease_owner = None





class PmtpLeasedTensor:

    """

    Contenedor con retención de lease de lectura atómico y anclaje de SharedMemory para DLPack/NumPy.

    Ancla el objeto SharedMemory nativo para garantizar que release_all() o unlinks

    NO desmapeen la memoria virtual (UnmapViewOfFile / munmap) mientras este tensor siga en uso,

    eliminando de raíz fallos de segmentación (SIGSEGV / 0xC0000005).

    """

    def __init__(self, bus: 'PmtpShmBus', slab_id: int, slot: int, generation: int, array: np.ndarray, shm: Any):

        self._bus = bus

        self._slab_id = slab_id

        self._slot = slot

        self._generation = generation

        # Root-buffer retention carries the lease through NumPy base-chain changes.

        # Do not introduce a wrapper/array ownership cycle.

        if isinstance(array, _LeasedArray):

            array._lease_owner = None

            array.flags.writeable = False  # protects ordinary NumPy callers; DLPack consumers must still be trusted

        self._array = array

        self._shm = shm

        self._released = False

        self._release_lock = threading.Lock()

        # Decrement only when the root storage buffer dies. Exporters must retain

        # this buffer through their base chain; DLPack consumers need separate QA.

        anchor = array

        while getattr(anchor, "base", None) is not None:

            anchor = anchor.base

        if not isinstance(anchor, ctypes.Array):

            raise TypeError("La vista leased debe tener un buffer raíz ctypes con lifetime propio")

        self._lease_finalizer = weakref.finalize(anchor, bus.release_reader_lease, slab_id, slot)

        bus._register_leased_view(self)



    @property

    def array(self) -> np.ndarray:

        if self._released or self._array is None:

            raise RuntimeError("La vista leased ya fue liberada; no puede reutilizarse")

        return self._array



    def release(self, immediate: bool = False):

        """Drop this wrapper's reference; the shared lease ends when all array exports die.

        If immediate=True, prohibited to prevent tearing physical memory under active DLPack/NumPy views."""

        if immediate:

            raise RuntimeError(

                "Liberación inmediata (immediate=True) prohibida: "

                "pueden existir vistas o tensores DLPack que retienen el almacenamiento compartido."

            )

        with self._release_lock:

            if self._released:

                return

            self._released = True

            self._array = None

        self._bus._unregister_leased_view(self)



    def __enter__(self):

        return self.array



    def __exit__(self, exc_type, exc_val, exc_tb):

        self.release()



    def __del__(self):

        # Destructors must not leak exceptions during interpreter shutdown.

        try:

            self.release()

        except Exception:

            pass



    def __array__(self, *args, **kwargs):

        return self.array.__array__(*args, **kwargs)



    def __getitem__(self, item):

        return self.array[item]



    def __setitem__(self, item, value):

        self.array[item] = value



    def __len__(self):

        return len(self.array)



    def __getattr__(self, name):

        return getattr(self.array, name)





class PmtpShmBus:

    """

    Bus de Memoria Compartida PMTP v1.0 con Doble Buffer Inmutable y Monitor Atómico.

    Garantías de Silicio:

    - Zero-copy: vistas NumPy y tensores PyTorch sin copia intermedia; el acceso DLPack es solo de lectura por contrato, no por enforcement del framework.

    - Cero torn-reads: conmutación atómica de slot y exclusión de escritura sobre slots leased.

    - Anti-Check-then-Act (T-MP20, MP-55): banderas de retiro explícitas en cabecera de 64 bytes.

    - Anti-ABA (T-MP17, MP-48): contadores atómicos de leases de lectura.

    """

    HEADER_SIZE = HEADER_COMPACT_SIZE



    def __init__(

        self,

        prefix: str = "pmtp",

        max_slabs: int = 64,

        max_dim: int = 8192,

        lease_timeout_ms: int = 30000,

        allow_multiwriter: bool = False,

        persistent_passive_slabs: bool = True,

        num_passive_slabs: int = 4,

    ):

        # Input validation (P12-P16 hardening)

        if not isinstance(prefix, str) or not prefix or '/' in prefix or '..' in prefix:

            raise ValueError(f"prefix must be a non-empty string without path separators: {prefix!r}")

        if not isinstance(max_slabs, int) or max_slabs <= 0:

            raise ValueError(f"max_slabs must be a positive integer: {max_slabs}")

        if not isinstance(max_dim, int) or max_dim <= 0:

            raise ValueError(f"max_dim must be a positive integer: {max_dim}")

        if not isinstance(lease_timeout_ms, int) or lease_timeout_ms < 0:

            raise ValueError(f"lease_timeout_ms must be a non-negative integer: {lease_timeout_ms}")

        self.prefix = prefix

        self.max_slabs = max_slabs

        self.max_dim = max_dim

        self.lease_timeout_ms = lease_timeout_ms

        self.allow_multiwriter = bool(allow_multiwriter)

        self.slabs: Dict[int, Dict[str, Any]] = {}

        self._next_slab_seq: int = 1

        self._local_lock = threading.RLock()

        # Weak references avoid keeping a lease alive solely because the bus tracks it.

        self._active_leased_views = weakref.WeakSet()

        self._local_lease_counts: Dict[Tuple[int, int], int] = {}

        self._deferred_slabs_to_close: Dict[int, Tuple[Any, bool]] = {}

        self._is_releasing: bool = False

        self._inflight_descriptor_publishes: set[int] = set()

        self._lease_records: Dict[int, Dict[str, Any]] = {}

        self._lease_seq: int = 1

        self.persistent_passive_slabs: bool = bool(persistent_passive_slabs)

        self.num_passive_slabs: int = max(1, min(int(num_passive_slabs), self.max_slabs))

        if self.persistent_passive_slabs:
            self._init_passive_slabs()

    def _init_passive_slabs(self):
        """Pre-allocate and maintain persistent passive slabs in shared memory."""
        for sid in range(1, self.num_passive_slabs + 1):
            try:
                self.allocate_tensor_slab(sid, self.max_dim, dtype=np.float64)
            except Exception:
                pass



    def _register_leased_view(self, view: 'PmtpLeasedTensor'):

        with self._local_lock:

            self._active_leased_views.add(view)



    def _unregister_leased_view(self, view: 'PmtpLeasedTensor'):

        with self._local_lock:

            self._active_leased_views.discard(view)

            if self._is_releasing and view._slab_id in self._deferred_slabs_to_close:

                # Comprobar si ya no quedan vistas vivas sobre este slab

                if not any(v._slab_id == view._slab_id for v in self._active_leased_views):

                    deferred = self._deferred_slabs_to_close.pop(view._slab_id, None)

                    if deferred is not None:

                        shm, is_creator = deferred

                        try:

                            shm.close()

                        except BufferError:

                            # Exported NumPy buffers still reference this mapping; keep it queued.

                            self._deferred_slabs_to_close[view._slab_id] = (shm, is_creator)

                        except (OSError, ValueError):

                            pass

                        else:

                            if is_creator:

                                try:

                                    shm.unlink()

                                except FileNotFoundError:

                                    pass



    def _compute_capability_token(self, epoch: int) -> str:

        """Deriva un token de capacidad criptográfico BLAKE2s de 256 bits a partir de la época del slab."""

        key = getattr(self, "_capability_key", b"PMTP_WRITER_CAP_KEY_V007")

        return hashlib.blake2s(str(epoch).encode("utf-8"), key=key).hexdigest()



    def get_writer_token(self, slab_id: int) -> str:

        """Obtiene el token de capacidad de escritura para compartir con procesos autorizados."""

        with self._local_lock:

            info = self.slabs.get(slab_id)

            if info is None:

                raise KeyError(f"Slab {slab_id} no encontrado")

            if not info.get("is_creator", False) and not info.get("is_writer", False):

                raise PermissionError(f"No tiene permisos de escritura en el slab {slab_id}")

            epoch = info.get("epoch", 0)

            return self._compute_capability_token(epoch)



    def attach_slab(self, slab_id: int, as_writer: bool = False, writer_token: Optional[str] = None) -> bool:

        """Attach only to a structurally valid slab; never guess an unknown dtype.



        SEC-015 hardening: as_writer is IGNORED. Attaching to an existing

        slab always grants read-only access. Only the creator (via

        allocate_tensor_slab) obtains write permission.

        """



        if as_writer and not writer_token:

            import warnings

            warnings.warn(

                "SEC-015: as_writer=True ignorado sin Capability Token válido. Solo el creador o portadores de token pueden escribir.",

                UserWarning, stacklevel=2

            )

        if isinstance(slab_id, bool) or not isinstance(slab_id, int) or not (1 <= slab_id <= 0xFFFFFFFF):

            raise ValueError("slab_id debe ser un entero entre 1 y UINT32_MAX")

        with self._local_lock:

            if self._is_releasing:

                raise RuntimeError("Bus en proceso de cierre; no se permiten nuevos attach")

            existing = self.slabs.get(slab_id)

            if existing is not None:

                return not existing.get("released", False)

            if len(self.slabs) >= self.max_slabs:

                raise RuntimeError(f"Límite máximo de slabs alcanzado ({self.max_slabs})")

            name = f"{self.prefix}_{slab_id:04x}"

            try:

                shm = _attach_shared_memory(name)

            except FileNotFoundError:

                return False

            except OSError:

                return False



            dtype_map = {

                PmtpDType.FP32.value: np.float32,

                PmtpDType.FP64.value: np.float64,

                PmtpDType.FP16.value: np.float16,

                PmtpDType.INT32.value: np.int32,

                PmtpDType.INT64.value: np.int64,

                PmtpDType.INT16.value: np.int16,

                PmtpDType.INT8.value: np.int8,

                PmtpDType.UINT64.value: np.uint64,

                PmtpDType.UINT32.value: np.uint32,

                PmtpDType.UINT16.value: np.uint16,

                PmtpDType.UINT8.value: np.uint8,

            }

            try:

                if len(shm.buf) < HEADER_COMPACT_SIZE:

                    return False

                hdr = self._read_header_from_mapping(shm)

                dtype = dtype_map.get(hdr.dtype_id)

                if (hdr.magic != PMTP_MAGIC_NUMBER or hdr.version != PMTP_VERSION_V1 or

                        hdr.slab_id != slab_id or hdr.active_slot not in (0, 1) or

                        hdr.num_elements <= 0 or hdr.num_elements > self.max_dim or

                        dtype is None or struct.unpack("<Q", hdr.reserved)[0] == 0):

                    return False

                itemsize = np.dtype(dtype).itemsize

                payload_bytes = hdr.num_elements * itemsize

                expected_size = HEADER_COMPACT_SIZE + 2 * payload_bytes

                if os.name == "nt":

                    if len(shm.buf) < expected_size:

                        return False

                else:

                    if expected_size != len(shm.buf):

                        return False

                hdr_epoch = struct.unpack("<Q", hdr.reserved)[0]

                is_auth_writer = False

                if writer_token is not None:

                    expected = self._compute_capability_token(hdr_epoch)

                    is_auth_writer = hmac.compare_digest(writer_token, expected)

                elif self.allow_multiwriter:

                    is_auth_writer = bool(as_writer)



                self.slabs[slab_id] = {

                    "shm": shm, "num_elements": hdr.num_elements, "dtype": dtype,

                    "itemsize": itemsize, "payload_bytes": payload_bytes, "name": name,

                    "released": False, "published_at_ns": hdr.timestamp_ns, "is_creator": False,

                    "is_writer": is_auth_writer,

                    "scale": hdr.scale, "epoch": hdr_epoch

                }

                return True

            finally:

                # Ownership transfers to self.slabs only after all validation succeeds.

                if slab_id not in self.slabs or self.slabs[slab_id].get("shm") is not shm:

                    try:

                        shm.close()

                    except (BufferError, OSError, ValueError):

                        pass



    def allocate_tensor_slab(

        self,

        slab_id: int,

        num_elements: int,

        dtype=np.float64,

        scale: float = 1.0,

        writer_token: Optional[str] = None

    ) -> shared_memory.SharedMemory:

        """Create a new slab exclusively or attach only to an exact compatible slab."""



        with self._local_lock:

            if self._is_releasing:

                raise RuntimeError("Bus en proceso de cierre; no se permiten nuevas asignaciones")

            if isinstance(slab_id, bool) or not isinstance(slab_id, int) or not (1 <= slab_id <= 0xFFFFFFFF):

                raise ValueError("slab_id debe ser un entero entre 1 y UINT32_MAX")

            if isinstance(num_elements, bool) or not isinstance(num_elements, (int, np.integer)) or num_elements <= 0 or num_elements > 0xFFFFFFFFFFFFFFFF:

                raise ValueError(f"num_elements debe ser un entero positivo representable en uint64: {num_elements}")

            if not np.isfinite(scale):

                raise ValueError("scale debe ser finito")

            np_dt = np.dtype(dtype)

            if np_dt.kind not in ("f", "i", "u"):

                raise TypeError(f"DType no numérico o no serializable rechazado: {dtype}")

            dtype_id = numpy_to_pmtp_dtype(np_dt).value

            itemsize = np_dt.itemsize

            if num_elements > (sys.maxsize - HEADER_COMPACT_SIZE) // (2 * itemsize):

                raise OverflowError("El tamaño solicitado excede el límite de direccionamiento de esta plataforma")

            payload_bytes = num_elements * itemsize

            total_nbytes = HEADER_COMPACT_SIZE + 2 * payload_bytes

            commit_header = getattr(_NATIVE_LIB, "pmtp_shm_commit_header_raw", None) if _NATIVE_LIB is not None else None

            if commit_header is None:

                raise RuntimeError("No se puede crear un slab seguro sin pmtp_shm_commit_header_raw en la biblioteca nativa")

            name = f"{self.prefix}_{slab_id:04x}"

            if num_elements > self.max_dim:

                raise ValueError(f"num_elements ({num_elements}) excede max_dim configurado ({self.max_dim})")

            with self._local_lock:

                existing = self.slabs.get(slab_id)

                if existing is not None:

                    if (not existing.get("released", False) and existing["num_elements"] == num_elements and

                            np.dtype(existing["dtype"]) == np_dt and existing.get("scale", 1.0) == float(scale)):

                        return existing["shm"]

                    raise RuntimeError(f"Slab {slab_id} ya existe en esta instancia con otro esquema/escala/estado; no se reemplaza implícitamente")

                if len(self.slabs) >= self.max_slabs:

                    raise RuntimeError(f"Límite máximo de slabs alcanzado ({self.max_slabs})")

            try:

                shm = shared_memory.SharedMemory(name=name, create=True, size=total_nbytes)

                is_creator = True

            except FileExistsError:

                # P15-01 mitigation: the SHM name may be visible before

                # ftruncate() completes.  Retry with bounded back-off so a

                # legitimate second client does not crash on an empty mapping.

                _P15_MAX_RETRIES = 40

                _P15_SLEEP_S = 0.005

                shm = None

                for _p15_attempt in range(_P15_MAX_RETRIES):

                    try:

                        shm = _attach_shared_memory(name)

                    except (ValueError, OSError) as _p15_exc:

                        # ValueError: "cannot mmap an empty file" on POSIX

                        # OSError: possible transient access error

                        if _p15_attempt >= _P15_MAX_RETRIES - 1:

                            raise RuntimeError(

                                f"P15-01: slab '{name}' exists but failed to attach after "

                                f"{_P15_MAX_RETRIES} retries ({_P15_SLEEP_S*_P15_MAX_RETRIES:.1f}s). "

                                f"Creator may have died before ftruncate. Last error: {_p15_exc}"

                            ) from _p15_exc

                        time.sleep(_P15_SLEEP_S)

                        continue

                    # Successfully attached; verify it has the expected size.

                    if len(shm.buf) < total_nbytes:

                        # Still being initialized (ftruncate in progress or creator sizing).

                        try:

                            shm.close()

                        except Exception:

                            pass

                        shm = None

                        if _p15_attempt >= _P15_MAX_RETRIES - 1:

                            raise RuntimeError(

                                f"P15-01: slab '{name}' has size {len(shm.buf) if shm else 0} "

                                f"after {_P15_MAX_RETRIES} retries; expected {total_nbytes}. "

                                f"Creator may have died during initialization."

                            )

                        time.sleep(_P15_SLEEP_S)

                        continue

                    # Check if magic/header is committed (non-zero magic).

                    try:

                        _p15_magic = struct.unpack_from("<I", shm.buf, 0)[0]

                    except Exception:

                        _p15_magic = 0

                    if _p15_magic == 0:

                        try:

                            shm.close()

                        except Exception:

                            pass

                        shm = None

                        if _p15_attempt >= _P15_MAX_RETRIES - 1:

                            raise RuntimeError(

                                f"P15-01: slab '{name}' sized correctly but magic=0 after "

                                f"{_P15_MAX_RETRIES} retries. Creator alive but header not committed."

                            )

                        time.sleep(_P15_SLEEP_S)

                        continue

                    break  # Attached, sized, magic committed.

                if shm is None:

                    raise RuntimeError(f"P15-01: failed to attach slab '{name}' (should not reach here)")

                is_creator = False



            try:

                if os.name == "nt":

                    if len(shm.buf) < total_nbytes:

                        raise ValueError(f"Tamaño de slab incompatible en Windows: {len(shm.buf)} menor que {total_nbytes}")

                else:

                    if len(shm.buf) != total_nbytes:

                        raise ValueError(f"Tamaño de slab incompatible: {len(shm.buf)} != {total_nbytes}")

                if is_creator:

                    timestamp_ns = time.time_ns()

                    epoch = secrets.randbits(64) or 1

                    header_bytes = HEADER_COMPACT_STRUCT.pack(

                        PMTP_MAGIC_NUMBER, PMTP_VERSION_V1, dtype_id, 0, slab_id,

                        num_elements, timestamp_ns, scale, 0, False, True, 0, 0, struct.pack("<Q", epoch)  # Generation 0 = EMPTY state

                    )

                    # Magic stays zero until all other fields are initialized; the native

                    # release-store of magic is the publication/initialization commit.

                    shm.buf[4:HEADER_COMPACT_SIZE] = header_bytes[4:HEADER_COMPACT_SIZE]

                    addr = ctypes.addressof(ctypes.c_char.from_buffer(shm.buf))

                    rc = commit_header(addr)

                    if rc != 0:

                        raise RuntimeError(f"No se pudo confirmar la inicialización de slab {slab_id}: código {rc}")

                else:

                    hdr = self._read_header_from_mapping(shm)

                    if (hdr.magic != PMTP_MAGIC_NUMBER or hdr.version != PMTP_VERSION_V1 or

                            hdr.slab_id != slab_id or hdr.dtype_id != dtype_id or

                            hdr.num_elements != num_elements or hdr.active_slot not in (0, 1) or

                            hdr.scale != float(scale) or

                            struct.unpack("<Q", hdr.reserved)[0] == 0):

                        raise ValueError("El segmento existente tiene una cabecera incompatible; no se modifica")

                hdr_epoch = epoch if is_creator else struct.unpack("<Q", hdr.reserved)[0]

                is_auth_writer = False

                if is_creator:

                    is_auth_writer = True

                elif writer_token is not None:

                    expected = self._compute_capability_token(hdr_epoch)

                    is_auth_writer = hmac.compare_digest(writer_token, expected)

                elif self.allow_multiwriter:

                    is_auth_writer = True



                self.slabs[slab_id] = {

                    "shm": shm, "num_elements": num_elements, "dtype": np_dt.type,

                    "itemsize": itemsize, "payload_bytes": payload_bytes, "name": name,

                    "is_creator": is_creator, "is_writer": is_auth_writer, "released": False, "scale": float(scale),

                    "epoch": hdr_epoch

                }

                return shm

            except Exception:

                try:

                    shm.close()

                except (BufferError, OSError, ValueError):

                    pass

                if is_creator:

                    try:

                        shm.unlink()

                    except FileNotFoundError:

                        pass

                raise



    @staticmethod

    def _read_header_from_mapping(shm: Any) -> PmtpCompactHeader:

        reader = getattr(_NATIVE_LIB, "pmtp_shm_read_header_raw", None) if _NATIVE_LIB is not None else None

        if reader is None:

            raise RuntimeError("Lectura coherente de cabecera no disponible: reconstruye la biblioteca nativa compatible")

        addr = ctypes.addressof(ctypes.c_char.from_buffer(shm.buf))

        out = ctypes.create_string_buffer(HEADER_COMPACT_SIZE)

        for _ in range(5000):

            rc = reader(addr, ctypes.cast(out, ctypes.c_void_p))

            if rc == 0:

                return PmtpCompactHeader.unpack(out.raw)

            if rc not in (-2, -6):

                raise RuntimeError(f"Lectura nativa de cabecera falló: código {rc}")

            time.sleep(0.0001)

        raise TimeoutError("Cabecera no inicializada o writer lock ocupado/abandonado tras 500 ms")



    def read_header(self, slab_id: int) -> PmtpCompactHeader:

        """Read a consistent header while holding the local mapping-lifetime lock."""

        with self._local_lock:

            info = self.slabs.get(slab_id)

            if info is None:

                raise KeyError(f"Slab {slab_id} no está adjunto")

            return self._read_header_from_mapping(info["shm"])



    def publish_snapshot_atomic(

        self,

        slab_id: int,

        data: np.ndarray,

        max_retries: int = 100,

        retry_delay_s: float = 0.0005

    ) -> int | bool:

        """Return the generation assigned by the native commit, or False on slot contention timeout."""

        native_publish = getattr(_NATIVE_LIB, "pmtp_shm_publish_raw", None) if _NATIVE_LIB is not None else None

        if native_publish is None:

            raise RuntimeError("Publicación segura no disponible: reconstruye la biblioteca nativa con pmtp_shm_publish_raw")

        if isinstance(max_retries, bool) or not isinstance(max_retries, int) or max_retries < 1:

            raise ValueError("max_retries debe ser un entero positivo")

        if not np.isfinite(retry_delay_s) or retry_delay_s < 0:

            raise ValueError("retry_delay_s debe ser finito y no negativo")

        with self._local_lock:

            info = self.slabs.get(slab_id)

            if info is None or info.get("released", False):

                raise RuntimeError(f"Slab {slab_id} no está adjunto o fue retirado")

            if self._is_releasing:

                raise RuntimeError("Bus en proceso de cierre; publicación rechazada")

            if not (info.get("is_creator", False) or info.get("is_writer", False)):

                raise PermissionError("Publicación prohibida: esta instancia no es propietaria del slab (SEC-015)")

            dtype = info["dtype"]

            expected_elements = info["num_elements"]

        raw_arr = np.asarray(data)

        target_dt = np.dtype(dtype)

        if raw_arr.dtype != target_dt:

            raise TypeError(f"Conversión implícita de tipo prohibida en transporte exacto: {raw_arr.dtype} != {target_dt}")

        if raw_arr.dtype.kind == "f" and not np.isfinite(raw_arr).all():

            raise ValueError("Payload numérico contiene valores no finitos (NaN o Infinito)")

        arr = raw_arr.reshape(-1)

        if arr.size != expected_elements:

            raise ValueError(f"Número de elementos incompatible: {arr.size} != {expected_elements}")

        arr = np.ascontiguousarray(arr)

        data_ptr = ctypes.c_void_p(arr.ctypes.data)

        dtype_id = numpy_to_pmtp_dtype(dtype).value

        for _attempt in range(max_retries):

            with self._local_lock:

                info = self.slabs.get(slab_id)

                if info is None or info.get("released", False) or self._is_releasing:

                    raise RuntimeError("Slab detach/cleanup iniciado antes de publicar")

                if not (info.get("is_creator", False) or info.get("is_writer", False)):

                    raise PermissionError("Publicación prohibida: instancia adjunta sin propiedad (SEC-015)")

                shm = info["shm"]

                buf_addr = ctypes.addressof(ctypes.c_char.from_buffer(shm.buf))

                out_generation = ctypes.c_uint32(0)

                rc = native_publish(buf_addr, len(shm.buf), data_ptr, arr.size, dtype_id,

                                    float(info.get("scale", 1.0)), ctypes.byref(out_generation))

                if rc == 0:

                    info["last_published_generation"] = out_generation.value

                    info["published_at_ns"] = time.time_ns()

                    return int(out_generation.value)

            if rc in (-4, -3, -2, -1, -7, -8, -9, -10, -11):

                raise RuntimeError(f"Publicación nativa rechazada con código {rc}; no se altera la cabecera por fallback")

            if rc in (-5, -6):

                time.sleep(retry_delay_s)

                continue

            raise RuntimeError(f"Error nativo de publicación no reconocido: {rc}")

        return False



    def acquire_reader_lease(

        self,

        slab_id: int,

        max_retries: int = 50,

        retry_delay_s: float = 0.0003,

    ) -> Tuple[int, int]:

        """Acquire a coherent slot/generation lease and record local ownership.



        Requires the native *consistent* path. Never silently fall back to the

        older raw slot-based acquisition with a torn slot/generation window.

        """

        native_acquire = getattr(_NATIVE_LIB, "pmtp_shm_acquire_consistent_raw", None) if _NATIVE_LIB is not None else None

        if native_acquire is None:

            raise RuntimeError("La biblioteca nativa debe exportar pmtp_shm_acquire_consistent_raw")

        if isinstance(max_retries, bool) or not isinstance(max_retries, int) or max_retries < 1:

            raise ValueError("max_retries debe ser un entero positivo")

        if not np.isfinite(retry_delay_s) or retry_delay_s < 0:

            raise ValueError("retry_delay_s debe ser finito y no negativo")

        for _ in range(max_retries):

            with self._local_lock:

                if self._is_releasing:

                    raise RuntimeError("Bus en proceso de cierre; nuevos leases rechazados")

                info = self.slabs.get(slab_id)

                if info is None or info.get("released", False):

                    raise RuntimeError(f"Slab {slab_id} no está adjunto o fue retirado")

                addr = ctypes.addressof(ctypes.c_char.from_buffer(info["shm"].buf))

                out_slot = ctypes.c_uint32(0)

                out_gen = ctypes.c_uint64(0)

                rc = native_acquire(addr, ctypes.byref(out_slot), ctypes.byref(out_gen))

                if rc == 0:

                    slot = int(out_slot.value)

                    if slot not in (0, 1) or out_gen.value == 0:

                        # Defensive fail-closed: release the lease if the native

                        # contract was violated before exposing any memory view.

                        if slot in (0, 1):

                            _NATIVE_LIB.pmtp_shm_release_lease_raw(addr, slot)

                        raise RuntimeError("Respuesta incoherente del acquire nativo")

                    key = (slab_id, slot)

                    self._local_lease_counts[key] = self._local_lease_counts.get(key, 0) + 1

                    lid = self._lease_seq

                    self._lease_seq += 1

                    now_m = time.monotonic()

                    self._lease_records[lid] = {

                        "lease_id": lid,

                        "slab_id": slab_id,

                        "slot": slot,

                        "generation": int(out_gen.value),

                        "pid": os.getpid(),

                        "acquired_at": now_m,

                        "last_heartbeat": now_m,

                        "released": False,

                    }

                    return slot, int(out_gen.value)

                if rc == -10:

                    raise RuntimeError(f"Slab {slab_id} está EMPTY")

                if rc == -3:

                    raise RuntimeError(f"Slab {slab_id} en destrucción")

                if rc != -6:

                    raise RuntimeError(f"Adquisición nativa rechazada: código {rc}")

            time.sleep(retry_delay_s)

        raise TimeoutError(f"No se pudo obtener lease consistente en slab {slab_id}")



    def release_reader_lease(self, slab_id: int, slot: int):

        """Release only a lease acquired through this bus instance."""

        if slot not in (0, 1):

            raise ValueError(f"Slot inválido: {slot}")

        if _NATIVE_LIB is None:

            raise RuntimeError("Liberación de lease segura no disponible: se requiere biblioteca nativa")

        with self._local_lock:

            info = self.slabs.get(slab_id)

            key = (slab_id, slot)

            owned = self._local_lease_counts.get(key, 0)

            if info is None or owned <= 0:

                raise RuntimeError(f"Esta instancia no posee un lease activo para slab={slab_id}, slot={slot}")

            buf_addr = ctypes.addressof(ctypes.c_char.from_buffer(info["shm"].buf))

            rc = _NATIVE_LIB.pmtp_shm_release_lease_raw(buf_addr, slot)

            if rc != 0:

                raise RuntimeError(f"Liberación nativa de lease falló: código {rc}")

            if owned == 1:

                self._local_lease_counts.pop(key, None)

            else:

                self._local_lease_counts[key] = owned - 1

            for lid, rec in self._lease_records.items():

                if rec["slab_id"] == slab_id and rec["slot"] == slot and not rec["released"]:

                    rec["released"] = True

                    break



    def read_snapshot_copy(

        self, slab_id: int, *, expected_epoch: Optional[int] = None,

        expected_generation: Optional[int] = None,

    ) -> Tuple[np.ndarray, int]:

        """Pin one mapping/epoch/generation atomically under the local lock.



        Release the Python lifecycle lock before the expensive payload copy;

        the acquired native lease prevents slot reuse until finally.

        """

        with self._local_lock:

            info = self.slabs.get(slab_id)

            if info is None or info.get("released", False):

                raise RuntimeError(f"Slab {slab_id} no está adjunto o fue retirado")

            if expected_epoch is not None and info.get("epoch") != expected_epoch:

                raise RuntimeError(f"Stale descriptor epoch rejected for slab {slab_id}")

            shm = info["shm"]

            slot, gen = self.acquire_reader_lease(slab_id)

            try:

                if expected_generation is not None and gen != expected_generation:

                    raise RuntimeError(f"ABA generation mismatch on slab {slab_id}: expected {expected_generation}, got {gen}")

                offset = HEADER_COMPACT_SIZE + slot * info["payload_bytes"]

                view = np.ndarray(shape=(info["num_elements"],), dtype=info["dtype"],

                                  buffer=shm.buf, offset=offset)

            except BaseException:

                self.release_reader_lease(slab_id, slot)

                raise

        try:

            return view.copy(), gen

        finally:

            self.release_reader_lease(slab_id, slot)



    def read_snapshot_leased(

        self, slab_id: int, *, expected_epoch: Optional[int] = None,

        expected_generation: Optional[int] = None,

    ) -> PmtpLeasedTensor:

        """Return a pinned zero-copy view. No physical read-only isolation.



        Both the expected epoch and generation are checked before exposing the

        view and while the mapping is protected by the lifecycle lock/lease.

        """

        with self._local_lock:

            info = self.slabs.get(slab_id)

            if info is None or info.get("released", False):

                raise RuntimeError(f"Slab {slab_id} no está adjunto o fue retirado")

            if expected_epoch is not None and info.get("epoch") != expected_epoch:

                raise RuntimeError(f"Stale descriptor epoch rejected for slab {slab_id}")

            shm = info["shm"]

            slot, gen = self.acquire_reader_lease(slab_id)

            try:

                if expected_generation is not None and gen != expected_generation:

                    raise RuntimeError(f"ABA generation mismatch on slab {slab_id}: expected {expected_generation}, got {gen}")

                offset = HEADER_COMPACT_SIZE + slot * info["payload_bytes"]

                # Every zero-copy derivative, including np.asarray, retains this

                # root buffer. Finalizing the ndarray subclass alone is unsafe:

                # NumPy can bypass that subclass in its base chain.

                anchor_type = ctypes.c_ubyte * info["payload_bytes"]

                anchor = anchor_type.from_buffer(shm.buf, offset)

                raw_view = np.ndarray(shape=(info["num_elements"],), dtype=info["dtype"],

                                      buffer=anchor).view(_LeasedArray)

                return PmtpLeasedTensor(self, slab_id, slot, gen, raw_view, shm)

            except BaseException:

                self.release_reader_lease(slab_id, slot)

                raise



    def get_zero_copy_dlpack_tensor(self, slab_id: int) -> PmtpLeasedTensor:

        """

        Soporte nativo DLPack Zero-Copy con anclaje seguro de ciclo de vida.

        Retorna PmtpLeasedTensor que mantiene el mapping de memoria abierto

        y libera el reader lease al destruirse el objeto en PyTorch/Python.

        """

        return self.read_snapshot_leased(slab_id)



    def detach_slab(self, slab_id: int):

        """Detach a consumer mapping only when this instance owns no active leases for it."""

        with self._local_lock:

            if self._is_releasing:

                raise RuntimeError("Bus en proceso de cierre")

            info = self.slabs.get(slab_id)

            if info is None:

                return

            if any(sid == slab_id and count for (sid, _slot), count in self._local_lease_counts.items()):

                raise RuntimeError(f"No se puede detach slab {slab_id}: esta instancia conserva leases activos")

            if info.get("is_creator", False):

                raise RuntimeError(f"Slab {slab_id} es propiedad de esta instancia; usa cleanup/release_all")

            try:

                info["shm"].close()

            except (BufferError, OSError, ValueError) as exc:

                raise RuntimeError(f"No se pudo cerrar slab {slab_id}; mapping conservado: {exc}") from exc

            self.slabs.pop(slab_id, None)



    def detach_all(self):

        """Detach consumer mappings; abort atomically if any local lease remains active."""

        with self._local_lock:

            if self._is_releasing:

                raise RuntimeError("Bus en proceso de cierre")

            active = {sid: count for (sid, _slot), count in self._local_lease_counts.items() if count}

            if active:

                raise RuntimeError(f"No se puede detach_all: quedan leases locales activos {active}")

            owners = [sid for sid, info in self.slabs.items() if info.get("is_creator", False)]

            if owners:

                raise RuntimeError(f"detach_all no destruye slabs propietarios {owners}; usa cleanup/release_all")

            for sid, info in list(self.slabs.items()):

                try:

                    info["shm"].close()

                except (BufferError, OSError, ValueError) as exc:

                    raise RuntimeError(f"No se pudo cerrar slab {sid}; mapping conservado: {exc}") from exc

                self.slabs.pop(sid, None)



    def release_all(self):

        """Close mappings safely; owners atomically stop new leases and drain existing readers.



        If readers do not drain before the timeout, this method raises and retains all mappings

        so the caller can release readers and retry. It never unlinks a live segment.

        """

        with self._local_lock:

            if self._inflight_descriptor_publishes:

                raise RuntimeError("Cierre rechazado: publicaciones de descriptor en curso")

            items = list(self.slabs.items())

            if not items:

                self._is_releasing = False

                return

            mark_destroying = getattr(_NATIVE_LIB, "pmtp_shm_mark_destroying_raw", None) if _NATIVE_LIB is not None else None

            if any(info.get("is_creator", False) for _, info in items) and mark_destroying is None:

                raise RuntimeError("Cierre seguro del propietario requiere biblioteca nativa con pmtp_shm_mark_destroying_raw")

            self._is_releasing = True



        try:

            # Prevent new leases before draining. This operation is an atomic fetch_or in native code.

            for sid, info in items:

                if info.get("is_creator", False):

                    addr = ctypes.addressof(ctypes.c_char.from_buffer(info["shm"].buf))

                    rc = mark_destroying(addr)

                    if rc != 0:

                        raise RuntimeError(f"No se pudo marcar slab {sid} en destrucción: código {rc}")



            deadline = time.monotonic() + 2.0  # CR-2/E-008: 2000 ms contract

            poll_count = 0

            while True:

                # Collect abandoned wrapper/ndarray cycles; a still-live DLPack tensor keeps

                # the ndarray reachable and therefore keeps its shared lease active.

                if poll_count % 20 == 0:

                    gc.collect()

                poll_count += 1

                local_live = list(self._active_leased_views)

                local_lease_pending = {sid: sum(count for (owned_sid, _slot), count in self._local_lease_counts.items()

                                                 if owned_sid == sid)

                                       for sid, _info in items}

                local_lease_pending = {sid: count for sid, count in local_lease_pending.items() if count}

                pending = []

                for sid, info in items:

                    if not info.get("is_creator", False):

                        continue

                    try:

                        hdr = self._read_header_from_mapping(info["shm"])

                    except Exception as exc:

                        raise RuntimeError(f"No se pudo verificar el drenaje del slab {sid}: {exc}") from exc

                    reader_bits = hdr.state_and_readers & ((1 << 63) - 1)

                    if reader_bits:

                        pending.append((sid, reader_bits))

                if not local_live and not local_lease_pending and not pending:

                    break

                if time.monotonic() >= deadline:

                    detail = f"vistas locales={len(local_live)}, leases locales={local_lease_pending}, leases compartidos pendientes={pending}"

                    raise TimeoutError(f"No se liberan los leases; no se cierra ni desvincula ningún slab. {detail}")

                time.sleep(0.005)



            # Close only after local views and (for owners) shared reader counters have drained.

            for sid, info in items:

                shm = info["shm"]

                is_creator = info.get("is_creator", False)

                try:

                    shm.close()

                except (BufferError, OSError, ValueError) as exc:

                    raise RuntimeError(f"No se puede cerrar slab {sid}; queda retenido para permitir reintento: {exc}") from exc

                if is_creator:

                    try:

                        shm.unlink()

                    except FileNotFoundError:

                        pass

                with self._local_lock:

                    current = self.slabs.get(sid)

                    if current is info:

                        self.slabs.pop(sid, None)

            with self._local_lock:

                if not self.slabs:

                    self._is_releasing = False

        except Exception:

            raise



    def cleanup(self):

        """Alias de release_all para limpieza determinista."""

        self.release_all()



    @property

    def _slabs(self) -> Dict[int, Tuple[int, Any]]:

        """Mapa de compatibilidad para inspección Red Team de buffers de memoria compartida."""

        out: Dict[int, Tuple[int, Any]] = {}

        for sid, info in self.slabs.items():

            hdr = self.read_header(sid)

            out[sid] = (hdr.active_slot, info["shm"])

        return out



    def publish_tensor(self, vec: np.ndarray, aux_tag: int = 0) -> str:

        """Publish and issue a descriptor without allowing local retirement mid-commit.



        The in-flight marker is held across retries, but the lock is not held

        during the whole native publish; local leases can still drain.

        """

        raw = np.asarray(vec)

        if raw.dtype != np.dtype("float64"):

            raise TypeError(

                f"Conversión implícita de tipo prohibida en transporte exacto (V006-NUM-017): "

                f"obtenido {raw.dtype}, esperado float64. Use allocate_tensor_slab/publish_snapshot_atomic "

                f"para publicar tipos nativos enteros/FP32 sin pérdida de precisión."

            )

        arr = np.ascontiguousarray(raw).reshape(-1)

        with self._local_lock:

            if self._is_releasing:

                raise RuntimeError("Bus en proceso de cierre; publicación rechazada")

            # Selección dinámica de slab compatible o asignación de slot libre
            attempts = 0
            sid = None
            while attempts < self.max_slabs:
                candidate_sid = (self._next_slab_seq % max(1, self.max_slabs)) + 1
                self._next_slab_seq += 1
                attempts += 1
                info = self.slabs.get(candidate_sid)
                if info is None:
                    self.allocate_tensor_slab(candidate_sid, arr.size, dtype=np.float64, scale=1.0)
                    sid = candidate_sid
                    break
                elif not info.get("released", False) and info["num_elements"] == arr.size and np.dtype(info["dtype"]) == np.dtype(np.float64):
                    sid = candidate_sid
                    break

            if sid is None:
                raise RuntimeError(f"No hay slabs compatibles o libres disponibles en el bus (max={self.max_slabs})")

            if sid in self._inflight_descriptor_publishes:

                raise RuntimeError(f"Publicación de descriptor para slab {sid} ya en progreso")

            self._inflight_descriptor_publishes.add(sid)

        try:

            generation = self.publish_snapshot_atomic(sid, arr)

            if not generation:

                raise RuntimeError(f"No se pudo publicar slab {sid}: slot ocupado o timeout")

            with self._local_lock:

                info = self.slabs.get(sid)

                if info is None or info.get("released", False) or self._is_releasing:

                    # The native commit cannot be rolled back here. Fail closed.

                    raise RuntimeError("Slab destruido o retirado durante la publicación")

                info["published_at_ns"] = time.time_ns()

                return f"SLAB_ID_{sid}_{generation}_{info['epoch']}"

        finally:

            with self._local_lock:

                self._inflight_descriptor_publishes.discard(sid)



    def read_tensor(self, slab_descriptor: str, verify_stiefel: bool = False,

                    copy: bool = True, shape: Optional[Tuple[int, int]] = None) -> Any:

        """Read a descriptor-bound snapshot without an epoch TOCTOU window.



        The epoch/generation checks occur during the native lease acquisition,

        not in a separate unlocked lookup. Flat tensors cannot establish 2-D

        Stiefel orthonormality. Security against hostile writers is NOT ensured.

        """

        match = re.fullmatch(r"SLAB_ID_([1-9][0-9]*)_([1-9][0-9]*)_([1-9][0-9]*)", str(slab_descriptor))

        if match is None:

            raise ValueError(f"Descriptor PMTP inválido o legado sin epoch: {slab_descriptor!r}")

        sid, expected_gen, expected_epoch = map(int, match.groups())

        with self._local_lock:

            info = self.slabs.get(sid)

            if info is None or info.get("released", False):

                if not self.attach_slab(sid):

                    raise RuntimeError(f"Stale or released slab descriptor rejected: {slab_descriptor}")



        if copy:

            arr, gen = self.read_snapshot_copy(sid, expected_epoch=expected_epoch,

                                               expected_generation=expected_gen)

            leased = None

        else:

            leased = self.read_snapshot_leased(sid, expected_epoch=expected_epoch,

                                               expected_generation=expected_gen)

            arr = leased.array

            gen = leased._generation



        if verify_stiefel:

            try:

                if (not isinstance(shape, tuple) or len(shape) != 2 or

                        any(isinstance(v, bool) or not isinstance(v, (int, np.integer)) for v in shape)):

                    raise ValueError("Stiefel requiere shape=(D,K) explícito y validado")

                d, k = map(int, shape)

                if not (1 <= k <= d) or d * k != arr.size:

                    raise ValueError("Shape Stiefel inválido o incompatible con longitud de payload")

                if arr.dtype != np.float64 or not np.isfinite(arr).all():

                    raise ValueError("Stiefel requiere FP64 finitos")

                x = arr.reshape((d, k))

                defect = float(np.linalg.norm(x.T @ x - np.eye(k), ord=2))

                tol = 128.0 * np.finfo(np.float64).eps * max(1, k)

                if not np.isfinite(defect) or defect > tol:

                    raise ValueError(f"Stiefel Gram defect={defect} excede tol={tol}")

            except BaseException:

                if leased is not None:

                    leased.release()

                raise

        return arr if copy else leased



    def release_slab(self, slab_descriptor: str):

        """Retire a descriptor locally only if both its epoch and current generation match."""

        match = re.fullmatch(r"SLAB_ID_([1-9][0-9]*)_([1-9][0-9]*)_([1-9][0-9]*)", str(slab_descriptor))

        if match is None:

            raise ValueError(f"Descriptor PMTP inválido o legado sin epoch: {slab_descriptor!r}")

        sid, generation, epoch = map(int, match.groups())

        with self._local_lock:

            if sid in self._inflight_descriptor_publishes:

                raise RuntimeError(f"Retiro rechazado: publicación de descriptor en curso para slab {sid}")

            info = self.slabs.get(sid)

            if info is None or info.get("epoch") != epoch:

                raise RuntimeError(f"No se puede retirar descriptor obsoleto o ajeno: {slab_descriptor}")

            hdr = self._read_header_from_mapping(info["shm"])

            if hdr.generation != generation:

                raise RuntimeError(f"No se puede retirar descriptor con generación obsoleta: {slab_descriptor}")

            info["released"] = True



    def heartbeat_lease(self, lease_id: Optional[int] = None) -> int:

        """Actualiza el timestamp de latido (heartbeat) en memoria de uno o todos los leases activos."""

        now_m = time.monotonic()

        updated = 0

        with self._local_lock:

            for lid, rec in self._lease_records.items():

                if not rec["released"] and (lease_id is None or lid == lease_id):

                    rec["last_heartbeat"] = now_m

                    updated += 1

        return updated



    def register_process_liveness(self, slab_id: int):

        """Registra el proceso en el directorio de runtime para auditoria de dead-readers cross-proceso."""

        try:

            reg_file = os.path.join(tempfile.gettempdir(), f"pmtp_proc_{slab_id}_{os.getpid()}.reader")

            with open(reg_file, "w", encoding="utf-8") as f:

                json.dump({"pid": os.getpid(), "slab_id": slab_id, "start": time.time()}, f)

        except Exception:

            pass



    def unregister_process_liveness(self, slab_id: int):

        """Elimina el registro de proceso al desconectar el slab."""

        try:

            reg_file = os.path.join(tempfile.gettempdir(), f"pmtp_proc_{slab_id}_{os.getpid()}.reader")

            if os.path.exists(reg_file):

                os.remove(reg_file)

        except Exception:

            pass



    def reap_expired_leases(self, timeout_seconds: Optional[float] = None) -> int:

        """Reclama activamente leases abandonados por procesos lectores caidos (dead-reader reclamation).



        Zero-disk en el camino critico de adquisición/liberación.

        Verifica latidos locales y liveness del OS (_is_pid_alive) para procesos externos.

        """

        if _NATIVE_LIB is None:

            return 0

        timeout = float(timeout_seconds) if timeout_seconds is not None else (self.lease_timeout_ms / 1000.0)

        now_mono = time.monotonic()

        reclaimed = 0



        with self._local_lock:

            # 1. Recuperacion en el registro de leases locales (in-memory)

            for lid, rec in list(self._lease_records.items()):

                if rec["released"]:

                    continue

                sid = rec["slab_id"]

                slot = rec["slot"]

                is_expired = (now_mono - rec["last_heartbeat"]) > timeout

                is_dead = not _is_pid_alive(rec["pid"])

                if is_expired or is_dead:

                    info = self.slabs.get(sid)

                    if info is not None and not info.get("released", False):

                        buf_addr = ctypes.addressof(ctypes.c_char.from_buffer(info["shm"].buf))

                        rc = _NATIVE_LIB.pmtp_shm_release_lease_raw(buf_addr, slot)

                        if rc == 0:

                            reclaimed += 1

                    rec["released"] = True

                    key = (sid, slot)

                    if key in self._local_lease_counts:

                        if self._local_lease_counts[key] <= 1:

                            self._local_lease_counts.pop(key, None)

                        else:

                            self._local_lease_counts[key] -= 1



            # 2. Recuperacion cross-proceso via registros de procesos en tempdir

            tmp_dir = tempfile.gettempdir()

            for sid, info in list(self.slabs.items()):

                if info.get("released", False):

                    continue

                try:

                    all_tmp = os.listdir(tmp_dir)

                    files = [

                        os.path.join(tmp_dir, fn) for fn in all_tmp

                        if (fn.startswith(f"pmtp_proc_{sid}_") and fn.endswith(".reader"))

                        or (fn.startswith(f"pmtp_lease_{sid}_") and fn.endswith(".lease"))

                    ]

                except OSError:

                    files = []

                for rpath in files:

                    try:

                        with open(rpath, "r", encoding="utf-8") as f_reg:

                            data = json.load(f_reg)

                        f_pid = int(data.get("pid", 0))

                        target_slot = data.get("slot")

                        if not _is_pid_alive(f_pid):

                            buf_addr = ctypes.addressof(ctypes.c_char.from_buffer(info["shm"].buf))

                            slots_to_check = [int(target_slot)] if target_slot in (0, 1) else []

                            for s in slots_to_check:

                                rc = _NATIVE_LIB.pmtp_shm_release_lease_raw(buf_addr, s)

                                if rc == 0:

                                    reclaimed += 1

                            try:

                                os.remove(rpath)

                            except OSError:

                                pass

                    except Exception:

                        pass



        return reclaimed

