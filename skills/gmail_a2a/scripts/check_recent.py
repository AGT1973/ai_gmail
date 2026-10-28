import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
accounts = ['account_a2a', 'account_sota']

for acc in accounts:
    tpath = os.path.join(r'E:\email_AGY\.secrets', acc, 'token.json')
    if os.path.exists(tpath):
        try:
            creds = Credentials.from_authorized_user_file(tpath, SCOPES)
            service = build('gmail', 'v1', credentials=creds)
            res = service.users().messages().list(userId='me', maxResults=5).execute()
            msgs = res.get('messages', [])
            print(f"\n==================== [{acc}] Últimos {len(msgs)} correos ====================")
            for m in msgs:
                msg_data = service.users().messages().get(userId='me', id=m['id'], format='metadata', metadataHeaders=['From', 'Subject', 'Date']).execute()
                headers = {h['name']: h['value'] for h in msg_data.get('payload', {}).get('headers', [])}
                labels = msg_data.get('labelIds', [])
                print(f"ID: {m['id']} | Leído: {'UNREAD' not in labels} | De: {headers.get('From', '')} | Asunto: {headers.get('Subject', '')} | Fecha: {headers.get('Date', '')}")
        except Exception as e:
            print(f"[{acc}] ERROR: {e}")
