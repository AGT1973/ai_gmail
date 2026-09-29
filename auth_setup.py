import os
import argparse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

# 🔍 RESOLUCIÓN DINÁMICA DE RUTAS (Silicon Contract: Sin Hardcoding)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ACCOUNT_MAP = {
    "account_a2a": "account_a2a",
    "account_sota": "account_sota",
    "account_cursos": "account_cursos",
    "account_cursos_ai": "account_cursos_ai",
    "account_clone": "account_clone",
    "curious-clone-503600-r1": "account_clone",
    "cursos.agt@gmail.com": "account_cursos",
    "cursos.ai.agt@gmail.com": "account_cursos_ai",
    "polydim.cla@gmail.com": "account_a2a",
    "ai.mpat.designer@gmail.com": "account_sota"
}

def authenticate_account(account_key="account_a2a"):
    target_vault = ACCOUNT_MAP.get(account_key.lower(), account_key)
    secrets_dir = os.path.join(BASE_DIR, ".secrets", target_vault)
    credentials_file = os.path.join(secrets_dir, "credentials.json")
    token_file = os.path.join(secrets_dir, "token.json")

    if not os.path.exists(secrets_dir):
        os.makedirs(secrets_dir, exist_ok=True)

    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    if not creds or not creds.valid:
        refreshed = False
        if creds and creds.expired and creds.refresh_token:
            print(f"[{target_vault}] Intentando refrescar token...")
            try:
                creds.refresh(Request())
                refreshed = True
            except Exception as e:
                print(f"[{target_vault}] El refresh token expiró o fue revocado ({e}). Re-autenticando vía navegador...")
        
        if not refreshed:
            if not os.path.exists(credentials_file):
                raise FileNotFoundError(
                    f"CRITICAL ERROR: No se encontró '{credentials_file}'. "
                    f"Descarga el archivo desde GCP para la cuenta ({account_key} -> {target_vault}) y colócalo dentro de '{secrets_dir}'."
                )
            if os.path.exists(token_file):
                try:
                    os.remove(token_file)
                except Exception:
                    pass
            print(f"[{target_vault}] Iniciando flujo OAuth con {credentials_file}...")
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            
            # Imprimir URL explícita para que el usuario pueda abrirla manualmente si falla el auto-open
            port = 8088
            flow.redirect_uri = f"http://localhost:{port}/"
            auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
            print("\n" + "="*80)
            print(f"👉 ABRIR EN EL NAVEGADOR (CUENTA: {target_vault}):")
            print(auth_url)
            print("="*80 + "\n")
            
            creds = flow.run_local_server(port=port, open_browser=True, prompt='consent')
        
        with open(token_file, "w") as token:
            token.write(creds.to_json())
            
    print(f"VERDICT: Autenticación OAuth 2.0 completada exitosamente para [{target_vault} ({account_key})]. Token fijado en vault.")
    return creds

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--account", 
        default="account_a2a", 
        choices=list(ACCOUNT_MAP.keys()),
        help="Cuenta a autenticar"
    )
    args = parser.parse_args()
    
    authenticate_account(args.account)
