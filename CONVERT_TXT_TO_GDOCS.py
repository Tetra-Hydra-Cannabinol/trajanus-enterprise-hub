#!/usr/bin/env python3
"""
TXT TO GOOGLE DOCS CONVERTER
Converts text files (.txt) to Google Docs in the same folder.
Designed for YouTube transcript files.
"""

import os
import sys
import pickle
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def safe_print(text):
    """Safe print that handles unicode on Windows"""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'ignore').decode('ascii'))

def get_credentials():
    """Load Google Drive credentials"""
    creds_path = Path('G:/My Drive/00 - Trajanus USA/00-Command-Center/001 Credentials/token.pickle')

    if not creds_path.exists():
        safe_print(f"[ERROR] Credentials not found: {creds_path}")
        sys.exit(1)

    with open(creds_path, 'rb') as token:
        creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(creds_path, 'wb') as token:
                pickle.dump(creds, token)

    return creds

def get_drive_folder_id(service, local_folder_path):
    """Get Google Drive folder ID that corresponds to a local path."""
    path_str = str(local_folder_path).replace('\\', '/')

    if 'My Drive/' in path_str:
        relative_path = path_str.split('My Drive/')[1]
    else:
        safe_print(f"[ERROR] Path not in Google Drive: {local_folder_path}")
        return None

    folder_names = [f for f in relative_path.split('/') if f]

    if not folder_names:
        return 'root'

    current_id = 'root'

    for folder_name in folder_names:
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

def convert_txt_to_gdoc(service, txt_file, folder_id):
    """Upload .txt and convert to Google Doc"""
    file_metadata = {
        'name': txt_file.stem,  # filename without extension
        'mimeType': 'application/vnd.google-apps.document',
        'parents': [folder_id]
    }

    media = MediaFileUpload(
        str(txt_file),
        mimetype='text/plain',
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
    # Get source folder from command line
    if len(sys.argv) > 1:
        source_folder = Path(sys.argv[1])
    else:
        safe_print("Usage: python CONVERT_TXT_TO_GDOCS.py <folder_path>")
        safe_print("\nExample:")
        safe_print('  python CONVERT_TXT_TO_GDOCS.py "G:\\My Drive\\00 - Trajanus USA\\00-Command-Center\\13-Knowledge-Base\\Transcripts\\LangChain"')
        sys.exit(1)

    safe_print("=" * 70)
    safe_print("TXT TO GOOGLE DOCS CONVERTER")
    safe_print("=" * 70)
    safe_print(f"Source: {source_folder}")

    if not source_folder.exists():
        safe_print(f"[ERROR] Folder not found: {source_folder}")
        sys.exit(1)

    # Get all .txt files
    txt_files = list(source_folder.glob('*.txt'))
    safe_print(f"Found: {len(txt_files)} text files")

    if len(txt_files) == 0:
        safe_print("[WARNING] No .txt files found")
        sys.exit(0)

    # Authenticate
    safe_print("[AUTH] Connecting to Google Drive...")
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    safe_print("[AUTH] Connected")

    # Find the Drive folder ID
    safe_print("[SETUP] Finding source folder in Drive...")
    folder_id = get_drive_folder_id(service, source_folder)

    if not folder_id:
        safe_print("[ERROR] Could not find source folder in Google Drive")
        sys.exit(1)

    safe_print(f"[SETUP] Drive folder ID: {folder_id}")
    safe_print("")

    # Convert each file
    converted = 0
    skipped = 0
    errors = 0

    for txt_file in sorted(txt_files):
        safe_print(f"[CONVERT] {txt_file.name}")

        # Check if Google Doc already exists (check for .gdoc file)
        gdoc_path = txt_file.with_suffix('.gdoc')
        if gdoc_path.exists():
            safe_print(f"  SKIP: .gdoc already exists")
            skipped += 1
            continue

        # Upload and convert
        result = convert_txt_to_gdoc(service, txt_file, folder_id)

        if result:
            safe_print(f"  DONE: {result['name']} (Google Doc created)")
            converted += 1
        else:
            errors += 1

    # Summary
    safe_print("")
    safe_print("=" * 70)
    safe_print("COMPLETE")
    safe_print("=" * 70)
    safe_print(f"Total: {len(txt_files)}")
    safe_print(f"Converted: {converted}")
    safe_print(f"Skipped: {skipped}")
    safe_print(f"Errors: {errors}")
    safe_print("=" * 70)

    if converted > 0:
        safe_print("")
        safe_print(f"Google Docs created in: {source_folder}")
        safe_print("")
        safe_print("Google Drive Desktop will sync and create .gdoc files automatically.")

if __name__ == '__main__':
    main()
