#   
A) Crear cuentas sobre limite

# 1) Ir a gmail luego de sing - out de tu cuenta y crear una nueva [https://accounts.google.com/signup](https://accounts.google.com/signup)

# 2) crearla MENOR A 13 AÑOS  
**para que no pida datos personales (solo 5 invitaciones – recomiendo no mas de 2 por dia)  
3) Ir a gmail creado y hacer una accion (crear mail, borrar, mandar )  
4) ir a la cuanta padre y acceder a gestionar tu cuenta google  
[https://myaccount.google.com**](https://myaccount.google.com/)

**A familia en el memu izquierdo**

**[https://myaccount.google.com/family/details?continue=https%3A%2F%2Fmyaccount.google.com%2F**](https://myaccount.google.com/family/details?continue=https%3A%2F%2Fmyaccount.google.com%2F)

**alli seleccionar la cuenta hijo, ir a fecha de nacimiento (si o si haber hecho punto 3 )  
cambiar para que sea mayor de 18  
5) desde la cuenta hijo podes desvincularte de la familia  
 (Esto permite que el padre tenga 5 invitaciones nuevamente)  
con esto el usuario no tiene mas relacion con el otro mail y tiene la posibilidad de usar gemini y antigravity**

**6) se verifica en **https://myaccount.google.com/family/details



# B) 📘 Manual de Cátedra: Conexión A2A (Gmail API + Antigravity Agent)

Este manual guía paso a paso al alumno para habilitar su cuenta de Gmail como canal de comunicación asíncrono para su agente de IA local



# Preparar cuenta para que la ia la use.  
**para usar con AI (antigravity / Claude code / gpt ← ver versión work)**



## PASO 1: Crear el Proyecto Base en Google Cloud (Bypass de Wizard)

Una vez creada y abierta la sesión en la cuenta de Gmail del alumno, hacer clic en el siguiente enlace directo:

👉 **[https://console.cloud.google.com/projectcreate**](https://console.cloud.google.com/projectcreate)

### Acciones del alumno:

1. Nombre del proyecto: `agente-alumno-mail` (o el nombre que prefiera). Te da in ID o código de proyecto

2. Hacer clic en **Crear**.

3. Esperar 10 segundos a que finalice el aprovisionamiento. Puede que sea hasta 1 día


## PASO 2: Habilitar la Gmail API

Debes estar en la cuenta de mail seleccionada para el uso de AI

Entrar directamente a la biblioteca de APIs del proyecto recién creado:

👉 **[https://console.cloud.google.com/apis/library/gmail.googleapis.com**](https://console.cloud.google.com/apis/library/gmail.googleapis.com)

### Acciones del alumno:

1. Verificar que en la barra superior esté seleccionado el proyecto creado en el Paso 1.

2. si no aparece el proyecto (nombre) ir a buscar y poner el id o código del proyecto dado en el punto 1

3. Hacer clic en el botón azul **Habilitar** (Enable).


## PASO 3: Configurar la Pantalla de Consentimiento (OAuth Consent Screen)

Entrar a la configuración de consentimiento:

👉 **[https://console.cloud.google.com/apis/credentials/consent**](https://console.cloud.google.com/apis/credentials/consent)

### Acciones del alumno:

1. Tipo de usuario: Seleccionar **Usuarios externos** (External) -\> Clic en **Crear**.

2. **Datos básicos:**

   - Nombre de la app:  `agente-alumno-mail`

   - Correo de asistencia: Seleccionar su propio correo.

   - Información de contacto del desarrollador: Escribir su propio correo.

   - Clic en **Guardar y continuar**.

3. **Permisos (Scopes):**

   - Clic en **Agregar o quitar permisos**.

   - Buscar o escribir: [`https://www.googleapis.com/auth/gmail.modify`](https://www.googleapis.com/auth/gmail.modify)

   - Seleccionarlo y hacer clic en **Guardar y continuar**.

4. **Usuarios de Prueba (Test Users) — ⚠️ CRÍTICO:**

   - Hacer clic en **+ ADD USERS**.

   - **Escribir el propio correo de Gmail del alumno** (y opcionalmente el del profesor).

   - Clic en **Guardar y continuar**.


## PASO 3.1: **apikey google aistudio**  
https://aistudio.google.com/api-keys

## **Antigravity para usar como agente (tokens renovables por semana)  apikey google aistudio AQ.zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz←para uso de MCP de Agente Gemini **

## PASO 4: Generar y Descargar la Credencial (Pasaporte)  
**Recordar que si el día de mañana cambian de pc o de sistema operativo (formatean) deben seguir desde aquí**

Entrar al gestor de credenciales:

👉 **[https://console.cloud.google.com/apis/credentials**](https://console.cloud.google.com/apis/credentials)

### Acciones del alumno:

1. En la barra superior, hacer clic en **+ CREAR CREDENCIALES** -\> **ID de cliente de OAuth**.

2. Tipo de aplicación: Seleccionar **Aplicación de escritorio** (Desktop app).

3. Nombre: dejar el nombre por defecto o el mail.

4. Clic en **Crear**.

5. En la ventana emergente, hacer clic en **DESCARGAR JSON**.

6. Moverlo a la carpeta `.secrets/` de su proyecto local.(importante para pasar en el punto 6)


## PASO 5: Enlace Criptográfico Local (Flujo Oauth)  
va a estar en el zip de la clase

Pedirle a tu que lea ** auth\_setup.py a tu AI (antigravity / Claude code / gpt ← ver versión work)**  
junto al json que bajaron en credenciales

\{"installed":\{"client\_id":"xxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com","project\_id":"agente-alumno-mail","auth\_uri":"https://accounts.google.com/o/oauth2/auth","token\_uri":"https://oauth2.googleapis.com/token","auth\_provider\_x509\_cert\_url":"https://www.googleapis.com/oauth2/v1/certs","client\_secret":"yyyyyyyyyyyyyyyyyyyyyyyy","redirect\_uris":\["http://localhost"\]\}\}


En la terminal del alumno, ejecutar windows + R cmd:

```
python auth\_setup.py --account tu cuenta gmail 
```

### Acciones del alumno:

1. El script imprimirá una URL de autorización.

2. Abrir la URL en el navegador donde esté iniciada la sesión del alumno.

3. Si aparece la advertencia *"Aplicación no verificada"*, hacer clic en **Avanzado** -\> **Ir a Agente Alumno Mail (Inseguro)**.

4. Otorgar los permisos de lectura/modificación y hacer clic en **Permitir**.

5. La terminal imprimirá: `VERDICT: Autenticación OAuth 2.0 completada exitosamente`.

## PASO 6: ultima confirmación  
al ejecutas va a mostrar en cmd una url larga que es valida por poco tiempo **auth\_setup.py → *[https://accounts.google.com/o/oauth2/auth?response\_type=code&client\_id=aaaaaaaaaaaaaaaaaaaaaa.apps.googleusercontent.com&redirect\_uri=http%3A%2F%2Flocalhost%3A50442%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.modify&state=bbbbbbbbbbbbbbb&access\_type=offline](https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=aaaaaaaaaaaaaaaaaaaaaa.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A50442%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.modify&state=bbbbbbbbbbbbbbb&access_type=offline)  
  
el suyo este es de ejemplo  
puede que redireccione en el navegador solo, sino pegar en la barra e ir. Alli confirmar  
Listo!**
