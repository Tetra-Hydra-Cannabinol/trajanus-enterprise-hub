#!/usr/bin/env python3
"""
Convert Excel and PowerPoint files to Google Sheets and Slides
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

def convert_file(service, file_path, folder_id=None):
    """
    Convert Excel or PowerPoint to Google format
    
    Args:
        service: Google Drive service object
        file_path: Path to the file
        folder_id: Optional - Google Drive folder ID
    """
    file_name = os.path.basename(file_path)
    base_name = os.path.splitext(file_name)[0]
    
    # Determine file type and target format
    if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        source_mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        target_mime = 'application/vnd.google-apps.spreadsheet'
        file_type = 'Sheets'
    elif file_path.endswith('.pptx') or file_path.endswith('.ppt'):
        source_mime = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        target_mime = 'application/vnd.google-apps.presentation'
        file_type = 'Slides'
    else:
        print(f"⚠️  Unsupported file type: {file_name}")
        return None
    
    # Set up file metadata
    file_metadata = {
        'name': base_name,
        'mimeType': target_mime
    }
    
    if folder_id:
        file_metadata['parents'] = [folder_id]
    
    # Upload and convert
    media = MediaFileUpload(file_path, mimetype=source_mime, resumable=True)
    
    try:
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink'
        ).execute()
        
        print(f"✅ {file_name} → Google {file_type}")
        return file
    except Exception as e:
        print(f"❌ Error: {file_name} - {e}")
        return None

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python convert_office_to_google.py <file1.xlsx> [file2.pptx] ...")
        print("   or: python convert_office_to_google.py folder_path")
        sys.exit(1)
    
    print("Excel/PowerPoint to Google Converter")
    print("=" * 50)
    print()
    
    # Authenticate
    print("Authenticating...")
    service = authenticate()
    print("✅ Authenticated!")
    print()
    
    # Process files
    paths = sys.argv[1:]
    files_to_convert = []
    
    for path in paths:
        if os.path.isdir(path):
            # Find all Excel and PowerPoint files in directory
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith(('.xlsx', '.xls', '.pptx', '.ppt')):
                        files_to_convert.append(os.path.join(root, file))
        elif os.path.isfile(path):
            files_to_convert.append(path)
    
    if not files_to_convert:
        print("No Excel or PowerPoint files found.")
        sys.exit(0)
    
    print(f"Converting {len(files_to_convert)} file(s)...")
    print()
    
    converted = 0
    failed = 0
    
    for file_path in files_to_convert:
        result = convert_file(service, file_path)
        if result:
            converted += 1
        else:
            failed += 1
    
    print()
    print("=" * 50)
    print(f"✅ Converted: {converted}")
    print(f"❌ Failed: {failed}")
    print("=" * 50)

if __name__ == '__main__':
    main()
