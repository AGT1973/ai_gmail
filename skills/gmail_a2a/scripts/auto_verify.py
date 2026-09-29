import os
import time
import json
import re
import urllib.request
import ssl
import base64
import argparse
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))

ACCOUNT_MAP = {
    "account_a2a": "account_a2a",
    "account_sota": "account_sota",
    "account_cursos": "account_cursos",
    "cursos.agt@gmail.com": "account_cursos",
    "cursos.ai.agt@gmail.com": "account_a2a",
    "polydim.cla@gmail.com": "account_a2a",
    "ai.mpat.designer@gmail.com": "account_sota"
}

def extract_urls(text):
    return re.findall(r'https?://[^\s<>"\']+', text)

def fast_burst_verification(account_key="account_sota", max_attempts=12, interval_seconds=5):
    """
    Bucle de Verificación Rápida (Burst Check):
    Escanea la bandeja cada `interval_seconds` segundos para capturar
    correos de activación/OTP que expiran rápido.
    """
    target_vault = ACCOUNT_MAP.get(account_key.lower(), account_key)
    secrets_dir = os.path.join(WORKSPACE_ROOT, ".secrets", target_vault)
    token_file = os.path.join(secrets_dir, "token.json")

    if not os.path.exists(token_file):
        print(f"[{target_vault}] ERROR: token.json no encontrado.")
        return False

    creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    service = build('gmail', 'v1', credentials=creds)

    print(f"[{target_vault}] Iniciando rafaga de verificacion rapida ({max_attempts} intentos cada {interval_seconds}s)...")

    for attempt in range(1, max_attempts + 1):
        print(f"  -> Intento {attempt}/{max_attempts}...")
        results = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD']).execute()
        messages = results.get('messages', [])

        for msg_pointer in messages:
            msg_id = msg_pointer['id']
            msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
            headers = msg['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'Sin Asunto')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Desconocido')

            keywords = ["confirm", "verify", "verific", "activ", "opt-in", "substack", "login", "suscri"]
            if any(kw in subject.lower() for kw in keywords) or any(kw in sender.lower() for kw in keywords):
                print(f"[BURST] CORREO DE VERIFICACION DETECTADO! Subject: '{subject}' De: {sender}")
                
                body = ""
                if 'parts' in msg['payload']:
                    for part in msg['payload']['parts']:
                        if part['mimeType'] == 'text/plain':
                            body = base64.urlsafe_b64decode(part['body'].get('data', '')).decode('utf-8', errors='ignore')
                elif msg['payload'].get('mimeType') == 'text/plain':
                    body = base64.urlsafe_b64decode(msg['payload']['body'].get('data', '')).decode('utf-8', errors='ignore')

                urls = extract_urls(body)
                confirm_url = None
                for u in urls:
                    if any(k in u.lower() for k in ["confirm", "verify", "token", "action", "subscribe", "redirect"]):
                        confirm_url = u
                        break

                if confirm_url:
                    print(f"  -> Activando enlace de confirmacion: {confirm_url[:80]}...")
                    try:
                        ctx = ssl.create_default_context()
                        req = urllib.request.Request(confirm_url, headers={"User-Agent": "Mozilla/5.0"})
                        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
                            print(f"[SUCCESS] ACTIVACION EXITOSA (HTTP Status {resp.status})")
                    except Exception as e:
                        print(f"[WARNING] Error activando URL: {e}")

                service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()
                return True

        time.sleep(interval_seconds)

    print("[DONE] Rafaga finalizada sin encontrar correos de verificacion pendientes.")
    return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--account", default="account_sota")
    parser.add_argument("--attempts", type=int, default=12)
    parser.add_argument("--interval", type=int, default=5)
    args = parser.parse_args()

    fast_burst_verification(args.account, args.attempts, args.interval)
