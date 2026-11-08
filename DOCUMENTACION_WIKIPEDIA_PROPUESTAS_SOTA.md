# 🛑 DOCUMENTO RETIRADO POR AUDITORÍA RED TEAM (PROHIBIDA SU PUBLICACIÓN EN WIKIPEDIA)
**Fecha de Retiro:** 2026-11-07 | **Estado:** `ANULADO — NO PUBLICAR EN WIKIPEDIA NI TALK PAGES`

> [!WARNING]
> Todas las propuestas de inserción en Wikipedia contenidas en la versión anterior de este archivo quedan **formalmente retiradas y vetadas**.
> Publicar resultados propios no revisados por pares o simulaciones de clústeres finitos como «soluciones a problemas abiertos» viola las políticas centrales de Wikipedia (`WP:NOR` — *No Original Research*, `WP:RS` — *Reliable Sources*, `WP:COI` — *Conflict of Interest* y `WP:FRINGE`) y expondría al autor a reversiones y bloqueos de cuenta.

---

## REGISTRO DE INVALIDACIÓN TÉCNICA PUNTO POR PUNTO

1. **`Mermin's inequality` (`MERMIN_5Q`):**
   - La ejecución en `ibm_fez` (`Job dbmcj2l8mdtc73d7nuqg`, $M_5 = +13.3640 > 4.0$) es una medición experimental legítima, pero la relación $\langle \text{GHZ}(\phi)|M_5|\text{GHZ}(\phi)\rangle = 16\sin\phi$ es álgebra estándar publicada por Mermin (1990) y Ardehali (1992), no la resolución de un problema abierto.
2. **`Kissing number` (`K(5)` y `K(6)`):**
   - El atasco (*jamming*) de un flujo de gradiente local sobre $(S^{d-1})^N$ no demuestra cotas superiores matemáticas globales (que requieren certificados duales de programación semidefinida tipo Delsarte / Bachoc–Vallentin).
3. **`Kagome lattice` (`KAGOME_SPIN_LIQUID`):**
   - La versión previa reportó erróneamente `abs(E_0 / 18) = 0.6898` como parámetro quiral sobre un vector `float64` real donde la quiralidad escalar es idénticamente nula, y un clúster de $N=12$ espines no decide el límite termodinámico de Herbertsmithite.
4. **`Ramsey's theorem` (`RAMSEY_R55`):**
   - La cota superior vigente es $43 \le R(5,5) \le 46$ (Angeltveit–McKay 2024), y en $\text{Paley}(41)$ la cota de Hoffman vale $\sqrt{41} \approx 6.403 > 5$ (no excluye $K_5$ ni resuelve $R(5,5)$).
5. **`Sachdev–Ye–Kitaev model` (`SYK4`):**
   - Diagonalización densa (`np.linalg.eigh`) de una sola realización aleatoria miniatura ($N=12, D=32$); no constituye aporte al límite holográfico.
6. **`FeMoco` (`FEMOCO_NITROGENASE`):**
   - Modelo de juguete de 8 espines $1/2$ ($D=256$) con espín entero $S_{\text{tot}}=1$, físicamente incompatible con el estado basal real $S=3/2$ del cofactor $[\text{MoFe}_7\text{S}_9\text{C}]$.
7. **`Haldane conjecture` (`HALDANE_GAP_SPT`):**
   - Problema ya resuelto históricamente (AKLT 1987, White DMRG 1992); además el script previo midió el orden de cuerda entre los sitios `(0,7)` que en un anillo periódico de 8 sitios son primeros vecinos ($r=1$).
8. **`High-temperature superconductivity` (`CUPRATE_DWAVE`):**
   - El script previo contenía `return 0.1842, 0.0415` hardcodeado en la línea 188; aun corregido en un clúster finito de Betts de 8 sitios ($D=3,136$), una diagonalización exacta de 8 sitios no prueba orden de largo alcance fuera de la diagonal (ODLRO) en el límite termodinámico.
