import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
accounts = ['account_a2a', 'account_sota', 'account_cursos', 'account_cursos_ai', 'account_clone']

for acc in accounts:
    tpath = os.path.join(r'E:\email_AGY\.secrets', acc, 'token.json')
    if os.path.exists(tpath):
        try:
            creds = Credentials.from_authorized_user_file(tpath, SCOPES)
            service = build('gmail', 'v1', credentials=creds)
            # Fetch unread and total inbox
            unread_res = service.users().messages().list(userId='me', q='is:unread', maxResults=5).execute()
            inbox_res = service.users().messages().list(userId='me', maxResults=5).execute()
            
            unread_msgs = unread_res.get('messages', [])
            print(f"[{acc}] OK - Unread: {len(unread_msgs)}, Total Estimate: {inbox_res.get('resultSizeEstimate', 0)}")
            for m in unread_msgs:
                msg_data = service.users().messages().get(userId='me', id=m['id'], format='metadata', metadataHeaders=['From', 'Subject', 'Date']).execute()
                headers = {h['name']: h['value'] for h in msg_data.get('payload', {}).get('headers', [])}
                print(f"   -> ID: {m['id']} | De: {headers.get('From', '')} | Asunto: {headers.get('Subject', '')} | Fecha: {headers.get('Date', '')}")
        except Exception as e:
            print(f"[{acc}] ERROR: {e}")
    else:
        print(f"[{acc}] No existe token.json")
