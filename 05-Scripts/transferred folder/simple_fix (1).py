import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive']

# Load credentials
creds = Credentials.from_authorized_user_file('token.json', SCOPES)
service = build('drive', 'v3', credentials=creds)

# Find Trajanus USA folder
results = service.files().list(
    q="name='00 - Trajanus USA' and mimeType='application/vnd.google-apps.folder' and trashed=false",
    fields='files(id)'
).execute()
trajanus_id = results['files'][0]['id']

# List what's currently there
print("\nCurrent folders in Trajanus USA:")
results = service.files().list(
    q=f"'{trajanus_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
    fields='files(name)',
    pageSize=100
).execute()
for f in sorted(results['files'], key=lambda x: x['name']):
    print(f"  {f['name']}")

# Create numbered folders
print("\nCreating folders:")
folders = ["00-Command-Center", "01-Core-Protocols", "02-Templates", "03-Living-Documents", 
           "04-Scripts", "05-Archives", "06-Project-State", "07-Session-Journal", 
           "08-EOS-Files", "09-Active-Projects", "10-PM-Toolbox", "11-Personal", "12-Credentials"]

for name in folders:
    try:
        folder = service.files().create(
            body={'name': name, 'mimeType': 'application/vnd.google-apps.folder', 'parents': [trajanus_id]},
            fields='id'
        ).execute()
        print(f"  CREATED: {name}")
    except Exception as e:
        if 'already exists' in str(e).lower():
            print(f"  EXISTS: {name}")
        else:
            print(f"  ERROR: {name} - {e}")

print("\nDone. Check Google Drive.")
