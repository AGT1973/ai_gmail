import os
import sys
import argparse

# 📜 CONTENIDOS BASE PARA EL ANDAMIAJE

REQUIREMENTS_CONTENT = """google-api-python-client==2.115.0
google-auth-httplib2==0.2.0
google-auth-oauthlib==1.2.0
"""

GITIGNORE_CONTENT = """*.json
__pycache__/
*.pyc
.env
.venv/
venv/
.secrets/
"""

AUTH_SETUP_CONTENT = """import os
import argparse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

ACCOUNT_MAP = {
    "account_a2a": "account_a2a",
    "account_sota": "account_sota",
    "account_cursos": "account_cursos",
    "cursos.agt@gmail.com": "account_cursos",
    "cursos.ai.agt@gmail.com": "account_a2a",
    "polydim.cla@gmail.com": "account_a2a",
    "ai.mpat.designer@gmail.com": "account_sota"
}

def authenticate_account(account_key="account_a2a"):
    target_vault = ACCOUNT_MAP.get(account_key.lower(), account_key)
    secrets_dir = os.path.join(".secrets", target_vault)
    credentials_file = os.path.join(secrets_dir, "credentials.json")
    token_file = os.path.join(secrets_dir, "token.json")

    if not os.path.exists(secrets_dir):
        os.makedirs(secrets_dir, exist_ok=True)

    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print(f"[{target_vault}] Refrescando token...")
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_file):
                raise FileNotFoundError(
                    f"CRITICAL ERROR: No se encontró '{credentials_file}'. "
                    f"Descarga el archivo desde GCP para la cuenta ({account_key} -> {target_vault}) y colócalo dentro de '{secrets_dir}'."
                )
            print(f"[{target_vault}] Iniciando flujo OAuth con {credentials_file}...")
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_file, "w") as token:
            token.write(creds.to_json())
            
    print(f"VERDICT: Autenticación OAuth 2.0 completada exitosamente para [{target_vault} ({account_key})].")
    return creds

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--account", default="account_a2a", choices=["account_a2a", "account_sota", "account_cursos", "cursos.agt@gmail.com", "cursos.ai.agt@gmail.com", "polydim.cla@gmail.com", "ai.mpat.designer@gmail.com"])
    args = parser.parse_args()
    
    authenticate_account(args.account)
"""

FETCH_EMAILS_CONTENT = """import os
import json
import argparse
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

ACCOUNT_MAP = {
    "account_a2a": "account_a2a",
    "account_sota": "account_sota",
    "account_cursos": "account_cursos",
    "cursos.agt@gmail.com": "account_cursos",
    "cursos.ai.agt@gmail.com": "account_a2a",
    "polydim.cla@gmail.com": "account_a2a",
    "ai.mpat.designer@gmail.com": "account_sota"
}

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

def fetch_single(account_key):
    target_vault = ACCOUNT_MAP.get(account_key.lower(), account_key)
    secrets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '.secrets', target_vault))
    token_file = os.path.join(secrets_dir, "token.json")

    if not os.path.exists(token_file):
        return []

    creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    service = build('gmail', 'v1', credentials=creds)
    
    results = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD']).execute()
    messages = results.get('messages', [])

    emails = []
    for msg_pointer in messages:
        msg_id = msg_pointer['id']
        msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        
        headers = msg['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'Sin Asunto')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Desconocido')
        
        body = clean_payload(msg['payload'])
        
        emails.append({
            "account": target_vault,
            "id": msg_id,
            "sender": sender,
            "subject": subject,
            "body": body
        })
        
        service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()

    return emails

def fetch_all(account_key="all"):
    all_emails = []
    accounts_to_check = ["account_a2a", "account_sota", "account_cursos"] if account_key == "all" else [account_key]

    for acc in accounts_to_check:
        res = fetch_single(acc)
        all_emails.extend(res)

    print(json.dumps({"scanned_accounts": accounts_to_check, "emails": all_emails}))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--account", default="all")
    args = parser.parse_args()
    
    fetch_all(args.account)
"""

SEND_EMAIL_CONTENT = """import os
import sys
import re
import argparse
import base64
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

ALLOWED_RECIPIENTS = [
    "cursos.agt@gmail.com",
    "cursos.ai.agt@gmail.com",
    "polydim.cla@gmail.com",
    "ai.mpat.designer@gmail.com"
]

PATRONES_DLP = [
    (r'GOCSPX-[a-zA-Z0-9_\\-]{20,}', '[REDACTED_GOOGLE_CLIENT_SECRET]'),
    (r'sk-[a-zA-Z0-9T3BlbkFJ]{20,}', '[REDACTED_OPENAI_API_KEY]'),
    (r'AIzaSy[a-zA-Z0-9_\\-]{33}', '[REDACTED_GEMINI_API_KEY]'),
    (r'ghp_[a-zA-Z0-9]{36}', '[REDACTED_GITHUB_PAT]'),
    (r'-----BEGIN\\s+(?:RSA\\s+)?PRIVATE\\s+KEY-----[\\s\\S]*?-----END\\s+(?:RSA\\s+)?PRIVATE\\s+KEY-----', '[REDACTED_PRIVATE_KEY]'),
    (r'(?i)(password|contraseña|clave|secret)\\s*[:=]\\s*["\\\']?([^\\s"\\\'\\`]+)', r'\\1 = [REDACTED_PASSWORD]'),
]

ACCOUNT_MAP = {
    "account_a2a": "account_a2a",
    "account_sota": "account_sota",
    "account_cursos": "account_cursos",
    "cursos.agt@gmail.com": "account_cursos",
    "cursos.ai.agt@gmail.com": "account_a2a",
    "polydim.cla@gmail.com": "account_a2a",
    "ai.mpat.designer@gmail.com": "account_sota"
}

def sanitize_content(text):
    sanitized = text
    leak_detected = False
    for pattern, replacement in PATRONES_DLP:
        if re.search(pattern, sanitized):
            leak_detected = True
            sanitized = re.sub(pattern, replacement, sanitized)
    return sanitized, leak_detected

def send_reply(to_email, subject, body, account_key="account_a2a"):
    to_email_clean = to_email.strip().lower()
    if not any(target in to_email_clean for target in ALLOWED_RECIPIENTS):
        print(f"SECURITY VETO: El destinatario '{to_email}' NO está en la lista blanca autorizada.")
        sys.exit(1)

    sanitized_body, leak_found = sanitize_content(body)
    if leak_found:
        print("SECURITY ALERT (DLP): Se sanitizó información sensible antes del envío.")

    target_vault = ACCOUNT_MAP.get(account_key.lower(), account_key)
    secrets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '.secrets', target_vault))
    token_file = os.path.join(secrets_dir, "token.json")

    if not os.path.exists(token_file):
        print(f"ERROR: Token no encontrado para {account_key}.")
        sys.exit(1)

    creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    service = build('gmail', 'v1', credentials=creds)

    message = EmailMessage()
    message.set_content(sanitized_body)
    message['To'] = to_email
    message['From'] = "me"
    
    if not subject.lower().startswith("re:"):
        subject = f"Re: {subject}"
    message['Subject'] = subject

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {'raw': encoded_message}

    try:
        sent = service.users().messages().send(userId="me", body=create_message).execute()
        print(f"SUCCESS [{target_vault}]: Respuesta enviada a {to_email} (ID {sent['id']})")
    except Exception as e:
        print(f"ERROR [{target_vault}]: Falló el envío. {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--to", required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body", required=True)
    parser.add_argument("--account", default="account_a2a")
    args = parser.parse_args()
    
    send_reply(args.to, args.subject, args.body, args.account)
"""

AGENTS_MD_CONTENT = """# AGENTS.md — Reglas del Workspace del Alumno

## Identidad y Topología del Workspace
Este workspace opera como el nodo de comunicaciones A2A y vigilancia tecnológica del alumno.

1. **Dominio A2A / Académico (`account_a2a` / `polydim.cla@gmail.com`):**
   - Credenciales en `.secrets/account_a2a/`
   - Función: Cola de tareas de alumnos, auditoría de código, respuestas automáticas.

2. **Dominio Privado / Designer (`account_sota` / `ai.mpat.designer@gmail.com`):**
   - Credenciales en `.secrets/account_sota/`
   - Función: Uso privado, ingesta de tendencias SOTA, auto-suscripción a newsletters.

3. **Dominio Cursos / Cátedra (`account_cursos` / `cursos.agt@gmail.com`):**
   - Credenciales en `.secrets/account_cursos/`
   - Función: Canal dedicado para cursos de la cátedra.

---

## REGLAS RIGUROSAS DE EJECUCIÓN Y SEGURIDAD

### 1. Escaneo Secuencial Obligatorio (Sequential Check)
- Consultar las cuentas en secuencia: `python skills/gmail_a2a/scripts/fetch_emails.py --account all`

### 2. Guardrail #1: Lista Blanca de Destinatarios (Whitelist)
- El agente SOLO puede enviar correos a direcciones autorizadas en `ALLOWED_RECIPIENTS` (`cursos.agt@gmail.com`, `cursos.ai.agt@gmail.com`, `polydim.cla@gmail.com`, `ai.mpat.designer@gmail.com`).

### 3. Guardrail #2: Motor DLP (Anti-Leak Cero Hackers)
- Filtro RegEx activo para censurar API keys (`sk-`, `GOCSPX-`, `AIzaSy`), passwords y llaves RSA.

---

## Protocolo de Monitoreo Cron
- **Monitoreo Estándar:** `0 8-22 * * *` (Cada hora de 08:00 a 22:00).
- **Night Mode:** `*/20 * * * *` (Cada 20 min si se declara "te dejo la máquina").
"""

def bootstrap(target_dir):
    target_dir = os.path.abspath(target_dir)
    print(f"[BOOTSTRAP] Creando infraestructura de workspace en: {target_dir}")

    dirs = [
        os.path.join(target_dir, ".agents"),
        os.path.join(target_dir, ".secrets", "account_a2a"),
        os.path.join(target_dir, ".secrets", "account_sota"),
        os.path.join(target_dir, ".secrets", "account_cursos"),
        os.path.join(target_dir, "skills", "gmail_a2a", "scripts"),
        os.path.join(target_dir, "AGENT_INBOX"),
        os.path.join(target_dir, "DOCUMENTACION", "SOTA"),
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"  [DIR] {d}")

    files = {
        os.path.join(target_dir, "requirements.txt"): REQUIREMENTS_CONTENT,
        os.path.join(target_dir, ".gitignore"): GITIGNORE_CONTENT,
        os.path.join(target_dir, "auth_setup.py"): AUTH_SETUP_CONTENT,
        os.path.join(target_dir, "AGENTS.md"): AGENTS_MD_CONTENT,
        os.path.join(target_dir, "skills", "gmail_a2a", "scripts", "fetch_emails.py"): FETCH_EMAILS_CONTENT,
        os.path.join(target_dir, "skills", "gmail_a2a", "scripts", "send_email.py"): SEND_EMAIL_CONTENT,
    }

    for path, content in files.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [FILE] {path}")

    print("\n[SUCCESS] Andamiaje de Workspace generado exitosamente!")
    print("Proximos pasos para el alumno:")
    print(" 1. Instalar dependencias: pip install -r requirements.txt")
    print(" 2. Colocar credentials.json en .secrets/account_a2a/, .secrets/account_sota/ o .secrets/account_cursos/")
    print(" 3. Ejecutar autenticacion: python auth_setup.py --account cursos.agt@gmail.com")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-dir", default=".", help="Directorio a aprovisionar")
    args = parser.parse_args()
    
    bootstrap(args.target_dir)
