#!/usr/bin/env python3
"""
Batch Convert Markdown to Google Docs
Converts all .md files in a folder to Google Docs format
"""

import os
import sys
import tempfile
import time
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

# Configuration
SCOPES = ['https://www.googleapis.com/auth/drive']
CREDENTIALS_PATH = r'G:\My Drive\00 - Trajanus USA\00-Command-Center\Credentials\token.json'


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


def convert_md_to_gdoc(service, md_path, target_folder_id=None):
    """Convert a markdown file to Google Docs"""
    try:
        filename = os.path.basename(md_path)
        doc_name = os.path.splitext(filename)[0]
        
        print(f"[CONVERTING] {filename}")
        
        # Create temporary file with proper encoding
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, filename)
        
        # Read markdown and write to temp file
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Upload and convert
        file_metadata = {
            'name': doc_name,
            'mimeType': 'application/vnd.google-apps.document'
        }
        
        if target_folder_id:
            file_metadata['parents'] = [target_folder_id]
        
        media = MediaFileUpload(
            temp_path,
            mimetype='text/plain',
            resumable=True
        )
        
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink'
        ).execute()
        
        print(f"[SUCCESS] Created: {file['name']}")
        print(f"[LINK] {file['webViewLink']}")
        
        # Cleanup temp file
        try:
            os.remove(temp_path)
        except Exception:
            pass
        
        time.sleep(0.5)  # Rate limiting
        return file['id']
        
    except HttpError as error:
        print(f"[ERROR] Failed to convert {md_path}: {error}")
        return None
    except Exception as error:
        print(f"[ERROR] Unexpected error with {md_path}: {error}")
        return None


def get_or_create_folder(service, folder_name, parent_id=None):
    """Get existing folder or create new one"""
    try:
        # Search for existing folder
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
        if parent_id:
            query += f" and '{parent_id}' in parents"
        
        results = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)'
        ).execute()
        
        folders = results.get('files', [])
        
        if folders:
            print(f"[INFO] Using existing folder: {folder_name}")
            return folders[0]['id']
        
        # Create new folder
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        if parent_id:
            file_metadata['parents'] = [parent_id]
        
        folder = service.files().create(
            body=file_metadata,
            fields='id'
        ).execute()
        
        print(f"[INFO] Created folder: {folder_name}")
        return folder['id']
        
    except HttpError as error:
        print(f"[ERROR] Failed to create folder {folder_name}: {error}")
        return None


def batch_convert_folder(service, folder_path):
    """Convert all markdown files in a folder"""
    print(f"\n[INFO] Processing folder: {folder_path}")
    
    if not os.path.exists(folder_path):
        print(f"[ERROR] Folder not found: {folder_path}")
        return
    
    # Get all .md files
    md_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.md'):
                md_files.append(os.path.join(root, file))
    
    if not md_files:
        print("[WARNING] No markdown files found")
        return
    
    print(f"[INFO] Found {len(md_files)} markdown files")
    
    # Convert each file
    success_count = 0
    fail_count = 0
    
    for md_path in md_files:
        result = convert_md_to_gdoc(service, md_path)
        if result:
            success_count += 1
        else:
            fail_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("CONVERSION COMPLETE")
    print("=" * 60)
    print(f"Successfully converted: {success_count}")
    print(f"Failed: {fail_count}")
    print(f"Total: {len(md_files)}")


def main():
    """Main execution"""
    if len(sys.argv) < 2:
        print("Usage: python batch_convert_md_only.py <folder_path>")
        print("\nExample:")
        print('  python batch_convert_md_only.py "G:\\My Drive\\00 - Trajanus USA\\03-Living-Documents"')
        sys.exit(1)
    
    folder_path = sys.argv[1]
    
    print("=" * 60)
    print("BATCH MARKDOWN TO GOOGLE DOCS CONVERTER")
    print("=" * 60)
    
    # Authenticate
    service = authenticate()
    
    # Process folder
    batch_convert_folder(service, folder_path)


if __name__ == '__main__':
    main()
