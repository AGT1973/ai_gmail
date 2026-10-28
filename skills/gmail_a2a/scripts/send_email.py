import os
import sys
import re
import argparse
import base64
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

# 🔍 RESOLUCIÓN DINÁMICA DE RUTAS (Silicon Contract: Sin Hardcoding)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))

# 🛡️ GUARDRAIL 1: Lista Blanca de Destinatarios Autorizados (VIPs Incluidos)
ALLOWED_RECIPIENTS = [
    "ariel.garcia.traba@gmail.com",
    "cursos.agt@gmail.com",
    "cursos.ai.agt@gmail.com",
    "polydim.cla@gmail.com",
    "ai.mpat.designer@gmail.com",
    "rasic.emilio@gmail.com",
    "kevinpiterman@gmail.com",
    "javieralcain@gmail.com",
    "lucas.esteban.percival@gmail.com",
    "ciordia6@hotmail.com",
    "leo@anzusingenieria.com",
    "leituz@gmail.com",
    "tubiog@gmail.com",
    "sofiasmutny@gmail.com",
    "James.Marlow@gmail.com",
    "cegactuario@gmail.com",
    "sergiofanchiotti@gmail.com",
    "sca.automatizaciones@gmail.com",
    "rafalore@gmail.com",
    "Caro.Corradi@gmail.com",
    "virginiacarstairs@gmail.com",
    "latinokarina@gmail.com",
    "mdelrrodriguez@gmail.com",
    "polydim.einsof@gmail.com",
    "queimam@hotmail.com",
    "marcoscba5@gmail.com"
]

# 🛡️ GUARDRAIL 2: Patrones DLP (Data Loss Prevention) - Anti-Leak de Claves y Passwords
PATRONES_DLP = [
    (r'GOCSPX-[a-zA-Z0-9_\-]{20,}', '[REDACTED_GOOGLE_CLIENT_SECRET]'),
    (r'sk-[a-zA-Z0-9T3BlbkFJ]{20,}', '[REDACTED_OPENAI_API_KEY]'),
    (r'AIzaSy[a-zA-Z0-9_\-]{33}', '[REDACTED_GEMINI_API_KEY]'),
    (r'ghp_[a-zA-Z0-9]{36}', '[REDACTED_GITHUB_PAT]'),
    (r'-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----[\s\S]*?-----END\s+(?:RSA\s+)?PRIVATE\s+KEY-----', '[REDACTED_PRIVATE_KEY]'),
    (r'(?i)(password|contraseña|clave|secret)\s*[:=]\s*["\']?([^\s"\'\`]+)', r'\1 = [REDACTED_PASSWORD]'),
]

ACCOUNT_MAP = {
    # Canonical directory names (human-readable)
    "polydim_cla": "polydim_cla",
    "mpat_designer": "mpat_designer",
    "cursos_agt": "cursos_agt",
    "cursos_ai_agt": "cursos_ai_agt",
    "polydim_einsof": "polydim_einsof",
    # Legacy aliases (backward compatibility)
    "account_a2a": "polydim_cla",
    "account_sota": "mpat_designer",
    "account_cursos": "cursos_agt",
    "account_cursos_ai": "cursos_ai_agt",
    "account_einsof": "polydim_einsof",
    # Email-based resolution
    "cursos.agt@gmail.com": "cursos_agt",
    "cursos.ai.agt@gmail.com": "cursos_ai_agt",
    "polydim.cla@gmail.com": "polydim_cla",
    "ai.mpat.designer@gmail.com": "mpat_designer",
    "polydim.einsof@gmail.com": "polydim_einsof",
    "ariel.garcia.traba@gmail.com": "polydim_cla"
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
    target_vault = ACCOUNT_MAP.get(account_key.lower(), account_key)
    is_course_channel = target_vault in ["cursos_agt", "cursos_ai_agt", "cursos_agt_ia"]
    to_email_clean = to_email.strip().lower()
    
    if not is_course_channel and not any(target.lower() in to_email_clean for target in ALLOWED_RECIPIENTS):
        print(f"SECURITY VETO: El destinatario '{to_email}' NO está en la lista blanca autorizada. Envío abortado.")
        sys.exit(1)

    sanitized_body, leak_found = sanitize_content(body)
    if leak_found:
        print("SECURITY ALERT (DLP): Se sanitizó información sensible antes del envío.")

    target_vault = ACCOUNT_MAP.get(account_key.lower(), account_key)
    secrets_dir = os.path.join(WORKSPACE_ROOT, ".secrets", target_vault)
    token_file = os.path.join(secrets_dir, "token.json")

    if not os.path.exists(token_file):
        print(f"ERROR: Token no encontrado para {account_key} ({target_vault}).")
        sys.exit(1)

    creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    service = build('gmail', 'v1', credentials=creds)

    message = EmailMessage()
    if "<html" in sanitized_body.lower() or "<div" in sanitized_body.lower() or "<p" in sanitized_body.lower():
        plain_text = re.sub(r'<[^>]+>', '', sanitized_body)
        message.set_content(plain_text)
        message.add_alternative(sanitized_body, subtype='html')
    else:
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
