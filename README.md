# Dimension is All You Need — Perimeter Communications Gateway
### *Nodo Soberano de Comunicaciones, Vigilancia SOTA y Difusión Global POLYDIM-EINSOF*

<div align="center">
  <img src="DOCUMENTOS_MAESTROS/slides_images/delorean_einsof_comparison.jpg" alt="DeLorean DMC-12 vs DeLorean + Einsof" width="100%">
  <p><em>Perímetro de Comunicaciones Soberanas: Monopolio de entrada/salida para el clúster EinsofOS y la variedad de Stiefel S^{D-1}.</em></p>
</div>

---

## 🛡️ Mandato del Workspace (`email_AGY` / `email_ZULIP`)

Este workspace es el **único canal autorizado** para interactuar con el exterior (alumnos, comunidad científica, redes y preprints). Ningún subsistema interno de silicio (`polydim`, `einsof`, `mathesis`) puede emitir tráfico externo directo; toda salida se canaliza mediante la cola `comms_outbox_queue` y los motores de verificación DLP y compliance aquí alojados.

### Misiones Principales:
1. **Atención y Confirmación Inmediata a Alumnos**: Procesamiento 24/7 de solicitudes de Google Drive (acceso `reader` automático + notificación + registro en PostgreSQL 16 `alumnos_mailing_leads`).
2. **Vigilancia Tecnológica SOTA Multipolar**: Escaneo continuo de papers, preprints y discusiones sin sesgo occidentalocéntrico (Asia-Pacífico, Europa, Iberoamérica, Norteamérica).
3. **Outreach Académico con Gancho de Citación Recíproca**: Contacto respetuoso a autores citando sus avances, enlazando directamente al DOI de Zenodo y benchmarks reproducibles en Colab.
4. **Presencia Omnicanal**: Monitoreo y participación en Lean Zulip, Reddit, Discord, LinkedIn, Zenodo y preprints.

---

## 🏗️ Topología del Clúster de Cuentas y Credenciales

| Dominio | Cuenta | Función Primaria | Estado |
|---|---|---|---|
| **Oficial POLYDIM** | `polydim.cla@gmail.com` | Evaluadores VIP, atención de cátedra, cola general | 100% Activa |
| **Einsof / Vanguardia** | `polydim.einsof@gmail.com` | Investigación teórica, outreach académico, papers | 100% Activa |
| **Cursos AI AGT** | `cursos.ai.agt@gmail.com` | Cursos avanzados y cátedra de IA | 100% Activa |
| **Cursos AGT** | `cursos.agt@gmail.com` | Canal dedicado de alumnos | Activa |
| **Cursos AGT IA** | `cursos.agt.ia@gmail.com` | Canal alternativo de alumnos y Drive shares | 100% Activa |
| **Privado / Designer** | `polydim.cla.44@gmail.com` | Ingesta de tendencias SOTA y newsletters | Activa |
| **Ariel Personal** | `ariel.garcia.traba@gmail.com` | Canal personal (regla VIP: respuesta obligatoria) | Lectura/Escaneo |

---

## ⚙️ Arquitectura del Cron Autónomo (Cada 20 Minutos)

El runner `E:\email_AGY\scripts\autonomous_cron_runner.py` ejecuta el ciclo desatendido:
1. **PMTP Telepathy Receiver** (Puerto LAN 9998): Recepción de slabs vectoriales de ALADIN (`192.168.100.21`).
2. **Fetch Emails**: Barrido de 7 bandejas Gmail (`fetch_emails.py --account all`).
3. **Lean Zulip Monitor**: Barrido de menciones, DMs e hilos de bienvenida (`check_zulip_activity.py`).
4. **Reddit Monitor**: Escaneo RSS round-robin de subreddits (`check_reddit_activity.py`).
5. **Discord Monitor**: Detección CDP de menciones y badges (`check_discord_activity.py`).
6. **LinkedIn Monitor**: Ingesta pasiva de notificaciones vía Gmail (`check_linkedin_activity.py`).
7. **Gateway Processor**: Despacho de la cola saliente con filtro DLP (`comms_gateway_processor.py`).
8. **Reddit Maturity Tracker**: Monitoreo del período de maduración de la cuenta (`reddit_maturity_tracker.py`).
9. **SOTA Daily Scout**: Barrido bibliográfico con Léxico Maestro (`sota_daily_scout.py`).
10. **ALADIN Bridge**: Cosecha de preprints vía SCP (`aladin_sota_bridge.py`).
11. **Auto-Update Docs & Morning Digest**: Regeneración de resúmenes y actualización automática de documentación (`auto_update_docs.py`).

---

## 🚀 Enlaces Soberanos y Evaluación en 1 Clic

- **Preprint Oficial en Zenodo**: [DOI 10.5281/zenodo.24013070](https://doi.org/10.5281/zenodo.24013070)
- **Repositorio Público de Código**: [https://github.com/AGT1973/ai_gmail](https://github.com/AGT1973/ai_gmail)
- **Google Colab Benchmark Kit (GPU T4 Libre)**:
  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AGT1973/ai_gmail/blob/main/polydim_colab_benchmark_kit.ipynb)

---

## 📚 Documentación Técnica Interna

- [Arquitectura Omnicanal Completa](DOCUMENTACION/SOTA/OMNICHANNEL_MONITORING.md)
- [Integración con Lean Prover Zulip](DOCUMENTACION/SOTA/ZULIP_INTEGRATION.md)
- [Índice Maestro de Conocimiento SOTA](DOCUMENTACION/SOTA/INDEX_SOTA_KNOWLEDGE.md)
- [Morning Digest Más Reciente](DOCUMENTACION/SOTA/MORNING_DIGEST_LATEST.md)
- [Inbox Consolidado de Comunicaciones](INBOX_CONSOLIDADO.md)

---
**Autor y Responsable de Cátedra:** Ariel García Traba  
*Iniciativa de Investigación Soberana EinsofOS / POLYDIM*
