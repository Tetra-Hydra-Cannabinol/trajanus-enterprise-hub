#!/usr/bin/env python3
"""
Convert single markdown file to Google Docs
Used by file watcher for real-time conversion
"""

import os
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate():
    """Authenticate with Google Drive"""
    creds = None
    token_path = 'Credentials/token.json'
    creds_path = 'Credentials/credentials.json'
    
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    return build('drive', 'v3', credentials=creds)

def convert_md_file(service, file_path):
    """Convert markdown file to Google Docs"""
    
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return False
    
    file_name = os.path.basename(file_path)
    base_name = os.path.splitext(file_name)[0]
    
    # Read markdown content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return False
    
    # Create Google Doc
    file_metadata = {
        'name': base_name,
        'mimeType': 'application/vnd.google-apps.document'
    }
    
    media = MediaFileUpload(
        file_path,
        mimetype='text/markdown',
        resumable=True
    )
    
    try:
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name'
        ).execute()
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python convert_single_md.py <file.md>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    service = authenticate()
    success = convert_md_file(service, file_path)
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
