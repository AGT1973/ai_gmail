# 🏛️ COMUNICACIÓN TÉCNICA Y ESTRATÉGICA: PROYECTO CARLOS-CYC
## Análisis de Supuestos Críticos, Tiempos de Entrega y Límites de Hardware: Adosado en Colab/Kaggle vs. Poda en Servidores Alibaba

**Para:** Carlos Gil (`cegactuario@gmail.com`)  
**De:** Ariel García Traba  
**Proyecto:** CARLOS-CYC / Ecosistema POLYDIM-EINSOF  
**Canal:** `E:\email_AGY` (Prioridad Socio CARLOS-CYC)  
**Fecha:** Noviembre 2026  
**Documento Maestro:** `E:\email_AGY\DOCUMENTOS_MAESTROS\COMUNICACION_CARLOS_CYC_SLM_ACTUARIAL_V2.md`

---

Estimado Carlos,

Te comparto esta actualización técnica donde plasmamos con total crudeza y precisión los **supuestos operativos, los tiempos reales de desarrollo y la frontera física entre lo que se puede hacer en entornos gratuitos (Colab / Kaggle) frente a lo que exige un servidor dedicado como Alibaba Cloud PAI.**

El objetivo del proyecto sigue siendo innegociable: **un asistente actuarial soberano, alojado físicamente en la oficina (on-premise), con costo de $0 USD mensuales en APIs externas, con secreto profesional absoluto y donde el modelo JAMÁS invente un número de cálculo.**

---

### 1. El Marco de Supuestos Críticos para la PyME

Para que el proyecto sea viable técnica y económicamente, debemos partir de supuestos claros:

1. **Supuesto de Concurrencia y Población:**
   - La PyME cuenta con **50 usuarios registrados**.
   - En operación normal el uso es esporádico (1 a 3 consultas en vuelo).
   - En momentos críticos (cierre mensual, balance, jornadas de tarificación masiva), se debe soportar un pico de **hasta 40 analistas concurrentes**.
2. **Supuesto de Precisión Matemática (Cero Alucinación):**
   - El modelo de lenguaje (SLM) **no es una calculadora**. Un LLM predice texto, no ejecuta matemáticas de punto flotante exactas.
   - **Solución implementada:** La IA solo traduce lenguaje natural a una llamada de función estructurada (`Tool Call` en formato JSON). El cálculo real de reservas, primas temporales y tablas CSO 2001 lo ejecuta un **Motor Actuarial Determinista en Python/Rust** con precisión Neumaier (error residual $\le 1.7 \times 10^{-16}$).
3. **Supuesto de Entorno de Ejecución Local:**
   - El sistema correrá on-premise. Se contempla como runtime local el uso de **Ollama**, o bien la integración directa con **Antigravity** orquestando al agente externo **`ia_cyc`**. Para el escalado masivo de 40 usuarios se utilizará **vLLM** compartiendo una única instancia en memoria.

---

### 2. La Frontera Técnica del Hardware: Colab / Kaggle vs. Alibaba Cloud

Existe una diferencia técnica estructural entre **adosar un adaptador (QLoRA)** y **recortar físicamente el modelo (Poda de Vocabulario)**:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│               FRONTERA DE ENTRENAMIENTO Y ESPECIALIZACIÓN DE MODELOS                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  EN COLAB (A100) / KAGGLE (Dual Tesla T4) ➔ $0 USD (Inversión Cero)                     │
│  ✔ ADOSADO (QLoRA): Congela el modelo base y le adosa matrices de adaptación.         │
│  ✔ ENCORSETADO: Se fijan instrucciones de sistema y rechazos estrictos para que hable   │
│     únicamente en español y sobre pólizas de la empresa.                                │
│  ❌ LÍMITE: NO PUEDE RECORTAR EL MODELO. El tamaño no se achica; de hecho, crece leve-  │
│     mente. Conserva intactos los 152.000 tokens multilingües en VRAM.                   │
│                                                                                         │
│  EN SERVIDORES DEDICADOS ALIBABA CLOUD (PAI-DLC / 8x A100/H800) ➔ $150 – $350 USD       │
│  ✔ RECORTE FÍSICO: Amputa físicamente ~120.000 tokens de idiomas ajenos (chino, árabe,  │
│     cirílico) reduciendo la matriz de 152k a solo 32k tokens (Español + Código).        │
│  ✔ CURACIÓN (HEALING CPT): Entrena el modelo podado con 200M–500M tokens en español    │
│     para re-alinear los pesos desbalanceados por la cirugía.                            │
│  ✔ RESULTADO: Un SLM nativo 35%–50% más liviano, que corre en placas de video chicas    │
│     y jamás puede emitir caracteres en idiomas extranjeros.                             │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### Comparativa Técnica Detallada de Ambas Vías:

| Parámetro | Vía 1: Adosado y Encorsetado (Colab / Kaggle) | Vía 2: Recorte Físico y Poda (Servidor Alibaba Cloud) |
| :--- | :--- | :--- |
| **Entorno de Entrenamiento** | **Google Colab o Kaggle** (GPUs gratuitas o suscripción Colab de \$12). | **Alibaba Cloud PAI-DLC** (Clúster multi-GPU dedicado para re-entrenamiento continuo). |
| **Técnica Aplicada** | **QLoRA + DPO de confinamiento.** Matrices de bajo rango acopladas a la atención. | **Poda de Vocabulario (152k ➔ 32k) + Poda de Capas + CPT (Continued Pre-Training).** |
| **Impacto en el Tamaño** | **No se reduce.** Qwen mantiene sus ~152.000 tokens en la entrada y salida (~1.100M parámetros solo en embeddings). | **Se reduce entre un 35% y un 50%.** Desaparecen cientos de millones de parámetros muertos. |
| **Generación de Idiomas** | El modelo puede generar chino o ruso si el usuario lo força; el corsé es solo a nivel de comportamiento. | **Físicamente imposible:** los tokens extranjeros fueron extirpados de la matriz de pesos. |
| **Velocidad de Inferencia** | Cada palabra generada evalúa probabilidades contra 152.000 logits en el Softmax final. | Evalúa contra 32.768 logits. **Inferencia entre 25% y 40% más veloz en la oficina.** |
| **Hardware Requerido en Oficina (para 40 usuarios)** | GPU de gama alta con **24 GB a 32 GB de VRAM** (NVIDIA RTX 4090 / RTX 5090). | GPU accesible de **12 GB a 16 GB de VRAM** (RTX 3060 12GB / RTX 4060 Ti 16GB / RTX 4070). |
| **Costo de Computación Nube** | **\$0 USD** (o \$12 en Colab). | **\$150 a \$350 USD** (pago único por las horas de clúster A100 en Alibaba). |

---

### 3. Estimación de Tiempos Reales de Producción

Los plazos de ingeniería no dependen solo de la programación, sino de las horas de cómputo, validación cruzada y pruebas de carga:

```
Línea de Tiempo del Proyecto (Semanas)
Semana 1 ➔ [Despliegue Prototipo Local + Conexión Ollama/Antigravity] (LISTO)
Semana 2 ➔ [Fase 1: Piloto 10 Analistas con QLoRA/Corsé en Colab/Kaggle]
Semana 3–5 ➔ [Pruebas de Carga Reales + Cosecha de Logs en PostgreSQL]
Semana 6 ➔ [Fase 2 (Opcional): Poda y Curación en Alibaba Cloud ➔ SLM Definitivo]
```

1. **Adosado y Encorsetado en Colab/Kaggle (Vía 1):**
   - **Tiempo de preparación del dataset:** 2 a 3 días.
   - **Tiempo de corrida de entrenamiento:** **2 a 4 horas** en GPU.
   - **Pruebas y ensamblado a Ollama/Antigravity:** 1 a 2 días.
   - **Disponibilidad para pruebas:** **Menos de 1 semana.**
2. **Recorte Físico, Poda y Healing en Alibaba Cloud (Vía 2):**
   - **Cirugía de vocabulario y tensores:** 2 días de desarrollo de scripts.
   - **Corrida de CPT (Healing de 500M tokens en Alibaba PAI):** **12 a 24 horas continuas** en clúster A100.
   - **Alineación final SFT + cuantización GGUF/AWQ:** 2 días.
   - **Validación de no-degradación lógica:** 3 a 5 días de pruebas actuariales.
   - **Disponibilidad del SLM recortado:** **2 a 3 semanas de trabajo.**

---

### 4. Salidas y Entregables del Sistema en Oficina

El sistema final entrega al analista una experiencia integrada sin fricción:
- **Pantalla Web HTML5 (Intranet):** Chat fluido, visualización inmediata de tablas de mortalidad y primas, sin necesidad de instalar nada en las 50 computadoras de los analistas.
- **Exportación en Excel (`.xlsx`):** Planilla con membrete corporativo y **fórmulas vivas** (ej. `=B5/12` para la prima mensual), permitiendo que el actuario audite y verifique las celdas en su planilla habitual.
- **Presentaciones PowerPoint (`.pptx`):** Diapositivas automáticas con resumen ejecutivo para comités o clientes.
- **Informes Word (`.docx`):** Documento formal con cláusulas, tablas numéricas y advertencias legales.
- **Despacho por Mail (`.eml`):** Correo generado automáticamente con los documentos adjuntos listo para enviar.

---

### 5. Recomendación Ejecutiva de Pasos a Seguir

Para que la PyME no asuma ningún riesgo financiero innecesario:

1. **Paso Inmediato (Fase 1 — Piloto a Costo Cero):**
   - Arrancar con **10 usuarios** utilizando el **modelo encorsetado mediante QLoRA/Prompting en Colab/Kaggle** (\$0 en cómputo).
   - Correrlo en la oficina con **Ollama** o directamente mediante **Antigravity** orquestando a **`ia_cyc`**.
   - Los cálculos corren bajo el motor determinista ya testeado (`Exit Code 0`).
2. **Paso Secundario (Fase 2 — Producción con 50 usuarios):**
   - Durante 30 días, el sistema registrará silenciosamente en PostgreSQL (`carlos_cyc.audit_log`) todas las preguntas y tablas que los analistas realmente consultan.
   - Con esa base empírica, decidimos si la oficina invierte en una placa grande (RTX 4090/5090) manteniendo el modelo completo, o si enviamos el modelo a **Alibaba Cloud (\$150–\$350 USD de cómputo)** para podarle los idiomas extranjeros y dejar un **SLM ultraliviano** que corra en computadoras convencionales.

Quedo a tu disposición para mostrarte el prototipo funcionando o revisar juntos las tablas de mortalidad incorporadas.

Un cordial saludo,

**Ariel García Traba**  
*Ecosistema POLYDIM-EINSOF*
