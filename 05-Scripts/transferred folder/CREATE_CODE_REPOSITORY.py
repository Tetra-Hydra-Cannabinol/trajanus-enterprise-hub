# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
CREATE_CODE_REPOSITORY.py
=========================
One-time script to create the Code_Repository_MASTER document.
Run this ONCE, then update the document ID in the other scripts.

Author: Claude (for Bill King, Trajanus USA)
Date: December 6, 2025
"""

import os
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

CONFIG = {
    'credentials_path': r'G:\My Drive\00 - Trajanus USA\00-Command-Center\Credentials\credentials.json',
    'token_path': r'G:\My Drive\00 - Trajanus USA\00-Command-Center\token.json',
}

def main():
    print("=" * 60)
    print("CREATE CODE REPOSITORY MASTER")
    print("=" * 60)
    
    # Authenticate
    creds = None
    if os.path.exists(CONFIG['token_path']):
        creds = Credentials.from_authorized_user_file(CONFIG['token_path'], SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CONFIG['credentials_path'], SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(CONFIG['token_path'], 'w') as token:
            token.write(creds.to_json())
    
    docs_service = build('docs', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)
    
    # Create document
    print("\n[1/3] Creating document...")
    doc = docs_service.documents().create(body={'title': 'Code_Repository_MASTER'}).execute()
    doc_id = doc.get('documentId')
    print(f"      Document ID: {doc_id}")
    
    # Add initial content
    print("[2/3] Adding initial content...")
    initial_content = f"""CODE REPOSITORY MASTER
======================
Trajanus USA Development Archive

This document contains ALL scripts and code developed for Trajanus USA.
Each entry includes: code, documentation, context, and timestamp.

PURPOSE:
- Complete development history
- Proof of work with timestamps
- Reference for future sessions
- Shareable with outside collaborators

STARTED: December 6, 2025
AUTHOR: Bill King with Claude AI
DOCUMENT ID: {doc_id}

======================================================================
"""
    
    requests = [{
        'insertText': {
            'location': {'index': 1},
            'text': initial_content
        }
    }]
    
    docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
    
    # Move to Living Documents folder (optional - find folder first)
    print("[3/3] Document created successfully!")
    
    print("\n" + "=" * 60)
    print("SUCCESS!")
    print("=" * 60)
    print(f"\nDocument ID: {doc_id}")
    print(f"\nURL: https://docs.google.com/document/d/{doc_id}/edit")
    print("\n[ACTION REQUIRED]")
    print("Update LIVING_DOCS['code']['id'] in these scripts:")
    print("  - append_to_living_docs.py")
    print("  - EOS_LIVING_DOCS.py")
    print(f"\nSet the ID to: '{doc_id}'")
    print("=" * 60)

if __name__ == "__main__":
    main()
