"""
Batch Convert MD to Google Docs
Converts all .md files in a selected folder
"""

import os
import re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

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
    """Determine which folder a file should go to"""
    session_patterns = [
        'SESSION_SUMMARY',
        'TECHNICAL_JOURNAL', 
        'SESSION_DIARY',
        r'\d{4}-\d{2}-\d{2}'
    ]
    
    for pattern in session_patterns:
        if re.search(pattern, filename, re.IGNORECASE):
            return FOLDER_IDS.get('SESSION_SUMMARIES')
    
    return FOLDER_IDS.get('LIVING_DOCUMENTS')

def convert_md_to_doc(md_file_path):
    """Convert markdown file to Google Doc"""
    
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    file_name = os.path.splitext(os.path.basename(md_file_path))[0]
    folder_id = determine_destination(file_name)
    
    if folder_id == FOLDER_IDS.get('SESSION_SUMMARIES'):
        destination = "Session-Summaries"
    elif folder_id == FOLDER_IDS.get('LIVING_DOCUMENTS'):
        destination = "Living-Documents"
    else:
        destination = "My Drive root"
        folder_id = None
    
    doc_metadata = {
        'name': file_name,
        'mimeType': 'application/vnd.google-apps.document'
    }
    
    if folder_id:
        doc_metadata['parents'] = [folder_id]
    
    doc = drive_service.files().create(body=doc_metadata).execute()
    doc_id = doc['id']
    
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
    
    print(f"[OK] {file_name} -> {destination}")
    
    return doc_id

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python batch_convert_to_gdocs.py <folder_path>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    
    if not os.path.exists(folder_path):
        print(f"[ERROR] Folder not found: {folder_path}")
        sys.exit(1)
    
    # Find all .md files
    md_files = [f for f in os.listdir(folder_path) if f.endswith('.md')]
    
    if not md_files:
        print(f"[ERROR] No .md files found in {folder_path}")
        sys.exit(1)
    
    print(f"Found {len(md_files)} markdown files")
    print("")
    
    success_count = 0
    error_count = 0
    
    for md_file in md_files:
        try:
            full_path = os.path.join(folder_path, md_file)
            convert_md_to_doc(full_path)
            success_count += 1
        except Exception as e:
            print(f"[ERROR] {md_file}: {str(e)}")
            error_count += 1
    
    print("")
    print(f"Conversion complete: {success_count} succeeded, {error_count} failed")
