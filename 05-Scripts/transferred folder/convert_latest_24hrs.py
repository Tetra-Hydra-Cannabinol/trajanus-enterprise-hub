#!/usr/bin/env python3
"""
convert_latest_24hrs.py
Trajanus USA - Command Center Script

Automatically finds and converts files modified in the last 24 hours.
Converts: .md → Google Docs, .docx → Google Docs

Author: Trajanus USA / Claude AI
Created: 2025-12-05
"""

import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Configuration
SCOPES = ['https://www.googleapis.com/auth/drive']
CREDENTIALS_PATH = r'G:\My Drive\00 - Trajanus USA\00-Command-Center\Credentials\credentials.json'
TOKEN_PATH = r'G:\My Drive\00 - Trajanus USA\00-Command-Center\Credentials\token.json'

# Folders to scan
SCAN_FOLDERS = [
    r'G:\My Drive\00 - Trajanus USA\00-Command-Center',
    r'G:\My Drive\00 - Trajanus USA\03-Living-Documents',
    r'G:\My Drive\00 - Trajanus USA\07-Session-Journals',
    r'G:\My Drive\00 - Trajanus USA\08-EOS-Files',
]

# File extensions to convert
CONVERTIBLE_EXTENSIONS = ['.md', '.docx', '.xlsx', '.pptx']

# MIME type mappings
MIME_TYPES = {
    '.md': 'text/markdown',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
}

GOOGLE_MIME_TYPES = {
    '.md': 'application/vnd.google-apps.document',
    '.docx': 'application/vnd.google-apps.document',
    '.xlsx': 'application/vnd.google-apps.spreadsheet',
    '.pptx': 'application/vnd.google-apps.presentation',
}

def get_credentials():
    """Get or refresh Google Drive API credentials."""
    creds = None
    
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_PATH):
                print(f"ERROR: Credentials file not found: {CREDENTIALS_PATH}")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def find_recent_files(hours=24):
    """Find files modified in the last N hours."""
    cutoff_time = datetime.now() - timedelta(hours=hours)
    recent_files = []
    
    for folder in SCAN_FOLDERS:
        if not os.path.exists(folder):
            print(f"  Skipping (not found): {folder}")
            continue
            
        for root, dirs, files in os.walk(folder):
            # Skip certain directories
            dirs[:] = [d for d in dirs if d not in ['Archive', '.git', 'node_modules', 'Credentials']]
            
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in CONVERTIBLE_EXTENSIONS:
                    filepath = os.path.join(root, file)
                    try:
                        mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                        if mtime > cutoff_time:
                            recent_files.append({
                                'path': filepath,
                                'name': file,
                                'ext': ext,
                                'modified': mtime
                            })
                    except Exception as e:
                        print(f"  Error checking {file}: {e}")
    
    return sorted(recent_files, key=lambda x: x['modified'], reverse=True)

def check_if_converted(service, filename):
    """Check if a Google Docs version already exists."""
    base_name = os.path.splitext(filename)[0]
    
    query = f"name contains '{base_name}' and mimeType='application/vnd.google-apps.document' and trashed=false"
    results = service.files().list(q=query, pageSize=5, fields="files(id, name, modifiedTime)").execute()
    
    return len(results.get('files', [])) > 0

def convert_to_google_doc(service, file_info):
    """Convert a file to Google Docs format."""
    try:
        file_metadata = {
            'name': os.path.splitext(file_info['name'])[0],  # Remove extension
            'mimeType': GOOGLE_MIME_TYPES.get(file_info['ext'], 'application/vnd.google-apps.document')
        }
        
        media = MediaFileUpload(
            file_info['path'],
            mimetype=MIME_TYPES.get(file_info['ext']),
            resumable=True
        )
        
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink'
        ).execute()
        
        return file
        
    except Exception as e:
        raise Exception(f"Error converting {file_info['name']}: {str(e)}")

def main():
    """Main function."""
    print("=" * 60)
    print("Convert Latest Files (24 Hours)")
    print("Trajanus USA - Command Center")
    print("=" * 60)
    print(f"\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Get credentials
    print("\nAuthenticating with Google Drive...")
    creds = get_credentials()
    if not creds:
        print("ERROR: Could not get credentials")
        return
    
    service = build('drive', 'v3', credentials=creds)
    print("✓ Authenticated")
    
    # Find recent files
    print("\nScanning for files modified in last 24 hours...")
    recent_files = find_recent_files(24)
    
    if not recent_files:
        print("\n✓ No new files to convert!")
        return
    
    print(f"\nFound {len(recent_files)} files to check:")
    for f in recent_files:
        print(f"  • {f['name']} (modified {f['modified'].strftime('%H:%M')})")
    
    # Convert files
    print("\n" + "-" * 40)
    print("Converting files...")
    print("-" * 40)
    
    converted = 0
    skipped = 0
    errors = 0
    
    for file_info in recent_files:
        print(f"\n→ {file_info['name']}")
        
        # Check if already converted
        if check_if_converted(service, file_info['name']):
            print("  ⊘ Already converted (skipping)")
            skipped += 1
            continue
        
        # Convert
        try:
            result = convert_to_google_doc(service, file_info)
            print(f"  ✓ Converted: {result['name']}")
            converted += 1
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            errors += 1
    
    # Summary
    print("\n" + "=" * 40)
    print("SUMMARY")
    print("=" * 40)
    print(f"  Converted: {converted}")
    print(f"  Skipped:   {skipped}")
    print(f"  Errors:    {errors}")
    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
