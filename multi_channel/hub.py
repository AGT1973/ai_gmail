"""
AGY Multi-Channel Orchestration Hub
==================================
Supervisa y ejecuta de forma concurrente los gateways de comunicación:
1. Servidor cognitivo local (Fast HTTP bridge en puerto 5055).
2. Telegram MTProto Userbot (si está autenticado).
3. WhatsApp Baileys Bridge (si está autenticado).
4. Discord Listener (si el token está presente).
"""

import os
import sys
import time
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
PYTHON_EXE = sys.executable

TG_SESSION = ROOT_DIR / "sessions" / "agy_telegram.session"
WPP_SESSION = ROOT_DIR / "sessions" / "whatsapp_auth" / "creds.json"
DISCORD_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

processes = []

def start_process(cmd, name, cwd=None):
    print(f"🚀 [HUB] Iniciando servicio: {name}...")
    p = subprocess.Popen(
        cmd,
        cwd=str(cwd or ROOT_DIR),
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    processes.append({"process": p, "name": name, "cmd": cmd, "cwd": cwd})
    return p

def main():
    print("="*65)
    print("🤖 INICIANDO AGY MULTI-CHANNEL HUB")
    print("="*65)

    # 1. Siempre iniciar el Servidor Cognitivo Local
    server_script = ROOT_DIR / "core" / "server_bridge.py"
    start_process([PYTHON_EXE, str(server_script)], "AGY Cognitive Server (HTTP 5055)")
    time.sleep(1)

    # 2. Iniciar Telegram si hay sesión
    if TG_SESSION.exists():
        tg_script = ROOT_DIR / "gateways" / "telegram_service.py"
        start_process([PYTHON_EXE, str(tg_script)], "Telegram MTProto Gateway")
    else:
        print("ℹ️ [HUB] Telegram no autenticado aún. (Ejecutar bootstrap_wizard.py para activar).")

    # 3. Iniciar WhatsApp si hay credenciales
    if WPP_SESSION.exists():
        wpp_dir = ROOT_DIR / "gateways" / "whatsapp"
        node_script = wpp_dir / "whatsapp_node_bridge.js"
        start_process(["node", str(node_script)], "WhatsApp Baileys Gateway", cwd=wpp_dir)
    else:
        print("ℹ️ [HUB] WhatsApp no autenticado aún. (Ejecutar bootstrap_wizard.py para activar).")

    # 4. Iniciar Discord si hay token
    if DISCORD_TOKEN:
        dc_script = ROOT_DIR / "gateways" / "discord_service.py"
        start_process([PYTHON_EXE, str(dc_script)], "Discord Bot Gateway")
    else:
        print("ℹ️ [HUB] Discord no configurado aún (DISCORD_BOT_TOKEN no definido).")

    print("\n⚡ [HUB] Todos los canales disponibles están activos.")
    print("Presione Ctrl+C para detener el Hub.")

    try:
        while True:
            time.sleep(5)
            # Chequear estado de los procesos
            for item in processes:
                poll = item["process"].poll()
                if poll is not None:
                    print(f"⚠️ [HUB] El servicio '{item['name']}' terminó con código {poll}. Reiniciando en 3s...")
                    time.sleep(3)
                    item["process"] = subprocess.Popen(
                        item["cmd"],
                        cwd=str(item["cwd"] or ROOT_DIR),
                        stdout=sys.stdout,
                        stderr=sys.stderr
                    )
    except KeyboardInterrupt:
        print("\n🛑 [HUB] Deteniendo todos los servicios...")
        for item in processes:
            item["process"].terminate()
        print("✅ [HUB] Todos los procesos finalizados limpiamente.")

if __name__ == "__main__":
    main()
