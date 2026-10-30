import os
import shutil
import zipfile
import json
from pathlib import Path

base_src = Path(r"E:\email_AGY")
build_dir = Path(r"E:\email_AGY\ENTREGABLE_ALUMNOS_BUILD")
zip_output = Path(r"E:\email_AGY\ENTREGABLE_ALUMNOS_GMAIL_AI.zip")

if build_dir.exists():
    shutil.rmtree(build_dir)
build_dir.mkdir(parents=True)

# 1. Crear estructura de carpetas
(build_dir / ".secrets" / "mi_cuenta_agente").mkdir(parents=True)
(build_dir / "AGENT_INBOX").mkdir(parents=True)
(build_dir / "_HISTORICO_MAIL").mkdir(parents=True)
(build_dir / "skills" / "gmail_a2a" / "scripts").mkdir(parents=True)
(build_dir / "skills" / "bootstrap_workspace" / "scripts").mkdir(parents=True)
(build_dir / "utils").mkdir(parents=True)

# 2. Archivos raíz esenciales
files_to_copy_root = [
    "requirements.txt",
    "polydim_mail_cron.py",
    "AGENTS.md"
]
for f in files_to_copy_root:
    src_f = base_src / f
    if src_f.exists():
        shutil.copy2(src_f, build_dir / f)

# 3. Copiar skills
if (base_src / "skills" / "gmail_a2a" / "SKILL.md").exists():
    shutil.copy2(base_src / "skills" / "gmail_a2a" / "SKILL.md", build_dir / "skills" / "gmail_a2a" / "SKILL.md")
for s in (base_src / "skills" / "gmail_a2a" / "scripts").glob("*.py"):
    shutil.copy2(s, build_dir / "skills" / "gmail_a2a" / "scripts" / s.name)

if (base_src / "skills" / "bootstrap_workspace" / "SKILL.md").exists():
    shutil.copy2(base_src / "skills" / "bootstrap_workspace" / "SKILL.md", build_dir / "skills" / "bootstrap_workspace" / "SKILL.md")
if (base_src / "skills" / "bootstrap_workspace" / "scripts" / "bootstrap.py").exists():
    shutil.copy2(base_src / "skills" / "bootstrap_workspace" / "scripts" / "bootstrap.py", build_dir / "skills" / "bootstrap_workspace" / "scripts" / "bootstrap.py")

# 4. Copiar utils
utils_to_copy = [
    "inspect_all_accounts.py",
    "dynamic_model_probe.py",
    "mail_event_reactor.py",
    "prune_and_extract_links.py"
]
for u in utils_to_copy:
    src_u = base_src / "utils" / u
    if src_u.exists():
        shutil.copy2(src_u, build_dir / "utils" / u)

# 5. Auth setup limpio para alumnos
auth_setup_code = '''import os
import argparse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def authenticate_account(account_name="mi_cuenta_agente"):
    secrets_dir = os.path.join(BASE_DIR, ".secrets", account_name)
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
            print(f"[{account_name}] Intentando refrescar token...")
            try:
                creds.refresh(Request())
                refreshed = True
            except Exception as e:
                print(f"[{account_name}] El refresh token expiro ({e}). Re-autenticando via navegador...")
        
        if not refreshed:
            if not os.path.exists(credentials_file):
                raise FileNotFoundError(
                    f"CRITICAL ERROR: No se encontro '{credentials_file}'.\\n"
                    f"Descarga el JSON de credenciales de Google Cloud y colocalo en '{secrets_dir}/credentials.json'."
                )
            if os.path.exists(token_file):
                try:
                    os.remove(token_file)
                except Exception:
                    pass
            
            print(f"[{account_name}] Iniciando flujo OAuth con {credentials_file}...")
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            
            port = 8088
            flow.redirect_uri = f"http://localhost:{port}/"
            auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
            print("\\n" + "="*80)
            print(f"👉 ABRIR EN EL NAVEGADOR PARA AUTORIZAR ({account_name}):")
            print(auth_url)
            print("="*80 + "\\n")
            
            creds = flow.run_local_server(port=port, open_browser=True, prompt='consent')
        
        with open(token_file, "w") as token:
            token.write(creds.to_json())
            
    print(f"\\nVERDICT: Autenticacion OAuth 2.0 completada exitosamente para [{account_name}]. Token fijado en .secrets/{account_name}/token.json")
    return creds

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autenticacion OAuth 2.0 para Agente Gmail")
    parser.add_argument("--account", default="mi_cuenta_agente", help="Nombre de la carpeta de la cuenta en .secrets/")
    args = parser.parse_args()
    authenticate_account(args.account)
'''
(build_dir / "auth_setup.py").write_text(auth_setup_code, encoding="utf-8")

# 6. Template de credenciales y .gitkeeps
cred_template = {
    "installed": {
        "client_id": "TU_CLIENT_ID.apps.googleusercontent.com",
        "project_id": "nombre-de-tu-proyecto",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "TU_CLIENT_SECRET",
        "redirect_uris": ["http://localhost"]
    }
}
(build_dir / ".secrets" / "mi_cuenta_agente" / "credentials_template.json").write_text(json.dumps(cred_template, indent=2), encoding="utf-8")
(build_dir / ".secrets" / ".gitignore").write_text("*\n!.gitignore\n!*/credentials_template.json\n", encoding="utf-8")
(build_dir / "AGENT_INBOX" / ".gitkeep").write_text("", encoding="utf-8")
(build_dir / "_HISTORICO_MAIL" / ".gitkeep").write_text("", encoding="utf-8")

# 7. Copiar el manual completo para alumnos y la guía para su IA
manual_src = Path(r"C:\Users\eluithi\.gemini\antigravity\brain\1c95a94c-081a-4602-8e1e-6c578fce0cec\manual_cuenta_ia_gmail.md")
if manual_src.exists():
    shutil.copy2(manual_src, build_dir / "MANUAL_COMPLETO_PASO_A_PASO.md")

ai_guide_src = base_src / "DOCUMENTACION" / "GUIA_AGENTE_INTERACTIVO_GMAIL.md"
if ai_guide_src.exists():
    (build_dir / "DOCUMENTACION").mkdir(parents=True, exist_ok=True)
    shutil.copy2(ai_guide_src, build_dir / "DOCUMENTACION" / "GUIA_AGENTE_INTERACTIVO_GMAIL.md")

# 8. Crear README_INSTRUCCIONES_ALUMNOS.md
readme_content = """# 🤖 Kit de Cátedra: Agente de IA Asíncrono sobre Gmail API (A2A)

Bienvenido. Este kit contiene toda la arquitectura de código y estructura de directorios limpia para que tu propio agente de Inteligencia Artificial (Antigravity, Claude Code, GPT, etc.) pueda:
1. Conectarse a una cuenta de Gmail de forma segura mediante **OAuth 2.0**.
2. Leer y clasificar correos en segundo plano (`AGENT_INBOX/`).
3. Ejecutar sondeo dinámico de modelos SOTA (`dynamic_model_probe.py`).
4. Reaccionar ante eventos y purgar automáticamente correos viejos (> 7 días) preservando enlaces útiles.

---

## 🚀 Inicio Rápido en 3 Pasos

### Paso 1: Configurar la Cuenta Gmail en Google Cloud
Seguí el manual incluido en este paquete:
👉 Abre y lee: `MANUAL_COMPLETO_PASO_A_PASO.md`

Allí se explica cómo crear el proyecto en Google Cloud, habilitar la Gmail API y descargar tu archivo `credentials.json`.

---

### Paso 2: Colocar tus Credenciales
1. Renombra el archivo descargado de Google Cloud como `credentials.json`.
2. Colócalo dentro de la carpeta:
   `.secrets/mi_cuenta_agente/credentials.json`

---

### Paso 3: Instalar Dependencias y Autenticar
En tu terminal:
```bash
pip install -r requirements.txt
python auth_setup.py --account mi_cuenta_agente
```

Se abrirá el navegador para autorizar a tu agente. Una vez aceptado, el sistema generará tu `token.json` automáticamente.

Para probar que tu agente ya lee el buzón:
```bash
python utils/inspect_all_accounts.py
```

---

## 🗂️ Estructura del Proyecto

```
.
├── auth_setup.py                  # Script de autenticación OAuth 2.0 local
├── polydim_mail_cron.py           # Demonio / Cron para descarga de correos
├── requirements.txt               # Librerías necesarias (google-api-python-client, etc.)
├── AGENTS.md                      # Reglas operativas para el agente de IA
├── MANUAL_COMPLETO_PASO_A_PASO.md  # Manual detallado con links y capturas conceptuales
├── .secrets/
│   └── mi_cuenta_agente/
│       └── credentials_template.json # Ejemplo de pasaporte descargado de Google Cloud
├── AGENT_INBOX/                   # Bandeja de entrada procesada para la IA (.md)
├── _HISTORICO_MAIL/               # Archivo histórico temporal
├── skills/
│   └── gmail_a2a/                 # Módulos de lectura, envío y verificación
│       ├── SKILL.md
│       └── scripts/
│           ├── fetch_emails.py    # Lector JSON de correos
│           └── send_email.py      # Emisor de correos
└── utils/
    ├── dynamic_model_probe.py     # Descubrimiento dinámico de modelos (Zero Hardcoding)
    ├── mail_event_reactor.py      # Reactor automático ante correos de proveedores IA
    ├── inspect_all_accounts.py    # Visualizador rápido de buzones en terminal
    └── prune_and_extract_links.py  # Purga inteligente semanal con extracción de links
```

---

*Desarrollado para el Taller de Agentes de IA & Arquitectura A2A.*
"""
(build_dir / "README_INSTRUCCIONES_ALUMNOS.md").write_text(readme_content, encoding="utf-8")

# 9. Empaquetar en ZIP
with zipfile.ZipFile(zip_output, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(build_dir):
        for file in files:
            file_path = Path(root) / file
            arcname = file_path.relative_to(build_dir)
            zipf.write(file_path, arcname)

# Limpiar build temporal
shutil.rmtree(build_dir)

print(f"✅ ZIP creado exitosamente en: {zip_output}")
print(f"Tamaño: {zip_output.stat().st_size / 1024:.2f} KB")
