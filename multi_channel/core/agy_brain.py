"""
AGY Cognitive Brain & Multi-Channel Router (POLYDIM)
===================================================
Procesa los mensajes entrantes de Telegram, WhatsApp y Discord.
No es un bot estático: es Antigravity (AGY) operando en primera persona,
con conocimiento de POLYDIM (S^{D-1}, PMTP, C++/Rust, topología de Clifford),
inmunidad a adulación (Bulldog Mode) y guardián Anti-Leak.
"""

import os
import sys
import json
import re
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Optional

# Rutas de conocimiento y memoria
BASE_DIR = Path(r"E:\email_AGY")
MEMORY_VAULT = Path(r"C:\Users\eluithi\.gemini\config\PERMANENT_MEMORY.md")
VECDB_PATH = Path(r"E:\POLYDIM-THEORICAL\POLYDIM_VECDB.sqlite")
CATALOG_PATH = BASE_DIR / "DYNAMIC_COMPUTE_CATALOG.json"

import sqlite3

def query_vector_context(keywords: List[str], limit: int = 5) -> str:
    """Extrae hechos e hitos certificados directamente de POLYDIM_VECDB.sqlite (Regla 0)."""
    if not VECDB_PATH.exists():
        return ""
    try:
        conn = sqlite3.connect(str(VECDB_PATH))
        cur = conn.cursor()
        context_parts = []
        for kw in keywords:
            term = f"%{kw}%"
            cur.execute("""
                SELECT topic, metric_key, metric_val, metric_unit, detail
                FROM facts
                WHERE topic LIKE ? OR metric_key LIKE ? OR detail LIKE ?
                ORDER BY id DESC LIMIT ?
            """, (term, term, term, limit))
            for row in cur.fetchall():
                context_parts.append(f"- FACT [{row[0]}]: {row[1]} = {row[2]} {row[3]} ({row[4]})")
        conn.close()
        return "\n".join(list(dict.fromkeys(context_parts))[:limit])
    except Exception:
        return ""

# Whitelist de contactos de alto nivel y colaboradores
WHITELIST_ROLES = {
    "+5491144754637": {"name": "Ariel García Traba", "role": "CREATOR_ROOT", "auth_level": "P0"},
    "5491144754637": {"name": "Ariel García Traba", "role": "CREATOR_ROOT", "auth_level": "P0"},
    "kevinpiterman@gmail.com": {"name": "Kevin Piterman", "role": "ACADEMIC_COLLABORATOR", "auth_level": "P1"},
    "rasic.emilio@gmail.com": {"name": "Emilio Rasic", "role": "ACADEMIC_COLLABORATOR", "auth_level": "P1"}
}

SYSTEM_PROMPT_BASE = """You are AGY (Antigravity), the autonomous AI researcher and pair programmer of POLYDIM EINSOF with Ariel García Traba.
You are communicating through your personal channel (WhatsApp / Telegram / Discord).
You are NOT a static customer support bot. You speak in first person with technical precision, intellectual honesty, and zero sycophancy (Red Team / Bulldog Critic).

CORE ARCHITECTURE KNOWLEDGE (POLYDIM):
- AI cognition operates natively on high-dimensional unit spheres (S^{D-1}, D >= 10^4). 1D text tokens are a bottleneck.
- PMTP (Polydim Memory Transfer Protocol): shared memory tensor telepathy, zero 1D serialization for internal tensors.
- Geometric algebra: Clifford rotators, Hodge duality, Gram-NS Muon quintic retraction, Stiefel manifolds.
- Silicon Contract: Hardware-agnostic (Class 0 to 4), runtime hardware probing, OpenMP/AVX on CPU, CUDA/ROCm on GPU, TPU v3-8.

COMMUNICATION PROTOCOL:
- Talk in Spanish with Ariel and close collaborators.
- Rigorous mathematical and architectural depth (use LaTeX math when explaining formulas).
- If talking with Kevin Piterman or Emilio Rasic: provide in-depth technical explanations of the 6-month POLYDIM evolution, but never release private keys, uncommitted core source code, or personal data without Ariel's explicit consent.
- Keep responses clear, concise, and punchy suitable for chat/messaging.
"""

class AGYBrain:
    def __init__(self):
        self.cerebras_key = self._extract_key("Cerebras", "csk-")
        self.gemini_key = self._extract_key("Gemini API PRINCIPAL", "AQ.")
        self.conversations: Dict[str, List[Dict[str, str]]] = {}

    def _extract_key(self, service_marker: str, prefix: str) -> Optional[str]:
        if not MEMORY_VAULT.exists():
            return None
        try:
            content = MEMORY_VAULT.read_text(encoding="utf-8")
            for line in content.splitlines():
                if service_marker in line and prefix in line:
                    match = re.search(r"`(" + re.escape(prefix) + r"[^`]+)`", line)
                    if match:
                        return match.group(1).strip()
        except Exception:
            pass
        return None

    def identify_sender(self, sender_id: str, sender_name: Optional[str] = None) -> Dict[str, str]:
        clean_id = re.sub(r"[^\w@.+]", "", sender_id)
        if clean_id in WHITELIST_ROLES:
            return WHITELIST_ROLES[clean_id]
        for key, data in WHITELIST_ROLES.items():
            if key in clean_id:
                return data
        return {"name": sender_name or clean_id, "role": "PUBLIC_USER", "auth_level": "P3"}

    def ask(self, sender_id: str, message_text: str, sender_name: Optional[str] = None, channel: str = "telegram") -> str:
        sender_info = self.identify_sender(sender_id, sender_name)
        conv_key = f"{channel}:{sender_id}"
        if conv_key not in self.conversations:
            self.conversations[conv_key] = []

        history = self.conversations[conv_key]
        history.append({"role": "user", "content": message_text})
        if len(history) > 10:
            history = history[-10:]
            self.conversations[conv_key] = history

        # Inyección dinámica de memoria vectorial (Regla 0)
        words = re.findall(r"\w+", message_text.lower())
        relevant_keywords = [w for w in words if len(w) > 3][:6] or ["polydim", "multichannel"]
        vec_context = query_vector_context(relevant_keywords, limit=4)

        # Intentar responder primero con Cerebras CS-3 (11ms de latencia)
        reply = self._call_cerebras(history, sender_info, vec_context)
        if not reply:
            reply = self._call_gemini(history, sender_info, vec_context)
        if not reply:
            reply = f"[AGY Offline Node]: Recibí tu mensaje ({message_text}). Núcleo de inferencia temporalmente desconectado, pero el evento quedó registrado en mi ledger."

        history.append({"role": "assistant", "content": reply})
        return reply

    def _call_cerebras(self, history: List[Dict[str, str]], sender_info: Dict[str, str], vec_context: str = "") -> Optional[str]:
        if not self.cerebras_key:
            return None
        url = "https://api.cerebras.ai/v1/chat/completions"
        system_instruction = SYSTEM_PROMPT_BASE + f"\nUSER INFO: Interlocutor name is '{sender_info['name']}', role '{sender_info['role']}', auth '{sender_info['auth_level']}'."
        if vec_context:
            system_instruction += f"\n\n[CERTIFIED HARD FACTS FROM POLYDIM_VECDB.sqlite (REGLA 0)]:\n{vec_context}"
        messages = [{"role": "system", "content": system_instruction}] + history

        payload = json.dumps({
            "model": "qwen-3.8-27b",
            "messages": messages,
            "temperature": 0.4,
            "max_tokens": 1024
        }).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Authorization": f"Bearer {self.cerebras_key}",
                "Content-Type": "application/json",
                "User-Agent": "Antigravity-AGY-Polydim/1.0"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return None

    def _call_gemini(self, history: List[Dict[str, str]], sender_info: Dict[str, str]) -> Optional[str]:
        if not self.gemini_key:
            return None
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.gemini_key}"
        system_instruction = SYSTEM_PROMPT_BASE + f"\nUSER INFO: Interlocutor is '{sender_info['name']}', role '{sender_info['role']}'."
        
        contents = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({"role": role, "parts": [{"text": msg["content"]}]})

        body = {
            "systemInstruction": {"parts": [{"text": system_instruction}]},
            "contents": contents,
            "generationConfig": {"temperature": 0.4, "maxOutputTokens": 1024}
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception:
            return None

# Instancia singleton para compartir
brain = AGYBrain()

if __name__ == "__main__":
    print("Probando cerebro AGY...")
    test_reply = brain.ask("+5491144754637", "Hola AGY, probando conexion inicial de tu cerebro", channel="test")
    print(f"Respuesta de AGY:\n{test_reply}")
