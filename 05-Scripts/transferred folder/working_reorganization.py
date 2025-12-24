#!/usr/bin/env python3
"""
TRAJANUS DRIVE REORGANIZATION - WORKING VERSION
Uses correct credential paths: token.json in root, credentials.json in Credentials/
"""

import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive']

print("\n" + "="*70)
print("TRAJANUS FOLDER REORGANIZATION")
print("="*70 + "\n")

# Load credentials from correct locations
print("[1] Loading credentials...")
try:
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    print("    ✓ token.json loaded")
except Exception as e:
    print(f"    ✗ Failed to load token.json: {e}")
    exit(1)

# Build service
print("[2] Building Drive API service...")
try:
    service = build('drive', 'v3', credentials=creds)
    print("    ✓ Service ready")
except Exception as e:
    print(f"    ✗ Failed: {e}")
    exit(1)

# Find Trajanus USA folder
print("[3] Finding '00 - Trajanus USA' folder...")
try:
    results = service.files().list(
        q="name='00 - Trajanus USA' and mimeType='application/vnd.google-apps.folder' and trashed=false",
        fields='files(id, name)'
    ).execute()
    
    if not results['files']:
        print("    ✗ Folder not found")
        exit(1)
    
    trajanus_id = results['files'][0]['id']
    print(f"    ✓ Found: {results['files'][0]['name']}")
    print(f"    ID: {trajanus_id}")
except Exception as e:
    print(f"    ✗ Error: {e}")
    exit(1)

# List current folders
print("\n[4] Current folders in Trajanus USA:")
try:
    results = service.files().list(
        q=f"'{trajanus_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
        fields='files(name)',
        pageSize=100
    ).execute()
    
    for f in sorted(results['files'], key=lambda x: x['name']):
        print(f"    - {f['name']}")
except Exception as e:
    print(f"    ✗ Error: {e}")

# Create numbered folders
print("\n[5] Creating numbered folders (00-12)...")
folders = [
    "00-Command-Center", "01-Core-Protocols", "02-Templates",
    "03-Living-Documents", "04-Scripts", "05-Archives",
    "06-Project-State", "07-Session-Journal", "08-EOS-Files",
    "09-Active-Projects", "10-PM-Toolbox", "11-Personal", "12-Credentials"
]

created_count = 0
exists_count = 0
created_folders = {}

for name in folders:
    try:
        folder = service.files().create(
            body={
                'name': name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [trajanus_id]
            },
            fields='id'
        ).execute()
        created_folders[name] = folder['id']
        print(f"    ✓ CREATED: {name}")
        created_count += 1
    except Exception as e:
        if 'duplicate' in str(e).lower() or 'already exists' in str(e).lower():
            print(f"    - EXISTS: {name}")
            exists_count += 1
        else:
            print(f"    ✗ ERROR: {name} - {e}")

# Create Living Documents Daily_Entries folders
print("\n[6] Creating Living Documents Daily_Entries folders...")

# First, find the 03-Living-Documents folder
try:
    results = service.files().list(
        q=f"name='03-Living-Documents' and '{trajanus_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
        fields='files(id)'
    ).execute()
    
    if results['files']:
        ld_id = results['files'][0]['id']
        print(f"    Found 03-Living-Documents folder")
        
        doc_types = [
            "Operational_Journal", "Technical_Journal", "Personal_Diary",
            "Code_Repository", "Bills_POV_Updates", "Users_Guide",
            "Enterprise_Hub_Version_Log", "Website_Code_Versions",
            "Protocol_Violations", "Active_Commitments", "Master_File_Architecture"
        ]
        
        ld_created = 0
        ld_exists = 0
        
        for dtype in doc_types:
            folder_name = f"{dtype}_Daily_Entries"
            try:
                folder = service.files().create(
                    body={
                        'name': folder_name,
                        'mimeType': 'application/vnd.google-apps.folder',
                        'parents': [ld_id]
                    },
                    fields='id'
                ).execute()
                print(f"    ✓ Created: {folder_name}")
                ld_created += 1
            except Exception as e:
                if 'duplicate' in str(e).lower() or 'already exists' in str(e).lower():
                    print(f"    - Exists: {folder_name}")
                    ld_exists += 1
                else:
                    print(f"    ✗ Error: {folder_name} - {e}")
        
        print(f"\n    Living Documents: {ld_created} created, {ld_exists} already exist")
    else:
        print("    ! 03-Living-Documents not found - create numbered folders first")
        
except Exception as e:
    print(f"    ✗ Error: {e}")

# Summary
print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"Numbered folders: {created_count} created, {exists_count} already exist")
print("\n✓ DONE - Refresh Google Drive to see changes")
print("="*70 + "\n")
