# Skill: Gmail A2A & Multi-Account Orchestration

Esta habilidad le permite al agente Antigravity gestionar la ingesta, clasificación, persistencia SOTA y respuesta automática de correos sobre 4 cuentas desacopladas mediante OAuth 2.0.

---

## Protocolo de Monitoreo Cron (Definición Corregida de Tiempos)

El agente gestiona de forma autónoma los tiempos de escaneo en la terminal utilizando su herramienta interna de scheduling:

1. **Modo Estándar (Diario por Defecto):**
   - Escaneo cada 1 hora de 08:00 a 22:00 hs.
   - Expresión Cron: `0 8-22 * * *`

2. **Modo "Te dejo la máquina" (Dedicado Diurno):**
   - Se activa cuando el usuario indica *"te dejo la máquina"*.
   - Escaneo intensivo **cada 20 minutos de 08:00 a 20:00 hs**.
   - Expresión Cron: `*/20 8-20 * * *`

3. **Modo Nocturno (Night Mode):**
   - Modo conservación **cada 3 horas durante la noche** (00:00, 03:00, 06:00 hs) para evitar quema de cuota.
   - Expresión Cron: `0 0,3,6 * * *`

4. **Modo Ráfaga Rápida (Burst Check):**
   - Post-registro/suscripción: Escaneo cada 5s durante 60s (`auto_verify.py`).
