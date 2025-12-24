#!/usr/bin/env python3
"""
TRAJANUS DRIVE REORGANIZATION SCRIPT
Creates complete numbered folder structure with Living Documents system
"""

import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pickle

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/drive']

# Color codes for terminal output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

def get_credentials():
    """Authenticate and return credentials"""
    creds = None
    
    # Token file stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

def find_folder_by_name(service, folder_name, parent_id=None):
    """Find a folder by name, optionally within a parent folder"""
    try:
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
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
    except HttpError as error:
        print(f"{RED}Error finding folder: {error}{RESET}")
        return None

def create_folder(service, folder_name, parent_id):
    """Create a folder in Google Drive"""
    try:
        # Check if folder already exists
        existing_id = find_folder_by_name(service, folder_name, parent_id)
        if existing_id:
            print(f"{YELLOW}Folder '{folder_name}' already exists{RESET}")
            return existing_id
        
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
        
        folder = service.files().create(
            body=file_metadata,
            fields='id, name'
        ).execute()
        
        print(f"{GREEN}✓ Created folder: {folder_name}{RESET}")
        return folder.get('id')
    
    except HttpError as error:
        print(f"{RED}Error creating folder '{folder_name}': {error}{RESET}")
        return None

def rename_folder(service, folder_id, new_name):
    """Rename an existing folder"""
    try:
        file_metadata = {'name': new_name}
        service.files().update(
            fileId=folder_id,
            body=file_metadata
        ).execute()
        print(f"{GREEN}✓ Renamed folder to: {new_name}{RESET}")
        return True
    except HttpError as error:
        print(f"{RED}Error renaming folder: {error}{RESET}")
        return False

def create_markdown_file(service, filename, content, parent_id):
    """Create a markdown file in Google Drive"""
    try:
        # Check if file already exists
        query = f"name='{filename}' and '{parent_id}' in parents and trashed=false"
        results = service.files().list(q=query, fields='files(id, name)').execute()
        items = results.get('files', [])
        
        if items:
            print(f"{YELLOW}File '{filename}' already exists{RESET}")
            return items[0]['id']
        
        file_metadata = {
            'name': filename,
            'mimeType': 'text/markdown',
            'parents': [parent_id]
        }
        
        media = MediaFileUpload(
            filename,
            mimetype='text/markdown',
            resumable=True
        )
        
        # Create temporary file with content
        temp_file = f"temp_{filename}"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Upload file
        from googleapiclient.http import MediaFileUpload
        media = MediaFileUpload(temp_file, mimetype='text/markdown')
        
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        # Clean up temp file
        os.remove(temp_file)
        
        print(f"{GREEN}✓ Created file: {filename}{RESET}")
        return file.get('id')
        
    except Exception as error:
        print(f"{RED}Error creating file '{filename}': {error}{RESET}")
        return None

def main():
    """Main reorganization function"""
    print(f"\n{BLUE}{'='*60}")
    print("TRAJANUS DRIVE REORGANIZATION")
    print(f"{'='*60}{RESET}\n")
    
    # Authenticate
    print("Authenticating...")
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    
    # Find Trajanus USA root folder
    print("\nFinding Trajanus USA folder...")
    trajanus_root = find_folder_by_name(service, "00 - Trajanus USA")
    
    if not trajanus_root:
        print(f"{RED}ERROR: Could not find '00 - Trajanus USA' folder{RESET}")
        return
    
    print(f"{GREEN}✓ Found Trajanus USA root folder{RESET}\n")
    
    # Define the complete folder structure
    folder_structure = {
        "00-Command-Center": "exists",
        "01-Core-Protocols": "exists",
        "02-Templates": "exists",
        "03-Living-Documents": "new",
        "04-Scripts": "rename_from_05-Scripts",
        "05-Archives": "new",
        "06-Project-State": "exists",
        "07-Session-Journal": "exists",
        "08-EOS-Files": "exists",
        "09-Active-Projects": "exists",
        "10-PM-Toolbox": "rename_from_PM-Toolbox",
        "11-Personal": "rename_from_Personal",
        "12-Credentials": "rename_from_Credentials"
    }
    
    # Living Documents structure - 11 document types
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
    
    created_folders = {}
    
    # Step 1: Handle renames
    print(f"{BLUE}STEP 1: Renaming folders without prefixes{RESET}")
    renames = {
        "05-Scripts": "04-Scripts",
        "PM-Toolbox": "10-PM-Toolbox",
        "Personal": "11-Personal",
        "Credentials": "12-Credentials"
    }
    
    for old_name, new_name in renames.items():
        folder_id = find_folder_by_name(service, old_name, trajanus_root)
        if folder_id:
            rename_folder(service, folder_id, new_name)
            created_folders[new_name] = folder_id
        else:
            # If doesn't exist, will create with new name
            print(f"{YELLOW}Folder '{old_name}' not found - will create as '{new_name}'{RESET}")
    
    print()
    
    # Step 2: Create main numbered folders
    print(f"{BLUE}STEP 2: Creating main folder structure{RESET}")
    for folder_name, status in folder_structure.items():
        if folder_name not in created_folders:
            folder_id = create_folder(service, folder_name, trajanus_root)
            if folder_id:
                created_folders[folder_name] = folder_id
    
    print()
    
    # Step 3: Create 03-Living-Documents structure
    print(f"{BLUE}STEP 3: Creating Living Documents structure (11 types){RESET}")
    living_docs_id = created_folders.get("03-Living-Documents")
    
    if living_docs_id:
        for doc_type in living_docs_types:
            print(f"\n{YELLOW}Creating {doc_type} structure...{RESET}")
            
            # Create Daily_Entries subfolder
            daily_folder_name = f"{doc_type}_Daily_Entries"
            daily_folder_id = create_folder(service, daily_folder_name, living_docs_id)
            
            # Note: MASTER files will be created by the Living Documents update script
            # This just creates the folder structure
    
    print()
    
    # Step 4: Create 05-Archives structure
    print(f"{BLUE}STEP 4: Creating Archives structure{RESET}")
    archives_id = created_folders.get("05-Archives")
    
    if archives_id:
        archive_folders = ["AI-Projects", "FILE-RECOVERY-1109-1315", "Chat-Files"]
        for folder_name in archive_folders:
            create_folder(service, folder_name, archives_id)
    
    print()
    
    # Summary
    print(f"\n{BLUE}{'='*60}")
    print("REORGANIZATION COMPLETE")
    print(f"{'='*60}{RESET}\n")
    
    print(f"{GREEN}✓ Main folders: {len(created_folders)}{RESET}")
    print(f"{GREEN}✓ Living Documents types: {len(living_docs_types)}{RESET}")
    print(f"{GREEN}✓ Daily entry folders: {len(living_docs_types)}{RESET}")
    print(f"{GREEN}✓ Archive folders: 3{RESET}")
    
    print(f"\n{YELLOW}NEXT STEPS:{RESET}")
    print("1. Manually move files from old folders to renamed folders if needed")
    print("2. Run Living Documents population script to create MASTER files")
    print("3. Begin daily entry creation process")
    
    print(f"\n{BLUE}{'='*60}{RESET}\n")

if __name__ == "__main__":
    main()
