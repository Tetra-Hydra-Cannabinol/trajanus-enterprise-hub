"""
Project Browser for Trajanus Command Center
============================================

Lists project folders and files from Google Drive.
Outputs JSON for the Electron app to consume.

Usage:
    python project_browser.py list-projects
    python project_browser.py list-files <folder_id>
    python project_browser.py download <file_id> <local_path>

Author: Claude & Bill
Date: November 24, 2025
"""

import os
import sys
import json
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive']

# Known project folders - add more as needed
PROJECT_FOLDERS = {
    "Traffic Study Knowledge Base": "1cyO2ShcG7QqcxqfIfWYmkS7t7JowjKCy",
    "Traffic Counts": "1fiR_6LDqaQtxecTny8pXaH4DCyDwlGI-",
    "Traffic Counts Growth Factor 2021": "1lefAdtwJ2nwO10tYLXFWLPxHbYaLCViw",
}


def get_credentials():
    """Get or refresh Google credentials."""
    creds = None
    token_path = 'credentials/token.json'
    credentials_path = 'credentials/credentials.json'
    
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    return creds


def get_service():
    """Build and return the Drive service."""
    creds = get_credentials()
    return build('drive', 'v3', credentials=creds)


def list_projects():
    """List all known project folders."""
    try:
        service = get_service()
        projects = []
        
        for name, folder_id in PROJECT_FOLDERS.items():
            try:
                # Get folder details
                folder = service.files().get(
                    fileId=folder_id,
                    fields='id, name, modifiedTime'
                ).execute()
                
                # Count files in folder
                results = service.files().list(
                    q=f"'{folder_id}' in parents and trashed=false",
                    fields="files(id)"
                ).execute()
                file_count = len(results.get('files', []))
                
                projects.append({
                    'id': folder_id,
                    'name': folder.get('name', name),
                    'modifiedTime': folder.get('modifiedTime', ''),
                    'fileCount': file_count
                })
            except HttpError:
                # Folder might not exist or no access
                projects.append({
                    'id': folder_id,
                    'name': name,
                    'modifiedTime': '',
                    'fileCount': 0,
                    'error': 'Unable to access folder'
                })
        
        print(json.dumps({'success': True, 'projects': projects}, indent=2))
        
    except Exception as e:
        print(json.dumps({'success': False, 'error': str(e)}))


def list_files(folder_id):
    """List all files in a folder."""
    try:
        service = get_service()
        
        # If folder_id is 'root', list root Drive contents
        if folder_id == 'root':
            query = "'root' in parents and trashed=false"
        else:
            query = f"'{folder_id}' in parents and trashed=false"
        
        results = service.files().list(
            q=query,
            fields="files(id, name, mimeType, size, modifiedTime, webViewLink)",
            orderBy="folder,name",
            pageSize=100
        ).execute()
        
        files = results.get('files', [])
        
        # Enhance file info
        for f in files:
            # Add file type category
            mime = f.get('mimeType', '')
            if 'folder' in mime:
                f['type'] = 'folder'
                f['icon'] = '📁'
            elif 'spreadsheet' in mime or 'excel' in mime or mime.endswith('.xlsx'):
                f['type'] = 'spreadsheet'
                f['icon'] = '📊'
            elif 'document' in mime or 'word' in mime or mime.endswith('.docx'):
                f['type'] = 'document'
                f['icon'] = '📄'
            elif 'pdf' in mime:
                f['type'] = 'pdf'
                f['icon'] = '📕'
            elif 'image' in mime:
                f['type'] = 'image'
                f['icon'] = '🖼️'
            elif 'zip' in mime or 'archive' in mime:
                f['type'] = 'archive'
                f['icon'] = '📦'
            elif 'presentation' in mime or 'powerpoint' in mime:
                f['type'] = 'presentation'
                f['icon'] = '📽️'
            else:
                f['type'] = 'file'
                f['icon'] = '📎'
            
            # Format size
            size = int(f.get('size', 0))
            if size > 1024 * 1024:
                f['sizeFormatted'] = f"{size / (1024 * 1024):.1f} MB"
            elif size > 1024:
                f['sizeFormatted'] = f"{size / 1024:.1f} KB"
            else:
                f['sizeFormatted'] = f"{size} bytes"
        
        print(json.dumps({'success': True, 'files': files, 'folderId': folder_id}, indent=2))
        
    except Exception as e:
        print(json.dumps({'success': False, 'error': str(e)}))


def download_file(file_id, local_path):
    """Download a file from Google Drive."""
    try:
        service = get_service()
        
        # Get file info first
        file_info = service.files().get(fileId=file_id, fields='name, mimeType').execute()
        mime_type = file_info.get('mimeType', '')
        
        # Handle Google Docs formats - export them
        export_map = {
            'application/vnd.google-apps.document': ('application/vnd.openxmlformats-officedocument.wordprocessingml.document', '.docx'),
            'application/vnd.google-apps.spreadsheet': ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', '.xlsx'),
            'application/vnd.google-apps.presentation': ('application/vnd.openxmlformats-officedocument.presentationml.presentation', '.pptx'),
        }
        
        if mime_type in export_map:
            export_mime, ext = export_map[mime_type]
            request = service.files().export_media(fileId=file_id, mimeType=export_mime)
            if not local_path.endswith(ext):
                local_path += ext
        else:
            request = service.files().get_media(fileId=file_id)
        
        # Download
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        
        done = False
        while not done:
            status, done = downloader.next_chunk()
        
        # Save to local path
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, 'wb') as f:
            f.write(file.getvalue())
        
        print(json.dumps({
            'success': True, 
            'localPath': local_path,
            'fileName': file_info.get('name'),
            'message': f"Downloaded to {local_path}"
        }))
        
    except Exception as e:
        print(json.dumps({'success': False, 'error': str(e)}))


def scan_for_projects():
    """Scan Google Drive for project folders (folders with 'Project' or 'Study' in name)."""
    try:
        service = get_service()
        
        # Search for folders that look like projects
        query = "mimeType='application/vnd.google-apps.folder' and trashed=false and (name contains 'Project' or name contains 'Study' or name contains 'Traffic' or name contains 'Command')"
        
        results = service.files().list(
            q=query,
            fields="files(id, name, modifiedTime)",
            orderBy="modifiedTime desc",
            pageSize=50
        ).execute()
        
        folders = results.get('files', [])
        
        print(json.dumps({'success': True, 'folders': folders}, indent=2))
        
    except Exception as e:
        print(json.dumps({'success': False, 'error': str(e)}))


def add_project(folder_id, display_name=None):
    """Add a folder to the known projects list."""
    try:
        service = get_service()
        
        # Get folder info
        folder = service.files().get(
            fileId=folder_id,
            fields='id, name'
        ).execute()
        
        name = display_name or folder.get('name')
        
        # For now, just print it - in production this would save to a config file
        print(json.dumps({
            'success': True,
            'project': {
                'id': folder_id,
                'name': name
            },
            'message': f"Add this to PROJECT_FOLDERS in project_browser.py:\n    \"{name}\": \"{folder_id}\","
        }, indent=2))
        
    except Exception as e:
        print(json.dumps({'success': False, 'error': str(e)}))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            'success': False, 
            'error': 'Usage: python project_browser.py <command> [args]',
            'commands': [
                'list-projects - List known project folders',
                'list-files <folder_id> - List files in a folder',
                'download <file_id> <local_path> - Download a file',
                'scan - Scan Drive for project folders',
                'add-project <folder_id> [display_name] - Add a project folder'
            ]
        }))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'list-projects':
        list_projects()
    elif command == 'list-files' and len(sys.argv) >= 3:
        list_files(sys.argv[2])
    elif command == 'download' and len(sys.argv) >= 4:
        download_file(sys.argv[2], sys.argv[3])
    elif command == 'scan':
        scan_for_projects()
    elif command == 'add-project' and len(sys.argv) >= 3:
        display_name = sys.argv[3] if len(sys.argv) >= 4 else None
        add_project(sys.argv[2], display_name)
    else:
        print(json.dumps({'success': False, 'error': f'Unknown command: {command}'}))
