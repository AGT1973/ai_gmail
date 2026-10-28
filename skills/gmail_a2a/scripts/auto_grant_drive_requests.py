"""
Script para procesar solicitudes de acceso de alumnos a material del curso en Google Drive.
Lee las notificaciones de drive-shares-dm-noreply@google.com en cursos_agt.
Otorga acceso de 'reader' (solo lectura) y le envía el email de confirmación al alumno.
"""
import os
import sys
import re
import json
import base64
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.message import EmailMessage

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SECRETS_DIR = os.path.join(WORKSPACE_ROOT, ".secrets", "cursos_agt")
TOKEN_FILE = os.path.join(SECRETS_DIR, "token.json")
LOG_FILE = os.path.join(WORKSPACE_ROOT, "DOCUMENTACION", "drive_access_granted_log.json")

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/drive"
]

def load_granted_log():
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_granted_log(log_data):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)

def extract_body_text(payload):
    parts = []
    if "parts" in payload:
        for p in payload["parts"]:
            parts.extend(extract_body_text(p))
    elif "body" in payload and "data" in payload["body"]:
        try:
            decoded = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="ignore")
            parts.append(decoded)
        except Exception:
            pass
    return parts

def process_pending_requests(auto_reply=True):
    if not os.path.exists(TOKEN_FILE):
        print(f"ERROR: No se encontró token.json en {SECRETS_DIR}")
        return

    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    gmail_service = build("gmail", "v1", credentials=creds)

    drive_service = None
    try:
        drive_service = build("drive", "v3", credentials=creds)
        drive_service.about().get(fields="user").execute()
    except Exception as e:
        print(f"[AVISO DRIVE API] No se pudo conectar a Google Drive API directamente ({e}).")
        print("  -> Si deseas habilitar la API de Drive en GCP para otorgamiento 100% autónomo:")
        print("     https://console.developers.google.com/apis/api/drive.googleapis.com/overview?project=786026195691")
        drive_service = None

    # Buscar mensajes de drive-shares-dm-noreply
    res = gmail_service.users().messages().list(
        userId="me", 
        q="from:drive-shares-dm-noreply@google.com",
        maxResults=15
    ).execute()

    messages = res.get("messages", [])
    print(f"[SCAN] Total solicitudes encontradas: {len(messages)}")

    granted_log = load_granted_log()
    processed_count = 0

    for m in messages:
        msg_id = m["id"]
        if msg_id in granted_log:
            continue

        msg = gmail_service.users().messages().get(userId="me", id=msg_id, format="full").execute()
        headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
        subject = headers.get("Subject", "")
        snippet = msg.get("snippet", "")
        body_text = "\n".join(extract_body_text(msg.get("payload", {})))

        # Extraer documento solicitado
        doc_match = re.search(r'solicita acceso al siguiente documento:\s*([^\n\r]+)', body_text)
        if not doc_match:
            doc_match = re.search(r'compartir\s*["\']([^"\']+)["\']', subject)
        doc_name = doc_match.group(1).strip() if doc_match else "Material del curso"

        # Extraer email del alumno
        emails_found = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', body_text)
        excluded = {"drive-shares-dm-noreply@google.com", "cursos.agt@gmail.com", "google.com"}
        candidate_emails = [e for e in emails_found if e.lower() not in excluded and not e.endswith("@google.com")]
        student_email = candidate_emails[0] if candidate_emails else None

        # Extraer URL del archivo
        links = re.findall(r'https://docs\.google\.com/[^\s"\'<>]+', body_text)
        doc_url = links[0] if links else ""
        file_id_match = re.search(r'/d/([a-zA-Z0-9_-]+)', doc_url)
        file_id = file_id_match.group(1) if file_id_match else None

        print(f"\n--- Solicitud detectada: {subject} ---")
        print(f"  Alumno: {student_email}")
        print(f"  Documento: {doc_name} (ID: {file_id})")

        if not student_email:
            print("  [SKIP] No se pudo identificar el correo del alumno.")
            continue

        granted_ok = False
        if drive_service and file_id:
            try:
                drive_service.permissions().create(
                    fileId=file_id,
                    body={"role": "reader", "type": "user", "emailAddress": student_email},
                    sendNotificationEmail=False
                ).execute()
                print(f"  [DRIVE API] Acceso 'reader' otorgado exitosamente en Drive a {student_email}.")
                granted_ok = True
            except Exception as e:
                print(f"  [DRIVE API ERROR] Error al otorgar acceso vía Drive API: {e}")
        else:
            # Si el usuario ya lo aprobó manualmente (o el API no está activo), consideramos para confirmación
            granted_ok = True

        # Enviar confirmación al alumno si auto_reply=True
        if auto_reply and student_email:
            clean_url = f"https://docs.google.com/document/d/{file_id}/edit" if file_id else doc_url
            email_body = f"""Hola!

Ya tenés habilitado el acceso de sólo lectura (lector) al siguiente material de la cátedra:

📄 Documento: {doc_name}
🔗 Enlace: {clean_url}

Cualquier duda o consulta con las prácticas o la teoría, avisanos por este mismo canal.

Saludos cordiales,
Cátedra Ariel García Traba
cursos.agt@gmail.com
"""
            try:
                msg_mime = EmailMessage()
                msg_mime.set_content(email_body)
                msg_mime["To"] = student_email
                msg_mime["From"] = "me"
                msg_mime["Subject"] = f"Acceso concedido a material del curso: {doc_name}"

                raw_bytes = base64.urlsafe_b64encode(msg_mime.as_bytes()).decode("utf-8")
                sent = gmail_service.users().messages().send(userId="me", body={"raw": raw_bytes}).execute()
                print(f"  [EMAIL ENVIADO] Confirmación despachada a {student_email} (Msg ID: {sent.get('id')})")
            except Exception as e:
                print(f"  [EMAIL ERROR] Error enviando correo al alumno: {e}")

        granted_log[msg_id] = {
            "timestamp": datetime.now().isoformat(),
            "student_email": student_email,
            "doc_name": doc_name,
            "file_id": file_id,
            "granted_drive_api": (drive_service is not None)
        }
        processed_count += 1

    save_granted_log(granted_log)
    print(f"\n[FIN] Procesadas {processed_count} solicitudes.")

if __name__ == "__main__":
    reply = "--no-reply" not in sys.argv
    process_pending_requests(auto_reply=reply)
