#!/usr/bin/env python3
"""
MOVE LIVING-DOCUMENTS FILES TO 03-LIVING-DOCUMENTS
Then delete the empty old folder
"""

import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive']

print("\n" + "="*70)
print("MOVING LIVING-DOCUMENTS FILES")
print("="*70 + "\n")

# Load credentials
print("[1] Loading credentials...")
creds = Credentials.from_authorized_user_file('token.json', SCOPES)
service = build('drive', 'v3', credentials=creds)
print("    ✓ Ready")

# Find Trajanus USA folder
print("[2] Finding Trajanus USA folder...")
results = service.files().list(
    q="name='00 - Trajanus USA' and mimeType='application/vnd.google-apps.folder' and trashed=false",
    fields='files(id)'
).execute()
trajanus_id = results['files'][0]['id']
print("    ✓ Found")

# Find both Living-Documents folders
print("[3] Finding Living-Documents folders...")
results = service.files().list(
    q=f"'{trajanus_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false and (name='Living-Documents' or name='03-Living-Documents')",
    fields='files(id, name)'
).execute()

folders = {f['name']: f['id'] for f in results['files']}

if 'Living-Documents' not in folders:
    print("    ✗ Living-Documents not found - may already be deleted")
    exit()

if '03-Living-Documents' not in folders:
    print("    ✗ 03-Living-Documents not found")
    exit()

old_id = folders['Living-Documents']
new_id = folders['03-Living-Documents']
print(f"    ✓ Found both folders")

# Get all files in old folder
print("\n[4] Getting files from Living-Documents...")
results = service.files().list(
    q=f"'{old_id}' in parents and trashed=false",
    fields='files(id, name, mimeType)',
    pageSize=100
).execute()

files_to_move = results.get('files', [])
print(f"    Found {len(files_to_move)} items to move")

# Move each file
print("\n[5] Moving files to 03-Living-Documents...")
moved_count = 0
error_count = 0

for file in files_to_move:
    try:
        service.files().update(
            fileId=file['id'],
            addParents=new_id,
            removeParents=old_id,
            fields='id, parents'
        ).execute()
        print(f"    ✓ Moved: {file['name']}")
        moved_count += 1
    except Exception as e:
        print(f"    ✗ Error moving {file['name']}: {e}")
        error_count += 1

# Delete the old folder if empty
print("\n[6] Checking if old folder is empty...")
results = service.files().list(
    q=f"'{old_id}' in parents and trashed=false",
    fields='files(id)',
    pageSize=1
).execute()

if not results.get('files'):
    print("    Folder is empty - deleting...")
    try:
        service.files().delete(fileId=old_id).execute()
        print("    ✓ Deleted: Living-Documents")
    except Exception as e:
        print(f"    ✗ Error deleting folder: {e}")
else:
    print("    - Folder not empty (skipped deletion)")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"Files moved: {moved_count}")
print(f"Errors: {error_count}")
print("\n✓ DONE - Refresh Google Drive\n")
