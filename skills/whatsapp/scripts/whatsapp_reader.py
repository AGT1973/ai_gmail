from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from utils.central_processor import procesar_con_ia

load_dotenv()
app = Flask(__name__)

VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "mi_token_secreto_123")
ACCESS_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_ID")

def enviar_mensaje(to, texto):
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": texto}
    }
    requests.post(url, headers=headers, json=data)

# 1. Verificación del webhook
@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Error de token", 403

# 2. Recepción de mensajes
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    try:
        entry = data['entry'][0]['changes'][0]['value']
        if 'messages' in entry:
            msg = entry['messages'][0]
            numero = msg['from']
            texto = msg['text']['body']
            # Forward to central IA processor
            procesar_con_ia("WhatsApp", numero, texto)
            # Opcional: respuesta automática
            enviar_mensaje(numero, f"Recibí: {texto[:50]}... Ya lo procesé.")
    except Exception as e:
        print(f"Error procesando webhook: {e}")
        print(data)
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
