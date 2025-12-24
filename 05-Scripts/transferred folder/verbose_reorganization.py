#!/usr/bin/env python3
"""
SUPER VERBOSE DIAGNOSTIC AND FIX SCRIPT
Shows exactly what's happening at every step
"""

import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive']

def get_credentials():
    """Load credentials from current directory"""
    print("\n[1] Loading credentials...")
    
    if not os.path.exists('token.json'):
        print("    ✗ token.json not found in current directory")
        print(f"    Current directory: {os.getcwd()}")
        return None
    
    if not os.path.exists('credentials.json'):
        print("    ✗ credentials.json not found in current directory")
        return None
    
    print("    ✓ Found token.json")
    print("    ✓ Found credentials.json")
    
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    print("    ✓ Credentials loaded successfully")
    return creds

def main():
    print("\n" + "="*70)
    print("TRAJANUS REORGANIZATION - SUPER VERBOSE MODE")
    print("="*70)
    
    # Step 1: Get credentials
    creds = get_credentials()
    if not creds:
        print("\nFAILED: Could not load credentials")
        print("Please make sure you're running this from the 00-Command-Center folder")
        return
    
    # Step 2: Build service
    print("\n[2] Building Drive API service...")
    try:
        service = build('drive', 'v3', credentials=creds)
        print("    ✓ Drive service created")
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return
    
    # Step 3: Find Trajanus folder
    print("\n[3] Finding '00 - Trajanus USA' folder...")
    try:
        query = "name='00 - Trajanus USA' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        print(f"    Query: {query}")
        
        results = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name, parents)',
            pageSize=10
        ).execute()
        
        items = results.get('files', [])
        print(f"    Found {len(items)} matching folders")
        
        if not items:
            print("    ✗ Trajanus folder not found!")
            return
        
        trajanus = items[0]
        trajanus_id = trajanus['id']
        print(f"    ✓ Found: {trajanus['name']}")
        print(f"    ✓ ID: {trajanus_id}")
        
    except HttpError as error:
        print(f"    ✗ API Error: {error}")
        return
    
    # Step 4: List existing folders
    print("\n[4] Listing all current folders in Trajanus USA...")
    try:
        query = f"'{trajanus_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)',
            pageSize=100
        ).execute()
        
        existing = results.get('files', [])
        print(f"    Found {len(existing)} existing folders:")
        for folder in sorted(existing, key=lambda x: x['name']):
            print(f"      📁 {folder['name']}")
        
        existing_names = {f['name']: f['id'] for f in existing}
        
    except HttpError as error:
        print(f"    ✗ API Error: {error}")
        return
    
    # Step 5: Create missing numbered folders
    print("\n[5] Creating numbered folders (00-12)...")
    
    needed_folders = [
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
    
    created_ids = {}
    
    for folder_name in needed_folders:
        print(f"\n    Processing: {folder_name}")
        
        if folder_name in existing_names:
            print(f"      ⚠ Already exists")
            created_ids[folder_name] = existing_names[folder_name]
            continue
        
        print(f"      → Creating new folder...")
        try:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [trajanus_id]
            }
            
            folder = service.files().create(
                body=file_metadata,
                fields='id, name'
            ).execute()
            
            created_ids[folder_name] = folder['id']
            print(f"      ✓ Created successfully")
            print(f"      ✓ ID: {folder['id']}")
            
        except HttpError as error:
            print(f"      ✗ Failed: {error}")
    
    # Step 6: Create Living Documents structure
    print("\n[6] Creating Living Documents structure...")
    
    ld_id = created_ids.get("03-Living-Documents")
    if not ld_id:
        print("    ✗ 03-Living-Documents folder not available")
    else:
        print(f"    Using folder ID: {ld_id}")
        
        # Check existing subfolders
        print("\n    Checking existing subfolders...")
        try:
            results = service.files().list(
                q=f"'{ld_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
                fields='files(id, name)',
                pageSize=50
            ).execute()
            
            existing_subs = {f['name'] for f in results.get('files', [])}
            print(f"    Found {len(existing_subs)} existing subfolders")
            
        except:
            existing_subs = set()
        
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
            print(f"\n    Processing: {folder_name}")
            
            if folder_name in existing_subs:
                print(f"      ⚠ Already exists")
                continue
            
            print(f"      → Creating...")
            try:
                file_metadata = {
                    'name': folder_name,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [ld_id]
                }
                
                folder = service.files().create(
                    body=file_metadata,
                    fields='id'
                ).execute()
                
                print(f"      ✓ Created successfully")
                
            except HttpError as error:
                print(f"      ✗ Failed: {error}")
    
    # Step 7: Create Archive structure
    print("\n[7] Creating Archive subfolders...")
    
    archive_id = created_ids.get("05-Archives")
    if not archive_id:
        print("    ✗ 05-Archives folder not available")
    else:
        print(f"    Using folder ID: {archive_id}")
        
        archive_folders = [
            "AI-Projects",
            "FILE-RECOVERY-1109-1315", 
            "Chat-Files",
            "Old-Numbered-Folders"
        ]
        
        for folder_name in archive_folders:
            print(f"\n    Processing: {folder_name}")
            print(f"      → Creating...")
            
            try:
                file_metadata = {
                    'name': folder_name,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [archive_id]
                }
                
                folder = service.files().create(
                    body=file_metadata,
                    fields='id'
                ).execute()
                
                print(f"      ✓ Created successfully")
                
            except HttpError as error:
                print(f"      ✗ Failed: {error}")
    
    # Summary
    print("\n" + "="*70)
    print("PROCESS COMPLETE")
    print("="*70)
    print(f"\n✓ Numbered folders (00-12): 13 processed")
    print(f"✓ Living Documents Daily_Entries: 11 processed")
    print(f"✓ Archive subfolders: 4 processed")
    print("\nRefresh Google Drive in your browser to see changes")
    print()

if __name__ == "__main__":
    main()
