"""
AGY Multi-Channel Bootstrap Wizard
==================================
Asistente interactivo en terminal para activar y gobernar los canales
de comunicación de AGY (Telegram, WhatsApp, Discord) de forma guiada
el día que Ariel tenga el celular con el chip.
"""

import os
import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
PYTHON_EXE = sys.executable

def banner():
    print("\n" + "="*65)
    print("🤖  ANTIGRAVITY (AGY) - ASISTENTE MULTICANAL HEADLESS")
    print("="*65)
    print("Este asistente te permite activar las identidades de AGY")
    print("usando el chip temporalmente en un celular para recibir")
    print("el código único. Luego podés retirar el chip y AGY seguirá")
    print("operando de forma autónoma desde esta PC 24/7.")
    print("="*65 + "\n")

def menu():
    print("Seleccione una opción:")
    print("  [1] Activar TELEGRAM (Ingresar número -> SMS único -> Sesión guardada)")
    print("  [2] Activar WHATSAPP (Generar Pairing Code de 8 dígitos para el celular)")
    print("  [3] Configurar DISCORD (Ingresar Token de Bot/Aplicación)")
    print("  [4] Probar el CEREBRO de AGY en consola (Inferencia directa)")
    print("  [5] INICIAR TODOS LOS CANALES ACTIVOS (Hub Multicanal 24/7)")
    print("  [0] Salir")
    print("-" * 65)

def activate_telegram():
    print("\n🔵 [TELEGRAM] Iniciando proceso de autenticación...")
    tg_script = ROOT_DIR / "gateways" / "telegram_service.py"
    subprocess.run([PYTHON_EXE, str(tg_script), "--auth"])

def activate_whatsapp():
    print("\n🟢 [WHATSAPP] Iniciando pasarela Baileys...")
    wpp_dir = ROOT_DIR / "gateways" / "whatsapp"
    node_script = wpp_dir / "whatsapp_node_bridge.js"
    subprocess.run(["node", str(node_script)], cwd=str(wpp_dir))

def configure_discord():
    print("\n🟣 [DISCORD] Configuración de bot...")
    dc_script = ROOT_DIR / "gateways" / "discord_service.py"
    subprocess.run([PYTHON_EXE, str(dc_script)])

def test_brain():
    print("\n🧠 [TEST CEREBRO] Verificando respuesta de AGY...")
    brain_script = ROOT_DIR / "core" / "agy_brain.py"
    subprocess.run([PYTHON_EXE, str(brain_script)])

def start_hub():
    print("\n🚀 [HUB MULTICANAL] Levantando todos los servicios en segundo plano...")
    hub_script = ROOT_DIR / "hub.py"
    subprocess.run([PYTHON_EXE, str(hub_script)])

def main():
    while True:
        banner()
        menu()
        choice = input("👉 Opción (0-5): ").strip()
        if choice == "1":
            activate_telegram()
        elif choice == "2":
            activate_whatsapp()
        elif choice == "3":
            configure_discord()
        elif choice == "4":
            test_brain()
        elif choice == "5":
            start_hub()
        elif choice == "0":
            print("\n👋 Saliendo del asistente. AGY en reposo.")
            break
        else:
            print("⚠️ Opción inválida. Intente de nuevo.")
        input("\nPresione ENTER para continuar...")

if __name__ == "__main__":
    main()
