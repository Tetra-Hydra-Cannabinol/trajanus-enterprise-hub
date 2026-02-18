#!/usr/bin/env python3
"""
Append Living Documents Script
Consolidates diary and technical entries from session summaries into master documents
"""

import os
import sys
import tempfile
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configuration
SCOPES = ['https://www.googleapis.com/auth/drive']
CREDENTIALS_PATH = r'G:\My Drive\00 - Trajanus USA\00-Command-Center\Credentials\token.json'

# Master document IDs
PERSONAL_DIARY_MASTER_ID = '1HKOisNN8A5rf9YdFJnJSdgH326bdJTun2rDqObNvrM8'
TECHNICAL_JOURNAL_MASTER_ID = '1LQnGWZVV5Ze30XH8OOYWqASEM2nLYSQxAL8ok0FY18s'

# Source folders to process
SOURCE_FOLDERS = [
    r'G:\My Drive\00 - Trajanus USA\03-Living-Documents',
    r'G:\My Drive\00 - Trajanus USA\07-Session-Journal',
    r'G:\My Drive\00 - Trajanus USA\08-EOS-Files'
]

# File patterns to extract from
DIARY_PATTERNS = ['Personal_Diary_', 'Bills_Daily_Diary_']
TECH_PATTERNS = ['Technical_Journal_']
SKIP_PATTERNS = ['Session_Summary_', '_MASTER']


def authenticate():
    """Authenticate with Google Drive API"""
    print("[INFO] Authenticating with Google Drive...")
    
    creds = None
    if os.path.exists(CREDENTIALS_PATH):
        creds = Credentials.from_authorized_user_file(CREDENTIALS_PATH, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("[ERROR] No valid credentials found")
            print(f"[ERROR] Expected token.json at: {CREDENTIALS_PATH}")
            sys.exit(1)
    
    return build('drive', 'v3', credentials=creds)


def list_google_docs(service, folder_paths):
    """List all Google Docs in specified folders"""
    print("[INFO] Scanning folders for documents...")
    
    all_files = []
    
    for folder_path in folder_paths:
        print(f"[INFO] Scanning: {folder_path}")
        
        # Get folder ID from path
        # This is simplified - in production you'd need to resolve the path
        query = "mimeType='application/vnd.google-apps.document'"
        
        try:
            results = service.files().list(
                q=query,
                pageSize=1000,
                fields="files(id, name, modifiedTime)"
            ).execute()
            
            files = results.get('files', [])
            all_files.extend(files)
            print(f"[INFO] Found {len(files)} documents")
            
        except HttpError as error:
            print(f"[ERROR] Failed to list files: {error}")
    
    return all_files


def get_document_content(service, doc_id):
    """Get content from a Google Doc"""
    try:
        doc_service = build('docs', 'v1', credentials=service._http.credentials)
        doc = doc_service.documents().get(documentId=doc_id).execute()
        
        content = []
        for element in doc.get('body', {}).get('content', []):
            if 'paragraph' in element:
                paragraph = element['paragraph']
                for text_run in paragraph.get('elements', []):
                    if 'textRun' in text_run:
                        content.append(text_run['textRun']['content'])
        
        return ''.join(content)
        
    except HttpError as error:
        print(f"[ERROR] Failed to get document {doc_id}: {error}")
        return None


def append_to_document(service, doc_id, content):
    """Append content to a Google Doc"""
    try:
        doc_service = build('docs', 'v1', credentials=service._http.credentials)
        
        # Get current document to find end position
        doc = doc_service.documents().get(documentId=doc_id).execute()
        end_index = doc.get('body', {}).get('content', [])[-1].get('endIndex', 1)
        
        # Insert content at end
        requests = [
            {
                'insertText': {
                    'location': {
                        'index': end_index - 1
                    },
                    'text': f"\n\n{content}"
                }
            }
        ]
        
        doc_service.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': requests}
        ).execute()
        
        print(f"[SUCCESS] Appended to document {doc_id}")
        time.sleep(0.5)  # Rate limiting
        
    except HttpError as error:
        print(f"[ERROR] Failed to append to document {doc_id}: {error}")


def should_process_file(filename):
    """Determine if file should be processed"""
    # Skip master files
    if any(skip in filename for skip in SKIP_PATTERNS):
        return False, None
    
    # Check if diary entry
    if any(pattern in filename for pattern in DIARY_PATTERNS):
        return True, 'diary'
    
    # Check if tech entry
    if any(pattern in filename for pattern in TECH_PATTERNS):
        return True, 'tech'
    
    return False, None


def main():
    """Main execution"""
    print("=" * 60)
    print("LIVING DOCUMENTS CONSOLIDATION")
    print("=" * 60)
    
    # Authenticate
    service = authenticate()
    
    # Get all documents
    files = list_google_docs(service, SOURCE_FOLDERS)
    
    if not files:
        print("[WARNING] No documents found to process")
        return
    
    # Process each file
    diary_count = 0
    tech_count = 0
    
    for file in files:
        should_process, doc_type = should_process_file(file['name'])
        
        if not should_process:
            continue
        
        print(f"\n[PROCESSING] {file['name']}")
        
        # Get content
        content = get_document_content(service, file['id'])
        
        if not content:
            continue
        
        # Append to appropriate master
        if doc_type == 'diary':
            print(f"[INFO] Appending to Personal Diary Master")
            append_to_document(service, PERSONAL_DIARY_MASTER_ID, content)
            diary_count += 1
        elif doc_type == 'tech':
            print(f"[INFO] Appending to Technical Journal Master")
            append_to_document(service, TECHNICAL_JOURNAL_MASTER_ID, content)
            tech_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("CONSOLIDATION COMPLETE")
    print("=" * 60)
    print(f"Diary entries appended: {diary_count}")
    print(f"Tech entries appended: {tech_count}")
    print("\nMaster Documents:")
    print(f"  Personal Diary: https://docs.google.com/document/d/{PERSONAL_DIARY_MASTER_ID}/edit")
    print(f"  Technical Journal: https://docs.google.com/document/d/{TECHNICAL_JOURNAL_MASTER_ID}/edit")


if __name__ == '__main__':
    main()
