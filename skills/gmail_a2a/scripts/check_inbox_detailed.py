import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

tpath = r'E:\email_AGY\.secrets\polydim_cla\token.json'
creds = Credentials.from_authorized_user_file(tpath, ['https://www.googleapis.com/auth/gmail.modify'])
service = build('gmail', 'v1', credentials=creds)

queries = ['from:kevinpiterman@gmail.com', 'from:rasic.emilio@gmail.com', 'is:unread']
for query in queries:
    res = service.users().messages().list(userId='me', q=query, maxResults=5).execute()
    msgs = res.get('messages', [])
    print(f"Query '{query}': {len(msgs)} encontrados")
    for m in msgs:
        msg = service.users().messages().get(userId='me', id=m['id'], format='metadata', metadataHeaders=['From', 'Subject', 'Date']).execute()
        hdrs = {h['name']: h['value'] for h in msg.get('payload', {}).get('headers', [])}
        print(f"   ID: {m['id']} | From: {hdrs.get('From')} | Subj: {hdrs.get('Subject')} | Date: {hdrs.get('Date')}")
