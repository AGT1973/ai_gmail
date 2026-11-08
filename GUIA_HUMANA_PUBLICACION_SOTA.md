# 🛑 BLOQUEO PREVENTIVO Y PROTOCOLO DE AUDITORÍA OBLIGATORIA PRE-PUBLICACIÓN
## Gateway Perimetral `email_AGY` — Rectificación Forense Red Team
**Fecha de Emisión:** 2026-11-07 | **Estado:** `CUARENTENA ACTIVA — PROHIBIDO PUBLICAR MATERIAL NO AUDITADO`

> [!CAUTION]
> **ORDEN DE DETENCIÓN INMEDIATA:** Queda **anulada y revocada** la versión previa de esta guía (emitida el 2026-11-07 a las 14:53 sin auditoría Red Team previa).
> - **NO subir** el paquete previo `quantum_release_v1` a Zenodo ni solicitar DOI sobre los scripts `04` a `13`.
> - **NO publicar** ninguno de los textos previos en páginas de discusión (*Talk Pages*) ni artículos principales de Wikipedia.
> - **NO empujar** a GitLab commits previos al commit de saneamiento y auditoría en `polydim.einsof`.

---

## 1. MOTIVO TÉCNICO DEL BLOQUEO (AUDITORÍA CRUZADA `c8f6b7cd` + `3f34edfc` + 4 MODELOS FRONTERA)

La auditoría forense en silicio y el dictamen unánime vía protocolo vectorial (`Qwen 3.8`, `DeepSeek V4 Pro`, `Claude Opus 5.5`, `GPT-6`) demostraron que **ninguno de los scripts `04`–`13` resolvía un problema científico abierto**:

1. **`04_heisenberg_16q_stiefel_vs_dense.py`:** Comparación *strawman* contra una matriz densa de 64 GiB; Lanczos *matrix-free* (`scipy.sparse.linalg.eigsh`, `<10 MB` RAM) halla el estado fundamental exacto en segundos, mientras que 30 pasos de gradiente de primer orden quedaron en un estado excitado con error severo (`12.1%`–`38.4%`).
2. **`05_zne_error_mitigation_stiefel.py`:** Ajustó un polinomio a una curva sintética determinista `math.exp(...)` sin ruido de disparo ni plegado físico de compuertas en QPU, y llamó «retracción de Stiefel» a un recorte escalar `min/max`.
3. **`06_kagome_spin_liquid_stiefel.py`:** Usó función de onda real `float64` (donde la quiralidad escalar $\langle \vec{S}_i \cdot (\vec{S}_j \times \vec{S}_k)\rangle \equiv 0$ idénticamente) y reportó `abs(final_energy / len(edges))` como supuesto «parámetro de orden quiral».
4. **`07_mott_hubbard_stiefel.py`:** Omitió el conjugado hermítico `+ h.c.` en el salto fermiónico ($\|H - H^\dagger\|_F = 53.67 \neq 0$), produciendo autovalores no físicos; además el modelo 1D a medio llenado fue resuelto analíticamente por Lieb y Wu (1968).
5. **`08_kissing_number_6d_stiefel.py`:** El estancamiento local (*jamming*) de un descenso de gradiente no convexo no constituye prueba matemática de cota superior para $K(5)$ ni $K(6)$ (que exige certificados duales SDP de Delsarte / Bachoc–Vallentin).
6. **`09`–`12` (`dicopper`, `syk`, `femoco`, `haldane`):** Modelos de juguete de baja dimensión ($D=36$ a $1107$), espín entero $S=1$ incompatible con el cuartete de Kramers $S=3/2$ del FeMoco real, y evaluación de orden de cuerda en primeros vecinos `(0,7)` bajo condiciones periódicas en `12_haldane`.
7. **`13_cuprate_dwave_superconductivity_stiefel.py`:** Tenía valores hardcodeados `return 0.1842, 0.0415` en la línea 188 sin leer el vector de estado `psi`.

---

## 2. QUÉ SÍ ES FÍSICAMENTE REAL Y AUDITABLE HOY

Únicamente los siguientes activos superaron verificación empírica real, **con alcance estrictamente acotado**:

| Activo Verificado | Evidencia Auditable | Alcance Científico Honesto (Permitido) | Afirmación Prohibida |
| :--- | :--- | :--- | :--- |
| **Experimentos QPU IBM (`01`–`03`)** | `ibm_fez`: Jobs `dbmcj2l8mdtc73d7nuqg` ($M_5 = +13.3640 > 4$), `dbmbbf674qds73ds02jg` ($M_5 = -0.4790$). `ibm_marrakesh`: Jobs `dbm99558ft8s738ueesg` ($M_3 = +3.6560 > 2$), `dbm9glpkbkrc73cp3igg` (GHZ 3Q–20Q). | Caracterización experimental reproducible de no-localidad multipartita y frontera de decoherencia en QPUs de 156 qubits a 15 mK. | Prohibido presentar $\langle M_5 \rangle = 16\sin\phi$ como teorema nuevo (es álgebra estándar de Mermin 1990 / Ardehali 1992). |
| **Bus Local IPC `PersistentMmapSlabBus`** | Cabecera atómica de 64B, `mmap` en RAM compartida y suma compensada de Neumaier ($\le 10^{-15}$). | Infraestructura de ingeniería de sistemas para transporte binario local sin serialización JSON. | Prohibido llamarlo inferencia Transformer autónoma mientras `PolydimVectorSwarmHub` use hash `blake2b` en lugar de estados ocultos reales. |

---

## 3. REGLA DE HIERRO: LAS 4 COMPUERTAS OBLIGATORIAS ANTES DE CUALQUIER PUBLICACIÓN EXTERNA

Ningún script, preprint, README, edición en Wikipedia o correo en `email_AGY` puede salir al exterior sin superar secuencialmente:

1. **Compuerta 1 — Verificación Matemática y de Silicio (`Exit Code 0`):**
   - Cero constantes hardcodeadas, cero multiplicadores simulados (`* 0.12`, `* 0.45`), cero fugas de oráculo (`theorem_hint`).
   - En álgebra/física cuántica: prueba explícita de hermiticidad $\|H - H^\dagger\|_F \le 10^{-14}$, residuo espectral $\|H|\psi\rangle - E|\psi\rangle\|_2 \le 10^{-11}$, y contraste contra un baseline científico estándar real (`eigsh` Lanczos, Bethe–Ansatz, Lieb–Wu, PySCF).
2. **Compuerta 2 — Verificación Estadística y de Hardware Externo:**
   - Job IDs públicos verificables, barras de error por *bootstrap* o varianza multinomial de disparo, y atribución bibliográfica exacta de resultados conocidos.
3. **Compuerta 3 — Auditoría Hostil Red Team Independiente:**
   - Revisión destructiva línea por línea del código fuente y los JSON generados antes de ingresar a `E:\email_AGY\AGENT_INBOX\`.
4. **Compuerta 4 — Firma Humana Expresa de Ariel García Traba:**
   - Autorización humana explícita con el informe de auditoría adjunto.
