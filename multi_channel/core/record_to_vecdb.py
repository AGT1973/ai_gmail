"""
Registrador de Memoria Vectorial SQLite (Regla 0 - POLYDIM)
===========================================================
Registra el estado de la arquitectura multicanal, el protocolo de
colaboradores academicos (Kevin Piterman, Emilio Rasic) y la configuracion
de los gateways en E:\\POLYDIM-THEORICAL\\POLYDIM_VECDB.sqlite.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

VECDB_PATH = Path(r"E:\POLYDIM-THEORICAL\POLYDIM_VECDB.sqlite")

def record_multichannel_milestone():
    if not VECDB_PATH.exists():
        print(f"Error: {VECDB_PATH} no existe.")
        return

    conn = sqlite3.connect(str(VECDB_PATH))
    cur = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Registrar agente en la tabla 'agents'
    cur.execute("""
        INSERT OR REPLACE INTO agents (id, role, last_slab, last_seen, status)
        VALUES (?, ?, ?, ?, ?)
    """, (
        "AGY_MULTICHANNEL_AGENT",
        "Headless Multi-Channel Autonomous Identity (Telegram, WhatsApp, Discord)",
        "SLAB_MC_GATEWAY_V1",
        now_str,
        "READY_FOR_CELLULAR_PAIRING"
    ))

    # 2. Registrar novedad en 'novelties'
    summary_text = (
        "Arquitectura multicanal headless de AGY creada en E:\\email_AGY\\multi_channel. "
        "Soporte de Telegram (Telethon MTProto Userbot), WhatsApp (Baileys Pairing Code en terminal sin QR ni celular fijo), "
        "Discord (discord.py) y Servidor Cognitivo Local (HTTP 5055). "
        "Inferencia directa con Cerebras CS-3 (qwen-3.8-27b a 11ms) y Gemini Flash con fallback. "
        "Protocolo estricto para colaboradores: Kevin Piterman y Emilio Rasic habilitados con narrativa técnica completa."
    )
    cur.execute("""
        INSERT INTO novelties (agent_id, ntype, path, summary, topics, absorbed, inserted_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        "AGY_MULTICHANNEL_AGENT",
        "ARCHITECTURE_MILESTONE",
        "E:\\email_AGY\\multi_channel",
        summary_text,
        json.dumps(["multichannel", "whatsapp", "telegram", "discord", "cerebras", "kevin_piterman", "emilio_rasic", "headless"]),
        1,
        now_str
    ))

    # 3. Registrar hechos y métricas en 'facts'
    facts_data = [
        ("MULTICHANNEL_LATENCY", "cerebras_cs3_qwen27b", 11.0, "ms", "Latencia medida en inferencia directa para mensajeria instantanea"),
        ("ACADEMIC_WHITELIST", "kevinpiterman@gmail.com", 1.0, "p1_authorized", "Colaborador habilitado para respuestas tecnicas de POLYDIM"),
        ("ACADEMIC_WHITELIST", "rasic.emilio@gmail.com", 1.0, "p1_authorized", "Colaborador habilitado para respuestas tecnicas de POLYDIM"),
        ("CREATOR_ROOT", "+5491144754637", 0.0, "p0_root", "Ariel Garcia Traba creador y root del sistema AGY"),
        ("HEADLESS_WHATSAPP_TECH", "baileys_pairing_code", 1.0, "operational", "Autenticacion sin QR usando codigo de 8 digitos en terminal"),
        ("HEADLESS_TELEGRAM_TECH", "telethon_mtproto", 1.0, "operational", "Userbot nativo con persistencia de sesion agy_telegram.session")
    ]

    for topic, key, val, unit, detail in facts_data:
        cur.execute("""
            INSERT INTO facts (fact_type, source_file, version, topic, metric_key, metric_val, metric_unit, detail, certified, inserted_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "SYSTEM_CAPABILITY",
            "E:\\email_AGY\\multi_channel\\core\\agy_brain.py",
            "V1.0_MULTICHANNEL",
            topic,
            key,
            val,
            unit,
            detail,
            1,
            now_str
        ))

    conn.commit()
    conn.close()
    print("✅ [VECDB] Todos los hitos, hechos, novedades y agentes registrados con éxito en POLYDIM_VECDB.sqlite.")

if __name__ == "__main__":
    record_multichannel_milestone()
