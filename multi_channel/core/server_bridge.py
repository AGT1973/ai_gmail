"""
AGY Local Cognitive Server Bridge
=================================
Expone un endpoint HTTP local ultraliviano (puerto 5055) para que
cualquier pasarela externa (Node.js/Baileys WhatsApp, scripts, webhooks)
pueda consultar al cerebro de AGY de forma no-bloqueante.
"""

import sys
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.agy_brain import brain

HOST = "127.0.0.1"
PORT = 5055

class AGYRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/ask":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                payload = json.loads(body)
                sender_id = str(payload.get("sender_id", "unknown"))
                sender_name = payload.get("sender_name", sender_id)
                message = payload.get("message", "")
                channel = payload.get("channel", "http")

                # Consultar al cerebro de AGY
                reply = brain.ask(
                    sender_id=sender_id,
                    message_text=message,
                    sender_name=sender_name,
                    channel=channel
                )

                response_bytes = json.dumps({"status": "ok", "reply": reply}).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(response_bytes)))
                self.end_headers()
                self.wfile.write(response_bytes)
            except Exception as e:
                err_bytes = json.dumps({"status": "error", "error": str(e)}).encode("utf-8")
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(err_bytes)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Silenciar logs ruidosos HTTP
        pass

def run_server():
    server = HTTPServer((HOST, PORT), AGYRequestHandler)
    print(f"🧠 [AGY SERVER] Puente cognitivo activo en http://{HOST}:{PORT}/ask")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor cognitivo detenido.")
        server.server_close()

if __name__ == "__main__":
    run_server()
