#!/usr/bin/env python3
"""
Google Drive Cleanup & Organization Agent
==========================================

Purpose: Safely audit, organize, and clean up Google Drive files
Author: Claude & Bill King
Date: December 11, 2025

Features:
- Detect and report duplicates (by name, by content hash)
- Identify files needing conversion to Google Docs
- Validate folder organization
- Detect misplaced files
- Generate comprehensive reports
- Safe mode: NO DELETIONS without approval

Usage:
    python gdrive_cleanup_agent.py --mode scan
    python gdrive_cleanup_agent.py --mode report
    python gdrive_cleanup_agent.py --mode execute --dry-run
"""

import os
import json
import hashlib
from datetime import datetime
from collections import defaultdict
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
import io

SCOPES = ['https://www.googleapis.com/auth/drive']

# Expected folder structure (from your File Structure Map)
EXPECTED_FOLDERS = {
    '00-Command-Center': 'System administration and sensitive credentials',
    '01-Core-Protocols': 'Fundamental operational procedures',
    '02-Memory-System': 'User profiles and persistent knowledge',
    '03-Living-Documents': 'Active project documentation',
    '04-Technical-Specs': 'Technical documentation and specifications',
    '05-Scripts': 'Automation and utility scripts',
    '06-User-Guides': 'Documentation and guides',
    '07-Session-Journal': 'Session summaries and handoffs',
    '08-EOS-Files': 'End of session files',
    '09-Archive': 'Historical and backup files',
    '10-Projects': 'Active project files',
    '11-Resources': 'Reference materials and resources',
    '12-Credentials': 'API keys and authentication files'
}

# File types that should be converted to Google Docs
CONVERTIBLE_TYPES = {
    '.md': 'Google Docs',
    '.txt': 'Google Docs',
    '.docx': 'Google Docs',
    '.doc': 'Google Docs',
    '.xlsx': 'Google Sheets',
    '.xls': 'Google Sheets',
    '.pptx': 'Google Slides',
    '.ppt': 'Google Slides'
}

class DriveCleanupAgent:
    def __init__(self, base_folder_name='00 - Trajanus USA'):
        """Initialize the cleanup agent."""
        self.base_folder_name = base_folder_name
        self.service = None
        self.base_folder_id = None
        self.scan_results = {
            'duplicates': [],
            'needs_conversion': [],
            'misplaced_files': [],
            'folder_inventory': {},
            'statistics': {},
            'scan_date': datetime.now().isoformat()
        }
        
        self.authenticate()
        self.find_base_folder()
    
    def authenticate(self):
        """Authenticate with Google Drive API."""
        creds = None
        token_path = 'credentials/token.json'
        creds_path = 'credentials/credentials.json'
        
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
        
        self.service = build('drive', 'v3', credentials=creds)
        print(f"✅ Authenticated with Google Drive")
    
    def find_base_folder(self):
        """Find the base Trajanus USA folder."""
        try:
            query = f"name='{self.base_folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = self.service.files().list(
                q=query,
                fields="files(id, name)"
            ).execute()
            
            files = results.get('files', [])
            if files:
                self.base_folder_id = files[0]['id']
                print(f"✅ Found base folder: {self.base_folder_name} (ID: {self.base_folder_id})")
            else:
                print(f"❌ Could not find folder: {self.base_folder_name}")
                
        except HttpError as error:
            print(f"❌ Error finding base folder: {error}")
    
    def get_all_files(self, folder_id=None, path=""):
        """Recursively get all files from a folder."""
        if folder_id is None:
            folder_id = self.base_folder_id
        
        all_files = []
        page_token = None
        
        while True:
            try:
                query = f"'{folder_id}' in parents and trashed=false"
                results = self.service.files().list(
                    q=query,
                    pageSize=1000,
                    pageToken=page_token,
                    fields="nextPageToken, files(id, name, mimeType, size, createdTime, modifiedTime, md5Checksum, parents)"
                ).execute()
                
                items = results.get('files', [])
                
                for item in items:
                    item['path'] = path
                    all_files.append(item)
                    
                    # If it's a folder, recurse
                    if item['mimeType'] == 'application/vnd.google-apps.folder':
                        subfolder_path = f"{path}/{item['name']}" if path else item['name']
                        all_files.extend(self.get_all_files(item['id'], subfolder_path))
                
                page_token = results.get('nextPageToken')
                if not page_token:
                    break
                    
            except HttpError as error:
                print(f"❌ Error listing files: {error}")
                break
        
        return all_files
    
    def detect_duplicates(self, files):
        """Detect duplicate files by name and by content hash."""
        print("\n🔍 Detecting duplicates...")
        
        # Duplicates by name
        by_name = defaultdict(list)
        for f in files:
            if f['mimeType'] != 'application/vnd.google-apps.folder':
                by_name[f['name']].append(f)
        
        name_duplicates = {name: files for name, files in by_name.items() if len(files) > 1}
        
        # Duplicates by content (MD5 hash)
        by_hash = defaultdict(list)
        for f in files:
            if 'md5Checksum' in f and f['mimeType'] != 'application/vnd.google-apps.folder':
                by_hash[f['md5Checksum']].append(f)
        
        hash_duplicates = {hash_val: files for hash_val, files in by_hash.items() if len(files) > 1}
        
        # Store results
        self.scan_results['duplicates'] = {
            'by_name': [
                {
                    'name': name,
                    'count': len(files),
                    'locations': [f"{f['path']}/{f['name']}" for f in files],
                    'file_ids': [f['id'] for f in files]
                }
                for name, files in name_duplicates.items()
            ],
            'by_content': [
                {
                    'hash': hash_val[:16] + '...',
                    'count': len(files),
                    'files': [
                        {
                            'name': f['name'],
                            'location': f"{f['path']}/{f['name']}",
                            'id': f['id'],
                            'size': f.get('size', 'N/A')
                        }
                        for f in files
                    ]
                }
                for hash_val, files in hash_duplicates.items()
            ]
        }
        
        print(f"   📊 Found {len(name_duplicates)} sets of name duplicates")
        print(f"   📊 Found {len(hash_duplicates)} sets of content duplicates")
        
        return self.scan_results['duplicates']
    
    def detect_needs_conversion(self, files):
        """Detect files that should be converted to Google Docs format."""
        print("\n🔍 Detecting files needing conversion...")
        
        needs_conversion = []
        
        for f in files:
            if f['mimeType'] == 'application/vnd.google-apps.folder':
                continue
            
            file_ext = Path(f['name']).suffix.lower()
            
            # Check if it's a convertible type AND not already a Google Doc
            if file_ext in CONVERTIBLE_TYPES and not f['mimeType'].startswith('application/vnd.google-apps'):
                needs_conversion.append({
                    'name': f['name'],
                    'extension': file_ext,
                    'current_type': f['mimeType'],
                    'target_type': CONVERTIBLE_TYPES[file_ext],
                    'location': f"{f['path']}/{f['name']}",
                    'id': f['id'],
                    'size': f.get('size', 'N/A')
                })
        
        self.scan_results['needs_conversion'] = needs_conversion
        
        print(f"   📊 Found {len(needs_conversion)} files needing conversion")
        
        return needs_conversion
    
    def validate_folder_organization(self, files):
        """Check if files are in the correct folders."""
        print("\n🔍 Validating folder organization...")
        
        misplaced = []
        
        # Get all folders
        folders = [f for f in files if f['mimeType'] == 'application/vnd.google-apps.folder']
        folder_names = {f['name']: f for f in folders}
        
        # Check if expected folders exist
        missing_folders = []
        for expected_name in EXPECTED_FOLDERS:
            if expected_name not in folder_names:
                missing_folders.append({
                    'name': expected_name,
                    'description': EXPECTED_FOLDERS[expected_name]
                })
        
        # Analyze file locations (simplified heuristics)
        for f in files:
            if f['mimeType'] == 'application/vnd.google-apps.folder':
                continue
            
            file_name = f['name'].lower()
            current_path = f['path']
            
            # Check for common patterns
            suggestions = []
            
            # Session files
            if 'session' in file_name and '07-Session-Journal' not in current_path:
                suggestions.append('07-Session-Journal')
            
            # Protocol files
            if 'protocol' in file_name and '01-Core-Protocols' not in current_path:
                suggestions.append('01-Core-Protocols')
            
            # Script files
            if file_name.endswith('.py') and '05-Scripts' not in current_path:
                suggestions.append('05-Scripts')
            
            # EOS files
            if 'eos' in file_name and '08-EOS-Files' not in current_path:
                suggestions.append('08-EOS-Files')
            
            # User guide files
            if 'guide' in file_name or 'user' in file_name and '06-User-Guides' not in current_path:
                suggestions.append('06-User-Guides')
            
            if suggestions:
                misplaced.append({
                    'file': f['name'],
                    'current_location': current_path,
                    'suggested_locations': suggestions,
                    'id': f['id']
                })
        
        self.scan_results['misplaced_files'] = misplaced
        self.scan_results['missing_folders'] = missing_folders
        
        print(f"   📊 Found {len(misplaced)} potentially misplaced files")
        print(f"   📊 Found {len(missing_folders)} missing expected folders")
        
        return misplaced
    
    def generate_folder_inventory(self, files):
        """Generate complete inventory of all folders."""
        print("\n🔍 Generating folder inventory...")
        
        inventory = {}
        
        # Group files by folder path
        by_folder = defaultdict(lambda: {'files': [], 'subfolders': [], 'stats': {}})
        
        for f in files:
            path = f['path'] if f['path'] else 'ROOT'
            
            if f['mimeType'] == 'application/vnd.google-apps.folder':
                parent_path = '/'.join(path.split('/')[:-1]) if '/' in path else 'ROOT'
                by_folder[parent_path]['subfolders'].append({
                    'name': f['name'],
                    'id': f['id']
                })
            else:
                by_folder[path]['files'].append({
                    'name': f['name'],
                    'type': f['mimeType'],
                    'size': f.get('size', 'N/A'),
                    'modified': f.get('modifiedTime', 'Unknown')
                })
        
        # Calculate statistics
        for path, data in by_folder.items():
            total_files = len(data['files'])
            total_subfolders = len(data['subfolders'])
            
            # Count file types
            type_counts = defaultdict(int)
            for file in data['files']:
                ext = Path(file['name']).suffix.lower() if '.' in file['name'] else 'no_extension'
                type_counts[ext] += 1
            
            data['stats'] = {
                'total_files': total_files,
                'total_subfolders': total_subfolders,
                'file_types': dict(type_counts)
            }
        
        self.scan_results['folder_inventory'] = dict(by_folder)
        
        print(f"   📊 Inventoried {len(by_folder)} folders")
        
        return inventory
    
    def calculate_statistics(self, files):
        """Calculate overall statistics."""
        print("\n📊 Calculating statistics...")
        
        stats = {
            'total_files': 0,
            'total_folders': 0,
            'total_size_bytes': 0,
            'file_types': defaultdict(int),
            'google_docs_count': 0,
            'needs_conversion_count': 0,
            'duplicate_files_count': 0
        }
        
        for f in files:
            if f['mimeType'] == 'application/vnd.google-apps.folder':
                stats['total_folders'] += 1
            else:
                stats['total_files'] += 1
                if 'size' in f:
                    stats['total_size_bytes'] += int(f['size'])
                
                ext = Path(f['name']).suffix.lower()
                stats['file_types'][ext] += 1
                
                if f['mimeType'].startswith('application/vnd.google-apps'):
                    stats['google_docs_count'] += 1
        
        stats['needs_conversion_count'] = len(self.scan_results['needs_conversion'])
        stats['duplicate_files_count'] = sum(d['count'] for d in self.scan_results['duplicates']['by_name'])
        stats['total_size_mb'] = round(stats['total_size_bytes'] / (1024 * 1024), 2)
        stats['file_types'] = dict(stats['file_types'])
        
        self.scan_results['statistics'] = stats
        
        print(f"   Total files: {stats['total_files']}")
        print(f"   Total folders: {stats['total_folders']}")
        print(f"   Total size: {stats['total_size_mb']} MB")
        print(f"   Google Docs: {stats['google_docs_count']}")
        print(f"   Need conversion: {stats['needs_conversion_count']}")
        print(f"   Duplicates: {stats['duplicate_files_count']}")
    
    def run_full_scan(self):
        """Run complete scan of Google Drive."""
        print("\n" + "="*70)
        print("  GOOGLE DRIVE CLEANUP AGENT - FULL SCAN")
        print("="*70)
        print(f"  Base folder: {self.base_folder_name}")
        print(f"  Scan started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        
        # Get all files
        print("\n📂 Scanning all files...")
        files = self.get_all_files()
        print(f"   Found {len(files)} total items")
        
        # Run all analyses
        self.detect_duplicates(files)
        self.detect_needs_conversion(files)
        self.validate_folder_organization(files)
        self.generate_folder_inventory(files)
        self.calculate_statistics(files)
        
        # Save results
        self.save_report()
        
        print("\n" + "="*70)
        print("  SCAN COMPLETE")
        print("="*70)
        print(f"\n📄 Report saved to: cleanup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        print(f"📄 Human-readable report: cleanup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        
        return self.scan_results
    
    def save_report(self):
        """Save scan results to file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # JSON report
        json_file = f"cleanup_report_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(self.scan_results, f, indent=2)
        
        # Human-readable report
        txt_file = f"cleanup_report_{timestamp}.txt"
        with open(txt_file, 'w') as f:
            f.write("="*70 + "\n")
            f.write("  GOOGLE DRIVE CLEANUP REPORT\n")
            f.write("="*70 + "\n")
            f.write(f"Scan Date: {self.scan_results['scan_date']}\n")
            f.write(f"Base Folder: {self.base_folder_name}\n\n")
            
            # Statistics
            f.write("STATISTICS\n")
            f.write("-"*70 + "\n")
            stats = self.scan_results['statistics']
            f.write(f"Total Files: {stats['total_files']}\n")
            f.write(f"Total Folders: {stats['total_folders']}\n")
            f.write(f"Total Size: {stats['total_size_mb']} MB\n")
            f.write(f"Google Docs: {stats['google_docs_count']}\n")
            f.write(f"Need Conversion: {stats['needs_conversion_count']}\n")
            f.write(f"Duplicates: {stats['duplicate_files_count']}\n\n")
            
            # Duplicates
            f.write("DUPLICATE FILES\n")
            f.write("-"*70 + "\n")
            for dup in self.scan_results['duplicates']['by_name']:
                f.write(f"\n📁 {dup['name']} ({dup['count']} copies)\n")
                for loc in dup['locations']:
                    f.write(f"   └─ {loc}\n")
            
            # Needs conversion
            f.write("\n\nFILES NEEDING CONVERSION\n")
            f.write("-"*70 + "\n")
            for item in self.scan_results['needs_conversion']:
                f.write(f"\n{item['name']} ({item['extension']})\n")
                f.write(f"   Location: {item['location']}\n")
                f.write(f"   Convert to: {item['target_type']}\n")
            
            # Misplaced files
            f.write("\n\nPOTENTIALLY MISPLACED FILES\n")
            f.write("-"*70 + "\n")
            for item in self.scan_results['misplaced_files']:
                f.write(f"\n{item['file']}\n")
                f.write(f"   Current: {item['current_location']}\n")
                f.write(f"   Suggested: {', '.join(item['suggested_locations'])}\n")
        
        print(f"\n✅ Reports saved: {json_file}, {txt_file}")

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Google Drive Cleanup Agent')
    parser.add_argument('--mode', choices=['scan', 'report', 'execute'], 
                       default='scan', help='Operation mode')
    parser.add_argument('--dry-run', action='store_true',
                       help='Dry run mode (no actual changes)')
    parser.add_argument('--base-folder', default='00 - Trajanus USA',
                       help='Base folder name to scan')
    
    args = parser.parse_args()
    
    agent = DriveCleanupAgent(base_folder_name=args.base_folder)
    
    if args.mode == 'scan':
        agent.run_full_scan()
    elif args.mode == 'report':
        # Load latest report and display
        print("Report mode not yet implemented")
    elif args.mode == 'execute':
        if args.dry_run:
            print("🔒 DRY RUN MODE - No changes will be made")
        print("Execute mode not yet implemented - use reports to review first")

if __name__ == '__main__':
    main()
