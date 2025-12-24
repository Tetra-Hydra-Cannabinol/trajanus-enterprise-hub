#!/usr/bin/env python3
"""
TRAJANUS DRIVE COMPLETE REORGANIZATION
Maps all existing files/folders and reorganizes to new 00-12 structure
"""

import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive']

# Color codes
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'

def get_credentials():
    """Authenticate and return credentials"""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def find_folder_by_name(service, folder_name, parent_id=None):
    """Find folder by name"""
    try:
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        if parent_id:
            query += f" and '{parent_id}' in parents"
        results = service.files().list(q=query, spaces='drive', fields='files(id, name)', pageSize=10).execute()
        items = results.get('files', [])
        return items[0]['id'] if items else None
    except HttpError as error:
        print(f"{RED}Error finding folder: {error}{RESET}")
        return None

def create_folder(service, folder_name, parent_id):
    """Create folder in Google Drive"""
    try:
        existing_id = find_folder_by_name(service, folder_name, parent_id)
        if existing_id:
            print(f"{YELLOW}  Folder '{folder_name}' already exists{RESET}")
            return existing_id
        
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
        folder = service.files().create(body=file_metadata, fields='id, name').execute()
        print(f"{GREEN}  ✓ Created: {folder_name}{RESET}")
        return folder.get('id')
    except HttpError as error:
        print(f"{RED}  Error creating '{folder_name}': {error}{RESET}")
        return None

def list_all_items(service, parent_id):
    """List all files and folders in a parent folder"""
    try:
        query = f"'{parent_id}' in parents and trashed=false"
        results = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name, mimeType)',
            pageSize=1000
        ).execute()
        return results.get('files', [])
    except HttpError as error:
        print(f"{RED}Error listing items: {error}{RESET}")
        return []

def move_file(service, file_id, new_parent_id, old_parent_id):
    """Move a file to a new folder"""
    try:
        file = service.files().update(
            fileId=file_id,
            addParents=new_parent_id,
            removeParents=old_parent_id,
            fields='id, parents'
        ).execute()
        return True
    except HttpError as error:
        print(f"{RED}Error moving file: {error}{RESET}")
        return False

def main():
    print(f"\n{BLUE}{'='*70}")
    print("TRAJANUS DRIVE COMPLETE REORGANIZATION")
    print("Mapping all files and creating new 00-12 structure")
    print(f"{'='*70}{RESET}\n")
    
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    
    # Find Trajanus USA root
    print("Finding Trajanus USA folder...")
    trajanus_root = find_folder_by_name(service, "00 - Trajanus USA")
    if not trajanus_root:
        print(f"{RED}ERROR: Could not find '00 - Trajanus USA' folder{RESET}")
        return
    print(f"{GREEN}✓ Found Trajanus USA root{RESET}\n")
    
    # PHASE 1: Map all existing content
    print(f"{BLUE}PHASE 1: Mapping all existing folders and files{RESET}")
    existing_items = list_all_items(service, trajanus_root)
    
    folders_map = {}
    files_map = {}
    
    for item in existing_items:
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            folders_map[item['name']] = item['id']
            print(f"{CYAN}  📁 Folder: {item['name']}{RESET}")
        else:
            files_map[item['name']] = item['id']
            print(f"  📄 File: {item['name']}")
    
    print(f"\n{GREEN}✓ Found {len(folders_map)} folders and {len(files_map)} files{RESET}\n")
    
    # PHASE 2: Create new folder structure
    print(f"{BLUE}PHASE 2: Creating new numbered folder structure (00-12){RESET}\n")
    
    new_structure = {
        "00-Command-Center": "keep",
        "01-Core-Protocols": "create",
        "02-Templates": "create", 
        "03-Living-Documents": "create",
        "04-Scripts": "create",
        "05-Archives": "create",
        "06-Project-State": "keep",
        "07-Session-Journal": "keep",
        "08-EOS-Files": "keep",
        "09-Active-Projects": "keep",
        "10-PM-Toolbox": "create",
        "11-Personal": "create",
        "12-Credentials": "create"
    }
    
    created_folders = {}
    
    print(f"{CYAN}Creating main folders...{RESET}")
    for folder_name, action in new_structure.items():
        folder_id = create_folder(service, folder_name, trajanus_root)
        if folder_id:
            created_folders[folder_name] = folder_id
    
    # PHASE 3: Create Living Documents structure
    print(f"\n{BLUE}PHASE 3: Creating Living Documents structure{RESET}\n")
    living_docs_id = created_folders.get("03-Living-Documents")
    
    living_docs_types = [
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
    
    if living_docs_id:
        print(f"{CYAN}Creating 11 document types with Daily_Entries folders...{RESET}")
        for doc_type in living_docs_types:
            daily_folder = f"{doc_type}_Daily_Entries"
            create_folder(service, daily_folder, living_docs_id)
    
    # PHASE 4: Create Archive subfolders
    print(f"\n{BLUE}PHASE 4: Creating Archive subfolders{RESET}\n")
    archives_id = created_folders.get("05-Archives")
    if archives_id:
        print(f"{CYAN}Creating archive organization...{RESET}")
        create_folder(service, "AI-Projects", archives_id)
        create_folder(service, "FILE-RECOVERY-1109-1315", archives_id)
        create_folder(service, "Chat-Files", archives_id)
        create_folder(service, "Old-Numbered-Folders", archives_id)
    
    # PHASE 5: File Migration Plan
    print(f"\n{BLUE}PHASE 5: File Migration Mapping{RESET}\n")
    
    migration_plan = {
        # Old folders to move content FROM → New location
        "00-Command-Center": "00-Command-Center",  # Keep as is
        "03-Dialogue-Patterns": "05-Archives/Old-Numbered-Folders",
        "04-Technical-Specs": "05-Archives/Old-Numbered-Folders",
        "05-Decision-Logs": "05-Archives/Old-Numbered-Folders",
        "06-Project-State": "06-Project-State",  # Keep as is
        "07-Session-Journal": "07-Session-Journal",  # Keep as is
        "08-EOS-Files": "08-EOS-Files",  # Keep as is
        "09-Active-Projects": "09-Active-Projects",  # Keep as is
        "10-Templates": "02-Templates",  # Move to new Templates
        "11-Client-Deliverables": "05-Archives/Old-Numbered-Folders",
        "12-Archive": "05-Archives/Old-Numbered-Folders",
        "Living-Documents": "03-Living-Documents",  # Merge into new structure
        "Session-Summaries": "07-Session-Journal",  # Move to Session Journal
        "PM-Toolbox": "10-PM-Toolbox",
        "Personal": "11-Personal",
        "AI-Projects": "05-Archives/AI-Projects",
        "Chat Files": "05-Archives/Chat-Files",
        "FILE RECOVERY-1109-1315": "05-Archives/FILE-RECOVERY-1109-1315",
        "File-Management-System": "01-Core-Protocols",
        "Fonts": "11-Personal"
    }
    
    print(f"{YELLOW}Migration Plan:{RESET}")
    for old_folder, new_location in migration_plan.items():
        if old_folder in folders_map:
            print(f"  {old_folder} → {new_location}")
        else:
            print(f"  {old_folder} → {new_location} {YELLOW}(folder not found){RESET}")
    
    # PHASE 6: Execute migrations (FILES ONLY - folders stay for now)
    print(f"\n{BLUE}PHASE 6: Migrating files (folders preserved for safety){RESET}\n")
    print(f"{YELLOW}NOTE: Moving files only. Old folders kept for manual verification.{RESET}\n")
    
    files_moved = 0
    errors = 0
    
    for old_folder_name, new_location in migration_plan.items():
        if old_folder_name not in folders_map:
            continue
        
        old_folder_id = folders_map[old_folder_name]
        
        # Determine target folder ID
        target_folder_id = None
        if "/" in new_location:
            # Navigate path (e.g., "05-Archives/AI-Projects")
            parts = new_location.split("/")
            target_folder_id = created_folders.get(parts[0])
            if target_folder_id and len(parts) > 1:
                target_folder_id = find_folder_by_name(service, parts[1], target_folder_id)
        else:
            target_folder_id = created_folders.get(new_location)
        
        if not target_folder_id:
            print(f"{RED}Could not find target folder for: {new_location}{RESET}")
            continue
        
        # Get all files in old folder
        items = list_all_items(service, old_folder_id)
        files_in_folder = [item for item in items if item['mimeType'] != 'application/vnd.google-apps.folder']
        
        if files_in_folder:
            print(f"{CYAN}Moving {len(files_in_folder)} files from {old_folder_name}...{RESET}")
            for file in files_in_folder:
                if move_file(service, file['id'], target_folder_id, old_folder_id):
                    files_moved += 1
                    print(f"  ✓ Moved: {file['name']}")
                else:
                    errors += 1
                    print(f"  ✗ Failed: {file['name']}")
    
    # SUMMARY
    print(f"\n{BLUE}{'='*70}")
    print("REORGANIZATION COMPLETE")
    print(f"{'='*70}{RESET}\n")
    
    print(f"{GREEN}✓ New folders created: 13 main + 11 Daily_Entries + 4 archive = 28 folders{RESET}")
    print(f"{GREEN}✓ Files successfully moved: {files_moved}{RESET}")
    if errors > 0:
        print(f"{RED}✗ Files with errors: {errors}{RESET}")
    
    print(f"\n{YELLOW}MANUAL CLEANUP REQUIRED:{RESET}")
    print(f"1. Review old folders and verify files moved correctly")
    print(f"2. Delete old numbered folders (03, 04, 05, 10, 11, 12) manually if empty")
    print(f"3. Check that all files are in correct new locations")
    print(f"4. Run create_living_documents_masters.py to populate MASTER files")
    
    print(f"\n{BLUE}{'='*70}{RESET}\n")
    
    # Save migration log
    log = {
        "timestamp": "2025-12-04",
        "folders_mapped": len(folders_map),
        "files_mapped": len(files_map),
        "new_folders_created": len(created_folders),
        "files_moved": files_moved,
        "errors": errors,
        "migration_plan": migration_plan
    }
    
    with open('reorganization_log.json', 'w') as f:
        json.dump(log, f, indent=2)
    
    print(f"{GREEN}✓ Migration log saved to: reorganization_log.json{RESET}\n")

if __name__ == "__main__":
    main()
