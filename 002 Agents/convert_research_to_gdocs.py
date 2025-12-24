#!/usr/bin/env python3
"""
Convert Research Markdown Files to Google Docs
Uses Google Drive API to upload .md files and convert to Google Docs format
"""

import os
import pickle
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# CRITICAL: Use forward slashes
RESEARCH_FOLDER = Path('G:/My Drive/00 - Trajanus USA/00-Command-Center/agents/research')
CREDS_PATH = Path('G:/My Drive/00 - Trajanus USA/00-Command-Center/Credentials')
OUTPUT_FOLDER_ID = '1GwQY0nI74Q8NeZEho0KVow43IejKhHCM'  # Research folder from earlier search

def get_credentials():
    """Load Google Drive credentials"""
    creds = None
    token_path = CREDS_PATH / 'token.pickle'
    
    if token_path.exists():
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
    
    return creds

def convert_md_to_gdoc(service, md_file, folder_id):
    """Upload markdown file and convert to Google Doc"""
    file_metadata = {
        'name': md_file.stem,  # Remove .md extension
        'mimeType': 'application/vnd.google-apps.document',
        'parents': [folder_id]
    }
    
    media = MediaFileUpload(
        str(md_file),
        mimetype='text/markdown',
        resumable=True
    )
    
    try:
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink'
        ).execute()
        
        return file
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None

def main():
    print("=" * 70)
    print("RESEARCH FINDINGS → GOOGLE DOCS CONVERTER")
    print("=" * 70)
    print(f"Source: {RESEARCH_FOLDER}")
    print(f"Output Folder ID: {OUTPUT_FOLDER_ID}")
    print("=" * 70)
    
    # Check source folder
    if not RESEARCH_FOLDER.exists():
        print(f"\n[ERROR] Research folder not found: {RESEARCH_FOLDER}")
        return
    
    # Get markdown files
    md_files = list(RESEARCH_FOLDER.glob('*.md'))
    print(f"\n[FOUND] {len(md_files)} markdown files\n")
    
    if len(md_files) == 0:
        print("[WARNING] No markdown files found")
        return
    
    # Authenticate
    print("[AUTH] Loading Google Drive credentials...")
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    print("[AUTH] ✓ Connected to Google Drive\n")
    
    # Convert each file
    converted = 0
    skipped = 0
    
    for md_file in sorted(md_files):
        print(f"[CONVERT] {md_file.name}")
        
        result = convert_md_to_gdoc(service, md_file, OUTPUT_FOLDER_ID)
        
        if result:
            print(f"  ✓ Created: {result['name']}")
            print(f"  ✓ Link: {result['webViewLink']}")
            converted += 1
        else:
            skipped += 1
        
        print()
    
    # Summary
    print("=" * 70)
    print("CONVERSION COMPLETE")
    print("=" * 70)
    print(f"Total Files: {len(md_files)}")
    print(f"Converted: {converted}")
    print(f"Skipped: {skipped}")
    print("\n[NEXT] Claude can now read these as Google Docs")
    print("=" * 70)

if __name__ == '__main__':
    main()
