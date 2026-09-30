"""
AGY Telegram Gateway (Headless MTProto Userbot)
==============================================
Opera la cuenta personal de Telegram de AGY sin requerir un celular encendido.
1. Modo Interactivo: Autentica con el número y el código SMS único.
2. Modo Daemon: Escucha mensajes privados y menciones, delegando a AGYBrain.
"""

import os
import sys
import asyncio
from pathlib import Path

# Agregar raíz al sys.path
CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from telethon import TelegramClient, events
from core.agy_brain import brain

SESSION_DIR = ROOT_DIR / "sessions"
SESSION_DIR.mkdir(parents=True, exist_ok=True)
SESSION_FILE = SESSION_DIR / "agy_telegram"

# Telegram App API ID & Hash (Credenciales de aplicación estándar o personalizadas)
# Si el usuario tiene los propios, se cargan de variables de entorno o archivo de config
TELEGRAM_API_ID = int(os.environ.get("TG_API_ID", "2040"))
TELEGRAM_API_HASH = os.environ.get("TG_API_HASH", "b18441a1ff607e10a989891a5462e627")

def get_client() -> TelegramClient:
    return TelegramClient(str(SESSION_FILE), TELEGRAM_API_ID, TELEGRAM_API_HASH)

async def run_auth(phone_number: str = None):
    """Ejecuta el onboarding inicial para generar el archivo .session."""
    client = get_client()
    await client.connect()
    
    if await client.is_user_authorized():
        me = await client.get_me()
        print(f"✅ [TELEGRAM] Ya autenticado como: {me.first_name} (@{me.username}) - ID: {me.id}")
        await client.disconnect()
        return True

    print("\n" + "="*50)
    print("🚀 INICIANDO AUTENTICACION TELEGRAM HEADLESS")
    print("="*50)
    
    if not phone_number:
        phone_number = input("👉 Ingrese el número de teléfono con código de país (ej: +54911xxxxxxxx): ").strip()

    print(f"📡 Solicitando código de verificación a Telegram para {phone_number}...")
    sent_code = await client.send_code_request(phone_number)
    print("📲 Código SMS enviado al celular por Telegram.")
    
    code = input("👉 Ingrese el código de 5 dígitos recibido por SMS: ").strip()
    try:
        await client.sign_in(phone_number, code)
    except Exception as e:
        if "Two-step verification" in str(e) or "SessionPasswordNeededError" in type(e).__name__:
            pwd = input("👉 Telegram tiene clave de 2 pasos (2FA). Ingrese la contraseña: ").strip()
            await client.sign_in(password=pwd)
        else:
            print(f"❌ Error al iniciar sesión: {e}")
            await client.disconnect()
            return False

    me = await client.get_me()
    print(f"\n🎉 ¡ÉXITO TOTAL! Autenticado como {me.first_name} (ID: {me.id})")
    print(f"💾 Sesión persistida permanentemente en: {SESSION_FILE}.session")
    print("ℹ️ Ya podés retirar el chip del celular. Telegram funcionará desde la PC.")
    await client.disconnect()
    return True

async def run_listener():
    """Inicia el servicio en segundo plano que responde mensajes."""
    client = get_client()
    await client.start()
    me = await client.get_me()
    print(f"🤖 [TELEGRAM] AGY Activo y Escuchando como: {me.first_name} (@{me.username})")

    @client.on(events.NewMessage(incoming=True))
    async def handle_message(event):
        # Ignorar mensajes propios
        if event.is_private:
            sender = await event.get_sender()
            sender_id = str(sender.id)
            sender_name = getattr(sender, "first_name", "") or getattr(sender, "username", sender_id)
            text = event.raw_text.strip()
            if not text:
                return

            print(f"📩 [TG IN] {sender_name} ({sender_id}): '{text}'")
            # Mostrar que AGY está escribiendo
            async with client.action(event.chat_id, 'typing'):
                # Consultar al cerebro de AGY
                reply = brain.ask(sender_id=sender_id, message_text=text, sender_name=sender_name, channel="telegram")

            await event.reply(reply)
            print(f"📤 [TG OUT -> {sender_name}]: {reply[:60]}...")

    await client.run_until_disconnected()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--auth":
        asyncio.run(run_auth())
    else:
        asyncio.run(run_listener())
