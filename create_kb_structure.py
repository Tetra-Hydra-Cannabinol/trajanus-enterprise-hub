"""
Create 13-Knowledge-Base Folder Structure
Standalone version - no external dependencies
Author: Claude
Date: December 9, 2025
"""

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate():
    """Authenticate with Google Drive"""
    creds = None
    
    # Look for token.json in multiple locations
    token_paths = [
        'credentials/token.json',
        '../credentials/token.json',
        '../../credentials/token.json'
    ]
    
    credentials_paths = [
        'credentials/credentials.json',
        '../credentials/credentials.json', 
        '../../credentials/credentials.json'
    ]
    
    token_path = None
    credentials_path = None
    
    for path in token_paths:
        if os.path.exists(path):
            token_path = path
            break
    
    for path in credentials_paths:
        if os.path.exists(path):
            credentials_path = path
            break
    
    if token_path and os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not credentials_path:
                print("ERROR: Cannot find credentials.json")
                print("Looked in: credentials/, ../credentials/, ../../credentials/")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save token for next time
        if token_path:
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
    
    return build('drive', 'v3', credentials=creds)

def find_folder(service, folder_name, parent_id='root'):
    """Find a folder by name"""
    try:
        query = f"name='{folder_name}' and '{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])
        
        if items:
            return items[0]['id']
        return None
    except HttpError as error:
        print(f"Error finding folder: {error}")
        return None

def create_folder(service, folder_name, parent_id=None):
    """Create a folder in Google Drive"""
    try:
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        if parent_id:
            file_metadata['parents'] = [parent_id]
        
        folder = service.files().create(body=file_metadata, fields='id, name').execute()
        return folder.get('id')
    except HttpError as error:
        print(f"Error creating folder: {error}")
        return None

def main():
    """Create complete Knowledge Base structure"""
    
    print("\n" + "="*60)
    print("CREATING TRAJANUS KNOWLEDGE BASE FOLDER STRUCTURE")
    print("="*60 + "\n")
    
    # Authenticate
    print("Authenticating with Google Drive...")
    service = authenticate()
    if not service:
        print("❌ Authentication failed")
        return False
    print("✓ Authenticated\n")
    
    # Find Trajanus USA folder
    print("Finding '00 - Trajanus USA' folder...")
    trajanus_id = find_folder(service, '00 - Trajanus USA')
    if not trajanus_id:
        print("❌ ERROR: Could not find '00 - Trajanus USA' folder")
        return False
    print(f"✓ Found folder\n")
    
    # Create main KB folder
    print("Creating main folder...")
    kb_id = create_folder(service, '13-Knowledge-Base', trajanus_id)
    if not kb_id:
        print("❌ ERROR: Could not create 13-Knowledge-Base folder")
        return False
    print("✓ Created: 13-Knowledge-Base\n")
    
    # Define structure
    folders = {
        "01-Building-Codes": ["NFPA-70", "IBC-2021", "UFC"],
        "02-USACE-Standards": ["Engineer-Regulations", "Engineer-Pamphlets"],
        "03-Project-History": ["2024-Q4", "2025-Q1"],
        "04-Technical-Decisions": ["Architecture", "Rejected-Approaches", "Design-Patterns"],
        "05-Code-Repository": ["Working-Examples", "Failed-Attempts"],
        "06-Protocols-Preferences": [],
        "07-Training-Materials": [],
        "08-Software-Documentation": ["Procore", "Primavera-P6", "RMS-3.0"],
        "09-Product-Data": ["Electrical", "Structural", "Mechanical"]
    }
    
    # Create all folders
    print("Creating subfolders...")
    for parent_name, subfolders in folders.items():
        parent_id = create_folder(service, parent_name, kb_id)
        if parent_id:
            print(f"  ✓ {parent_name}")
            
            for subfolder_name in subfolders:
                subfolder_id = create_folder(service, subfolder_name, parent_id)
                if subfolder_id:
                    print(f"    ✓ {parent_name}/{subfolder_name}")
                else:
                    print(f"    ❌ Failed: {parent_name}/{subfolder_name}")
        else:
            print(f"  ❌ Failed: {parent_name}")
    
    print("\n" + "="*60)
    print("✅ FOLDER STRUCTURE CREATED SUCCESSFULLY!")
    print("="*60)
    print("\nLocation: G:\\My Drive\\00 - Trajanus USA\\13-Knowledge-Base\\")
    print("\nRefresh Google Drive in File Explorer (F5) to see folders.\n")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("✓ Done. Ready for Supabase setup.")
        else:
            print("❌ Failed. Check error messages above.")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
