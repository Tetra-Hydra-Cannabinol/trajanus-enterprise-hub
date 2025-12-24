#!/usr/bin/env python3
"""
TRAJANUS DRIVE CLEANUP AND MIGRATION
Removes duplicates, moves content, archives old folders
"""

import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive']

print("\n" + "="*70)
print("TRAJANUS DRIVE CLEANUP AND MIGRATION")
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
print(f"    ✓ Found")

# Get all folders
print("[3] Scanning all folders...")
results = service.files().list(
    q=f"'{trajanus_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
    fields='files(id, name)',
    pageSize=100
).execute()

folders = {f['name']: f['id'] for f in results['files']}
print(f"    ✓ Found {len(folders)} folders")

# Delete duplicates (the ones with " (1)" suffix)
print("\n[4] Deleting duplicate folders...")
duplicates = [
    "00-Command-Center (1)",
    "01-Core-Protocols (1)", 
    "06-Project-State (1)",
    "07-Session-Journal (1)",
    "08-EOS-Files (1)",
    "09-Active-Projects (1)"
]

for dup in duplicates:
    if dup in folders:
        try:
            service.files().delete(fileId=folders[dup]).execute()
            print(f"    ✓ Deleted: {dup}")
        except Exception as e:
            print(f"    ✗ Error deleting {dup}: {e}")
    else:
        print(f"    - Not found: {dup}")

# Move files from old folders to new folders
print("\n[5] Moving content to new folders...")

moves = [
    ("Living-Documents", "03-Living-Documents"),
    ("Session-Summaries", "07-Session-Journal"),
    ("PM-Toolbox", "10-PM-Toolbox"),
    ("Personal", "11-Personal")
]

for old_name, new_name in moves:
    if old_name in folders and new_name in folders:
        old_id = folders[old_name]
        new_id = folders[new_name]
        
        print(f"    Moving files from {old_name} to {new_name}...")
        
        # Get files in old folder
        try:
            files_result = service.files().list(
                q=f"'{old_id}' in parents and trashed=false",
                fields='files(id, name)',
                pageSize=100
            ).execute()
            
            files_to_move = files_result.get('files', [])
            
            if not files_to_move:
                print(f"      - Empty folder: {old_name}")
            else:
                for file in files_to_move:
                    try:
                        # Move file
                        service.files().update(
                            fileId=file['id'],
                            addParents=new_id,
                            removeParents=old_id,
                            fields='id, parents'
                        ).execute()
                        print(f"      ✓ Moved: {file['name']}")
                    except Exception as e:
                        print(f"      ✗ Error moving {file['name']}: {e}")
                        
        except Exception as e:
            print(f"      ✗ Error: {e}")
    else:
        print(f"    - Skipped: {old_name} or {new_name} not found")

# Create Archive subfolders if they don't exist
print("\n[6] Creating Archive subfolders...")

if "05-Archives" in folders:
    archive_id = folders["05-Archives"]
    
    # Check if subfolders exist
    results = service.files().list(
        q=f"'{archive_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
        fields='files(id, name)'
    ).execute()
    
    archive_subfolders = {f['name']: f['id'] for f in results['files']}
    
    # Create Old-Numbered-Folders if needed
    if "Old-Numbered-Folders" not in archive_subfolders:
        try:
            folder = service.files().create(
                body={
                    'name': 'Old-Numbered-Folders',
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [archive_id]
                },
                fields='id'
            ).execute()
            archive_subfolders["Old-Numbered-Folders"] = folder['id']
            print("    ✓ Created: Old-Numbered-Folders")
        except Exception as e:
            print(f"    ✗ Error: {e}")
    else:
        print("    - Exists: Old-Numbered-Folders")
    
    # Create Junk subfolder if needed
    if "Junk" not in archive_subfolders:
        try:
            folder = service.files().create(
                body={
                    'name': 'Junk',
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [archive_id]
                },
                fields='id'
            ).execute()
            archive_subfolders["Junk"] = folder['id']
            print("    ✓ Created: Junk")
        except Exception as e:
            print(f"    ✗ Error: {e}")
    else:
        print("    - Exists: Junk")

# Move old numbered folders to Archives
print("\n[7] Moving old numbered folders to Archives...")

old_numbered = [
    "02-Memory-System",
    "03-Dialogue-Patterns", 
    "04-Technical-Specs",
    "05-Decision-Logs"
]

if "05-Archives" in folders:
    archive_id = folders["05-Archives"]
    
    # Get Old-Numbered-Folders ID
    results = service.files().list(
        q=f"name='Old-Numbered-Folders' and '{archive_id}' in parents and trashed=false",
        fields='files(id)'
    ).execute()
    
    if results['files']:
        old_numbered_id = results['files'][0]['id']
        
        for old_folder in old_numbered:
            if old_folder in folders:
                try:
                    service.files().update(
                        fileId=folders[old_folder],
                        addParents=old_numbered_id,
                        removeParents=trajanus_id,
                        fields='id, parents'
                    ).execute()
                    print(f"    ✓ Moved: {old_folder}")
                except Exception as e:
                    print(f"    ✗ Error moving {old_folder}: {e}")
            else:
                print(f"    - Not found: {old_folder}")

# Move junk folders to Archives/Junk
print("\n[8] Moving junk folders to Archives/Junk...")

junk_folders = [
    "AI-Projects",
    "Chat Files",
    "FILE RECOVERY-1109-1315",
    "File-Management-System",
    "Fonts"
]

if "05-Archives" in folders:
    archive_id = folders["05-Archives"]
    
    # Get Junk folder ID
    results = service.files().list(
        q=f"name='Junk' and '{archive_id}' in parents and trashed=false",
        fields='files(id)'
    ).execute()
    
    if results['files']:
        junk_id = results['files'][0]['id']
        
        for junk_folder in junk_folders:
            if junk_folder in folders:
                try:
                    service.files().update(
                        fileId=folders[junk_folder],
                        addParents=junk_id,
                        removeParents=trajanus_id,
                        fields='id, parents'
                    ).execute()
                    print(f"    ✓ Moved: {junk_folder}")
                except Exception as e:
                    print(f"    ✗ Error moving {junk_folder}: {e}")
            else:
                print(f"    - Not found: {junk_folder}")

# Delete now-empty old folders
print("\n[9] Deleting empty old folders...")

old_folders_to_delete = [
    "Living-Documents",
    "Session-Summaries", 
    "PM-Toolbox",
    "Personal"
]

for old_folder in old_folders_to_delete:
    if old_folder in folders:
        # Check if empty
        try:
            results = service.files().list(
                q=f"'{folders[old_folder]}' in parents and trashed=false",
                fields='files(id)',
                pageSize=1
            ).execute()
            
            if not results.get('files'):
                # Empty - delete it
                service.files().delete(fileId=folders[old_folder]).execute()
                print(f"    ✓ Deleted: {old_folder}")
            else:
                print(f"    - Not empty (skipped): {old_folder}")
                
        except Exception as e:
            print(f"    ✗ Error: {e}")

print("\n" + "="*70)
print("CLEANUP COMPLETE")
print("="*70)
print("\n✓ Refresh Google Drive to see changes\n")
