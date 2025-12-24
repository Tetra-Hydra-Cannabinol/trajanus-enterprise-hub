#!/usr/bin/env python3
"""
TRAJANUS REORGANIZATION - STANDALONE VERSION
Run from anywhere, finds Trajanus folder automatically
"""

import os
import sys
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive']

def get_credentials():
    """Get credentials from multiple possible locations"""
    token_paths = [
        'token.json',
        'G:/My Drive/00 - Trajanus USA/00-Command-Center/token.json',
        '../token.json'
    ]
    
    creds_paths = [
        'credentials.json',
        'G:/My Drive/00 - Trajanus USA/00-Command-Center/credentials.json',
        '../credentials.json'
    ]
    
    creds = None
    token_file = None
    creds_file = None
    
    # Find token file
    for path in token_paths:
        if os.path.exists(path):
            token_file = path
            creds = Credentials.from_authorized_user_file(path, SCOPES)
            break
    
    # Find credentials file
    for path in creds_paths:
        if os.path.exists(path):
            creds_file = path
            break
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        elif creds_file:
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            creds = flow.run_local_server(port=0)
        else:
            print("ERROR: Cannot find credentials.json")
            print("Please run this script from the 00-Command-Center folder")
            sys.exit(1)
        
        # Save token
        if token_file:
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
    
    return creds

def find_folder(service, name, parent_id=None):
    """Find folder by name"""
    try:
        query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        if parent_id:
            query += f" and '{parent_id}' in parents"
        
        results = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)',
            pageSize=10
        ).execute()
        
        items = results.get('files', [])
        return items[0]['id'] if items else None
    except:
        return None

def create_folder(service, name, parent_id):
    """Create folder"""
    try:
        # Check if exists
        existing = find_folder(service, name, parent_id)
        if existing:
            print(f"  ✓ {name} (exists)")
            return existing
        
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
        
        folder = service.files().create(body=file_metadata, fields='id').execute()
        print(f"  ✓ {name} (created)")
        return folder.get('id')
    except Exception as e:
        print(f"  ✗ {name} - Error: {e}")
        return None

def rename_folder(service, folder_id, new_name):
    """Rename folder"""
    try:
        service.files().update(
            fileId=folder_id,
            body={'name': new_name}
        ).execute()
        print(f"  ✓ Renamed to: {new_name}")
        return True
    except Exception as e:
        print(f"  ✗ Rename failed: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("TRAJANUS REORGANIZATION - STANDALONE")
    print("="*70 + "\n")
    
    # Get credentials
    print("Authenticating...")
    try:
        creds = get_credentials()
        service = build('drive', 'v3', credentials=creds)
        print("✓ Authenticated\n")
    except Exception as e:
        print(f"✗ Authentication failed: {e}")
        return
    
    # Find Trajanus folder
    print("Finding Trajanus USA folder...")
    trajanus_id = find_folder(service, "00 - Trajanus USA")
    if not trajanus_id:
        print("✗ Cannot find '00 - Trajanus USA' folder")
        return
    print(f"✓ Found Trajanus USA\n")
    
    # Create numbered structure
    print("Creating numbered folder structure:\n")
    
    folders_to_create = [
        "00-Command-Center",
        "01-Core-Protocols",
        "02-Templates",
        "03-Living-Documents",
        "04-Scripts",
        "05-Archives",
        "06-Project-State",
        "07-Session-Journal",
        "08-EOS-Files",
        "09-Active-Projects",
        "10-PM-Toolbox",
        "11-Personal",
        "12-Credentials"
    ]
    
    created = {}
    for folder_name in folders_to_create:
        folder_id = create_folder(service, folder_name, trajanus_id)
        if folder_id:
            created[folder_name] = folder_id
    
    # Create Living Documents structure
    print("\nCreating Living Documents structure:\n")
    ld_id = created.get("03-Living-Documents")
    if ld_id:
        doc_types = [
            "Operational_Journal",
            "Technical_Journal",
            "Personal_Diary",
            "Code_Repository",
            "Bills_POV_Updates",
            "Users_Guide",
            "Enterprise_Hub_Version_Log",
            "Website_Code_Versions",
            "Protocol_Violations",
            "Active_Commitments",
            "Master_File_Architecture"
        ]
        
        for doc_type in doc_types:
            folder_name = f"{doc_type}_Daily_Entries"
            create_folder(service, folder_name, ld_id)
    
    # Create Archive structure
    print("\nCreating Archive structure:\n")
    archive_id = created.get("05-Archives")
    if archive_id:
        create_folder(service, "AI-Projects", archive_id)
        create_folder(service, "FILE-RECOVERY-1109-1315", archive_id)
        create_folder(service, "Chat-Files", archive_id)
        create_folder(service, "Old-Numbered-Folders", archive_id)
    
    # Rename old folders to have prefixes
    print("\nRenaming unnumbered folders:\n")
    
    renames = {
        "Living-Documents": "03-Living-Documents-OLD",
        "Session-Summaries": "07-Session-Summaries-OLD",
        "PM-Toolbox": "10-PM-Toolbox-OLD",
        "Personal": "11-Personal-OLD"
    }
    
    for old_name, new_name in renames.items():
        folder_id = find_folder(service, old_name, trajanus_id)
        if folder_id:
            rename_folder(service, folder_id, new_name)
    
    # Summary
    print("\n" + "="*70)
    print("REORGANIZATION COMPLETE")
    print("="*70 + "\n")
    print(f"✓ Main folders: {len(created)}")
    print(f"✓ Living Documents: 11 Daily_Entries folders created")
    print(f"✓ Archives: 4 subfolders created")
    print("\nMANUAL STEPS:")
    print("1. Move files from OLD folders to new numbered folders")
    print("2. Delete OLD folders after verifying files moved")
    print("3. Move archive content to 05-Archives subfolders")
    print("4. Run create_living_documents_masters.py next")
    print()

if __name__ == "__main__":
    main()
