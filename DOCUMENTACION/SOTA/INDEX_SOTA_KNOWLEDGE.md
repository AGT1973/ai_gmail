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

---

### 5. Caída de Precios y Nuevos Modelos de Contexto Largo (Thinking Machines Lab / Tinker)
- **Fecha de Ingesta:** 2026-10-10
- **Archivo Fuente:** `DOCUMENTACION/SOTA/SOTA_20261010_1a12366917f6ad40_Price_drops_and_new_models_for_long_context_work.md`
- **Conceptos Clave:**
  - **Eliminación del Long-Context Premium:** Tarifas planas de prefill/muestreo a 128K y 256K en Kimi K2.6, gpt-oss-120b.
  - **GLM-5.3-Flash (Z.ai):** Mecanismo de atención de bajo cómputo para tareas agénticas multimodales (4.5x/5.8x menor coste).
  - **DeepSeek-v4.1-Flash:** Alta esparsidad y velocidad.
  - **Deprecaciones:** Salida de Qwen3.6-27B, Nemotron-3-Nano y DeepSeek-v3.1 el 23 de octubre.
- **🎯 Aplicación al Proyecto POLYDIM:**
  - Optimización de asignación de presupuesto (Regla 20) y enrutamiento en Watchdogs / subagentes.

---

### 6. Aprendizaje y Persistencia en Agentes Auto-Mejorables (The AI Edge)
- **Fecha de Ingesta:** 2026-10-10
- **Archivo Fuente:** `DOCUMENTACION/SOTA/SOTA_20261010_1a12369538ca4f23_How_Self_Improving_Agents_Learn_from_Experience.md`
- **Conceptos Clave:**
  - **Persistencia Post-Run:** Necesidad de artefactos retenidos y conexiones reales a ejecuciones posteriores.
  - **Entornos Ejecutables vs. Logs:** El aprendizaje requiere entornos evaluables que produzcan nueva experiencia frente a fallas.
- **🎯 Aplicación al Proyecto POLYDIM:**
  - Valida la arquitectura de memoria permanente en PostgreSQL 16 y el desacople de ciclos de hardening.

---

### 7. Retiro de Serie MiMo V2.5 y Migración a V2.6 (Xiaomi MiMo)
- **Fecha de Ingesta:** 2026-10-10
- **Archivo Fuente:** `DOCUMENTACION/SOTA/SOTA_20261010_1a12368d867e17b5_MIMO_V2_5_PRO_and_MIMO_V2_5_Retirement_Notice.md`
- **Conceptos Clave:**
  - **Migración Forzosa:** Reemplazo de `mimo-v2.5-pro` por `mimo-v2.6-pro` y `mimo-v2.5` por `mimo-v2.6-flash`.
  - **Plazos:** Enrutamiento automático el 14 de octubre de 2026; corte definitivo el 21 de octubre.
- **🎯 Aplicación al Proyecto POLYDIM:**
  - Actualización de identificadores en el pool de modelos y conectores MCP.

---

### 8. Cuello de Botella Termodinámico e Hídrico en Centros de Datos (Xatakaletter #281)
- **Fecha de Ingesta:** 2026-10-11
- **Archivo Fuente:** `DOCUMENTACION/SOTA/SOTA_20261011_1a12c5fd4b62565b_Aragon_Datacenters_IA_Energy_Bottleneck.md`
- **Conceptos Clave:**
  - **Límite Físico de Escala:** AWS demandando 10.800 GWh/año y 755.000 m³ de agua en Aragón; 34% de la capacidad de red asignada a datacenters.
  - **Crisis del Paradigma Transformer:** La compensación de la pérdida entrópica por DPI obliga a un sobredimensionamiento masivo de clusters.
- **🎯 Aplicación al Proyecto POLYDIM:**
  - Justificación en la tesis de por qué la arquitectura continua en $S^{D-1}$ y el transporte PMTP Zero-Copy IPC son el camino necesario para una IA termodinámicamente viable frente a la fuerza bruta de la nube.

---

### 9. Retiro de Preprints Matemáticos por Falla de Matriz/Traza (OpenAI Math / K3 Hodge)
- **Fecha de Ingesta:** 2026-10-12
- **Archivo Fuente:** `DOCUMENTACION/SOTA/SOTA_20261012_OPENAI_MATH_RETRACTION_K3_HODGE.md`
- **Conceptos Clave:**
  - **Withdrawal Notice Oficial (6-7 Oct 2026):** Retiro de tres artículos del repositorio `openai/math`: *Algebraicity of Weil classes*, *Algebraicity of Kuga–Satake Correspondences* y *The rational Hodge conjecture for products of K3 surfaces*.
  - **Falla de Silicio / Manipulación Matricial:** Error de signo ($\pm 1$) en convención geométrica que invalidó la cancelación por estabilización de traza (*signed-double-point cancellation*).
- **🎯 Aplicación al Proyecto POLYDIM:**
  - Demostración empírica de la fragilidad del razonamiento puramente sintáctico 1D en álgebras complejas. Refuerza la necesidad del acumulador Neumaier compensado y verificación en silicio real con tolerancia $\le 10^{-15}$.

---

### 10. Liberación de Hardware Abierto de Google: Coral NPU en RISC-V y Giro TPU/JAX
- **Fecha de Ingesta:** 2026-10-12
- **Archivo Fuente:** `DOCUMENTACION/SOTA/SOTA_20261012_GOOGLE_CORAL_NPU_OPEN_HARDWARE_TPU_STRATEGY.md`
- **Conceptos Clave:**
  - **Acelerador de Tensores Abierto:** Google DeepMind / Research libera la IP completa de Coral NPU en Chisel/Verilog con estándar abierto RISC-V (`RV32IMF_Zve32x`) y motor matricial dedicado AXI4.
  - **Stack Completo Open-Source:** Toolchain basada en MLIR/IREE con soporte directo a JAX, PyTorch y LiteRT.
  - **Estrategia TPU Cloud vs. Open Edge:** Datacenter TPUs permanecen con stack de compilador abierto (OpenXLA/PJRT), mientras el silicio sintetizable abierto baja a ultra bajo consumo.
- **🎯 Aplicación al Proyecto POLYDIM:**
  - Ejecución del **Silicon Contract (Regla 27)**: diversificación inmediata de POLYDIM más allá del vendor-lock de NVIDIA (CUDA/Triton) hacia TPUs de Google Cloud vía `@jax.jit` / HLO estático y silicio abierto RISC-V acoplable con el Nodo Aladín.

---

### 11. Google Workspace MCP Servers y Clasificación Agentic OAuth (Google Cloud)
- **Fecha de Ingesta:** 2026-10-13
- **Archivo Fuente:** `DOCUMENTACION/SOTA/SOTA_20261013_GOOGLE_WORKSPACE_MCP_AGENTIC_OAUTH.md`
- **Conceptos Clave:**
  - **Servidores MCP Oficiales en Google Workspace:** Exposición directa de herramientas en Gmail, Drive y Calendar para agentes de IA mediante el protocolo estándar abierto Model Context Protocol (MCP).
  - **Flag Obligatoria `is_agentic`:** Google clasifica el tráfico de IA mediante la propiedad agentic en credenciales OAuth 2.0. Rechazo de peticiones no clasificadas a partir del 11 de noviembre de 2026.
  - **Inmutabilidad Post-Plazo:** Desde el 12 de noviembre de 2026, la configuración no se puede alternar en credenciales existentes.
- **🎯 Aplicación al Proyecto POLYDIM:**
  - Regula la infraestructura de agentes y herramientas MCP en el proyecto `agente-mail-508816`. Exige marcar las credenciales de agentes de correo/asistentes antes del 11 de noviembre de 2026 para garantizar interoperabilidad directa sin disrupción en los servidores MCP de Workspace.

---

### 12. Dimuon: Nuevo Optimizador SOTA para Fine-Tuning LoRA (Thinking Machines Lab / Tinker)
- **Fecha de Ingesta:** 2026-10-15
- **Archivo Fuente:** `DOCUMENTACION/SOTA/SOTA_20261015_165720_1a13d3498705b01d_Dimuon__a_new_optimizer_for_LoRA_fine-tuning.md`
- **Conceptos Clave:**
  - **Superación de AdamW en SFT:** Dimuon alcanza menor pérdida de entrenamiento en sustancialmente menos pasos que AdamW tradicional durante fine-tuning de adaptadores LoRA.
  - **Continuidad SFT -> RL:** Eficiencia de aprendizaje comparable a AdamW en cargas de Reinforcement Learning (RL), permitiendo mantener el mismo optimizador en todo el pipeline de post-entrenamiento.
- **🎯 Aplicación al Proyecto POLYDIM:**
  - Evaluación directa en los ciclos de calibración geométrica y afinamiento de capas de proyección en $S^{D-1}$, sustituyendo o contrastando el optimizador AdamW convencional por Dimuon en silicio local y clusters remotos.

---

### 13. Modelos de Decisión Clef y Soporte Jev en Local (Ollama)
- **Fecha de Ingesta:** 2026-10-15
- **Archivo Fuente:** `DOCUMENTACION/SOTA/SOTA_20261015_165722_1a101d6d8e0b79d8_Clef_and_Clef_Flash_Decision_Models_are_now_on_Oll.md`
- **Conceptos Clave:**
  - **Modelos de Decisión Autocontenidos:** Integración en Ollama de Clef y Clef Flash optimizados para flujos de decisión y enrutamiento en un solo paso.
  - **Soporte de Arquitecturas Jev-like:** Inferencia local ultrarrápida de orquestadores de decisión sin requerir llamadas costosas a APIs en la nube.
- **🎯 Aplicación al Proyecto POLYDIM:**
  - Despliegue en el Nodo Aladín (Debian 13 Headless) para el router local de tareas de hardening y triaje de subagentes sin latencia de red.

---

### 14. Auditoría de Benchmarks y Fingerprinting de Modelos Frontera ("Name That LLM" - Kaggle)
- **Fecha de Ingesta:** 2026-10-16
- **Archivo Fuente:** `DOCUMENTACION/SOTA/SOTA_20261016_090034_1a144886d9b0fda0_Competition_Launch__Name_That_LLM.md`
- **Conceptos Clave:**
  - **Atribución y Huella Textual:** Identificación y diferenciación estadística de 18 modelos frontera a partir de pasajes cortos no etiquetados (análisis de pistas léxicas, tono y sintaxis).
  - **Auditoría de Procedencia (AI Provenance):** Métodos de fingerprinting para detectar contaminación en benchmarks abiertos y caracterizar familias de pesos.
- **🎯 Aplicación al Proyecto POLYDIM:**
  - Relevancia directa para el protocolo Red Team y validación asintótica: demuestra cómo las representaciones lingüísticas 1D colapsadas dejan artefactos espurios identificables, reforzando la tesis de POLYDIM de preservar las invariantes puras en el espacio proyectivo $S^{D-1}$.

---

### 15. DeepSeek Search & Fetch API: Tarificación y Fin del Período Gratuito (DeepSeek)
- **Fecha de Ingesta:** 2026-10-18
- **Archivo Fuente:** `DOCUMENTACION/SOTA/SOTA_20261018_084657_1a14dc507481ae02_Notice_of_DeepSeek_Search_API_Pricing.md`
- **Conceptos Clave:**
  - **Soporte Server-Side de Búsqueda Web y Extracción:** DeepSeek API integra formalmente capacidades nativas de `web search` y `fetch` para sus modelos frontera.
  - **Estructura de Precios:** $0.75 por cada 1.000 peticiones exitosas (\$0.00075 por request).
  - **Impacto en Herramientas y Subagentes (Claude Code, Codex, DeepSeek Harness):** Las llamadas server-side ya golpean estas APIs. El período gratuito de prueba expira el **1 de noviembre de 2026 a las 00:00 (hora de Beijing)** (31 de octubre de 2026 a las 13:00 ART / 16:00 UTC), momento en que inicia la facturación obligatoria por petición.
- **🎯 Aplicación al Proyecto POLYDIM:**
  - **Blindaje Presupuestario y Economía de Tokens (Reglas 20 y 34b):** Monitorear y auditar la configuración de `polydim_deepseek_r1_agent` y scripts Python de triage para evitar consumos involuntarios de saldo. Separar formalmente las consultas de razonamiento puro en memoria/Stiefel de las búsquedas web, enrutando estas últimas preferentemente por Perplexity Sonar-Pro o herramientas locales del agente.

---

### 16. Coconut (Chain of Continuous Thought, arXiv:2412.06769) vs. Variedad POLYDIM
- **Fecha de Ingesta:** 2026-10-18
- **Archivo Fuente:** `DOCUMENTACION/SOTA/SOTA_20261018_083825_1a14ece8232c93c9_Emilio_Rasic_Feedback_y_Paper_Coconut.md`
- **Conceptos Clave:**
  - **Reasoning en Espacio Latente Continuo:** Coconut (Meta FAIR / UC Berkeley / CMU) sustituye tokens de razonamiento por retroalimentación directa del último *hidden state* continuo en un modelo autoregresivo.
  - **Divergencia Arquitectónica:** Coconut opera de forma recurrente dentro de *un único modelo* en espacio euclidiano $\mathbb{R}^d$ no acotado (riesgo de deriva numérica). POLYDIM opera como un **bus IPC inter-agente y multi-modelo en silicio (`PMTP`)** anclado a la **variedad de Stiefel $S^{D-1}$** con retracción polar de orden 4 y estabilidad isométrica garantizada.
- **🎯 Aplicación al Proyecto POLYDIM:**
  - Respaldo académico formal para el paper y whitebook: valida que la comunidad científica de frontera reconoce el límite de la serialización 1D discreta (CoT en texto) e impulsa el tránsito hacia el razonamiento continuo. POLYDIM lleva esta idea al nivel de **sistema operativo distribuido y hardware heterogéneo (C++/Rust/Triton)**.
