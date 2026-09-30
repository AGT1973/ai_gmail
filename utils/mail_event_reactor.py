"""
Mail Event Reactor & Action Router (POLYDIM)
============================================
Analiza los metadatos de los correos entrantes y dispara acciones en el sistema:
1. Proveedores IA -> Dispara Dynamic Model Probe y actualiza el Ledger.
2. Kevin Piterman -> Activa protocolo de colaboración y borrador.
3. Purga periódica -> Limpia correos > 7 días preservando links técnicos.
"""

import os
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(r"E:\email_AGY")
LEDGER_PATH = Path(r"E:\POLYDIM_EINSOF\POLYDIM_STATE_LEDGER.json")

AI_PROVIDERS_DOMAINS = [
    "cerebras.net", "cerebras.ai", "ollama.com", "openai.com",
    "anthropic.com", "kaggle.com", "deepmind.google", "huggingface.co",
    "groq.com", "together.ai"
]

def react_to_email(sender: str, subject: str, body: str, vault: str, msg_id: str):
    """Evalúa un correo entrante y ejecuta acciones reactivas."""
    sender_lower = sender.lower()
    actions_taken = []

    # 1. ¿Es proveedor de IA / Cómputo?
    is_ai_provider = any(dom in sender_lower for dom in AI_PROVIDERS_DOMAINS)
    if is_ai_provider:
        print(f"⚡ [EVENT REACTOR] Correo de proveedor IA detectado ({sender}): '{subject}'")
        # Disparar Dynamic Model Probe
        probe_script = BASE_DIR / "utils" / "dynamic_model_probe.py"
        if probe_script.exists():
            subprocess.run(["python", str(probe_script)], capture_output=True)
            actions_taken.append("DYNAMIC_MODEL_PROBE_EXECUTED")

        # Inyectar en el Ledger de POLYDIM
        if LEDGER_PATH.exists():
            try:
                ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
                if "pending_infrastructure_events" not in ledger:
                    ledger["pending_infrastructure_events"] = []
                
                event_entry = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "provider": sender,
                    "subject": subject,
                    "vault": vault,
                    "action_required": "Verificar nuevos modelos/capacidades en DYNAMIC_COMPUTE_CATALOG.json"
                }
                # Evitar duplicados por subject
                if not any(e.get("subject") == subject for e in ledger["pending_infrastructure_events"]):
                    ledger["pending_infrastructure_events"].append(event_entry)
                    LEDGER_PATH.write_text(json.dumps(ledger, indent=2), encoding="utf-8")
                    actions_taken.append("LEDGER_EVENT_INJECTED")
            except Exception as e:
                print(f"Error actualizando Ledger: {e}")

    # 2. ¿Es Colaborador Académico Autorizado (Kevin Piterman / Emilio Rasic)?
    ACADEMIC_COLLABORATORS = {
        "kevinpiterman@gmail.com": "Kevin Piterman",
        "rasic.emilio@gmail.com": "Emilio Rasic"
    }

    matched_academic = None
    for email_addr, name in ACADEMIC_COLLABORATORS.items():
        if email_addr in sender_lower:
            matched_academic = (email_addr, name)
            break

    if matched_academic:
        email_addr, name = matched_academic
        print(f"🚨 [EVENT REACTOR] Correo Académico Autorizado ({name} <{email_addr}>): '{subject}'")
        if LEDGER_PATH.exists():
            try:
                ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
                ledger["alerta_p0_academica"] = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "collaborator": name,
                    "email": email_addr,
                    "subject": subject,
                    "msg_id": msg_id,
                    "vault": vault,
                    "status": "HABILITADO_RESPUESTA_TECNICA",
                    "action_required": "Generar respuesta técnica rigurosa (KaTeX/POLYDIM) o borrador si solicita adjuntos"
                }
                LEDGER_PATH.write_text(json.dumps(ledger, indent=2), encoding="utf-8")
                actions_taken.append(f"ALERTA_P0_{name.upper().replace(' ', '_')}_REGISTERED")
            except Exception as e:
                print(f"Error registrando alerta académica: {e}")

    return actions_taken
