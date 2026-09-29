import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
base_dir = r'E:\email_AGY\.secrets'
accounts = ['account_a2a', 'account_sota', 'account_cursos_ai', 'account_clone']

for acc in accounts:
    token_path = os.path.join(base_dir, acc, 'token.json')
    if not os.path.exists(token_path):
        print(f"=== [{acc}] SIN TOKEN ===")
        continue
    try:
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        service = build('gmail', 'v1', credentials=creds)
        profile = service.users().getProfile(userId='me').execute()
        email_address = profile.get('emailAddress', 'N/A')
        total_messages = profile.get('messagesTotal', 0)
        
        res = service.users().messages().list(userId='me', maxResults=6).execute()
        messages = res.get('messages', [])
        
        print("=" * 80)
        print(f"CUENTA: {acc} | EMAIL: {email_address} | TOTAL EN BUZON: {total_messages}")
        print("=" * 80)
        if not messages:
            print("  (Bandeja vacia)\n")
            continue
            
        for m in messages:
            msg_id = m['id']
            msg = service.users().messages().get(userId='me', id=msg_id, format='metadata', metadataHeaders=['From', 'Subject', 'Date']).execute()
            headers = {h['name']: h['value'] for h in msg.get('payload', {}).get('headers', [])}
            labels = msg.get('labelIds', [])
            date_str = headers.get('Date', 'N/A')
            from_str = headers.get('From', 'N/A')
            subject_str = headers.get('Subject', 'Sin Asunto')
            print(f"  * ID:      {msg_id}")
            print(f"    Fecha:   {date_str}")
            print(f"    De:      {from_str}")
            print(f"    Asunto:  {subject_str}")
            print(f"    Labels:  {labels}")
            print("  " + "-" * 70)
        print("\n")
    except Exception as e:
        print(f"Error en {acc}: {e}\n")
