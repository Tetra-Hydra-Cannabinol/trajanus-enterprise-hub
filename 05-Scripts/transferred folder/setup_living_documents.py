"""
Trajanus USA - Living Documents Setup
======================================

PURPOSE: One-time setup script that creates:
1. MASTER_DOCUMENTS folder in Google Drive
2. All 10 Living Document MASTER Google Docs
3. Returns all document IDs for use in update scripts

RUN ONCE: After running, copy the IDs into update_living_documents_v2.py

USAGE:
    python setup_living_documents.py

CREATED: 2025-11-24
VERSION: 1.0
"""

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime
import os

# Configuration
TOKEN_FILE = 'token.json'
BASE_FOLDER_ID = '10WRsfNnlckGCmBJAE-ThYpsvJWW0O7jC'  # 00-Command-Center folder

# The 10 Living Documents
LIVING_DOCUMENTS = [
    {
        'name': 'Technical_Journal',
        'existing_id': '1iPZAmi2bYBRmDnsgwZK3UZFCsB_YHj9RvRtKWJqDb2Q',  # Already exists with content
        'description': 'Professional work entries - what was built, how, why'
    },
    {
        'name': 'Personal_Diary',
        'existing_id': '1HKOisNN8A5rf9YdFJnJSdgH326bdJTun2rDqObNvrM8',  # Already exists with content
        'description': 'First-person reflections - how the work felt'
    },
    {
        'name': 'Session_Summary',
        'existing_id': '1ug6hyU9kE-n369M0lr1ZAElaphfpP3IfNL3duCtnXu0',  # Exists but empty
        'description': 'End-of-session handoff notes for continuity'
    },
    {
        'name': 'Testing_Errors_Log',
        'existing_id': None,  # Needs creation
        'description': 'What broke, how we fixed it, lessons learned'
    },
    {
        'name': 'Operational_Protocols',
        'existing_id': None,  # Needs creation
        'description': 'The rulebook - HOW Claude operates during sessions'
    },
    {
        'name': 'POV',
        'existing_id': None,  # Needs creation
        'description': 'WHO Bill is - personality, triggers, communication style'
    },
    {
        'name': 'Code_Repository',
        'existing_id': None,  # Needs creation
        'description': 'Manifest + versioned code archive for developer handoff'
    },
    {
        'name': 'Website_Development',
        'existing_id': None,  # Needs creation
        'description': 'Track website content, structure, and design decisions'
    },
    {
        'name': 'Decisions_Log',
        'existing_id': None,  # Needs creation
        'description': 'Major strategic choices with rationale'
    },
    {
        'name': 'Process_Documentation',
        'existing_id': None,  # Needs creation
        'description': 'Repeatable processes and automation docs'
    }
]

def get_services():
    """Initialize Google Drive and Docs services"""
    creds = Credentials.from_authorized_user_file(TOKEN_FILE)
    drive_service = build('drive', 'v3', credentials=creds)
    docs_service = build('docs', 'v1', credentials=creds)
    return drive_service, docs_service

def create_master_folder(drive_service):
    """Create MASTER_DOCUMENTS folder if it doesn't exist"""
    folder_name = "MASTER_DOCUMENTS"
    
    # Check if folder exists
    query = f"name='{folder_name}' and '{BASE_FOLDER_ID}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = drive_service.files().list(q=query, fields='files(id, name)').execute()
    folders = results.get('files', [])
    
    if folders:
        print(f"✓ Found existing folder: {folder_name}")
        return folders[0]['id']
    
    # Create folder
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [BASE_FOLDER_ID]
    }
    folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
    print(f"✓ Created folder: {folder_name}")
    return folder['id']

def create_master_doc(drive_service, docs_service, doc_config, folder_id):
    """Create a MASTER document with initial content"""
    
    # If document already exists, return existing ID
    if doc_config['existing_id']:
        print(f"  ✓ Using existing: {doc_config['name']}")
        return doc_config['existing_id']
    
    # Create new document
    month_year = datetime.now().strftime('%B_%Y')
    doc_name = f"{doc_config['name']}_{month_year}_MASTER"
    
    # Check if it already exists in the folder
    query = f"name='{doc_name}' and '{folder_id}' in parents and mimeType='application/vnd.google-apps.document' and trashed=false"
    results = drive_service.files().list(q=query, fields='files(id, name)').execute()
    existing = results.get('files', [])
    
    if existing:
        print(f"  ✓ Already exists: {doc_name}")
        return existing[0]['id']
    
    # Create the document
    doc_metadata = {
        'name': doc_name,
        'parents': [folder_id],
        'mimeType': 'application/vnd.google-apps.document'
    }
    doc = drive_service.files().create(body=doc_metadata, fields='id').execute()
    doc_id = doc['id']
    
    # Add initial content
    initial_content = f"""# {doc_config['name'].replace('_', ' ').upper()}
## Trajanus USA - MASTER Document

**Purpose:** {doc_config['description']}
**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Document ID:** {doc_id}

---

## ENTRIES

"""
    
    requests = [{
        'insertText': {
            'location': {'index': 1},
            'text': initial_content
        }
    }]
    docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
    
    print(f"  ✓ Created: {doc_name}")
    return doc_id

def main():
    """Main execution"""
    print("\n" + "="*80)
    print("TRAJANUS USA - LIVING DOCUMENTS SETUP")
    print("="*80 + "\n")
    
    # Get services
    print("[STEP 1] Connecting to Google Drive...")
    drive_service, docs_service = get_services()
    print("✓ Connected\n")
    
    # Create master folder
    print("[STEP 2] Creating MASTER_DOCUMENTS folder...")
    master_folder_id = create_master_folder(drive_service)
    print(f"  Folder ID: {master_folder_id}\n")
    
    # Create all master documents
    print("[STEP 3] Creating MASTER documents...")
    document_ids = {}
    
    for doc_config in LIVING_DOCUMENTS:
        doc_id = create_master_doc(drive_service, docs_service, doc_config, master_folder_id)
        document_ids[doc_config['name']] = doc_id
    
    # Summary
    print("\n" + "="*80)
    print("SETUP COMPLETE")
    print("="*80)
    
    print(f"\nMASTER_DOCUMENTS Folder ID: {master_folder_id}")
    print(f"Location: 00-Command-Center/MASTER_DOCUMENTS/")
    
    print("\n" + "-"*80)
    print("COPY THESE IDs INTO update_living_documents_v2.py:")
    print("-"*80 + "\n")
    
    print("MASTER_DOC_IDS = {")
    for name, doc_id in document_ids.items():
        print(f"    '{name}': '{doc_id}',")
    print("}")
    
    print("\n" + "-"*80)
    print("DOCUMENT URLS:")
    print("-"*80 + "\n")
    
    for name, doc_id in document_ids.items():
        print(f"{name}:")
        print(f"  https://docs.google.com/document/d/{doc_id}/edit\n")
    
    # Save IDs to file
    ids_file = 'MASTER_DOC_IDS.txt'
    with open(ids_file, 'w') as f:
        f.write("TRAJANUS USA - MASTER DOCUMENT IDs\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*60 + "\n\n")
        f.write("MASTER_DOC_IDS = {\n")
        for name, doc_id in document_ids.items():
            f.write(f"    '{name}': '{doc_id}',\n")
        f.write("}\n\n")
        f.write("="*60 + "\n")
        f.write("DOCUMENT URLS:\n")
        f.write("="*60 + "\n\n")
        for name, doc_id in document_ids.items():
            f.write(f"{name}:\n")
            f.write(f"  https://docs.google.com/document/d/{doc_id}/edit\n\n")
    
    print(f"\n✓ IDs saved to: {ids_file}")
    print("\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
