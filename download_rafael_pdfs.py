import os
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

token_file = 'E:/email_AGY/.secrets/polydim_cla/token.json'
creds = Credentials.from_authorized_user_file(token_file, ['https://www.googleapis.com/auth/gmail.modify'])
service = build('gmail', 'v1', credentials=creds)

save_dir = 'E:/email_AGY/DOCUMENTACION/INFORMES_RAFAEL_KAGGLE'
os.makedirs(save_dir, exist_ok=True)

items = [
    ('1a1f8f3d49d29d0c', 'POLYDIM_EinsofOS_Informe_Rondas_v2_v3_v4_19Nov.pdf'),
    ('1a1f95713d9b55eb', 'POLYDIM_EinsofOS_Informe_Ronda_5_20Nov2026.pdf')
]

for mid, out_name in items:
    m = service.users().messages().get(userId='me', id=mid, format='full').execute()
    for p in m['payload'].get('parts', []):
        fn = p.get('filename')
        att_id = p.get('body', {}).get('attachmentId')
        if att_id:
            att = service.users().messages().attachments().get(userId='me', messageId=mid, id=att_id).execute()
            data = base64.urlsafe_b64decode(att['data'].encode('utf-8'))
            target_path = os.path.join(save_dir, out_name)
            with open(target_path, 'wb') as f:
                f.write(data)
            print(f"[OK] Descargado: {target_path} ({len(data)} bytes)")
