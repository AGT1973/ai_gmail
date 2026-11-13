# PROTOCOLO DE REGISTRO PREPRINT & DEPÓSITO ZENODO (VÍA PERÍMETRO EXCLUSIVO `email_AGY`)

**Fecha:** 2026-11-08  
**Autor:** Ariel García Traba  
**Proyecto Emisor:** `POLYDIM_EINSOF`  
**Gateway Autorizado de Publicación:** `email_AGY` (`E:\email_AGY`)

---

## 🛡️ MANDATO PERIMETRAL GLOBAL (REGLA 1 & 2):
Ningún proyecto de programación, álgebra o tensores (`POLYDIM`, `EinsofOS`) tiene autorización para comunicarse directamente con el exterior o subir archivos a Zenodo/arXiv. Todo depósito debe ser ejecutado exclusivamente a través del workspace perimetral `email_AGY`.

---

## 📦 CONTENIDO DEL PAQUETE DE PREPRINT LISTO PARA DEPÓSITO:
1. **Manuscrito Principal:** `E:\POLYDIM_EINSOF\PREPRINT_ZENODO_ARXIV_READY\manuscript_ieee_stiefel_quantum_routing.md`  
   - 35.5 kB, formato IEEE Transactions / ACM.
   - Aprobado por el Tribunal SOTA (DeepSeek 8.6/10, Qwen MoE).
   - 16 ejecuciones físicas verificadas en procesadores superconductores IBM Quantum de 156 qubits (`ibm_fez`, `ibm_kingston`, `ibm_marrakesh`).
2. **Metadatos Zenodo (JSON):** `E:\POLYDIM_EINSOF\PREPRINT_ZENODO_ARXIV_READY\metadata_zenodo.json`  
   - Título, autores, filiación, resumen ejecutivo, 11 palabras clave y licencia CC-BY-4.0.

---

## 🚀 PASOS PARA `email_AGY`:
1. Abrir sesión en `email_AGY`.
2. Leer `E:\POLYDIM_EINSOF\PREPRINT_ZENODO_ARXIV_READY\metadata_zenodo.json`.
3. Iniciar depósito en la API de Zenodo (`https://zenodo.org/api/deposit/depositions`) usando el token de Zenodo de `email_AGY`.
4. Subir el archivo `manuscript_ieee_stiefel_quantum_routing.md` (o su versión compilada en PDF).
5. Publicar el depósito para obtener el **DOI definitivo de Zenodo** (e.g. `10.5281/zenodo.XXXXXXX`).
6. Retornar el DOI obtenido a `polydim_active_db.active_vault` con clave `zenodo_paper_a_doi`.
