import os
import re
import base64
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Configuración Arquitectónica Dinámica (Silicon Contract)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRETS_DIR = os.path.join(BASE_DIR, ".secrets")
INBOX_DIR = os.path.join(BASE_DIR, "AGENT_INBOX")
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

ACCOUNT_VAULTS = ["account_a2a", "account_sota", "account_cursos_ai", "account_clone"]

def clean_payload(payload):
    """Extrae texto plano para ingesta de IA, eliminando HTML para evitar pérdida de entropía."""
    if 'parts' in payload:
        for part in payload['parts']:
            if part.get('mimeType') == 'text/plain':
                data = part['body'].get('data', '')
                return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    elif payload.get('mimeType') == 'text/plain':
        data = payload['body'].get('data', '')
        return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    return "[ERROR: Payload no contenía texto plano inteligible para el Agente]"

def safe_filename(subject):
    """Genera un nombre de archivo seguro para el sistema operativo."""
    clean = re.sub(r'[^a-zA-Z0-9_\-]', '_', subject)
    return clean[:50]

def agent_pull_tasks():
    """Bucle cron A2A (Agent-to-Agent): Descarga tareas y papers para ingesta de IA."""
    os.makedirs(INBOX_DIR, exist_ok=True)
    any_processed = False

    for vault in ACCOUNT_VAULTS:
        token_file = os.path.join(SECRETS_DIR, vault, "token.json")
        if not os.path.exists(token_file):
            continue

        try:
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
            service = build('gmail', 'v1', credentials=creds)
            results = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD']).execute()
            messages = results.get('messages', [])

            if not messages:
                continue

            print(f"AGENT STATUS [{vault}]: {len(messages)} paquetes detectados. Inyectando a disco local...")
            any_processed = True

            for msg_pointer in messages:
                msg_id = msg_pointer['id']
                try:
                    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
                    headers = msg.get('payload', {}).get('headers', [])
                    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'Sin_Asunto')
                    sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Desconocido')
                    date_str = next((h['value'] for h in headers if h['name'] == 'Date'), str(datetime.now()))
                    body = clean_payload(msg.get('payload', {}))
                    
                    file_name = f"TASK_{vault}_{msg_id}_{safe_filename(subject)}.md"
                    file_path = os.path.join(INBOX_DIR, file_name)
                    markdown_content = f"""# TAREA / INGESTA A2A
**Cuenta:** {vault}
**ID Origen:** {msg_id}
**Remitente:** {sender}
**Fecha:** {date_str}
**Asunto:** {subject}

---
## PAYLOAD (Contexto SOTA):
{body}
"""
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(markdown_content)

                    service.users().messages().modify(
                        userId='me', 
                        id=msg_id, 
                        body={'removeLabelIds': ['UNREAD']}
                    ).execute()
                    print(f" -> [{vault}] Tarea compilada en: {file_path}")
                except Exception as msg_err:
                    print(f" -> [{vault}] Error procesando msg {msg_id}: {msg_err}")
        except Exception as e:
            print(f" -> [{vault}] Error conectando con Gmail API: {e}")

    if not any_processed:
        print("AGENT STATUS: Sin nuevas tareas en cola en ninguna cuenta.")

if __name__ == '__main__':
    agent_pull_tasks()
