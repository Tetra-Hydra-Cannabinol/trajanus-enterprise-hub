#!/usr/bin/env python3
"""
Batch convert markdown files to Google Docs format
NO APPEND - Just conversion
"""

import os
import sys
import tempfile
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def get_drive_service():
    """Initialize Google Drive API service"""
    token_path = r'G:\My Drive\00 - Trajanus USA\00-Command-Center\Credentials\token.json'
    creds = Credentials.from_authorized_user_file(token_path, 
        ['https://www.googleapis.com/auth/drive'])
    return build('drive', 'v3', credentials=creds)

def convert_md_to_gdoc(service, md_file_path, parent_folder_id=None):
    """Convert single markdown file to Google Doc"""
    
    file_name = os.path.basename(md_file_path)
    gdoc_name = file_name.replace('.md', '')
    
    print(f"Converting: {file_name}")
    
    # Read markdown content
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create temp file with proper Windows path
    temp_file = os.path.join(tempfile.gettempdir(), file_name)
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Upload as Google Doc
    file_metadata = {
        'name': gdoc_name,
        'mimeType': 'application/vnd.google-apps.document'
    }
    
    if parent_folder_id:
        file_metadata['parents'] = [parent_folder_id]
    
    media = MediaFileUpload(temp_file, 
                           mimetype='text/plain',
                           resumable=True)
    
    try:
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink'
        ).execute()
        
        print(f"  ✓ Created: {file.get('name')}")
        print(f"    URL: {file.get('webViewLink')}")
        
        # Clean up temp file
        os.remove(temp_file)
        
        return file
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return None

def get_folder_id_by_path(service, folder_path):
    """Get Google Drive folder ID from path"""
    
    # Common folder IDs (update these with actual IDs)
    folder_map = {
        '07-Session-Journal': 'YOUR_FOLDER_ID_HERE',
        '08-EOS-Files': 'YOUR_FOLDER_ID_HERE',
        '03-Living-Documents': 'YOUR_FOLDER_ID_HERE'
    }
    
    folder_name = os.path.basename(folder_path)
    
    if folder_name in folder_map:
        return folder_map[folder_name]
    
    # Search for folder by name
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
    results = service.files().list(q=query, fields='files(id, name)').execute()
    files = results.get('files', [])
    
    if files:
        return files[0]['id']
    
    return None

def process_folder(service, folder_path, parent_folder_id=None):
    """Process all .md files in folder recursively"""
    
    folder_path = Path(folder_path)
    
    if not folder_path.exists():
        print(f"Error: Folder not found: {folder_path}")
        return
    
    print(f"\nProcessing folder: {folder_path}")
    print("=" * 60)
    
    # Find all .md files
    md_files = list(folder_path.rglob('*.md'))
    
    if not md_files:
        print("No markdown files found.")
        return
    
    print(f"Found {len(md_files)} markdown files\n")
    
    converted = 0
    failed = 0
    
    for md_file in md_files:
        result = convert_md_to_gdoc(service, str(md_file), parent_folder_id)
        if result:
            converted += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"SUMMARY:")
    print(f"  Converted: {converted}")
    print(f"  Failed: {failed}")
    print(f"  Total: {len(md_files)}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python batch_convert_md_only.py <folder_path> [parent_folder_id]")
        print("\nExample:")
        print('  python batch_convert_md_only.py "G:\\My Drive\\00 - Trajanus USA\\07-Session-Journal"')
        sys.exit(1)
    
    folder_path = sys.argv[1]
    parent_folder_id = sys.argv[2] if len(sys.argv) > 2 else None
    
    print("=" * 60)
    print("BATCH MARKDOWN TO GOOGLE DOCS CONVERTER")
    print("=" * 60)
    
    service = get_drive_service()
    
    # If no parent folder ID provided, try to find it
    if not parent_folder_id:
        parent_folder_id = get_folder_id_by_path(service, folder_path)
        if parent_folder_id:
            print(f"Found parent folder ID: {parent_folder_id}")
    
    process_folder(service, folder_path, parent_folder_id)
    
    print("\nConversion complete!")

if __name__ == '__main__':
    main()
