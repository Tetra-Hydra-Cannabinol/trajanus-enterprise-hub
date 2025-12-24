"""
Google Drive Manager for Trajanus Command Center
================================================

This script handles all Google Drive operations:
- Authentication
- File upload/download
- Folder creation and organization
- File management (move, rename, delete)
- Integration with Claude workflows

Author: Claude & Bill
Date: October 27, 2025
"""

import os
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload, MediaIoBaseUpload

# SCOPES defines what permissions we're requesting
# If modifying these scopes, delete the file token.json
SCOPES = ['https://www.googleapis.com/auth/drive']

class GoogleDriveManager:
    """
    Manages all Google Drive operations for the Trajanus Command Center.
    """
    
    def __init__(self, credentials_path='credentials/credentials.json', token_path='credentials/token.json'):
        """
        Initialize the Google Drive Manager.
        
        Args:
            credentials_path: Path to the credentials.json file from Google Cloud Console
            token_path: Path where the token.json file will be stored after authentication
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.creds = None
        self.service = None
        
        # Authenticate and build the service
        self.authenticate()
    
    def authenticate(self):
        """
        Handles the OAuth authentication flow.
        
        On first run:
        - Opens browser for user to authorize
        - Saves token.json for future use
        
        On subsequent runs:
        - Uses saved token.json
        - Refreshes if expired
        """
        # Check if we have a saved token
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        
        # If no valid credentials, let user log in
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                # Refresh the token if it's expired
                print("Refreshing expired token...")
                self.creds.refresh(Request())
            else:
                # First-time authentication
                print("Opening browser for first-time authentication...")
                print("Please authorize the app in your browser.")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(self.token_path, 'w') as token:
                token.write(self.creds.to_json())
            print(f"Authentication successful! Token saved to {self.token_path}")
        
        # Build the Drive service
        try:
            self.service = build('drive', 'v3', credentials=self.creds)
            print("Google Drive service initialized successfully!")
        except HttpError as error:
            print(f"An error occurred: {error}")
            self.service = None
    
    def list_files(self, folder_id=None, max_results=100):
        """
        List files in Google Drive.
        
        Args:
            folder_id: Optional - ID of folder to list files from. If None, lists from root.
            max_results: Maximum number of files to return
            
        Returns:
            List of file dictionaries with name, id, mimeType, etc.
        """
        try:
            query = f"'{folder_id}' in parents" if folder_id else None
            
            results = self.service.files().list(
                pageSize=max_results,
                q=query,
                fields="nextPageToken, files(id, name, mimeType, parents, createdTime, modifiedTime, size)"
            ).execute()
            
            items = results.get('files', [])
            
            if not items:
                print('No files found.')
                return []
            
            print(f'Found {len(items)} files:')
            for item in items:
                print(f"  - {item['name']} ({item['mimeType']})")
            
            return items
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []
    
    def find_folder_by_path(self, path):
        """
        Find a folder by its path (e.g., "Trajanus USA/AI Projects/00_Command_Center")
        
        Args:
            path: String path with folders separated by /
            
        Returns:
            Folder ID if found, None otherwise
        """
        parts = path.split('/')
        current_parent = 'root'
        
        for part in parts:
            try:
                query = f"name='{part}' and '{current_parent}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
                results = self.service.files().list(
                    q=query,
                    fields="files(id, name)"
                ).execute()
                
                items = results.get('files', [])
                if not items:
                    print(f"Folder not found: {part}")
                    return None
                
                current_parent = items[0]['id']
                
            except HttpError as error:
                print(f"An error occurred: {error}")
                return None
        
        return current_parent
    
    def create_folder(self, folder_name, parent_folder_id=None):
        """
        Create a new folder in Google Drive.
        
        Args:
            folder_name: Name of the folder to create
            parent_folder_id: Optional - ID of parent folder. If None, creates in root.
            
        Returns:
            ID of the created folder
        """
        try:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            if parent_folder_id:
                file_metadata['parents'] = [parent_folder_id]
            
            folder = self.service.files().create(
                body=file_metadata,
                fields='id, name'
            ).execute()
            
            print(f"Created folder: {folder.get('name')} (ID: {folder.get('id')})")
            return folder.get('id')
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None
    
    def upload_file(self, local_file_path, drive_folder_id=None, drive_filename=None):
        """
        Upload a file to Google Drive.
        
        Args:
            local_file_path: Path to the file on your computer
            drive_folder_id: Optional - ID of folder to upload to. If None, uploads to root.
            drive_filename: Optional - Name for file in Drive. If None, uses local filename.
            
        Returns:
            ID of the uploaded file
        """
        try:
            # Get the filename if not provided
            if not drive_filename:
                drive_filename = os.path.basename(local_file_path)
            
            # Prepare file metadata
            file_metadata = {'name': drive_filename}
            if drive_folder_id:
                file_metadata['parents'] = [drive_folder_id]
            
            # Upload the file
            media = MediaFileUpload(local_file_path, resumable=True)
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink'
            ).execute()
            
            print(f"Uploaded: {file.get('name')}")
            print(f"  File ID: {file.get('id')}")
            print(f"  View: {file.get('webViewLink')}")
            
            return file.get('id')
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None
    
    def download_file(self, file_id, local_path):
        """
        Download a file from Google Drive.
        
        Args:
            file_id: ID of the file in Google Drive
            local_path: Where to save the file on your computer
            
        Returns:
            True if successful, False otherwise
        """
        try:
            request = self.service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            
            done = False
            print(f"Downloading file...")
            while done is False:
                status, done = downloader.next_chunk()
                print(f"  Progress: {int(status.progress() * 100)}%")
            
            # Write to local file
            with open(local_path, 'wb') as f:
                f.write(file.getvalue())
            
            print(f"Downloaded to: {local_path}")
            return True
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return False
    
    def move_file(self, file_id, new_folder_id):
        """
        Move a file to a different folder.
        
        Args:
            file_id: ID of the file to move
            new_folder_id: ID of the destination folder
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get current parents
            file = self.service.files().get(
                fileId=file_id,
                fields='parents'
            ).execute()
            
            previous_parents = ",".join(file.get('parents', []))
            
            # Move the file
            file = self.service.files().update(
                fileId=file_id,
                addParents=new_folder_id,
                removeParents=previous_parents,
                fields='id, parents'
            ).execute()
            
            print(f"Moved file (ID: {file_id}) to folder (ID: {new_folder_id})")
            return True
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return False
    
    def rename_file(self, file_id, new_name):
        """
        Rename a file in Google Drive.
        
        Args:
            file_id: ID of the file to rename
            new_name: New name for the file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            file = self.service.files().update(
                fileId=file_id,
                body={'name': new_name},
                fields='id, name'
            ).execute()
            
            print(f"Renamed file to: {file.get('name')}")
            return True
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return False
    
    def delete_file(self, file_id):
        """
        Delete a file from Google Drive.
        
        Args:
            file_id: ID of the file to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.service.files().delete(fileId=file_id).execute()
            print(f"Deleted file (ID: {file_id})")
            return True
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return False
    
    def create_text_file(self, content, filename, folder_id=None, mime_type='text/plain'):
        """
        Create a text file directly in Google Drive from a string.
        
        Args:
            content: Text content to write to file
            filename: Name for the file
            folder_id: Optional - ID of folder to create in
            mime_type: MIME type of the file
            
        Returns:
            ID of the created file
        """
        try:
            # Prepare file metadata
            file_metadata = {'name': filename}
            if folder_id:
                file_metadata['parents'] = [folder_id]
            
            # Create file from string content
            media = MediaIoBaseUpload(
                io.BytesIO(content.encode('utf-8')),
                mimetype=mime_type,
                resumable=True
            )
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink'
            ).execute()
            
            print(f"Created file: {file.get('name')}")
            print(f"  View: {file.get('webViewLink')}")
            
            return file.get('id')
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None


# Example usage functions
def setup_trajanus_folders(manager):
    """
    Creates the standard Trajanus USA folder structure if it doesn't exist.
    """
    print("\n=== Setting up Trajanus folder structure ===\n")
    
    # Try to find existing Trajanus USA folder
    trajanus_id = manager.find_folder_by_path("Trajanus USA")
    
    if not trajanus_id:
        print("Creating Trajanus USA root folder...")
        trajanus_id = manager.create_folder("Trajanus USA")
    
    # Create AI Projects folder
    ai_projects_id = manager.find_folder_by_path("Trajanus USA/AI Projects")
    if not ai_projects_id:
        print("Creating AI Projects folder...")
        ai_projects_id = manager.create_folder("AI Projects", trajanus_id)
    
    # Create Command Center folder
    command_center_id = manager.find_folder_by_path("Trajanus USA/AI Projects/00_Command_Center")
    if not command_center_id:
        print("Creating Command Center folder...")
        command_center_id = manager.create_folder("00_Command_Center", ai_projects_id)
    
    print("\n=== Folder structure ready! ===\n")
    return command_center_id


if __name__ == "__main__":
    """
    Main execution - demonstrates basic usage
    """
    print("=" * 60)
    print("TRAJANUS GOOGLE DRIVE MANAGER")
    print("=" * 60)
    print()
    
    # Initialize the manager
    print("Initializing Google Drive Manager...")
    manager = GoogleDriveManager()
    
    if manager.service:
        print("\nâœ“ Successfully connected to Google Drive!")
        print()
        
        # List files in root
        print("Listing files in your Google Drive root:")
        print("-" * 60)
        files = manager.list_files(max_results=10)
        
        # Example: Setup folder structure
        # Uncomment these lines to create folders:
        # print("\nSetting up Trajanus folder structure...")
        # folder_id = setup_trajanus_folders(manager)
        
        print()
        print("=" * 60)
        print("Ready to use! Import this module in your Python scripts.")
        print("=" * 60)
    else:
        print("\nâœ— Failed to connect to Google Drive.")
        print("Please check your credentials and try again.")
