#!/usr/bin/env python3
"""
sync_protocols.py
Trajanus USA - Command Center Script

Syncs protocol documents between local folders and ensures
all protocol files are properly organized and up to date.

Author: Trajanus USA / Claude AI
Created: 2025-12-05
"""

import os
import shutil
from datetime import datetime
from pathlib import Path

# Configuration
TRAJANUS_ROOT = r'G:\My Drive\00 - Trajanus USA'
PROTOCOL_FOLDERS = {
    'core': os.path.join(TRAJANUS_ROOT, '01-Core-Protocols'),
    'eos': os.path.join(TRAJANUS_ROOT, '08-EOS-Files'),
    'command': os.path.join(TRAJANUS_ROOT, '00-Command-Center'),
}

# Protocol files to track
PROTOCOL_FILES = [
    'OPERATIONAL_PROTOCOL.md',
    'The_Commandments_of_AI.docx',
    'End_of_Session_Protocol.md',
    'Morning_Session_Startup.docx',
    'End_Of_Session_Closeout.docx',
    'Operational_Protocols.docx',
    'Bills_POV.md',
    '6_Category_System_Guide.docx',
    'File_Systems_User_Guide.docx',
]

def find_protocol_files():
    """Find all protocol files across folders."""
    found_files = {}
    
    for folder_name, folder_path in PROTOCOL_FOLDERS.items():
        if not os.path.exists(folder_path):
            print(f"  Warning: Folder not found - {folder_path}")
            continue
            
        for root, dirs, files in os.walk(folder_path):
            # Skip archive folders
            dirs[:] = [d for d in dirs if 'archive' not in d.lower()]
            
            for file in files:
                if file in PROTOCOL_FILES or 'protocol' in file.lower():
                    filepath = os.path.join(root, file)
                    mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                    
                    if file not in found_files:
                        found_files[file] = []
                    
                    found_files[file].append({
                        'path': filepath,
                        'folder': folder_name,
                        'modified': mtime
                    })
    
    return found_files

def check_sync_status(found_files):
    """Check if protocol files are in sync."""
    issues = []
    
    for filename, locations in found_files.items():
        if len(locations) > 1:
            # Multiple copies exist - check if they're in sync
            times = [loc['modified'] for loc in locations]
            if max(times) - min(times) > timedelta(minutes=5):
                issues.append({
                    'file': filename,
                    'type': 'out_of_sync',
                    'locations': locations
                })
        
        # Check if file should be in core protocols
        if filename in PROTOCOL_FILES:
            in_core = any(loc['folder'] == 'core' for loc in locations)
            if not in_core:
                issues.append({
                    'file': filename,
                    'type': 'missing_from_core',
                    'locations': locations
                })
    
    return issues

def sync_file_to_core(source_path, filename):
    """Copy file to Core Protocols folder."""
    dest_path = os.path.join(PROTOCOL_FOLDERS['core'], filename)
    
    # Backup if exists
    if os.path.exists(dest_path):
        backup_name = f"{os.path.splitext(filename)[0]}_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}{os.path.splitext(filename)[1]}"
        backup_path = os.path.join(PROTOCOL_FOLDERS['core'], 'Archive', backup_name)
        
        # Create archive folder if needed
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        shutil.copy2(dest_path, backup_path)
        print(f"    Backup created: {backup_name}")
    
    # Copy file
    shutil.copy2(source_path, dest_path)
    return dest_path

def main():
    """Main function."""
    print("=" * 60)
    print("Protocol Sync Tool")
    print("Trajanus USA - Command Center")
    print("=" * 60)
    print(f"\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Find all protocol files
    print("\nScanning for protocol files...")
    found_files = find_protocol_files()
    
    print(f"\nFound {len(found_files)} protocol files:")
    for filename, locations in found_files.items():
        print(f"\n  📄 {filename}")
        for loc in locations:
            print(f"     └─ {loc['folder']}: {loc['modified'].strftime('%Y-%m-%d %H:%M')}")
    
    # Check sync status
    print("\n" + "-" * 40)
    print("Checking sync status...")
    print("-" * 40)
    
    from datetime import timedelta
    issues = check_sync_status(found_files)
    
    if not issues:
        print("\n✓ All protocols are in sync!")
    else:
        print(f"\n⚠ Found {len(issues)} issues:")
        
        for issue in issues:
            print(f"\n  • {issue['file']}")
            print(f"    Issue: {issue['type'].replace('_', ' ').title()}")
            
            if issue['type'] == 'out_of_sync':
                # Find newest version
                newest = max(issue['locations'], key=lambda x: x['modified'])
                print(f"    Newest: {newest['folder']} ({newest['modified'].strftime('%H:%M')})")
                
                # Offer to sync
                response = input("    Sync to Core Protocols? (y/n): ").strip().lower()
                if response == 'y':
                    try:
                        dest = sync_file_to_core(newest['path'], issue['file'])
                        print(f"    ✓ Synced to: {dest}")
                    except Exception as e:
                        print(f"    ✗ Error: {str(e)}")
            
            elif issue['type'] == 'missing_from_core':
                # Find the file location
                source = issue['locations'][0]
                print(f"    Found in: {source['folder']}")
                
                response = input("    Copy to Core Protocols? (y/n): ").strip().lower()
                if response == 'y':
                    try:
                        dest = sync_file_to_core(source['path'], issue['file'])
                        print(f"    ✓ Copied to: {dest}")
                    except Exception as e:
                        print(f"    ✗ Error: {str(e)}")
    
    # Summary
    print("\n" + "=" * 40)
    print("Sync Complete")
    print("=" * 40)
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
