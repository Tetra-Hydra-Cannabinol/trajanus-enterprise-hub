#!/usr/bin/env python3
"""
SMART DUPLICATE CLEANUP
Only deletes files from Living-Documents that already exist in 03-Living-Documents
"""

import os
import re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive']

print("\n" + "="*70)
print("SMART DUPLICATE CLEANUP")
print("="*70 + "\n")

# Load credentials
print("[1] Loading credentials...")
creds = Credentials.from_authorized_user_file('token.json', SCOPES)
service = build('drive', 'v3', credentials=creds)
print("    ✓ Ready")

# Find both folders
print("[2] Finding folders...")
results = service.files().list(
    q="(name='Living-Documents' or name='03-Living-Documents') and trashed=false",
    fields='files(id, name)'
).execute()

folders = {f['name']: f['id'] for f in results['files']}

if 'Living-Documents' not in folders:
    print("    ✗ Living-Documents not found")
    exit()
if '03-Living-Documents' not in folders:
    print("    ✗ 03-Living-Documents not found")
    exit()

old_id = folders['Living-Documents']
new_id = folders['03-Living-Documents']
print("    ✓ Found both folders")

# Get files from Living-Documents
print("\n[3] Getting files from Living-Documents...")
results = service.files().list(
    q=f"'{old_id}' in parents and trashed=false",
    fields='files(id, name)',
    pageSize=200
).execute()
old_files = results.get('files', [])
print(f"    Found {len(old_files)} files")

# Get files from 03-Living-Documents
print("[4] Getting files from 03-Living-Documents...")
results = service.files().list(
    q=f"'{new_id}' in parents and trashed=false",
    fields='files(id, name)',
    pageSize=200
).execute()
new_files = results.get('files', [])
print(f"    Found {len(new_files)} files")

# Build set of base names in 03-Living-Documents
# Strip " (1)", " (2)" etc to get base names
def get_base_name(name):
    """Remove (1), (2), (3) suffixes to get base name"""
    return re.sub(r' \(\d+\)$', '', name)

new_base_names = {get_base_name(f['name']) for f in new_files}

print(f"\n[5] Comparing files...")
print(f"    Unique base names in 03-Living-Documents: {len(new_base_names)}")

# Separate files into duplicates (already in new folder) and unique (not in new folder)
duplicates = []
unique = []

for f in old_files:
    base_name = get_base_name(f['name'])
    if base_name in new_base_names:
        duplicates.append(f)
    else:
        unique.append(f)

print(f"    Duplicates to delete: {len(duplicates)}")
print(f"    Unique files to move: {len(unique)}")

# Delete duplicates
print("\n[6] Deleting duplicates from Living-Documents...")
deleted = 0
for dup in duplicates:
    try:
        service.files().delete(fileId=dup['id']).execute()
        print(f"    ✓ Deleted: {dup['name']}")
        deleted += 1
    except Exception as e:
        print(f"    ✗ Error deleting {dup['name']}: {e}")

# Move unique files
print(f"\n[7] Moving {len(unique)} unique files to 03-Living-Documents...")
moved = 0
for f in unique:
    try:
        service.files().update(
            fileId=f['id'],
            addParents=new_id,
            removeParents=old_id,
            fields='id, parents'
        ).execute()
        print(f"    ✓ Moved: {f['name']}")
        moved += 1
    except Exception as e:
        print(f"    ✗ Error moving {f['name']}: {e}")

# Delete Living-Documents if empty
print("\n[8] Checking if Living-Documents is empty...")
results = service.files().list(
    q=f"'{old_id}' in parents and trashed=false",
    fields='files(id)',
    pageSize=1
).execute()

if not results.get('files'):
    try:
        service.files().delete(fileId=old_id).execute()
        print("    ✓ Deleted empty Living-Documents folder")
    except Exception as e:
        print(f"    ✗ Error: {e}")
else:
    print(f"    - Still has files, not deleting")

print("\n" + "="*70)
print("CLEANUP COMPLETE")
print("="*70)
print(f"\nDuplicates deleted: {deleted}")
print(f"Unique files moved: {moved}")
print("\n✓ Refresh Google Drive\n")
