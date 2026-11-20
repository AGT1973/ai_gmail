# 🏛️ PROYECTO CARLOS-CYC: ASISTENTE ACTUARIAL SOBERANO ON-PREMISE

**Para:** Carlos Gil (`cegactuario@gmail.com`) / Ariel García Traba  
**Canal:** `E:\email_AGY` (Regla 4.1 Prioridad Socio CARLOS-CYC)  
**Fecha:** Noviembre 2026 | **Versión:** 1.0 (Piloto Funcional Certificado)

---

## 1. Resumen Ejecutivo y Tesis de Arquitectura

El proyecto implementa un asistente inteligente especializado en cálculo actuarial y gestión de carteras para una PyME de 50 usuarios, con despliegue en 2 fases:
- **Fase 1 (Piloto):** 10 usuarios de prueba, 1 a 2 consultas concurrentes. Costo de infraestructura y cómputo: **$0 USD adicionales**.
- **Fase 2 (Producción):** 50 analistas registrados, pico de hasta 40 consultas concurrentes en cierre mensual.

### Los 4 Principios Anticolapso (Reglas de Silicio)
1. **El SLM NUNCA calcula números:** La IA no hace aritmética de mortalidad, reservas ni primas. Únicamente interpreta en lenguaje natural, invoca herramientas deterministas mediante Tool-Calling (`JSON Schema`), y redacta el informe explicativo.
2. **Motor Actuarial Determinista:** Tablas CSO 2001, factores de descuento $v = (1+i)^{-1}$, anualidades temporales $\ddot{a}_{x:\overline{n}|}$, y reservas prospectivas calculadas en microcódigo con acumulación compensada de Neumaier ($\text{error} \le 1.7 \times 10^{-16}$).
3. **Generación Fiel de Documentos:** Salida nativa a **HTML5 interactivo**, planillas **Excel (`.xlsx`) con fórmulas vivas**, presentaciones **PowerPoint (`.pptx`)**, informes **Word (`.docx`)** y despacho por **Mail (`.eml`)**.
4. **Soberanía y $0 USD Recurrentes:** Cero fugas de datos confidenciales de pólizas hacia APIs comerciales externas. Operación 100% on-premise.

---

## 2. Hoja de Ruta en 2 Fases

| Parámetro | Fase 1: Piloto (Inmediato) | Fase 2: Producción (Escalado) |
| :--- | :--- | :--- |
| **Población** | 10 analistas clave | 50 usuarios corporativos |
| **Concurrencia Pico** | 1 – 2 consultas simultáneas | Hasta 40 consultas simultáneas |
| **Motor de Inferencia** | **Ollama** en nodo ALADIN / local | **vLLM** (Continuous Batching + PagedAttention + XGrammar) |
| **Modelo Base** | `Qwen 2.5 3B` / `4B` GGUF | `Qwen 3/3.8 4B u 8B` (SFT actuarial + Poda 32k español) |
| **Hardware** | PC existente / Nodo ALADIN (CPU o GPU 8-12 GB) | 1 Servidor On-Premise con 1× RTX 4090 (24GB) o RTX 5090 (32GB) |
| **Costo Nube / APIs** | **$0 USD** | **$0 USD/mes** ($150–$350 pago único si se poda en Alibaba) |

---

## 3. Pruebas de Silicio Certificadas (Exit Code 0)

Todos los módulos del núcleo han sido compilados y ejecutados en hardware físico:

1. **`actuarial.py` (Exit Code 0):**
   - Mortalidad $q_x$ a 40 años (M): `0.002220` (Esperanza curtate: 28.13 años).
   - Seguro Temporal 20 años, 35 años (M), \$1.000.000 suma asegurada:
     - Prima Única Neta (PUN): **\$52,190.15**
     - Prima Nivelada Anual (PNA): **\$3,776.12** (Mensual: **\$314.68**)
   - Reserva Matemática prospectiva al año 10: **\$21,682.59**.
2. **`db.py` (Exit Code 0):**
   - Base de datos `carlos_cyc` inicializada en PostgreSQL 16 con extensión `pgvector` y tablas de auditoría de tokens/latencias.
3. **`exporters.py` (Exit Code 0):**
   - Generación comprobada de archivos reales en `E:\POLYDIM_EINSOF\CARLOS_CYC\piloto_actuarial\exports\`.
4. **`benchmark_toolcall.py` (Exit Code 0 — Task 417):**
   - Modelo: `qwen2.5:3b` ejecutándose en el nodo ALADIN (`192.168.100.21:11434`).
   - Tasa de acierto de Tool-Calling estructurado: **83.3%** (`APTO`).
   - Latencia promedio: **10.3 segundos** (nodo CPU/GPU compartida sin vLLM).

---

## 4. Estructura de Archivos del Prototipo

Ubicación en el repositorio: `E:\POLYDIM_EINSOF\CARLOS_CYC\piloto_actuarial\`
- [`actuarial.py`](file:///e:/POLYDIM_EINSOF/CARLOS_CYC/piloto_actuarial/actuarial.py): Motor matemático puro (IEEE-754 / Neumaier).
- [`db.py`](file:///e:/POLYDIM_EINSOF/CARLOS_CYC/piloto_actuarial/db.py): Esquema relacional y vectorial en PostgreSQL 16.
- [`exporters.py`](file:///e:/POLYDIM_EINSOF/CARLOS_CYC/piloto_actuarial/exporters.py): Renderizadores para Office y correo.
- [`llm_client.py`](file:///e:/POLYDIM_EINSOF/CARLOS_CYC/piloto_actuarial/llm_client.py): Orquestador compatible OpenAI/Ollama/vLLM.
- [`server.py`](file:///e:/POLYDIM_EINSOF/CARLOS_CYC/piloto_actuarial/server.py): Backend FastAPI con WebSocket para streaming y auditoría.
- [`static/index.html`](file:///e:/POLYDIM_EINSOF/CARLOS_CYC/piloto_actuarial/static/index.html): Frontend corporativo Web HTML5 sin dependencias externas.

---

## 5. Instrucciones de Puesta en Marcha (Piloto)

Para levantar el piloto inmediatamente en la red de la oficina:
```bash
cd E:\POLYDIM_EINSOF\CARLOS_CYC\piloto_actuarial
python -m pip install -r requirements.txt
python server.py
```
Acceso en navegador: `http://localhost:8080/` (o la IP interna de la máquina servidora).
