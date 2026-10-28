"""
Script de autorización OAuth interactivo para cuentas de email_AGY.
Abre el navegador para el flujo de consentimiento y guarda el token.json resultante.
"""
import os
import sys
import argparse
from google_auth_oauthlib.flow import InstalledAppFlow

# Forzar flush inmediato en Windows
sys.stdout.reconfigure(line_buffering=True)

# Scopes unificados: Gmail + Google Drive (para otorgar acceso de lectura a alumnos)
DEFAULT_SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/drive"
]

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def authorize(account_key, port=8090, with_drive=True):
    secrets_dir = os.path.join(WORKSPACE_ROOT, ".secrets", account_key)
    creds_file = os.path.join(secrets_dir, "credentials.json")
    token_file = os.path.join(secrets_dir, "token.json")

    if not os.path.exists(creds_file):
        print(f"ERROR: No se encontro credentials.json en {secrets_dir}", flush=True)
        sys.exit(1)

    scopes = DEFAULT_SCOPES if with_drive else ["https://www.googleapis.com/auth/gmail.modify"]

    print(f"[AUTH] Iniciando flujo OAuth para cuenta: {account_key}", flush=True)
    print(f"[AUTH] Credentials: {creds_file}", flush=True)
    print(f"[AUTH] Token destino: {token_file}", flush=True)
    print(f"[AUTH] Scopes solicitados: {scopes}", flush=True)

    flow = InstalledAppFlow.from_client_secrets_file(creds_file, scopes)
    
    try:
        creds = flow.run_local_server(
            host="localhost",
            port=port,
            authorization_prompt_message="[AUTH_URL] Visitá esta URL si no se abrió el navegador:\n{url}\n",
            success_message="Autenticación completada con éxito. Ya podés cerrar esta pestaña.",
            open_browser=True
        )
    except Exception as e:
        print(f"[AUTH_ERROR] Error en run_local_server con puerto {port}: {e}", flush=True)
        print("[AUTH_RETRY] Reintentando con puerto aleatorio...", flush=True)
        creds = flow.run_local_server(
            host="localhost",
            port=0,
            authorization_prompt_message="[AUTH_URL] Visitá esta URL:\n{url}\n",
            success_message="Autenticación completada con éxito. Ya podés cerrar esta pestaña.",
            open_browser=True
        )

    with open(token_file, "w", encoding="utf-8") as f:
        f.write(creds.to_json())

    print(f"[OK] Token guardado exitosamente en: {token_file}", flush=True)

    # Verificación inmediata de Gmail
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    creds2 = Credentials.from_authorized_user_file(token_file, scopes)
    svc = build("gmail", "v1", credentials=creds2)
    profile = svc.users().getProfile(userId="me").execute()
    print(f"[VERIFICADO] Email autenticado: {profile.get('emailAddress')} | Mensajes: {profile.get('messagesTotal')}", flush=True)
    
    # Verificación de Drive si está activo
    if with_drive:
        try:
            drive_svc = build("drive", "v3", credentials=creds2)
            about = drive_svc.about().get(fields="user").execute()
            print(f"[VERIFICADO DRIVE] Usuario Drive: {about.get('user', {}).get('displayName')} ({about.get('user', {}).get('emailAddress')})", flush=True)
        except Exception as e:
            print(f"[AVISO DRIVE] Drive API retornó: {e}", flush=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autorizacion OAuth para cuentas de email_AGY")
    parser.add_argument("--account", required=True, help="Nombre del directorio de la cuenta")
    parser.add_argument("--port", type=int, default=8090, help="Puerto local para callback")
    parser.add_argument("--no-drive", action="store_true", help="No solicitar permisos de Google Drive")
    args = parser.parse_args()
    authorize(args.account, args.port, with_drive=(not args.no_drive))
