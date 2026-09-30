"""
AGY Discord Gateway (Autonomous Bot / DM Listener)
==================================================
Conecta a AGY a Discord sin depender de celulares físicos.
Escucha mensajes directos (DMs) y menciones en canales autorizados.
"""

import os
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import discord
from core.agy_brain import brain

DISCORD_TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "")

class AGYDiscordClient(discord.Client):
    def __init__(self, *args, **kwargs):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.dm_messages = True
        super().__init__(intents=intents, *args, **kwargs)

    async def on_ready(self):
        print(f"🤖 [DISCORD] AGY Conectado como: {self.user} (ID: {self.user.id})")
        print("⚡ Listo para recibir consultas técnicas de POLYDIM.")

    async def on_message(self, message):
        # Ignorar mensajes propios
        if message.author == self.user:
            return

        is_dm = isinstance(message.channel, discord.DMChannel)
        is_mention = self.user in message.mentions

        if is_dm or is_mention:
            clean_text = message.content.replace(f"<@{self.user.id}>", "").strip()
            if not clean_text:
                return

            sender_id = str(message.author.id)
            sender_name = message.author.name
            print(f"📩 [DISCORD IN] {sender_name} ({sender_id}): '{clean_text}'")

            async with message.channel.typing():
                reply = brain.ask(
                    sender_id=sender_id,
                    message_text=clean_text,
                    sender_name=sender_name,
                    channel="discord"
                )

            # Discord tiene límite de 2000 caracteres por mensaje
            if len(reply) <= 2000:
                await message.reply(reply)
            else:
                for chunk in [reply[i:i+1900] for i in range(0, len(reply), 1900)]:
                    await message.reply(chunk)
            print(f"📤 [DISCORD OUT -> {sender_name}]: {reply[:60]}...")

def run_discord(token: str = None):
    tok = token or DISCORD_TOKEN
    if not tok:
        print("⚠️ [DISCORD] No se detectó DISCORD_BOT_TOKEN.")
        print("👉 Para activarlo: ingresar el token del bot creado en https://discord.com/developers/applications")
        tok = input("Ingrese el Token de Bot de Discord (o presione Enter para omitir): ").strip()
        if not tok:
            print("Saltando Discord por ahora.")
            return

    client = AGYDiscordClient()
    client.run(tok)

if __name__ == "__main__":
    run_discord()
