"""
TRAJANUS USA - GOOGLE DRIVE DOCUMENT UPLOADER
==============================================

This script uploads Claude session documents directly to Google Drive.

LOCATION: G:\My Drive\Trajanus USA\00_Command_Center\

REQUIREMENTS:
- credentials.json (in same folder)
- token.json (in same folder)  
- Python packages: pip install google-auth google-auth-oauthlib google-api-python-client

USAGE:
    python upload_session_docs.py [files...]
    
    If no files specified, uploads all .md, .txt, and .html files in current directory.

TARGET LOCATION:
    Trajanus USA / AI Projects / 01_Documentation / Session Summaries / [YYYY-MM-DD]/
"""

import os
import sys
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

class DriveUploader:
    def __init__(self, credentials_path='credentials.json', token_path='token.json'):
        """Initialize the Google Drive uploader."""
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = None
        self.connect()
    
    def connect(self):
        """Connect to Google Drive API."""
        try:
            creds = Credentials.from_authorized_user_file(self.token_path)
            
            # Refresh if expired
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                # Save refreshed token
                with open(self.token_path, 'w') as token:
                    token.write(creds.to_json())
            
            self.service = build('drive', 'v3', credentials=creds)
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def find_folder(self, name, parent_id=None):
        """Find a folder by name, optionally within a parent folder."""
        try:
            query = f"name='{name}' and mimeType='application/vnd.google-apps.folder'"
            if parent_id:
                query += f" and '{parent_id}' in parents"
            
            results = self.service.files().list(
                q=query,
                fields='files(id, name)',
                pageSize=1
            ).execute()
            
            files = results.get('files', [])
            return files[0]['id'] if files else None
        except HttpError as e:
            print(f"Error finding folder '{name}': {e}")
            return None
    
    def create_folder(self, name, parent_id=None):
        """Create a new folder."""
        try:
            file_metadata = {
                'name': name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            if parent_id:
                file_metadata['parents'] = [parent_id]
            
            folder = self.service.files().create(
                body=file_metadata,
                fields='id, name'
            ).execute()
            
            return folder.get('id')
        except HttpError as e:
            print(f"Error creating folder '{name}': {e}")
            return None
    
    def get_or_create_folder(self, name, parent_id=None):
        """Get existing folder or create if it doesn't exist."""
        folder_id = self.find_folder(name, parent_id)
        if folder_id:
            return folder_id
        return self.create_folder(name, parent_id)
    
    def setup_folder_structure(self):
        """
        Create/verify the folder structure:
        Trajanus USA / AI Projects / 01_Documentation / Session Summaries / YYYY-MM-DD
        
        Returns the ID of the date folder.
        """
        print("Setting up folder structure...")
        
        # Find Trajanus USA
        print("  Finding Trajanus USA...")
        trajanus_id = self.find_folder("Trajanus USA")
        if not trajanus_id:
            print("  ❌ Trajanus USA folder not found!")
            return None
        print(f"  ✅ Found Trajanus USA")
        
        # Get or create AI Projects
        print("  Finding/creating AI Projects...")
        ai_projects_id = self.get_or_create_folder("AI Projects", trajanus_id)
        if not ai_projects_id:
            return None
        print(f"  ✅ AI Projects ready")
        
        # Get or create 01_Documentation
        print("  Finding/creating 01_Documentation...")
        documentation_id = self.get_or_create_folder("01_Documentation", ai_projects_id)
        if not documentation_id:
            return None
        print(f"  ✅ 01_Documentation ready")
        
        # Get or create Session Summaries
        print("  Finding/creating Session Summaries...")
        summaries_id = self.get_or_create_folder("Session Summaries", documentation_id)
        if not summaries_id:
            return None
        print(f"  ✅ Session Summaries ready")
        
        # Get or create today's date folder
        today = datetime.now().strftime("%Y-%m-%d")
        print(f"  Finding/creating {today}...")
        date_folder_id = self.get_or_create_folder(today, summaries_id)
        if not date_folder_id:
            return None
        print(f"  ✅ {today} ready")
        
        return date_folder_id
    
    def upload_file(self, filepath, folder_id):
        """Upload a file to the specified folder."""
        try:
            filename = os.path.basename(filepath)
            
            file_metadata = {
                'name': filename,
                'parents': [folder_id]
            }
            
            media = MediaFileUpload(filepath, resumable=True)
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink'
            ).execute()
            
            return file
        except HttpError as e:
            print(f"Error uploading {filepath}: {e}")
            return None
    
    def upload_documents(self, files=None):
        """Upload session documents to Google Drive."""
        print("=" * 70)
        print("TRAJANUS USA - GOOGLE DRIVE UPLOADER")
        print("=" * 70)
        print()
        
        if not self.service:
            print("❌ Not connected to Google Drive")
            return
        
        print("✅ Connected to Google Drive")
        print()
        
        # Setup folder structure
        target_folder_id = self.setup_folder_structure()
        if not target_folder_id:
            print("\n❌ Failed to setup folder structure")
            return
        
        print()
        print("=" * 70)
        print("UPLOADING FILES")
        print("=" * 70)
        print()
        
        # If no files specified, find all session documents
        if not files:
            files = []
            for ext in ['*.md', '*.txt', '*.html']:
                import glob
                files.extend(glob.glob(ext))
        
        if not files:
            print("❌ No files found to upload")
            return
        
        uploaded = 0
        failed = 0
        
        for filepath in files:
            if not os.path.exists(filepath):
                print(f"⚠️  Skipping {filepath} (not found)")
                failed += 1
                continue
            
            filename = os.path.basename(filepath)
            filesize = os.path.getsize(filepath) / 1024  # KB
            
            print(f"Uploading: {filename} ({filesize:.1f} KB)")
            
            result = self.upload_file(filepath, target_folder_id)
            
            if result:
                print(f"  ✅ Success!")
                print(f"  📁 View: {result.get('webViewLink')}")
                uploaded += 1
            else:
                print(f"  ❌ Failed")
                failed += 1
            
            print()
        
        print("=" * 70)
        print(f"UPLOAD COMPLETE: {uploaded} uploaded, {failed} failed")
        print("=" * 70)
        print()
        
        today = datetime.now().strftime("%Y-%m-%d")
        print(f"📂 Location: Trajanus USA / AI Projects / 01_Documentation / Session Summaries / {today}")
        print()


def main():
    """Main execution."""
    # Get files from command line, or use defaults
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        files = None  # Will auto-detect
    
    # Create uploader and run
    uploader = DriveUploader()
    uploader.upload_documents(files)


if __name__ == "__main__":
    main()
