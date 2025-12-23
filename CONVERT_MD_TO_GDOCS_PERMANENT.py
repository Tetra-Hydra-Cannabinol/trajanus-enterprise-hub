#!/usr/bin/env python3
"""
PERMANENT MARKDOWN TO GOOGLE DOCS CONVERTER
Universal script that ALWAYS works - no pandoc, no bullshit

FIXED: Now creates .gdoc files in the SAME folder as source .md files
"""

import os
import sys
import json
import pickle
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def safe_print(text):
    """Safe print that handles emoji/unicode on Windows"""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'ignore').decode('ascii'))

def get_credentials():
    """Load Google Drive credentials"""
    # Hard-coded credential path (fixed folder name)
    creds_path = Path('G:/My Drive/00 - Trajanus USA/00-Command-Center/001 Credentials')
    token_path = creds_path / 'token.pickle'

    if not token_path.exists():
        safe_print(f"[ERROR] Credentials not found: {token_path}")
        sys.exit(1)

    with open(token_path, 'rb') as token:
        creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)

    return creds

def get_drive_folder_id(service, local_folder_path):
    """
    Get Google Drive folder ID that corresponds to a local path.
    Navigates Drive folder hierarchy to find the matching folder.
    """
    # Convert path and extract parts after "My Drive"
    path_str = str(local_folder_path).replace('\\', '/')

    if 'My Drive/' in path_str:
        relative_path = path_str.split('My Drive/')[1]
    else:
        safe_print(f"[ERROR] Path not in Google Drive: {local_folder_path}")
        return None

    # Split into folder names
    folder_names = [f for f in relative_path.split('/') if f]

    if not folder_names:
        return 'root'

    # Navigate through folders
    current_id = 'root'

    for folder_name in folder_names:
        # Escape single quotes in folder name
        escaped_name = folder_name.replace("'", "\\'")
        query = f"name='{escaped_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false and '{current_id}' in parents"

        try:
            results = service.files().list(q=query, fields='files(id, name)').execute()
            files = results.get('files', [])

            if not files:
                safe_print(f"[ERROR] Folder not found in Drive: {folder_name}")
                return None

            current_id = files[0]['id']
        except Exception as e:
            safe_print(f"[ERROR] Drive API error: {e}")
            return None

    return current_id

def create_gdoc_file(md_file_path, doc_id):
    """
    Create a Windows URL shortcut (.url) in the SAME folder as the source .md file.

    Note: Google Drive Desktop blocks .gdoc file creation, so we use .url
    shortcuts instead. Double-clicking opens the Google Doc in browser.
    """
    # Build the Google Doc URL
    doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"

    # Windows URL shortcut format
    url_content = f"""[InternetShortcut]
URL={doc_url}
IconIndex=0
"""

    # Build path - use .url extension
    md_path_str = str(md_file_path)
    if md_path_str.lower().endswith('.md'):
        base_path = md_path_str[:-3]
    else:
        base_path = md_path_str

    url_path = base_path + '.url'

    try:
        with open(url_path, 'w', encoding='utf-8') as f:
            f.write(url_content)
        return url_path
    except Exception as e:
        safe_print(f"  ERROR creating shortcut: {e}")
        return None

def convert_md_to_gdoc(service, md_file, folder_id):
    """Upload markdown file and convert to Google Doc"""
    file_metadata = {
        'name': md_file.stem,
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
            fields='id, name'
        ).execute()
        return file
    except Exception as e:
        safe_print(f"  ERROR uploading: {e}")
        return None

def main():
    # Get source folder from command line or use default
    if len(sys.argv) > 1:
        source_folder = Path(sys.argv[1])
    else:
        source_folder = Path('G:/My Drive/00 - Trajanus USA/00-Command-Center/agents/research')

    safe_print("=" * 70)
    safe_print("MARKDOWN TO GOOGLE DOCS CONVERTER")
    safe_print("=" * 70)
    safe_print(f"Source: {source_folder}")

    if not source_folder.exists():
        safe_print(f"[ERROR] Folder not found: {source_folder}")
        sys.exit(1)

    # Get all markdown files
    md_files = list(source_folder.glob('*.md'))
    safe_print(f"Found: {len(md_files)} markdown files")

    if len(md_files) == 0:
        safe_print("[WARNING] No markdown files found")
        sys.exit(0)

    # Authenticate
    safe_print("[AUTH] Connecting to Google Drive...")
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    safe_print("[AUTH] Connected")

    # Find the Drive folder ID that matches the local source folder
    safe_print("[SETUP] Finding source folder in Drive...")
    folder_id = get_drive_folder_id(service, source_folder)

    if not folder_id:
        safe_print("[ERROR] Could not find source folder in Google Drive")
        safe_print("        Make sure the folder exists and is synced")
        sys.exit(1)

    safe_print(f"[SETUP] Drive folder ID: {folder_id}")
    safe_print(f"[SETUP] Google Docs will be created in SAME folder as .md files")
    safe_print(f"[SETUP] Google Drive Desktop will auto-create .gdoc shortcuts")

    # Convert each file
    safe_print("")
    converted = 0
    skipped = 0

    for md_file in sorted(md_files):
        safe_print(f"[CONVERT] {md_file.name}")

        # Check if Google Doc already exists (check for .gdoc file)
        gdoc_path = str(md_file)[:-3] + '.gdoc'
        if os.path.exists(gdoc_path):
            safe_print(f"  SKIP: .gdoc already exists")
            skipped += 1
            continue

        # Upload and convert to the SAME Drive folder
        result = convert_md_to_gdoc(service, md_file, folder_id)

        if result:
            safe_print(f"  DONE: {result['name']} (Google Doc created)")
            converted += 1
        else:
            skipped += 1

    # Summary
    safe_print("")
    safe_print("=" * 70)
    safe_print("COMPLETE")
    safe_print("=" * 70)
    safe_print(f"Total: {len(md_files)}")
    safe_print(f"Converted: {converted}")
    safe_print(f"Skipped: {skipped}")
    safe_print("=" * 70)

    # Note about .gdoc files
    if converted > 0:
        safe_print("")
        safe_print(f"Google Docs created in: {source_folder}")
        safe_print("")
        safe_print("Google Drive Desktop will sync and create .gdoc files automatically.")
        safe_print("This may take a few moments. Refresh File Explorer to see them.")

if __name__ == '__main__':
    main()
