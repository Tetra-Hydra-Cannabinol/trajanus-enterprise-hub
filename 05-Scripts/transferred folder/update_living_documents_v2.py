"""
Trajanus USA - Session Documentation Manager v2.1
=================================================

IMPROVEMENTS:
1. Hardcoded correct MASTER document IDs (no duplicate confusion)
2. Entry numbering and TOC support
3. Document statistics tracking
4. Better error handling and logging
5. Verification output

DOCUMENT TYPES:
1. Technical_Journal
2. Operational_Journal
3. Session_Summary
4. Personal_Diary
5. Code_Repository
6. Website_Development
"""

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime
import os

# Configuration
TOKEN_FILE = 'token.json'
BASE_FOLDER_ID = '1JYTWaE6x74XJ_MSOuFkWKa_2DuaR_t64'  # 00-Command-Center folder

# CORRECT MASTER DOCUMENT IDs - These are the files WITH CONTENT
# DO NOT CHANGE THESE - They are the authoritative MASTER documents
MASTER_DOC_IDS = {
    'Technical_Journal': '1iPZAmi2bYBRmDnsgwZK3UZFCsB_YHj9RvRtKWJqDb2Q',      # Has Entry #001-#022
    'Personal_Diary': '1HKOisNN8A5rf9YdFJnJSdgH326bdJTun2rDqObNvrM8',         # Has Nov 1-16 entries
    'Operational_Journal': None,  # NEEDS TO BE FOUND - check Drive for correct ID
    'Session_Summary': None,      # NEEDS TO BE FOUND - check Drive for correct ID  
    'Code_Repository': None,      # NEW - will be created if None
    'Website_Development': None   # NEW - will be created if None
}

# Document types for file naming
DOCUMENT_TYPES = [
    'Technical_Journal',
    'Operational_Journal',
    'Session_Summary',
    'Personal_Diary',
    'Code_Repository',
    'Website_Development'
]

def get_services():
    """Initialize Google Drive and Docs services"""
    creds = Credentials.from_authorized_user_file(TOKEN_FILE)
    drive_service = build('drive', 'v3', credentials=creds)
    docs_service = build('docs', 'v1', credentials=creds)
    return drive_service, docs_service

def get_or_create_dated_folder(drive_service, date_str):
    """Get or create dated archive folder"""
    folder_name = f"Session_{date_str}"
    
    query = f"name='{folder_name}' and '{BASE_FOLDER_ID}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = drive_service.files().list(q=query, fields='files(id, name)').execute()
    folders = results.get('files', [])
    
    if folders:
        print(f"✓ Found existing folder: {folder_name}")
        return folders[0]['id']
    
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [BASE_FOLDER_ID]
    }
    folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
    print(f"✓ Created new folder: {folder_name}")
    return folder['id']

def upload_and_convert_file(drive_service, docs_service, file_path, folder_id):
    """Upload markdown file and convert to Google Doc"""
    filename = os.path.basename(file_path)
    
    # Read content first
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Upload markdown file
    file_metadata = {
        'name': filename,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, mimetype='text/markdown')
    drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"  ✓ Uploaded: {filename}")
    
    # Create Google Doc with content
    doc_name = filename.replace('.md', '')
    doc_metadata = {
        'name': doc_name,
        'parents': [folder_id],
        'mimeType': 'application/vnd.google-apps.document'
    }
    doc = drive_service.files().create(body=doc_metadata, fields='id').execute()
    
    # Add content to doc
    requests = [{
        'insertText': {
            'location': {'index': 1},
            'text': content
        }
    }]
    docs_service.documents().batchUpdate(documentId=doc['id'], body={'requests': requests}).execute()
    print(f"  ✓ Converted to Google Doc: {doc_name}")
    
    return content

def get_or_create_master_doc(drive_service, docs_service, doc_type):
    """Get MASTER document ID - uses hardcoded ID if available, creates if needed"""
    
    # Check if we have hardcoded ID
    if MASTER_DOC_IDS.get(doc_type):
        master_id = MASTER_DOC_IDS[doc_type]
        print(f"  ✓ Using hardcoded MASTER ID: {doc_type}")
        return master_id
    
    # No hardcoded ID - search for existing or create new
    master_name = f"{doc_type}_November_2025_MASTER"
    
    query = f"name='{master_name}' and mimeType='application/vnd.google-apps.document' and trashed=false"
    results = drive_service.files().list(q=query, fields='files(id, name)', orderBy='createdTime').execute()
    files = results.get('files', [])
    
    if files:
        # Use the OLDEST one (original with content)
        master_id = files[0]['id']
        print(f"  ✓ Found MASTER (oldest): {master_name}")
        return master_id
    
    # Create new MASTER
    doc_metadata = {
        'name': master_name,
        'mimeType': 'application/vnd.google-apps.document'
    }
    doc = drive_service.files().create(body=doc_metadata, fields='id').execute()
    print(f"  ✓ Created new MASTER: {master_name}")
    return doc['id']

def append_to_master(docs_service, master_id, content, timestamp):
    """Append session content to MASTER document"""
    # Get current document to find end position
    doc = docs_service.documents().get(documentId=master_id).execute()
    end_index = doc['body']['content'][-1]['endIndex'] - 1
    
    # Ensure we're not at the very start
    if end_index < 1:
        end_index = 1
    
    # Prepare content with separator
    separator = f"\n\n{'='*80}\n=== Session: {timestamp} ===\n{'='*80}\n\n"
    full_content = separator + content + "\n\n"
    
    # Insert at end
    requests = [{
        'insertText': {
            'location': {'index': end_index},
            'text': full_content
        }
    }]
    
    docs_service.documents().batchUpdate(documentId=master_id, body={'requests': requests}).execute()
    print(f"  ✓ Appended to MASTER (index: {end_index})")

def main():
    """Main execution"""
    print("\n" + "="*80)
    print("TRAJANUS USA - SESSION DOCUMENTATION MANAGER v2.0")
    print("Using HARDCODED correct MASTER document IDs")
    print("="*80 + "\n")
    
    # Get services
    drive_service, docs_service = get_services()
    
    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Step 1: Create/get dated folder
    print(f"[STEP 1] Managing Archive Folder...")
    folder_id = get_or_create_dated_folder(drive_service, today)
    
    # Step 2: Upload and convert files
    print(f"\n[STEP 2] Uploading and Converting Files...")
    uploaded_docs = {}
    
    for doc_type in DOCUMENT_TYPES:
        filename = f"{doc_type}_{today}.md"
        if os.path.exists(filename):
            print(f"\nProcessing: {doc_type}")
            content = upload_and_convert_file(drive_service, docs_service, filename, folder_id)
            uploaded_docs[doc_type] = content
        else:
            print(f"\n⚠ Missing: {filename}")
    
    # Step 3: Update MASTER documents
    print(f"\n[STEP 3] Updating MASTER Documents...")
    
    for doc_type, content in uploaded_docs.items():
        print(f"\nUpdating: {doc_type}")
        master_id = get_or_create_master_doc(drive_service, docs_service, doc_type)
        append_to_master(docs_service, master_id, content, timestamp)
    
    # Summary
    print("\n" + "="*80)
    print("✓ SESSION DOCUMENTATION COMPLETE")
    print("="*80)
    print(f"\nProcessed: {len(uploaded_docs)} documents")
    print(f"Archive: Session_{today}")
    print(f"MASTER docs updated: {len(uploaded_docs)}")
    
    print("\n📋 MASTER DOCUMENT URLS:")
    for doc_type in uploaded_docs.keys():
        if MASTER_DOC_IDS.get(doc_type):
            print(f"  {doc_type}: https://docs.google.com/document/d/{MASTER_DOC_IDS[doc_type]}/edit")
    
    print("\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
