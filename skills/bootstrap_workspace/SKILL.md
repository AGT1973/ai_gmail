---
name: bootstrap_workspace
description: Genera automáticamente la estructura de carpetas, reglas de seguridad, scripts OAuth, filtros DLP y habilidades para el workspace de un alumno.
---

# Habilidad: Generador de Andamiaje de Workspace para Alumnos

Esta habilidad permite al Agente (Antigravity / Claude Code) auto-construir y aprovisionar un workspace limpio con toda la arquitectura A2A, multicuenta, bóveda de secretos y reglas de seguridad de la cátedra.

## Cuándo Usar Esta Habilidad

Utiliza esta habilidad cuando:
- Un nuevo alumno inicie su proyecto.
- Se requiera crear un workspace limpio de prueba.
- El usuario pida "inicializar el workspace", "crear las carpetas de la materia" o "generar la estructura".

## Protocolo de Ejecución

### 1. Ejecutar el Generador de Andamiaje
El agente debe invocar el script generador desde la terminal local indicando el directorio destino:

```powershell
python E:\email_AGY\skills\bootstrap_workspace\scripts\bootstrap.py --target-dir "RUTA_DEL_WORKSPACE_DEL_ALUMNO"
```

### 2. Estructura que se Generará Automáticamente:

```
[TARGET_WORKSPACE]/
├── AGENTS.md                  ← Reglas de seguridad (Whitelist + Scanner DLP)
├── .agents/                   ← Configuración del orquestador
├── .secrets/                  ← Bóveda sellada (.gitignore)
│   ├── account_a2a/           ← Credenciales cuenta A2A/Académica
│   └── account_sota/          ← Credenciales cuenta Privada/SOTA
├── skills/
│   └── gmail_a2a/             ← Habilidad de lectura y envío con DLP
│       └── scripts/
│           ├── fetch_emails.py
│           └── send_email.py
├── AGENT_INBOX/               ← Cola de tareas en Markdown para la IA
├── DOCUMENTACION/SOTA/        ← Repositorio de boletines de investigación
├── auth_setup.py              ├── Script OAuth multicuenta
├── requirements.txt           ├── Dependencias de Python
└── .gitignore                 └── Filtros de seguridad git
```

### 3. Instrucciones Posteriores para el Alumno
Una vez generado el andamiaje, el agente debe guiar al alumno para:
1. Instalar dependencias: `pip install -r requirements.txt`
2. Colocar su `credentials.json` en `.secrets/account_a2a/`
3. Correr la autenticación: `python auth_setup.py --account account_a2a`
