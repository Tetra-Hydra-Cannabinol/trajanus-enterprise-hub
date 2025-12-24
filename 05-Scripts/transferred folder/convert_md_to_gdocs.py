"""
Smart MD to Google Docs Converter
Automatically routes files to correct folders
"""

import os
import re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Authenticate
creds = Credentials.from_authorized_user_file('token.json')
service = build('docs', 'v1', credentials=creds)
drive_service = build('drive', 'v3', credentials=creds)

# Load folder IDs
FOLDER_IDS = {}
if os.path.exists('folder_ids.txt'):
    with open('folder_ids.txt', 'r') as f:
        for line in f:
            key, value = line.strip().split('=')
            FOLDER_IDS[key] = value

def determine_destination(filename):
    """
    Determine which folder a file should go to based on its name
    """
    # Session documentation patterns
    session_patterns = [
        'SESSION_SUMMARY',
        'TECHNICAL_JOURNAL', 
        'SESSION_DIARY',
        r'\d{4}-\d{2}-\d{2}'  # Date pattern YYYY-MM-DD
    ]
    
    # Check if it's a session document
    for pattern in session_patterns:
        if re.search(pattern, filename, re.IGNORECASE):
            return FOLDER_IDS.get('SESSION_SUMMARIES')
    
    # Everything else goes to Living Documents
    return FOLDER_IDS.get('LIVING_DOCUMENTS')

def convert_md_to_doc(md_file_path, force_folder_id=None):
    """
    Convert markdown file to Google Doc
    Auto-routes to correct folder unless folder_id specified
    """
    
    # Read markdown file
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Get filename without extension
    file_name = os.path.splitext(os.path.basename(md_file_path))[0]
    
    # Determine destination folder
    if force_folder_id:
        folder_id = force_folder_id
        destination = "Specified folder"
    else:
        folder_id = determine_destination(file_name)
        if folder_id == FOLDER_IDS.get('SESSION_SUMMARIES'):
            destination = "Session-Summaries"
        elif folder_id == FOLDER_IDS.get('LIVING_DOCUMENTS'):
            destination = "Living-Documents"
        else:
            destination = "My Drive root"
            folder_id = None
    
    # Create Google Doc metadata
    doc_metadata = {
        'name': file_name,
        'mimeType': 'application/vnd.google-apps.document'
    }
    
    if folder_id:
        doc_metadata['parents'] = [folder_id]
    
    # Create empty doc
    doc = drive_service.files().create(body=doc_metadata).execute()
    doc_id = doc['id']
    
    # Insert content
    requests = [{
        'insertText': {
            'location': {'index': 1},
            'text': md_content
        }
    }]
    
    service.documents().batchUpdate(
        documentId=doc_id,
        body={'requests': requests}
    ).execute()
    
    print(f"[OK] Converted: {file_name}")
    print(f"     Destination: {destination}")
    print(f"     Doc ID: {doc_id}")
    print(f"     URL: https://docs.google.com/document/d/{doc_id}/edit")
    print("")
    
    return doc_id

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python convert_md_to_gdocs.py <markdown_file> [folder_id]")
        print("")
        print("Auto-routing rules:")
        print("  - SESSION_SUMMARY_* -> Session-Summaries folder")
        print("  - TECHNICAL_JOURNAL_* -> Session-Summaries folder")
        print("  - SESSION_DIARY_* -> Session-Summaries folder")
        print("  - Files with YYYY-MM-DD -> Session-Summaries folder")
        print("  - Everything else -> Living-Documents folder")
        sys.exit(1)
    
    md_file = sys.argv[1]
    folder_id = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(md_file):
        print(f"[ERROR] File not found: {md_file}")
        sys.exit(1)
    
    # Check if folder IDs are configured
    if not FOLDER_IDS and not folder_id:
        print("[WARNING] folder_ids.txt not found. Run create_folders.py first!")
        print("[WARNING] Files will be saved to My Drive root")
    
    try:
        convert_md_to_doc(md_file, folder_id)
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
