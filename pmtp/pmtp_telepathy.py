"""
pmtp_telepathy.py — Cliente Canónico PMTP Trans-Nodo AGY Host <-> Aladín.
Protocolo de red SOTA: Frame binario 128B exacto, soporte de tensores en S^{D-1}
y eventos de metadatos JSON opcionales, con handshake bidireccional y ACK IEEE-754.
"""

import socket
import struct
import time
import os
import json
import numpy as np
from typing import Dict, Any, Optional

DEFAULT_ALADIN_HOST = "192.168.100.21"
DEFAULT_ALADIN_PORT = 9999
DEFAULT_HOST_PORT = 9998
MAGIC_PMTP = 0x504D5450
HEADER_STRUCT = "<IHHQ4I QIIQQ 64s"
HEADER_SIZE = 128
MAX_PAYLOAD_BYTES = 1024 * 1024 * 16  # 16 MB

class AladinTelepathyClient:
    """Cliente de telepatía tensorial PMTP entre nodos heterogéneos."""

    def __init__(
        self,
        host: str = DEFAULT_ALADIN_HOST,
        port: int = DEFAULT_ALADIN_PORT,
        shared_secret: bytes = b"POLYDIM_PMTP_KEY_2026_SOVEREIGN_",
    ):
        self.host = host
        self.port = port
        self.shared_secret = shared_secret
        self.sequence_id = int(time.time() * 1000) & 0xFFFFFFFF

    def send_tensor(
        self,
        tensor: np.ndarray,
        slab_id: str = "pmtp_telepathy",
        metadata: Optional[Dict[str, Any]] = None,
        timeout: float = 8.0,
    ) -> Dict[str, Any]:
        """
        Transmite un tensor binario FP64 alineado con encabezado canónico PMTP de 128 bytes
        y metadatos JSON opcionales en el payload secundario.
        """
        t0 = time.perf_counter()
        tensor = np.ascontiguousarray(tensor, dtype=np.float64)
        dim = int(tensor.shape[-1] if tensor.ndim >= 1 else len(tensor))
        raw_bytes = tensor.tobytes()
        byte_len = len(raw_bytes)

        if byte_len > MAX_PAYLOAD_BYTES:
            raise ValueError(f"Payload tensorial {byte_len} supera el límite de {MAX_PAYLOAD_BYTES} B")

        meta_bytes = b""
        if metadata:
            meta_bytes = json.dumps(metadata).encode("utf-8")
        reserved_meta_len = len(meta_bytes)

        self.sequence_id = (self.sequence_id + 1) & 0xFFFFFFFF
        seq = self.sequence_id
        epoch = int(time.time())

        # Formato: <IHHQ4I QIIQQ 64s (Exactamente 128 bytes)
        version = 3
        flags = 1
        node = 1
        pid = os.getpid() & 0xFFFFFFFF
        domain = 0
        state = 0
        dtype = 1  # FP64
        rank = 1
        slab_id_raw = slab_id.encode("utf-8").ljust(64, b"\x00")[:64]

        header = struct.pack(
            HEADER_STRUCT,
            MAGIC_PMTP, version, flags, epoch,
            node, pid, domain, state,
            dim, dtype, rank, byte_len, reserved_meta_len,
            slab_id_raw
        )
        assert len(header) == HEADER_SIZE, f"Header size is {len(header)} != 128"

        # Transmisión TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            sock.connect((self.host, self.port))
            sock.sendall(header + raw_bytes + meta_bytes)

            ack_buf = bytearray(22)
            view = memoryview(ack_buf)
            read_bytes = 0
            while read_bytes < 22:
                n = sock.recv_into(view[read_bytes:], 22 - read_bytes)
                if n == 0:
                    raise ConnectionError(f"ACK truncado por el nodo remoto {self.host}:{self.port}")
                read_bytes += n
        finally:
            sock.close()

        magic_ack, status, norm_err, proc_ms = struct.unpack("<IHdd", ack_buf)
        if magic_ack != MAGIC_PMTP:
            raise ValueError(f"Magic ACK inválido recibido: {hex(magic_ack)}")

        roundtrip_ms = (time.perf_counter() - t0) * 1000.0
        return {
            "exit_code": int(status),
            "status": "SUCCESS" if status == 0 else f"ERR_STATUS_{status}",
            "sequence_id": seq,
            "dimension": dim,
            "byte_len": byte_len,
            "meta_len": reserved_meta_len,
            "roundtrip_ms": roundtrip_ms,
            "remote_proc_ms": proc_ms,
            "norm_err": norm_err,
        }
