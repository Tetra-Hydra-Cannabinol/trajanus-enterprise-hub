"""
Create folder structure in Google Drive
"""
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Authenticate
creds = Credentials.from_authorized_user_file('token.json')
drive_service = build('drive', 'v3', credentials=creds)

# Find Trajanus USA folder
query = "name = '00 - Trajanus USA' and mimeType = 'application/vnd.google-apps.folder'"
results = drive_service.files().list(q=query, fields="files(id, name)").execute()
trajanus_folder = results.get('files', [])[0]
trajanus_id = trajanus_folder['id']

print(f"Found Trajanus folder: {trajanus_id}")

# Create Session-Summaries folder
session_metadata = {
    'name': 'Session-Summaries',
    'mimeType': 'application/vnd.google-apps.folder',
    'parents': [trajanus_id]
}
session_folder = drive_service.files().create(body=session_metadata, fields='id, name').execute()
print(f"[OK] Created: Session-Summaries (ID: {session_folder['id']})")

# Create Living-Documents folder
living_metadata = {
    'name': 'Living-Documents',
    'mimeType': 'application/vnd.google-apps.folder',
    'parents': [trajanus_id]
}
living_folder = drive_service.files().create(body=living_metadata, fields='id, name').execute()
print(f"[OK] Created: Living-Documents (ID: {living_folder['id']})")

# Save folder IDs to config file
with open('folder_ids.txt', 'w') as f:
    f.write(f"SESSION_SUMMARIES={session_folder['id']}\n")
    f.write(f"LIVING_DOCUMENTS={living_folder['id']}\n")

print("\nFolder IDs saved to folder_ids.txt")
