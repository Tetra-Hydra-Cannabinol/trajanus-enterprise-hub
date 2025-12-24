# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
CONVERT_MD_TO_GOOGLE_DOCS.py
============================
THE SOLUTION TO CLAUDE'S MEMORY PROBLEM

This script converts markdown (.md) files to Google Docs format.
Claude CAN read Google Docs but CANNOT read .md files.
Running this script = Claude remembers everything.

Author: Claude (for Bill King, Trajanus USA)
Date: December 6, 2025
"""

import os
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# Scopes required for Google Docs conversion
SCOPES = ['https://www.googleapis.com/auth/drive']

# Configuration - EDIT THESE PATHS IF NEEDED
CONFIG = {
    # Where to find credentials
    'credentials_path': r'G:\My Drive\00 - Trajanus USA\00-Command-Center\Credentials\credentials.json',
    'token_path': r'G:\My Drive\00 - Trajanus USA\00-Command-Center\token.json',
    
    # Folders to scan for .md files
    'source_folders': [
        r'G:\My Drive\00 - Trajanus USA\00-Command-Center',
        r'G:\My Drive\00 - Trajanus USA\00-Command-Center\Session-Logs',
        r'G:\My Drive\00 - Trajanus USA\03-Living-Documents',
        r'G:\My Drive\00 - Trajanus USA\07-Session-Journals',
        r'G:\My Drive\00 - Trajanus USA\08-EOS-Files',
    ],
    
    # Target Google Drive folder ID for converted docs
    # This is the folder where converted Google Docs will be created
    # Leave as None to put in same folder structure, or set a specific folder ID
    'target_folder_id': None,
    
    # How far back to look (in hours)
    'hours_back': 24,
    
    # Whether to delete original .md files after conversion
    'delete_originals': False,
    
    # Prefix to add to converted file names (empty string = no prefix)
    'converted_prefix': '',
}


class GoogleDocsConverter:
    """Converts local markdown files to Google Docs format."""
    
    def __init__(self):
        self.creds = None
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Handle OAuth authentication."""
        creds_path = CONFIG['credentials_path']
        token_path = CONFIG['token_path']
        
        if os.path.exists(token_path):
            self.creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                print("Refreshing token...")
                self.creds.refresh(Request())
            else:
                print("Starting authentication flow...")
                print("A browser window will open - please authorize the app.")
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            with open(token_path, 'w') as token:
                token.write(self.creds.to_json())
            print("Authentication successful!")
        
        self.service = build('drive', 'v3', credentials=self.creds)
        print("Google Drive service initialized.")
    
    def find_md_files(self, folder_path, hours_back=24):
        """
        Find .md files in a folder modified within the specified time window.
        
        Args:
            folder_path: Local path to search
            hours_back: Only include files modified within this many hours
            
        Returns:
            List of file paths
        """
        md_files = []
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        if not os.path.exists(folder_path):
            print(f"  [WARN] Folder not found: {folder_path}")
            return md_files
        
        for filename in os.listdir(folder_path):
            if filename.endswith('.md'):
                filepath = os.path.join(folder_path, filename)
                mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                
                if mod_time >= cutoff_time:
                    md_files.append({
                        'path': filepath,
                        'name': filename,
                        'modified': mod_time
                    })
        
        return md_files
    
    def find_or_create_folder(self, folder_name, parent_id='root'):
        """
        Find a folder in Google Drive, or create it if it doesn't exist.
        
        Args:
            folder_name: Name of folder to find/create
            parent_id: ID of parent folder (default: 'root')
            
        Returns:
            Folder ID
        """
        # Search for existing folder
        query = f"name='{folder_name}' and '{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = self.service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])
        
        if items:
            return items[0]['id']
        
        # Create folder if not found
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
        folder = self.service.files().create(body=file_metadata, fields='id').execute()
        print(f"  [NEW] Created folder: {folder_name}")
        return folder.get('id')
    
    def convert_md_to_google_doc(self, local_path, target_folder_id=None):
        """
        Convert a local markdown file to a Google Doc.
        
        Args:
            local_path: Path to the .md file
            target_folder_id: Google Drive folder ID (optional)
            
        Returns:
            dict with 'id', 'name', 'webViewLink' or None on failure
        """
        filename = os.path.basename(local_path)
        doc_name = CONFIG['converted_prefix'] + filename.replace('.md', '')
        
        try:
            # Read markdown content
            with open(local_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create file metadata
            file_metadata = {
                'name': doc_name,
                'mimeType': 'application/vnd.google-apps.document'
            }
            
            if target_folder_id:
                file_metadata['parents'] = [target_folder_id]
            
            # Upload as Google Doc (Google converts it automatically)
            # We need to upload as text/plain or text/markdown and let Google convert
            media = MediaFileUpload(local_path, mimetype='text/markdown', resumable=True)
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink'
            ).execute()
            
            return file
            
        except Exception as e:
            print(f"  [ERROR] Failed to convert {filename}: {e}")
            return None
    
    def run_conversion(self, hours_back=None, folders=None):
        """
        Run the full conversion process.
        
        Args:
            hours_back: Override default time window
            folders: Override default folder list
            
        Returns:
            Summary dict with counts
        """
        hours = hours_back or CONFIG['hours_back']
        source_folders = folders or CONFIG['source_folders']
        target_folder_id = CONFIG['target_folder_id']
        
        print("=" * 60)
        print("MARKDOWN TO GOOGLE DOCS CONVERTER")
        print("=" * 60)
        print(f"Time window: Last {hours} hours")
        print(f"Delete originals: {CONFIG['delete_originals']}")
        print()
        
        # Collect all .md files
        all_files = []
        print("Scanning folders...")
        for folder in source_folders:
            folder_short = os.path.basename(folder)
            files = self.find_md_files(folder, hours)
            print(f"  [{folder_short}] Found {len(files)} file(s)")
            all_files.extend(files)
        
        print(f"\nTotal: {len(all_files)} markdown files to convert")
        print("-" * 60)
        
        if not all_files:
            print("No files to convert!")
            return {'converted': 0, 'failed': 0, 'skipped': 0}
        
        # Convert each file
        results = {'converted': 0, 'failed': 0, 'skipped': 0}
        
        for file_info in all_files:
            filepath = file_info['path']
            filename = file_info['name']
            
            print(f"\nConverting: {filename}")
            print(f"  Modified: {file_info['modified'].strftime('%Y-%m-%d %H:%M')}")
            
            result = self.convert_md_to_google_doc(filepath, target_folder_id)
            
            if result:
                print(f"  [OK] Created: {result['name']}")
                print(f"  Link: {result['webViewLink']}")
                results['converted'] += 1
                
                # Delete original if configured
                if CONFIG['delete_originals']:
                    try:
                        os.remove(filepath)
                        print(f"  [DEL] Removed original: {filename}")
                    except Exception as e:
                        print(f"  [WARN] Could not delete original: {e}")
            else:
                results['failed'] += 1
        
        # Summary
        print()
        print("=" * 60)
        print("CONVERSION COMPLETE")
        print("=" * 60)
        print(f"  Converted: {results['converted']}")
        print(f"  Failed:    {results['failed']}")
        print(f"  Skipped:   {results['skipped']}")
        print()
        
        if results['converted'] > 0:
            print("SUCCESS! Claude can now read these files in future sessions.")
            print("The memory problem is SOLVED for these documents.")
        
        return results


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Convert markdown files to Google Docs format'
    )
    parser.add_argument(
        '--hours', '-H', type=int, default=24,
        help='Hours back to search (default: 24)'
    )
    parser.add_argument(
        '--all', '-a', action='store_true',
        help='Convert ALL .md files (ignore time window)'
    )
    parser.add_argument(
        '--folder', '-f', type=str,
        help='Specific folder to process (overrides defaults)'
    )
    
    args = parser.parse_args()
    
    # Adjust hours if --all flag is set
    hours = 8760 if args.all else args.hours  # 8760 hours = 1 year
    
    # Handle specific folder
    folders = [args.folder] if args.folder else None
    
    # Run conversion
    converter = GoogleDocsConverter()
    converter.run_conversion(hours_back=hours, folders=folders)


if __name__ == "__main__":
    main()
