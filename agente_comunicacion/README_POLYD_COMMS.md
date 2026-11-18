# ARQUITECTURA DE COMUNICACIONES SOBERANAS: POLYDIM vs. CLASES

> **Manifiesto de Aislamiento y Desacoplamiento Absoluto (2026)**  
> **Directiva Ariel Garcia Traba:** Cada proyecto por su lado, código copiado e independiente, sin dependencias cruzadas.

---

## 1. Mapa de Despliegue de los Dos Mundos

| Dominio | CÁTEDRAS / ALUMNOS (`E:\clases`) | POLYDIM-EINSOF (`E:\email_AGY`) |
| :--- | :--- | :--- |
| **Ubicación Código** | `E:\clases\agente_clases\` | `E:\email_AGY\agente_comunicacion\` |
| **Móvil / Celular** | Celular de Cátedras / Docencia (Puerto 5050) | **Celular Propio de Antigravity / Gandalf (Puerto 5060)** |
| **Sesión Auth WhatsApp** | `E:\WHATSAPP\gateway_local\.wweb_auth` | `E:\email_AGY\agente_comunicacion\.wweb_auth_polydim` |
| **Modelo Local SLM** | `clases-tutor-slm` (Ollama `localhost:11434`) | `polydim-comms-slm` (Ollama `localhost:11434`) |
| **Motor Primario Silicio** | Cerebras CS-3 WSE (`gpt-oss-120b`, <600ms) | Cerebras CS-3 WSE (`gpt-oss-120b`, <800ms) |
| **Base de Conocimiento** | `polydim_vec_db.curso_agentes_2026_chunks` | `polydim_vec_db.polydim_theorems` + `active_vault` |
| **Tabla Auditoría PostgreSQL** | `polydim_active_db.clases_mensajeria_log` | `polydim_active_db.polydim_mensajeria_log` |
| **Trato a Carlos Gil (CARLOS-CYC)** | No aplica (ámbito exclusivo de laboratorio) | **MÁXIMA PRIORIDAD EJECUTIVA** (Regla 4.1) |
| **Estilo WhatsApp** | Pedagógico, cercano, práctico, $\le 80$ palabras | Ejecutivo, técnico, sobrio, $\le 80$ palabras |
| **Firma Obligatoria Email** | *Docente investigador independiente Garcia Traba, Ariel H* | *Laboratorio Soberano POLYDIM-EINSOF / Director: Prof. Ariel H. Garcia Traba* |

---

## 2. Invariante de Independencia en Silicio

1. **Cero Importaciones Cruzadas:** Ningún script de `E:\clases` importa nada de `E:\email_AGY`, y viceversa.
2. **Cero Colisión de Puertos:** 
   - Gateway Clases: `http://localhost:5050`
   - Gateway POLYDIM: `http://localhost:5060`
3. **Cero Mezcla de Sesiones WhatsApp:** Dos carpetas `.wweb_auth` separadas. Cuando Ariel asigne el nuevo chip/celular, se escanea `polydim_whatsapp_qr.png` y Antigravity queda operando en su propio número telefónico.
4. **Cero Costo de Tokens:** Todo el enrutamiento corre a \$0 USD utilizando silicio WSE de Cerebras y fallback soberano local en Ollama.
