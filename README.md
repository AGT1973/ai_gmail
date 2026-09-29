<style>
@page { size: 21cm 29.7cm; margin: 2cm }
th p { font-weight: bold; text-align: center; orphans: 0; widows: 0; background: transparent }
td p { orphans: 0; widows: 0; background: transparent }
h3 { margin-top: 0.25cm; margin-bottom: 0.21cm; background: transparent; page-break-after: avoid }
h3.western { font-family: "Liberation Sans", sans-serif; font-weight: bold; font-size: 14pt }
h3.cjk { font-size: 14pt; font-family: "Microsoft YaHei"; font-weight: bold }
h3.ctl { font-family: "Arial"; font-size: 14pt; font-weight: bold }
pre { background: transparent }
pre.western { font-family: "Liberation Mono", monospace; font-size: 10pt }
pre.cjk { font-size: 10pt; font-family: "NSimSun", monospace }
pre.ctl { font-family: "Liberation Mono", monospace; font-size: 10pt }
h2 { margin-top: 0.35cm; margin-bottom: 0.21cm; background: transparent; page-break-after: avoid }
h2.western { font-family: "Liberation Sans", sans-serif; font-weight: bold; font-size: 16pt }
h2.cjk { font-size: 16pt; font-family: "Microsoft YaHei"; font-weight: bold }
h2.ctl { font-family: "Arial"; font-size: 16pt; font-weight: bold }
blockquote { margin-left: 1cm; margin-right: 1cm; background: transparent }
h1 { margin-bottom: 0.21cm; background: transparent; page-break-after: avoid }
h1.western { font-family: "Liberation Sans", sans-serif; font-weight: bold; font-size: 18pt }
h1.cjk { font-size: 18pt; font-family: "Microsoft YaHei"; font-weight: bold }
h1.ctl { font-family: "Arial"; font-size: 18pt; font-weight: bold }
p { line-height: 115%; margin-bottom: 0.25cm; background: transparent }
a:link { color: #000080; text-decoration: underline }
</style>

# 📧 Manual: Crear una Cuenta Gmail y Habilitarla para una IA

### ¿Para qué sirve esto?
Este manual te permite crear cuentas Gmail adicionales para asignarlas como "buzón" de un agente de IA (Antigravity, Claude Code, GPT, etc.). El agente puede leer, clasificar y responder correos de forma autónoma usando esa cuenta, sin tocar tu correo personal.

---

### 🧠 Contexto: ¿Por qué este proceso es necesario?
Google limita la cantidad de cuentas adultas que se pueden crear seguidas desde un mismo dispositivo/red. Para generar cuentas adicionales sin ese bloqueo, se usa un truco legal: crear la cuenta como menor de 13 años (que no pide datos personales ni teléfono), agregarla al grupo familiar de una cuenta padre, cambiar la fecha de nacimiento a mayor de 18, y luego desvincularla. El resultado es una cuenta adulta normal y funcional.

Luego, la segunda parte del manual explica cómo conectar esa cuenta a la Gmail API de Google para que tu agente de IA pueda leer y enviar correos de forma autónoma.

---

# SECCIÓN A — Crear la Cuenta Gmail

> ⚠️ **Si ya tenés una cuenta Gmail adulta disponible para usar con la IA, podés saltear toda esta sección e ir directo a la Sección B.**

---

### Paso A1: Crear la cuenta como menor de 13 años
* **¿Por qué?** Google permite crear cuentas de menores sin pedir número de teléfono ni datos personales adicionales. Esto saltea el límite de altas masivas de cuentas adultas.
* **¿Por qué máximo 2 por día?** Crear muchas cuentas seguidas desde el mismo dispositivo puede activar bloqueos automáticos de Google. Ritmo recomendado: 2 por día como máximo.
* **¿Por qué máximo 5 en total por cuenta padre?** El grupo familiar de Google permite un máximo de 5 miembros. Cuando desvincules la cuenta hijo (Paso A4), la cuenta padre recupera ese slot y puede volver a invitar a otra cuenta.

👉 **Ir a:** [https://accounts.google.com/signup](https://accounts.google.com/signup)

**Acciones:**
1. Cerrar sesión de tu cuenta personal antes de entrar al link.
2. Completar nombre, usuario y contraseña.
3. En la fecha de nacimiento: ingresar una fecha que resulte en **menos de 13 años** de edad.
4. Completar el registro. Google no pedirá teléfono ni datos extra para menores.
5. **Una vez creada, abrir Gmail con esa cuenta y hacer al menos una acción** (crear un borrador, borrar un mail, enviar algo). Esto es obligatorio para el Paso A3.

---

### Paso A2: Agregar la cuenta hijo al grupo familiar desde la cuenta padre
* **¿Por qué?** El grupo familiar de Google permite que una cuenta padre gestione cuentas de menores, incluyendo la posibilidad de ver y editar su fecha de nacimiento. Sin este paso no podés cambiarle la edad.

👉 **Ir a (con la cuenta padre):** [https://myaccount.google.com/family/details](https://myaccount.google.com/family/details)

**Acciones:**
1. Hacer clic en **Invitar a un familiar**.
2. Ingresar el correo de la cuenta recién creada (la del menor).
3. Aceptar la invitación desde la cuenta hijo.

---

### Paso A3: Cambiar la fecha de nacimiento a mayor de 18 años
* **¿Por qué?** Con la cuenta hijo dentro del grupo familiar, el padre puede editar su fecha de nacimiento. Al cambiarla a una fecha que resulte en más de 18 años, Google la convierte en una cuenta adulta con todos los privilegios.
* **¿Por qué es obligatorio haber hecho una acción en Gmail primero (Paso A1)?** Google no muestra la opción de editar la fecha de nacimiento si la cuenta nunca tuvo actividad en Gmail. El sistema considera que la cuenta no fue "activada". Hacer cualquier acción (borrador, lectura) desbloquea esa opción.

👉 **Ir a (con la cuenta padre):** [https://myaccount.google.com/family/details](https://myaccount.google.com/family/details)

**Acciones:**
1. Seleccionar la cuenta hijo en la lista.
2. Ir a **Fecha de nacimiento**.
3. Cambiarla a una fecha que resulte en **más de 18 años de edad**.
4. Confirmar el cambio.

---

### Paso A4: Desvincular la cuenta hijo del grupo familiar
* **¿Por qué?** Una vez que la cuenta es adulta, no necesita seguir bajo la supervisión de la cuenta padre. Desvincularse la convierte en una cuenta completamente independiente. Además, libera el slot del grupo familiar para que la cuenta padre pueda crear otra cuenta hijo en el futuro.

👉 **Ir a (con la cuenta hijo, ya convertida en adulta):**  
[https://families.google.com](https://families.google.com)

**Acciones:**
1. Iniciar sesión con la cuenta hijo.
2. Buscar la opción **"Salir de la familia"** o **"Dejar el grupo familiar"**.
3. Confirmar.

> ℹ️ El link exacto con token (`TL=...`) lo genera Google dinámicamente para cada cuenta. No es posible compartir un link universal. Buscá la opción dentro del panel de familias de Google.  
> **Este funciona:** [Enlace directo de graduación](https://families.google.com/lifecycle/steps/teengraduation/intro?TL=ACv9tzF4E9MExNSTqFmPcRJB9tGK_1uzdmaiYzGNw3dSin2E3pMzsAtlnxC9pbDl&utm_source=google-account&utm_medium=web&hl=es&theme=mn)

---

### Paso A5: Verificar que la desvinculación fue exitosa
👉 **Ir a (con la cuenta padre):** [https://myaccount.google.com/family/details](https://myaccount.google.com/family/details)  
La cuenta hijo ya no debe aparecer en la lista. Si desaparece: éxito. El slot vuelve a estar disponible para una nueva invitación.

---

# SECCIÓN B — Habilitar la Cuenta para Uso con una IA (Gmail API + OAuth)

> **¿Qué hace esta sección?**  
> Conecta la cuenta Gmail a la infraestructura de Google Cloud para que un agente de IA (Antigravity, Claude Code, GPT, etc.) pueda leer y modificar los correos de forma programática usando la Gmail API.  
> El "pasaporte" de esa conexión es un archivo JSON (`credentials.json`) y un `token.json` que se generan en este proceso.

---

### Paso 1: Crear el Proyecto en Google Cloud
* **¿Por qué?** La Gmail API es un servicio de Google Cloud. Para usarla, necesitás un proyecto que actúe como contenedor: ahí se habilitan las APIs, se crean las credenciales y se controla quién tiene acceso. Es el punto de partida obligatorio.

👉 **Ir a (con la cuenta Gmail que va a usar la IA):** [https://console.cloud.google.com/projectcreate](https://console.cloud.google.com/projectcreate)

**Acciones:**
1. Nombre del proyecto: `agente-alumno-mail` (o el nombre que prefieras).
2. Hacer clic en **Crear**.
3. Esperar entre 10 segundos y hasta 1 día (en general tarda segundos).
4. Google te asignará un **ID de proyecto** (por ejemplo: `agente-alumno-mail-123456`). Guardarlo, lo vas a necesitar en los siguientes pasos.

---

### Paso 2: Habilitar la Gmail API
* **¿Por qué?** Los proyectos de Google Cloud no tienen ninguna API activa por defecto. Hay que habilitarla explícitamente. Sin esto, cualquier llamada a la API devuelve un error 403 (acceso denegado).

👉 **Ir a:** [https://console.cloud.google.com/apis/library/gmail.googleapis.com](https://console.cloud.google.com/apis/library/gmail.googleapis.com)

**Acciones:**
1. Verificar en la barra superior que esté seleccionado el proyecto creado en el Paso 1.
2. Si no aparece: hacer clic en el selector de proyecto → buscar por nombre o por el ID del Paso 1.
3. Hacer clic en el botón azul **Habilitar (Enable)**.

---

### Paso 3: Configurar la Pantalla de Consentimiento OAuth
* **¿Por qué?** Cuando el agente de IA pide acceso a tu Gmail, Google le muestra al usuario una pantalla preguntando "¿autorizás esta app?". Esa pantalla necesita estar configurada con el nombre de la app, el correo de contacto y los permisos que va a solicitar. Sin esta configuración, no es posible generar credenciales OAuth.

👉 **Ir a:** [https://console.cloud.google.com/apis/credentials/consent](https://console.cloud.google.com/apis/credentials/consent)

**Acciones:**
* **Tipo de usuario:**  
  Seleccionar **Usuarios externos (External)** → Clic en **Crear**.
* **Datos básicos:**  
  * Nombre de la app: `agente-alumno-mail`  
  * Correo de asistencia al usuario: tu propio correo Gmail  
  * Información de contacto del desarrollador: tu propio correo Gmail  
  * Clic en **Guardar y continuar**.
* **Permisos (Scopes):**  
  * Clic en **Agregar o quitar permisos**.  
  * Buscar y seleccionar: `https://www.googleapis.com/auth/gmail.modify`  
  * *¿Por qué este scope?* Permite leer, etiquetar y modificar correos (marcar como leído, mover, borrar). Es el mínimo necesario para que el agente opere sin poder eliminar la cuenta ni cambiar contraseñas.  
  * Clic en **Guardar y continuar**.
* **Usuarios de prueba ⚠️ CRÍTICO:**  
  * Clic en **+ ADD USERS**.  
  * Escribir el correo Gmail de la cuenta (el mismo que estás configurando).  
  * Opcionalmente agregar el correo del profesor.  
  * Clic en **Guardar y continuar**.  
  * *¿Por qué es crítico?* Mientras la app esté en modo "Prueba", solo los correos agregados aquí pueden autorizarla. Si tu correo no está en la lista, el flujo OAuth falla con un error de acceso bloqueado.

---

### Paso 4: Generar y Descargar la Credencial OAuth (el "Pasaporte")
* **¿Por qué?** La credencial OAuth es el archivo que le dice a Google "esta app es legítima y tiene permiso para pedir acceso". Es el equivalente a un documento de identidad para tu agente de IA. Sin él, no hay autenticación posible.

> 💾 **Importante:** Si en el futuro cambiás de PC o formateás el sistema, podés retomar desde este paso descargando nuevamente el JSON desde Google Cloud, sin tener que repetir todo desde el Paso 1.

👉 **Ir a:** [https://console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials)

**Acciones:**
1. Clic en **+ CREAR CREDENCIALES** → **ID de cliente de OAuth**.
2. Tipo de aplicación: **Aplicación de escritorio (Desktop app)**.  
   *(¿Por qué Desktop app? Porque el flujo OAuth local que usamos con `auth_setup.py` requiere este tipo).*
3. Nombre: podés dejar el que sugiere Google o poner tu correo.
4. Clic en **Crear**.
5. En la ventana emergente: clic en **DESCARGAR JSON**.
6. Renombrar el archivo a `credentials.json`.
7. Moverlo a la carpeta `.secrets/nombre_de_tu_cuenta/` de tu proyecto local.

El archivo tiene esta estructura (con tus datos reales en lugar de los ejemplos):
```json
{
  "installed": {
    "client_id": "xxxxxxxxxxxxx.apps.googleusercontent.com",
    "project_id": "agente-alumno-mail",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "yyyyyyyyyyyyyyyyyyyy",
    "redirect_uris": ["http://localhost"]
  }
}
```

---

### Paso 5: Agregar el Usuario de Prueba (si no lo hiciste en el Paso 3)
* **¿Por qué?** Es la misma razón del Paso 3: sin el usuario de prueba registrado, Google bloquea el flujo OAuth con "Acceso bloqueado". Este paso es redundante si ya lo hiciste en el Paso 3, pero se incluye como verificación.

👉 **Ir a (reemplazando `TU-ID-DE-PROYECTO` por el ID del Paso 1):**  
`https://console.cloud.google.com/auth/audience?project=TU-ID-DE-PROYECTO`

**Acciones:**
1. Sección **Usuarios de prueba**.
2. Clic en **+ ADD USERS**.
3. Ingresar el correo Gmail de la cuenta.
4. Guardar.

---

### Paso 6: Ejecutar el Flujo OAuth Local (Enlace Criptográfico)
* **¿Por qué?** Este paso genera el `token.json`, que es el token de acceso real que usa el agente de IA para operar. El `credentials.json` del Paso 4 es solo la identidad de la app; el `token.json` es la autorización específica de tu cuenta. Este proceso se hace una sola vez (o cuando el token expira).

El script `auth_setup.py` viene en el repositorio.

En la terminal (Windows + R → cmd):
```bash
python auth_setup.py --account nombre_de_tu_cuenta
```

**¿Qué pasa al ejecutarlo?**
* El script abre automáticamente el navegador con la pantalla de autorización de Google.
* Si no se abre solo, en la terminal aparecerá una URL larga — copiala y pegala en el navegador donde tengas la sesión Gmail iniciada.

**En el navegador:**
1. Seleccionar la cuenta Gmail correcta.
2. Si aparece **"Google no ha verificado esta aplicación"**:
   * Clic en **Configuración avanzada** (o *"Mostrar configuración avanzada"*).
   * Clic en **"Ir a [nombre de tu app] (no seguro)"**.
   * *(¿Por qué aparece esto? Porque la app está en modo "Prueba" y no fue verificada por Google. Es completamente normal para apps de uso propio. No significa que sea peligrosa — vos sos el desarrollador).*
3. Clic en **Continuar**.
4. Otorgar los permisos solicitados → clic en **Permitir**.
5. La terminal imprimirá: `VERDICT: Autenticación OAuth 2.0 completada exitosamente.`

---

### Paso 7: Evitar que el Token Expire a los 7 Días
* **¿Por qué expira?** Cuando la app está en modo "Prueba", Google revoca automáticamente los tokens de refresh cada 7 días como medida de seguridad. Para que el token sea permanente, la app tiene que completar su información de marca y ser publicada.
* **¿Por qué pide información de marca?** Google requiere que las apps OAuth externas tengan una página de inicio, política de privacidad y términos de servicio públicamente accesibles. Para apps de uso personal, podés usar el link de tu repositorio GitHub como sustituto de los tres.

👉 **Ir a (con la cuenta Gmail correspondiente):**  
`https://console.cloud.google.com/auth/audience?project=TU-ID-DE-PROYECTO`

#### Parte 7A — Completar la Información de Marca
Ir a → **Información de marca**:

| Campo | Qué poner |
| :--- | :--- |
| **Nombre de la aplicación** | `agente-alumno-mail` (o el que elegiste) |
| **Correo de asistencia** | tu correo Gmail |
| **Correo de contacto del desarrollador** | tu correo Gmail |
| **Página principal de la app** | tu repositorio GitHub (ej: `https://github.com/tuusuario/tu-repo`) |
| **Política de privacidad** | el mismo link de GitHub |
| **Condiciones del servicio** | el mismo link de GitHub |
| **Dominios autorizados** | solo el dominio raíz: `github.com` (sin https:// ni rutas) |

> ⚠️ Si aparece un segundo dominio autorizado por defecto, borrarlo. Solo debe quedar uno.  
> 🖼️ **Logotipo:** es opcional. Podés saltear ese campo sin problemas. Si lo cargás, Google te pedirá verificación adicional de la app, lo que complica el proceso innecesariamente.

Clic en **Guardar**.

#### Parte 7B — Publicar la App
Ir a → **Público** → Clic en **Publicar app** → **Confirmar**.

*(¿Por qué publicar si no es una app real? "Publicar" en este contexto solo significa cambiar el estado de "Prueba" a "En producción". No aparece en ninguna tienda ni es accesible para otros. El único efecto práctico es que los tokens dejan de expirar cada 7 días).*

---

### Paso 8 (Opcional): Obtener API Key de AI Studio para Gemini
* **¿Para qué sirve?** Esta API key permite que el agente use los modelos de lenguaje de Google (Gemini) para procesar y clasificar los correos. Es diferente a las credenciales OAuth: OAuth da acceso a Gmail, esta key da acceso al modelo de IA.
* Los créditos de esta key se renuevan semanalmente en el tier gratuito.

👉 **Ir a:** [https://aistudio.google.com/api-keys](https://aistudio.google.com/api-keys)

**Acciones:**
1. Clic en **Crear API Key**.
2. Seleccionar el proyecto del Paso 1.
3. Copiar la key generada (formato: `AQ.zzzzzzzzzzzzzzzzz...`).
4. Guardarla en el archivo de configuración de tu agente (nunca en el código fuente directamente).

---

### ✅ Verificación Final

Una vez completados todos los pasos, ejecutar nuevamente:
```bash
python auth_setup.py --account nombre_de_tu_cuenta
```

Si el token ya existe y es válido, el script imprimirá directamente el veredicto de éxito sin abrir el navegador.

Para verificar que el agente puede leer correos:
```bash
python utils/inspect_all_accounts.py
```

Debería mostrar el total de mensajes en el buzón y los encabezados de los más recientes.

---

### 🗂️ Resumen de Archivos Generados

| Archivo | Ubicación | Qué es |
| :--- | :--- | :--- |
| `credentials.json` | `.secrets/nombre_cuenta/` | Identidad de la app OAuth (descargado de Google Cloud) |
| `token.json` | `.secrets/nombre_cuenta/` | Token de acceso de la cuenta (generado por `auth_setup.py`) |

> 🔒 **Anti-Leak:** Ninguno de estos archivos debe subirse a Git. Verificar que `.gitignore` los excluya antes de hacer cualquier commit.

---

*Manual generado para el proyecto POLYDIM — Agente de IA sobre Gmail API*  
*Versión: 2026-09-28*
