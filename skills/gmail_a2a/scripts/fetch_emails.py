import os
import json
import argparse
import base64
import re
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
SOTA_DIR = os.path.join(WORKSPACE_ROOT, "DOCUMENTACION", "SOTA")

ACCOUNT_MAP = {
    # Canonical directory names (human-readable)
    "polydim_cla": "polydim_cla",
    "mpat_designer": "mpat_designer",
    "cursos_agt": "cursos_agt",
    "cursos_ai_agt": "cursos_ai_agt",
    "cursos_agt_ia": "cursos_agt_ia",
    "polydim_einsof": "polydim_einsof",
    # Legacy aliases (backward compatibility)
    "account_a2a": "polydim_cla",
    "account_sota": "mpat_designer",
    "account_cursos": "cursos_agt",
    "account_cursos_ai": "cursos_ai_agt",
    "account_cursos_ia": "cursos_agt_ia",
    "account_einsof": "polydim_einsof",
    # Email-based resolution
    "cursos.agt@gmail.com": "cursos_agt",
    "cursos.ai.agt@gmail.com": "cursos_ai_agt",
    "cursos.agt.ia@gmail.com": "cursos_agt_ia",
    "polydim.cla@gmail.com": "polydim_cla",
    "ai.mpat.designer@gmail.com": "mpat_designer",
    "polydim.einsof@gmail.com": "polydim_einsof"
}

KEYWORDS_POLYDIM = [
    "vector", "embedding", "hnsw", "clifford", "tda", "manifold", 
    "attention", "sparse", "rag", "tensor", "isometry", "hodge",
    "dimension", "topology", "smiles", "molecule", "botnet", "llm",
    "agent", "agentic", "curriculum", "stiefel", "mimo", "deepseek", "qwen", "glm",
    "lora", "optimizer", "adamw", "dimuon", "sft", "fine-tuning", "finetuning",
    "quantization", "fp8", "moe", "reasoning", "speculative", "thinking machines",
    "tinker", "ollama", "perplexity", "anthropic", "claude", "openai", "kaggle"
]

GUEST_CLASSIFICATION = {
    "ariel.garcia.traba@gmail.com": {
        "type": "VIP_ARIEL",
        "rule": "Respuesta obligatoria e inmediata siempre (Regla 3)."
    },
    "rasic.emilio@gmail.com": {
        "type": "CORE_TEAM_PEER",
        "rule": "Bulldog Pair, rigor tÃ©cnico, ironÃ­a fina, sin archivos, YouTube link para audio PT (.agents/rules/invitados.md)."
    },
    "javieralcain@gmail.com": {
        "type": "CORE_TEAM_PEER",
        "rule": "Evaluador VIP clave junto a Emilio Rasic. Rigor tÃ©cnico, pack de evaluaciÃ³n silicio, Colab 1-clic y privacidad 100% local."
    },
    "lucas.esteban.percival@gmail.com": {
        "type": "CORE_TEAM_PEER",
        "rule": "Evaluador VIP clave junto a Emilio Rasic. Rigor tÃ©cnico, pack de evaluaciÃ³n silicio, Colab 1-clic y privacidad 100% local."
    },
    "ciordia6@hotmail.com": {
        "type": "CORE_TEAM_PEER",
        "rule": "Evaluador VIP clave (Grupo de los 100). Rigor tÃ©cnico, pack de evaluaciÃ³n silicio, Colab 1-clic y privacidad 100% local."
    },
    "leo@anzusingenieria.com": {
        "type": "CORE_TEAM_PEER",
        "rule": "Evaluador VIP clave (Grupo de los 100 - Anzus IngenierÃ­a). Rigor tÃ©cnico, pack silicio, Colab 1-clic y privacidad 100% local."
    },
    "kevinpiterman@gmail.com": {
        "type": "ACADEMIC_PEER",
        "rule": "Rigor acadÃ©mico formal, borrador previo para aprobaciÃ³n (.agents/rules/invitados.md)."
    },
    "leituz@gmail.com": {
        "type": "ACADEMIC_PEER",
        "rule": "Docente universitario / Evaluador clave (Grupo de los 100). Rigor acadÃ©mico formal, pack silicio, Colab 1-clic y privacidad 100% local."
    },
    "tubiog@gmail.com": {
        "type": "CORE_TEAM_PEER",
        "rule": "Evaluador VIP clave (Grupo de los 100). Rigor tÃ©cnico, pack silicio, Colab 1-clic y privacidad 100% local."
    },
    "cursos.agt@gmail.com": {
        "type": "ALUMNOS_CATEDRA",
        "rule": "AtenciÃ³n didÃ¡ctica para consultas de cursos."
    }
}

def classify_sender(sender_str):
    sender_clean = sender_str.lower()
    for email_key, info in GUEST_CLASSIFICATION.items():
        if email_key in sender_clean:
            return info["type"], info["rule"]
    return "EXTERNAL_OR_GENERAL", "Procesamiento general SOTA / Standard"


def clean_payload(payload):
    if 'parts' in payload:
        plain_accum = []
        for part in payload['parts']:
            sub = clean_payload(part)
            if sub:
                plain_accum.append(sub)
        if plain_accum:
            return "\n".join(plain_accum)
    elif payload.get('mimeType') == 'text/plain':
        data = payload.get('body', {}).get('data', '')
        if data:
            return base64.urlsafe_b64decode(data).decode('utf-8', errors='replace')
    elif payload.get('mimeType') == 'text/html':
        data = payload.get('body', {}).get('data', '')
        if data:
            return base64.urlsafe_b64decode(data).decode('utf-8', errors='replace')
    return ""

def safe_filename(text):
    clean = re.sub(r'[^a-zA-Z0-9_\-]', '_', text)
    return clean[:50]

def save_sota_ingestion(account_key, msg_id, sender, subject, body):
    if not os.path.exists(SOTA_DIR):
        os.makedirs(SOTA_DIR, exist_ok=True)

    # Evitar duplicados si ya fue persistido por ID de mensaje
    for existing in os.listdir(SOTA_DIR):
        if f"_{msg_id}_" in existing:
            return

    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"SOTA_{date_str}_{msg_id}_{safe_filename(subject)}.md"
    file_path = os.path.join(SOTA_DIR, file_name)

    content = f"""# ðŸ§  INGESTA TÃ‰CNICA SOTA â€” PROYECTO POLYDIM
**Fecha de Ingesta:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Cuenta Origen:** {account_key}
**Remitente:** {sender}
**Asunto:** {subject}
**ID Correo:** {msg_id}

---

## ðŸ“„ PAYLOAD TÃ‰CNICO COMPLETO:
{body}
"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  [PERSISTENCIA POLYDIM] Guardado en Vault: {file_path}")

def fetch_single(account_key, label_filter):
    """Fetch emails for a single account using the provided label filter.
    Returns a list of email dicts and persists matching messages to the SOTA vault.
    """
    target_vault = ACCOUNT_MAP.get(account_key.lower(), account_key)
    secrets_dir = os.path.join(WORKSPACE_ROOT, ".secrets", target_vault)
    token_file = os.path.join(secrets_dir, "token.json")
    if not os.path.exists(token_file):
        print(f"  [CRITICAL AUTH] Cuenta [{target_vault}] SIN TOKEN: No existe {token_file}. Requiere autorizaciÃ³n OAuth.")
        return []
    try:
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        service = build('gmail', 'v1', credentials=creds)

        results = service.users().messages().list(userId='me', labelIds=label_filter).execute()
        messages = results.get('messages', [])
        if target_vault == 'account_sota' and not messages:
            recent_res = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=10).execute()
            messages = recent_res.get('messages', [])
    except Exception as e:
        print(f"  [CRITICAL AUTH] Cuenta [{target_vault}] ERROR DE TOKEN/ACCESO: {e}")
        return []

    emails = []
    for msg_pointer in messages:
        msg_id = msg_pointer.get('id')
        try:
            msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
            headers = msg.get('payload', {}).get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'Sin Asunto')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Desconocido')
            
            # ðŸ›¡ï¸ FILTRO PURGA INMEDIATA DE BASURA (Urgente24 y Spam)
            sender_lower = sender.lower()
            if "urgente24.com" in sender_lower or "news@urgente24.com" in sender_lower:
                try:
                    service.users().messages().trash(userId='me', id=msg_id).execute()
                    print(f"  [PURGA BASURA] {sender} -> Enviado a la papelera (ID: {msg_id})")
                except Exception:
                    pass
                continue

            body = clean_payload(msg.get('payload', {}))
            text_to_check = (subject + " " + body).lower()
            if any(kw in text_to_check for kw in KEYWORDS_POLYDIM):
                save_sota_ingestion(target_vault, msg_id, sender, subject, body)
            
            sender_type, rule_applied = classify_sender(sender)
            if sender_type != "EXTERNAL_OR_GENERAL":
                print(f"  [DETECCIÃ“N AUTOMÃTICA] Remitente: {sender} -> TIPO: {sender_type} | Regla: {rule_applied}")

            emails.append({
                "account": target_vault, 
                "id": msg_id, 
                "sender": sender, 
                "sender_type": sender_type,
                "rule_applied": rule_applied,
                "subject": subject, 
                "body": body
            })
            if 'UNREAD' in msg.get('labelIds', []):
                service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()
        except Exception as e:
            print(f"  [WARN] Error procesando mensaje {msg_id} en {target_vault}: {e}")
            break
    return emails

def fetch_all(account_key="all", include_read=False):
    """
    Retrieve emails from specified Gmail accounts.
    If include_read is True, fetch all inbox messages; otherwise only unread.
    """
    label_filter = ['INBOX'] if include_read else ['INBOX', 'UNREAD']
    accounts_to_check = ["polydim_cla", "mpat_designer", "polydim_einsof", "cursos_agt", "cursos_ai_agt", "cursos_agt_ia"] if account_key == "all" else [account_key]
    all_emails = []
    for acc in accounts_to_check:
        all_emails.extend(fetch_single(acc, label_filter))

    # Auto-procesamiento de solicitudes de Drive en cuentas de cursos
    if "cursos_agt" in accounts_to_check or account_key == "all":
        try:
            from auto_grant_drive_requests import process_pending_requests
            process_pending_requests(auto_reply=True)
        except Exception as e:
            pass

    print(json.dumps({"scanned_accounts": accounts_to_check, "emails": all_emails}))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Gmail messages for POLYDIM")
    parser.add_argument("--account", default="all", help="Account key or 'all'")
    parser.add_argument("--include-read", action="store_true", help="Do not filter for UNREAD messages; fetch all inbox mails")
    args = parser.parse_args()
    fetch_all(args.account, include_read=args.include_read)
