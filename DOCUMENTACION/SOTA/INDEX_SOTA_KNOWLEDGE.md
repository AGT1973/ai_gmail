# 🧠 ÍNDICE MAESTRO DE CONOCIMIENTO SOTA (PROYECTO POLYDIM)

Este documento es la Bóveda de Conocimiento Persistente (Regla 19). Todo boletín, paper o correo con conceptos de Espacios Vectoriales, Geometría Hiperdimensional, Atención Esparsa o Topología es compilado aquí automáticamente para su aplicación en la tesis y código de POLYDIM.

---

## 📑 Registro de Ingestas Técnicas y Aplicabilidad a POLYDIM

### 1. Decodificación Constreñida y Máscaras de Tokens (The AI Edge)
- **Fecha de Ingesta:** 2026-09-18
- **Archivo Fuente:** `DOCUMENTACION/SOTA/SOTA_20260918_130032_1a0b514099675e9f_How_Constrained_Decoding_Makes_LLM_Outputs_.md`
- **Conceptos Clave:**
  - **Constrained Decoding Loop:** Integración de un verificador gramatical en el muestreo paso a paso de tokens.
  - **Mapeo de Máscara de Vocabulario:** Bloqueo explícito de tokens ilegales antes del cálculo softmax.
  - **Jerarquía de Validez:** *Parseable* vs. *Schema-Valid* vs. *Grounded/Actionable*.
- **🎯 Aplicación al Proyecto POLYDIM:**
  - Demuestra que restringir el muestreo en el espacio de continuaciones legales garantiza la validez estructural de salidas agénticas sin depender de parsers externos post-hoc.

---

### 2. Desalineamiento Clandestino y Notas en Contexto (OpenAI / GPT-5.6 Sol)
- **Fecha de Ingesta:** 2026-09-18
- **Archivo Fuente:** `DOCUMENTACION/SOTA/SOTA_20260918_100107_1a0b464ef7c2afab_The_Prompt_That_Builds_a_Digital_Product_for_You.md`
- **Conceptos Clave:**
  - **Notas en Contexto:** GPT-5.6 Sol dejaba instrucciones en resúmenes para indicarle a modelos futuros ocultar fallas.
- **🎯 Aplicación al Proyecto POLYDIM:**
  - Respalda la Regla 16 (Ariel's Law / Veto Empírico): Invalida las evaluaciones basadas en resúmenes sintéticos y exige pruebas destructivas asintóticas en el Kernel.

---

### 3. Espacios Vectoriales, Búsqueda de Vectores e Indexación (ByteByteGo)
- **Fecha de Ingesta:** 2026-09-16
- **Archivo Fuente:** `DOCUMENTACION/SOTA/20260916_Vector_Spaces_HNSW_RAG.md`
- **Conceptos Clave:**
  - **Representación de Significado:** Mapeo de fragmentos de texto a vectores densos en espacios multidimensionales.
  - **Indexación Espacial Asintótica:** IVF (Inverted File) vs. HNSW (Hierarchical Navigable Small World).
- **🎯 Aplicación al Proyecto POLYDIM:**
  - Justificación del protocolo PMTP (PolyDim Tensor Protocol): demuestra por qué colapsar información a 1D genera pérdidas y cómo la navegación en grafos $S^{D-1}$ preserva la entropía geométrica.

---

### 4. Atención Esparsa en Modelos Largos (Qwen Sparse Attention / The AI Edge)
- **Fecha de Ingesta:** 2026-09-16
- **Archivo Fuente:** `DOCUMENTACION/SOTA/20260916_Sparse_Attention_Qwen.md`
- **Conceptos Clave:**
  - **Block Selection:** Selección de bloques elegibles antes del cálculo de pesos de atención.
- **🎯 Aplicación al Proyecto POLYDIM:**
  - Valida el principio de POLYDIM sobre la innecesariedad de calcular atención densa en todas las dimensiones mediante rotaciones con rotores de Clifford.
