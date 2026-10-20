"""
Script de purga y limpieza de basura (Urgente24, spam, promociones no deseadas)
utilizando batchModify para enviar directamente a la papelera.
"""
import os
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(line_buffering=True)
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
sys.path.insert(0, WORKSPACE_ROOT)

from skills.gmail_a2a.scripts.send_email import ALLOWED_RECIPIENTS

JUNK_SENDERS = [
    "urgente24.com",
    "news@urgente24.com"
]

def purge_junk_from_account(account_key="polydim_cla"):
    tpath = os.path.join(WORKSPACE_ROOT, ".secrets", account_key, "token.json")
    if not os.path.exists(tpath):
        return
    creds = Credentials.from_authorized_user_file(tpath, SCOPES)
    svc = build('gmail', 'v1', credentials=creds)

    print(f"[{account_key}] Buscando basura en bandeja de entrada...", flush=True)
    res = svc.users().messages().list(userId='me', q='from:urgente24.com OR from:news@urgente24.com', maxResults=500).execute()
    msgs = res.get('messages', [])
    if not msgs:
        print(f"[{account_key}] Bandeja limpia: 0 mensajes de basura.", flush=True)
        return

    ids = [m['id'] for m in msgs]
    svc.users().messages().batchModify(
        userId='me',
        body={'ids': ids, 'addLabelIds': ['TRASH'], 'removeLabelIds': ['INBOX', 'UNREAD']}
    ).execute()
    print(f"[{account_key}] ✅ {len(ids)} mensajes enviados a la papelera exitosamente.", flush=True)

if __name__ == "__main__":
    for acc in ["polydim_cla", "mpat_designer", "polydim_einsof"]:
        purge_junk_from_account(acc)
