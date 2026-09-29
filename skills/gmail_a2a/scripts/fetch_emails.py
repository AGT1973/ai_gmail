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
    "account_a2a": "account_a2a",
    "account_sota": "account_sota",
    "account_cursos": "account_cursos",
    "account_clone": "account_clone",
    "curious-clone-503600-r1": "account_clone",
    "cursos.agt@gmail.com": "account_cursos",
    "cursos.ai.agt@gmail.com": "account_a2a",
    "polydim.cla@gmail.com": "account_a2a",
    "ai.mpat.designer@gmail.com": "account_sota"
}

KEYWORDS_POLYDIM = [
    "vector", "embedding", "hnsw", "clifford", "tda", "manifold", 
    "attention", "sparse", "rag", "tensor", "isometry", "hodge",
    "dimension", "topology", "smiles", "molecule", "botnet", "llm"
]

def clean_payload(payload):
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data', '')
                return base64.urlsafe_b64decode(data).decode('utf-8')
    elif payload.get('mimeType') == 'text/plain':
        data = payload['body'].get('data', '')
        return base64.urlsafe_b64decode(data).decode('utf-8')
    return ""

def safe_filename(text):
    clean = re.sub(r'[^a-zA-Z0-9_\-]', '_', text)
    return clean[:50]

def save_sota_ingestion(account_key, msg_id, sender, subject, body):
    if not os.path.exists(SOTA_DIR):
        os.makedirs(SOTA_DIR, exist_ok=True)

    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"SOTA_{date_str}_{msg_id}_{safe_filename(subject)}.md"
    file_path = os.path.join(SOTA_DIR, file_name)

    content = f"""# 🧠 INGESTA TÉCNICA SOTA — PROYECTO POLYDIM
**Fecha de Ingesta:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Cuenta Origen:** {account_key}
**Remitente:** {sender}
**Asunto:** {subject}
**ID Correo:** {msg_id}

---

## 📄 PAYLOAD TÉCNICO COMPLETO:
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
        return []
    creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    service = build('gmail', 'v1', credentials=creds)

    results = service.users().messages().list(userId='me', labelIds=label_filter).execute()
    messages = results.get('messages', [])

    emails = []
    for msg_pointer in messages:
        msg_id = msg_pointer.get('id')
        try:
            msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
            headers = msg.get('payload', {}).get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'Sin Asunto')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Desconocido')
            body = clean_payload(msg.get('payload', {}))
            text_to_check = (subject + " " + body).lower()
            if any(kw in text_to_check for kw in KEYWORDS_POLYDIM):
                save_sota_ingestion(target_vault, msg_id, sender, subject, body)
            emails.append({"account": target_vault, "id": msg_id, "sender": sender, "subject": subject, "body": body})
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
    accounts_to_check = ["account_a2a", "account_sota", "account_cursos_ai", "account_clone"] if account_key == "all" else [account_key]
    all_emails = []
    for acc in accounts_to_check:
        all_emails.extend(fetch_single(acc, label_filter))
    print(json.dumps({"scanned_accounts": accounts_to_check, "emails": all_emails}))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Gmail messages for POLYDIM")
    parser.add_argument("--account", default="all", help="Account key or 'all'")
    parser.add_argument("--include-read", action="store_true", help="Do not filter for UNREAD messages; fetch all inbox mails")
    args = parser.parse_args()
    fetch_all(args.account, include_read=args.include_read)
