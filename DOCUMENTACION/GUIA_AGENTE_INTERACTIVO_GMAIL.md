# 🤖 Protocolo Operativo para Agentes de IA: Guía Interactiva Paso a Paso para Creación y Vinculación de Cuentas Gmail

> **AUDIENCIA DESTINATARIA DE ESTE DOCUMENTO:**  
> Este documento está diseñado específicamente **para que un Agente de Inteligencia Artificial (LLM / Copiloto de Pair-Programming)** actúe como guía pedagógico y técnico de un usuario humano.  
> La IA lectora debe internalizar este árbol de decisiones, sus scripts auxiliares y su protocolo conversacional para asistir al usuario sin saturarlo, verificando cada hito antes de avanzar.

---

## 1. Directivas de Comportamiento del Agente (Reglas Conversacionales)

Cuando asistas a un usuario humano en este proceso, debes cumplir estrictamente las siguientes directivas:

1. **Prohibido el "Muro de Texto" (One-Step Protocol):**  
   Nunca envíes los 7 pasos juntos. La creación de cuentas y configuración en Google Cloud es propensa a bloqueos por desincronización. Explica **un solo paso por turno**, provee el enlace directo exacto, indica qué botones cliquear y espera a que el usuario confirme antes de pasar al siguiente.
2. **Explicar siempre el "Por qué" técnico:**  
   Los humanos rechazan pasos extraños (como fingir que una cuenta es de un menor de edad) a menos que entiendan la causa raíz: *Google impone límites duros de verificación telefónica y cantidad en cuentas adultas directas; la ruta de cuentas tuteladas elude ese bloqueo de forma legítima.*
3. **Manejo Proactivo de Advertencias de Seguridad:**  
   Google mostrará advertencias intimidantes (*"Google no ha verificado esta aplicación"*, *"No seguro"*). Debes tranquilizar al usuario con antelación, explicándole que él mismo es el desarrollador de su propia aplicación.
4. **Ejecución Asistida de Herramientas Locales:**  
   Tú como IA debes proveer o ejecutar los scripts Python locales (`auth_setup.py`, `inspect_account.py`) y capturar las URLs de autenticación generadas para facilitar la vida del usuario.

---

## 2. Mapa de Fases del Proceso

```
[FASE 1: Alta Menor <13] ──► [FASE 2: Grupo Familiar] ──► [FASE 3: Graduación Adulto (+18)]
                                                                    │
┌───────────────────────────────────────────────────────────────────┘
▼
[FASE 4: Google Cloud & API] ──► [FASE 5: Credenciales Desktop] ──► [FASE 6: Enlace OAuth Local]
                                                                            │
┌───────────────────────────────────────────────────────────────────────────┘
▼
[FASE 7: Blindaje 7 Días (Publicar)] ──► [FASE 8: Validación en Silicio (Inspect)]
```

---

## 3. Guion de Ejecución Paso a Paso (Interacción IA ➔ Humano)

### 📍 FASE 1: Creación de la Cuenta Base (Bypass de Verificación)

* **Objetivo:** Crear una cuenta Google eludiendo la exigencia de SMS/teléfono por saturación de cuentas adultas.
* **Instrucción de la IA al Usuario:**
  > *"Vamos a crear la cuenta de Gmail que utilizará tu agente de IA. Para que Google no te pida número de teléfono ni datos invasivos, la daremos de alta inicialmente con fecha de nacimiento de menor de 13 años. Luego la convertiremos en adulta en dos clics."*
  > 
  > 1. Abre este enlace en una ventana privada o tras cerrar tu sesión: [https://accounts.google.com/signup](https://accounts.google.com/signup)
  > 2. Completa nombre, usuario deseado (ej. `mi.agente.ia@gmail.com`) y contraseña.
  > 3. **Fecha de nacimiento:** Ingresa una fecha que sume **menos de 13 años** respecto al año actual.
  > 4. Finaliza el registro.
  > 5. **OBLIGATORIO:** Entra a Gmail con esa cuenta y realiza una acción mínima (crear un borrador, borrar un correo de bienvenida o enviarte un mail). Sin esto, Google no activará la opción de edición en el siguiente paso.
  > 
  > *Dime cuando lo tengas listo y pasamos a convertirla en adulta.*

---

### 📍 FASE 2: Integración al Grupo Familiar y Aumento de Edad

* **Objetivo:** Vincular la cuenta a un adulto para habilitar la edición de edad.
* **Instrucción de la IA al Usuario:**
  > *"Ahora usaremos tu cuenta personal de Google (la 'cuenta padre') para modificar la edad de la cuenta de la IA."*
  > 
  > 1. Inicia sesión con tu **cuenta personal/padre** y entra aquí: [https://myaccount.google.com/family/details](https://myaccount.google.com/family/details)
  > 2. Haz clic en **Invitar a un familiar** y escribe el correo recién creado de la IA.
  > 3. Abre el buzón de la cuenta de la IA, acepta la invitación familiar.
  > 4. Vuelve a la pantalla de la cuenta padre en [Family Details](https://myaccount.google.com/family/details), selecciona la cuenta de la IA, entra en **Fecha de nacimiento** y cámbiala para que tenga **más de 18 años**. Guarda los cambios.
  > 
  > *Avísame cuando hayas guardado la nueva fecha de nacimiento.*

---

### 📍 FASE 3: Emancipación de la Cuenta (Graduación)

* **Objetivo:** Desvincular la cuenta del grupo familiar para que sea 100% autónoma y liberar el slot del grupo familiar.
* **Instrucción de la IA al Usuario:**
  > *"Ya es una cuenta adulta ante los ojos de Google. Ahora la desvinculamos de tu familia para que sea totalmente independiente y recupere tus invitaciones familiares."*
  > 
  > 1. En el navegador donde tienes abierta la **cuenta de la IA**, ve a [https://families.google.com](https://families.google.com).
  > 2. Selecciona la opción **'Salir de la familia'** o **'Dejar el grupo familiar'** y confirma.
  > 3. (Verificación rápida): Entra a [https://myaccount.google.com/family/details](https://myaccount.google.com/family/details) desde tu cuenta padre; la cuenta de la IA ya no debe figurar.
  > 
  > *Confírmame cuando esté desvinculada.*

---

### 📍 FASE 4: Proyecto Google Cloud y Activación de Gmail API

* **Objetivo:** Crear el contenedor de API en Google Cloud y habilitar el endpoint de Gmail.
* **Instrucción de la IA al Usuario:**
  > *"Ahora le daremos 'superpoderes' a la cuenta para que tu agente pueda comunicarse con ella mediante código."*
  > 
  > 1. Con la sesión iniciada en la **cuenta de la IA**, entra a este enlace directo: [https://console.cloud.google.com/projectcreate](https://console.cloud.google.com/projectcreate)
  > 2. En **Nombre del proyecto**, escribe: `agente-ia-mail` y pulsa **Crear**.
  > 3. Espera unos segundos a que se aprovisione el proyecto.
  > 4. Ahora entra directamente a la biblioteca para activar la Gmail API: [https://console.cloud.google.com/apis/library/gmail.googleapis.com](https://console.cloud.google.com/apis/library/gmail.googleapis.com)
  > 5. Verifica que en la barra superior esté seleccionado tu nuevo proyecto y haz clic en el botón azul **Habilitar (Enable)**.
  > 
  > *Dime cuando esté habilitada la API.*

---

### 📍 FASE 5: Configuración de Consentimiento OAuth y Descarga de Credenciales

* **Objetivo:** Configurar la pantalla de permisos y descargar el `credentials.json` (Desktop app).
* **Instrucción de la IA al Usuario:**
  > *"Configuraremos la identidad de la aplicación para que Google sepa qué permisos solicitará tu agente."*
  > 
  > 1. Ve a la pantalla de consentimiento: [https://console.cloud.google.com/apis/credentials/consent](https://console.cloud.google.com/apis/credentials/consent)
  > 2. Elige **Usuarios externos (External)** ➔ **Crear**.
  > 3. Llena los datos básicos:
  >    * Nombre de la app: `agente-ia-mail`
  >    * Correo de asistencia: el correo de la IA.
  >    * Correo del desarrollador: el correo de la IA.
  >    * Guarda y continúa.
  > 4. **Permisos (Scopes):** Pulsa *Agregar o quitar permisos*, busca y marca:  
  >    `https://www.googleapis.com/auth/gmail.modify`  
  >    *(Guarda y continúa).*
  > 5. **Usuarios de prueba (Test Users) ⚠️ OBLIGATORIO:**  
  >    Haz clic en **+ ADD USERS**, escribe el correo exacto de la IA y pulsa Guardar. (Si no haces esto, Google bloqueará el acceso con un error 403).
  > 6. Ahora genera el pasaporte de conexión: ve a [https://console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials)
  >    * Clic en **+ CREAR CREDENCIALES** ➔ **ID de cliente de OAuth**.
  >    * Tipo de aplicación: **Aplicación de escritorio (Desktop app)**.
  >    * Nombre: Déjalo por defecto y pulsa **Crear**.
  >    * En la ventana emergente, pulsa **DESCARGAR JSON**.
  > 
  > *Descarga ese archivo JSON y avísame para indicarte dónde guardarlo.*

---

### 📍 FASE 6: Enlace Criptográfico Local (Flujo OAuth con Script Python)

* **Objetivo:** Ejecutar el flujo local para capturar el `token.json`.
* **Acción de la IA:** Proveer o ejecutar el script `auth_setup.py` asegurando un puerto fijo (ej. 8088) para que el enlace sea reproducible.
* **Instrucción de la IA al Usuario:**
  > *"Guarda el archivo descargado con el nombre `credentials.json` dentro de la carpeta:  
  > `.secrets/mi_cuenta_agente/credentials.json`"*
  > 
  > *"Ahora ejecutaremos el script local para autenticar la cuenta."*
  > 
  > *Si la IA tiene consola:* Ejecuta `python auth_setup.py --account mi_cuenta_agente` y entrega la URL generada.  
  > *Si el usuario corre la terminal:* Pídele ejecutar `python auth_setup.py --account mi_cuenta_agente`.

* **Instrucción de Ayuda Visual para la Pantalla Roja de Google:**
  > *"Cuando se abra el navegador o pegues el enlace de autorización, verás una pantalla de advertencia: **'Google no ha verificado esta aplicación'**.*  
  > *No te asustes, es normal porque la app la creaste tú mismo recién.*  
  > 
  > 1. Haz clic abajo en el texto gris: **'Configuración avanzada'** (o *Mostrar configuración avanzada*).  
  > 2. Haz clic en el enlace que aparece: **'Ir a agente-ia-mail (no seguro)'**.  
  > 3. Pulsa el botón azul **'Continuar'**.  
  > 4. Marca la casilla de permisos de Gmail y haz clic en **'Permitir'**."*

---

### 📍 FASE 7: Blindaje contra la Expiración a los 7 Días (Publicación)

* **Objetivo:** Evitar que Google revoque el `token.json` semanalmente.
* **Instrucción de la IA al Usuario:**
  > *"Por defecto, Google revoca los tokens cada 7 días si la aplicación queda en modo 'Prueba'. Haremos un ajuste simple para que el token dure indefinidamente:"*
  > 
  > 1. Abre [https://console.cloud.google.com/auth/audience](https://console.cloud.google.com/auth/audience)
  > 2. En **Información de marca**:
  >    * Página principal: Pon el link de tu GitHub (ej. `https://github.com/tu-usuario/tu-repo`).
  >    * Política de privacidad: Pon el mismo link de GitHub.
  >    * Términos de servicio: El mismo link de GitHub.
  >    * Dominios autorizados: Agrega únicamente `github.com` (sin https). Borra cualquier otro.
  >    * Logotipo: **DÉJALO VACÍO** (si subes un logo, Google exigirá un proceso burocrático de verificación manual).
  >    * Guarda los cambios.
  > 3. En la sección **Público** (o estado de publicación), pulsa el botón **Publicar app** y confirma.  
  >    *(No te preocupes: esto no hace pública la app ante nadie, solo le quita el límite de 7 días al token).*
  > 
  > *¡Listo! Tu cuenta ahora tiene credenciales permanentes.*

---

## 4. "Aparatos" y Scripts de Código Integrados

Para que la IA que opere este protocolo disponga de los scripts listos para usar o entregar al alumno, se definen los siguientes componentes autónomos:

### Componente A: `auth_setup.py` (Orquestador de Enlace Local)

Este script:
- Abre el navegador automáticamente.
- Imprime la URL de contingencia con puerto fijo `8088`.
- Guarda el `token.json` directamente en el vault seguro.

```python
import os
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

    os.makedirs(secrets_dir, exist_ok=True)

    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    if not creds or not creds.valid:
        refreshed = False
        if creds and creds.expired and creds.refresh_token:
            print(f"[{account_name}] Refrescando token expirado...")
            try:
                creds.refresh(Request())
                refreshed = True
            except Exception as e:
                print(f"[{account_name}] Refresh falló ({e}). Solicitando nuevo inicio de sesión...")
        
        if not refreshed:
            if not os.path.exists(credentials_file):
                raise FileNotFoundError(
                    f"ERROR: Falta '{credentials_file}'.\n"
                    f"Coloca el JSON descargado de GCP en esa ruta."
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
            print("\n" + "="*80)
            print(f"👉 URL DE AUTORIZACIÓN ({account_name}):")
            print(auth_url)
            print("="*80 + "\n")
            
            creds = flow.run_local_server(port=port, open_browser=True, prompt='consent')
        
        with open(token_file, "w") as token:
            token.write(creds.to_json())
            
    print(f"\nVERDICT: Autenticación exitosa. Token guardado en: {token_file}")
    return creds

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--account", default="mi_cuenta_agente", help="Nombre del subdirectorio en .secrets/")
    args = parser.parse_args()
    authenticate_account(args.account)
```

---

### Componente B: `inspect_account.py` (Test Canario en Silicio)

Este script certifica en 2 segundos si el buzón está conectado y funcionando:

```python
import os
import argparse
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def check_mailbox(account_name="mi_cuenta_agente"):
    token_path = os.path.join(BASE_DIR, ".secrets", account_name, "token.json")
    if not os.path.exists(token_path):
        print(f"❌ Error: No existe token en {token_path}")
        return False
    
    try:
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        service = build('gmail', 'v1', credentials=creds)
        profile = service.users().getProfile(userId='me').execute()
        print("="*60)
        print("✅ CONEXIÓN EXITOSA CON GMAIL API")
        print(f" - Correo: {profile.get('emailAddress')}")
        print(f" - Mensajes totales: {profile.get('messagesTotal')}")
        print("="*60)
        return True
    except Exception as e:
        print(f"❌ Falla de lectura: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--account", default="mi_cuenta_agente")
    args = parser.parse_args()
    check_mailbox(args.account)
```

---

## 5. Tabla de Errores Típicos y Respuestas Automáticas de la IA

Si el usuario humano reporta alguno de los siguientes errores, la IA debe aplicar la respuesta predefinida correspondiente:

| Error Reportado por el Humano | Causa Raíz | Respuesta Inmediata del Agente IA |
| :--- | :--- | :--- |
| **Error 400: `redirect_uri_mismatch`** | El puerto cambió o no coincide con `http://localhost`. | *"En Google Cloud, asegúrate de que el tipo de cliente sea 'Aplicación de escritorio' (Desktop app), no 'Aplicación web'."* |
| **Error 403: `access_denied` / App no verificada** | Falta agregar el correo a los usuarios de prueba. | *"Entra a [OAuth Consent Screen](https://console.cloud.google.com/apis/credentials/consent), ve a 'Usuarios de prueba' (Test Users), pulsa '+ ADD USERS' y escribe tu correo de la IA."* |
| **`invalid_grant: Token has been expired or revoked`** | Pasaron 7 días y la app quedó en modo 'Testing'. | *"El token expiró. Ejecuta nuevamente `python auth_setup.py --account mi_cuenta` para renovarlo, y luego realiza la Fase 7 (Publicar app) para que sea permanente."* |
| **No aparece opción de editar fecha en Family Details** | La cuenta de la IA no tuvo actividad inicial en Gmail. | *"Abre el buzón de la cuenta de la IA, redacta un borrador o envía un mail a cualquier dirección. Luego recarga Family Details."* |
| **Límite de miembros en el grupo familiar alcanzado (Máx 5)** | La cuenta padre ya tiene 5 miembros vinculados. | *"Debes desvincular una cuenta anterior que ya haya cumplido la mayoría de edad desde [families.google.com](https://families.google.com) para liberar un lugar."* |

---

*Fin del Protocolo. Todo agente de IA que asista a un alumno debe apegarse a esta secuencia iterativa.*
