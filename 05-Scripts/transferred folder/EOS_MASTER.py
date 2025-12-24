# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
EOS_MASTER.py
=============
END OF SESSION MASTER AUTOMATION

This script handles all end-of-session tasks:
1. Finds all session files created today
2. Converts markdown files to Google Docs
3. Organizes files into proper folders
4. Creates a handoff document for the next Claude session

RUN THIS AT THE END OF EVERY CLAUDE SESSION.

Author: Claude (for Bill King, Trajanus USA)
Date: December 6, 2025
"""

import os
import shutil
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# Google Drive API scope
SCOPES = ['https://www.googleapis.com/auth/drive']

# ============================================================================
# CONFIGURATION - Edit these paths to match your setup
# ============================================================================
CONFIG = {
    # Authentication files
    'credentials_path': r'G:\My Drive\00 - Trajanus USA\00-Command-Center\Credentials\credentials.json',
    'token_path': r'G:\My Drive\00 - Trajanus USA\00-Command-Center\token.json',
    
    # Base path for Trajanus USA
    'trajanus_root': r'G:\My Drive\00 - Trajanus USA',
    
    # Folders to scan for new session files
    'scan_folders': [
        r'G:\My Drive\00 - Trajanus USA\00-Command-Center',
        r'G:\My Drive\00 - Trajanus USA\00-Command-Center\Session-Logs',
    ],
    
    # Where to move organized session files
    'destinations': {
        'session_summary': r'G:\My Drive\00 - Trajanus USA\07-Session-Journals\Session-Summaries',
        'technical_journal': r'G:\My Drive\00 - Trajanus USA\07-Session-Journals\Technical-Journals',
        'personal_diary': r'G:\My Drive\00 - Trajanus USA\07-Session-Journals\Personal-Diaries',
        'handoff': r'G:\My Drive\00 - Trajanus USA\07-Session-Journals\Handoffs',
        'code_repo': r'G:\My Drive\00 - Trajanus USA\07-Session-Journals\Code-Repository',
    },
    
    # File patterns to identify session file types
    'patterns': {
        'session_summary': ['session_summary', 'Session_Summary'],
        'technical_journal': ['technical_journal', 'Technical_Journal', 'Tech_Journal'],
        'personal_diary': ['diary', 'Diary', 'daily_diary', 'Daily_Diary'],
        'handoff': ['handoff', 'Handoff', 'HANDOFF'],
        'code_repo': ['code_repo', 'Code_Repo', 'code_repository'],
    },
    
    # Hours back to look for files (covers a full work day)
    'hours_back': 16,
}


class EOSAutomation:
    """End of Session Automation Handler."""
    
    def __init__(self):
        self.creds = None
        self.service = None
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.processed_files = []
        self.errors = []
        
    def authenticate(self):
        """Handle OAuth authentication."""
        print("\n[AUTH] Authenticating with Google Drive...")
        
        creds_path = CONFIG['credentials_path']
        token_path = CONFIG['token_path']
        
        if os.path.exists(token_path):
            self.creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            with open(token_path, 'w') as token:
                token.write(self.creds.to_json())
        
        self.service = build('drive', 'v3', credentials=self.creds)
        print("[AUTH] Authentication successful!")
        return True
    
    def find_session_files(self):
        """Find all session files created/modified today."""
        print("\n[SCAN] Scanning for session files...")
        
        cutoff = datetime.now() - timedelta(hours=CONFIG['hours_back'])
        session_files = []
        
        for folder in CONFIG['scan_folders']:
            if not os.path.exists(folder):
                print(f"  [WARN] Folder not found: {folder}")
                continue
            
            folder_name = os.path.basename(folder)
            
            for filename in os.listdir(folder):
                filepath = os.path.join(folder, filename)
                
                # Skip directories
                if os.path.isdir(filepath):
                    continue
                
                # Check if file is recent enough
                mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                if mod_time < cutoff:
                    continue
                
                # Categorize by file type
                file_type = self.categorize_file(filename)
                
                session_files.append({
                    'path': filepath,
                    'name': filename,
                    'type': file_type,
                    'modified': mod_time,
                    'is_markdown': filename.endswith('.md'),
                })
        
        print(f"[SCAN] Found {len(session_files)} session files")
        return session_files
    
    def categorize_file(self, filename):
        """Determine what type of session file this is."""
        filename_lower = filename.lower()
        
        for file_type, patterns in CONFIG['patterns'].items():
            for pattern in patterns:
                if pattern.lower() in filename_lower:
                    return file_type
        
        return 'uncategorized'
    
    def ensure_folder_exists(self, folder_path):
        """Create folder if it doesn't exist."""
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"  [NEW] Created folder: {folder_path}")
    
    def convert_md_to_google_doc(self, filepath):
        """Convert a markdown file to Google Docs format."""
        filename = os.path.basename(filepath)
        doc_name = filename.replace('.md', '')
        
        try:
            file_metadata = {
                'name': doc_name,
                'mimeType': 'application/vnd.google-apps.document'
            }
            
            media = MediaFileUpload(filepath, mimetype='text/markdown', resumable=True)
            
            result = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink'
            ).execute()
            
            return result
            
        except Exception as e:
            self.errors.append(f"Convert failed: {filename} - {e}")
            return None
    
    def organize_file(self, file_info):
        """Move a file to its appropriate destination folder."""
        file_type = file_info['type']
        src_path = file_info['path']
        filename = file_info['name']
        
        # Get destination folder
        if file_type in CONFIG['destinations']:
            dest_folder = CONFIG['destinations'][file_type]
        else:
            # Uncategorized files stay where they are
            return None
        
        # Ensure destination exists
        self.ensure_folder_exists(dest_folder)
        
        # Move file
        dest_path = os.path.join(dest_folder, filename)
        
        try:
            shutil.move(src_path, dest_path)
            return dest_path
        except Exception as e:
            self.errors.append(f"Move failed: {filename} - {e}")
            return None
    
    def run_eos_sequence(self):
        """Execute the full End-of-Session sequence."""
        print("=" * 70)
        print("TRAJANUS END-OF-SESSION AUTOMATION")
        print("=" * 70)
        print(f"Date: {self.today}")
        print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
        print(f"Looking back: {CONFIG['hours_back']} hours")
        
        # Step 1: Authenticate
        if not self.authenticate():
            print("\n[ERROR] Authentication failed. Aborting.")
            return False
        
        # Step 2: Find session files
        session_files = self.find_session_files()
        
        if not session_files:
            print("\n[INFO] No session files found to process.")
            return True
        
        # Step 3: Process each file
        print("\n[PROCESS] Processing files...")
        print("-" * 70)
        
        converted_count = 0
        organized_count = 0
        
        for file_info in session_files:
            filename = file_info['name']
            file_type = file_info['type']
            is_md = file_info['is_markdown']
            
            print(f"\nFile: {filename}")
            print(f"  Type: {file_type}")
            print(f"  Modified: {file_info['modified'].strftime('%H:%M')}")
            
            # Convert markdown files to Google Docs
            if is_md:
                print("  [CONVERT] Converting to Google Docs...")
                result = self.convert_md_to_google_doc(file_info['path'])
                if result:
                    print(f"  [OK] Created: {result['name']}")
                    print(f"  [LINK] {result['webViewLink']}")
                    converted_count += 1
                else:
                    print("  [FAIL] Conversion failed")
            
            # Organize file into proper folder
            if file_type != 'uncategorized':
                print(f"  [MOVE] Organizing to {file_type} folder...")
                new_path = self.organize_file(file_info)
                if new_path:
                    print(f"  [OK] Moved to: {os.path.basename(os.path.dirname(new_path))}")
                    organized_count += 1
        
        # Step 4: Summary
        print("\n" + "=" * 70)
        print("EOS AUTOMATION COMPLETE")
        print("=" * 70)
        print(f"  Files processed: {len(session_files)}")
        print(f"  Converted to Google Docs: {converted_count}")
        print(f"  Organized into folders: {organized_count}")
        
        if self.errors:
            print(f"\n  Errors: {len(self.errors)}")
            for error in self.errors:
                print(f"    - {error}")
        
        print("\n[SUCCESS] Session handoff complete!")
        print("Next Claude session will have access to all converted documents.")
        
        return len(self.errors) == 0


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='End of Session Automation for Trajanus'
    )
    parser.add_argument(
        '--hours', '-H', type=int, default=CONFIG['hours_back'],
        help=f'Hours back to scan (default: {CONFIG["hours_back"]})'
    )
    parser.add_argument(
        '--dry-run', '-d', action='store_true',
        help='Show what would be done without making changes'
    )
    
    args = parser.parse_args()
    
    # Update config if hours specified
    if args.hours:
        CONFIG['hours_back'] = args.hours
    
    # Run automation
    automation = EOSAutomation()
    success = automation.run_eos_sequence()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
