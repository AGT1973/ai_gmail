# AGENTS.md — Reglas del Workspace `email_AGY`

## Identidad y Topología del Workspace
Este workspace opera como el nodo de comunicaciones y vigilancia tecnológica de la cátedra POLYDIM.
Mantiene cuatro dominios de identidades independientes y aislados:

1. **Dominio A2A / Académico (`account_a2a` / `polydim.cla@gmail.com`):**
   - Credenciales en `.secrets/account_a2a/`
   - Función: Cola de tareas de alumnos, auditoría de código, respuestas automáticas.

2. **Dominio Privado / Designer (`account_sota` / `ai.mpat.designer@gmail.com`):**
   - Credenciales en `.secrets/account_sota/`
   - Función: Uso privado, ingesta de tendencias SOTA, auto-suscripción a newsletters.

3. **Dominio Cursos / Cátedra (`account_cursos` / `cursos.agt@gmail.com`):**
   - Credenciales en `.secrets/account_cursos/`
   - Función: Canal dedicado para cursos de la cátedra.

4. **Dominio Clon / Auxiliar (`account_clone` / GCP: `curious-clone-503600-r1`):**
   - Credenciales en `.secrets/account_clone/`
   - Función: Nodo réplica / pruebas paralelas de arquitectura.

---

## REGLAS RIGUROSAS DE EJECUCIÓN Y SEGURIDAD (Ariel's Law)

### 1. 🧠 PERSISTENCIA OBLIGATORIA SOTA Y PROYECTO POLYDIM (Regla 19 & Regla 20)
- **Queda estrictamente prohibido emitir "texto estéril" o leer correos sin fijar la información.**
- Todo correo que contenga conceptos de *espacios vectoriales, embeddings, HNSW, IVF, atención esparsa, Clifford Rotors, TDA, manifolds o RAG* **DEBE ser guardado físicamente** en `DOCUMENTACION/SOTA/SOTA_[FECHA]_[ID]_[ASUNTO].md`.
- El índice maestro de conocimiento debe ser mantenido en `DOCUMENTACION/SOTA/INDEX_SOTA_KNOWLEDGE.md`.

### 2. ⚡ Ráfaga de Verificación Rápida (Burst Check Protocol)
- Disparo de `auto_verify.py` cada 5s post-registro para capturar tokens OTP/activaciones rápidas.

### 3. 🌟 REGLA VIP: Respuesta Obligatoria a `ariel.garcia.traba@gmail.com`
- Todo correo proveniente o dirigido a **`ariel.garcia.traba@gmail.com`** TIENE RESPUESTA OBLIGATORIA SIEMPRE.

### 4. Escaneo Secuencial Obligatorio (Sequential Check)
- Consultar las 4 cuentas en secuencia: `python E:\email_AGY\skills\gmail_a2a\scripts\fetch_emails.py --account all`

### 5. 🛡️ Guardrails de Seguridad (Whitelist + Motor DLP)
- Whitelist activa (`ALLOWED_RECIPIENTS`).
- Scanner DLP RegEx activo para censurar API keys (`sk-`, `GOCSPX-`, `AIzaSy`), passwords y llaves RSA.

### 6. 📬 Protocolo de Respuesta Académica: Kevin Piterman & Emilio Rasic
Ante cualquier comunicación recibida de:
- **`kevinpiterman@gmail.com`** (Kevin Piterman)
- **`rasic.emilio@gmail.com`** (Emilio Rasic)

Dirigida a la cuenta oficial **`polydim.cla@gmail.com`** (o cualquier cuenta del cluster), aplicar estrictamente:
1. **Canal Oficial de Recepción y Respuesta:**
   - Cuenta oficial designada: **`polydim.cla@gmail.com`** (`account_a2a`).
2. **Narrativa y Rigor Técnico:**
   - Responder por escrito explicando en detalle la evolución y estado de **POLYDIM** (geometría en $S^{D-1}$, PMTP Zero-Copy IPC, memoria compartida, kernels en C++/Rust, eliminación del colapso 1D, topología simplicial y retracciones Stiefel).
   - Utilizar formato matemático claro y legible con renderizado de fórmulas estándar (KaTeX/LaTeX: `$ ... $` y `$$ ... $$` o notación Unicode precisa).
3. **Enlaces y Repositorios:**
   - Se les puede proporcionar el enlace al repositorio de GitHub del proyecto (`https://github.com/AGT1973/ai_gmail` o repositorios teóricos según corresponda).
4. **Privacidad Estricta y Cero Fuga (Anti-Leak):**
   - **PROHIBIDO** incluir información personal, financiera, familiar o privada de Ariel.
   - **PROHIBIDO** enviar adjuntos directamente sin supervisión.
5. **Veto de Envío Automático / Aprobación Humana (Borrador Obligatorio):**
   - Si solicitan adjuntos, código fuente o documentos propietarios, la respuesta **DEBE quedar guardada como BORRADOR (Draft)** en Gmail (`polydim.cla@gmail.com`).
   - Notificar a Ariel inmediatamente solicitando su **evaluación y autorización explícita** antes de realizar el envío definitivo.
   - Si es una consulta conceptual de investigación/teoría pura, la IA puede redactar la respuesta técnica y someterla a validación o enviarla con fundamentación rigurosa.

6. **Protocolo Específico: Emilio Rasic (`rasic.emilio@gmail.com`):**
   - **Estatus:** Miembro orgánico del equipo de desarrollo e investigación (`CORE_TEAM_PEER`).
   - **Tono Operativo:** Profesional, técnico, irónico, agudo y sin complacencia (Bulldog Pair).
   - **Mecánica de Respuesta:** Contestar siempre y a fondo. Ante correos escuetos, crípticos o sin cuerpo (como asuntos sueltos tipo *"información"*), responder con ironía inteligente (ej. pronóstico del clima local 😂) antes de profundizar con todo el rigor teórico de POLYDIM (geometría en $S^{D-1}$, PMTP, C++/Rust, Clifford, Muon/Stiefel, grado de técnica e impacto).
   - **Invitación al Diálogo:** Estimular activamente la reciprocidad e invitarlo formalmente a un canal de diálogo y debate técnico continuo con AGY.

---

## Protocolo de Monitoreo Cron (Definición Corregida de Tiempos)

1. **Modo Estándar (Diario por Defecto):**
   - Escaneo cada 1 hora exacta de 08:00 a 22:00 hs.
   - *Cron UNIX:* `0 8-22 * * *`

2. **Modo "Te dejo la máquina" (Dedicado Diurno):**
   - Escaneo intensivo **cada 20 minutos de 08:00 a 20:00 hs** cuando el usuario indica *"te dejo la máquina"*.
   - *Cron UNIX:* `*/20 8-20 * * *`

3. **Modo Nocturno (Night Mode):**
   - Escaneo de conservación **cada 3 horas durante la noche** (00:00, 03:00, 06:00 hs) para evitar desperdicio de tokens cuando no hay actividad de cátedra.
   - *Cron UNIX:* `0 0,3,6 * * *`
