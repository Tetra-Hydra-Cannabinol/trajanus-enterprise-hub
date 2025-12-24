#!/usr/bin/env python3
"""
EOS File Parser and Distributor - Trajanus USA
Automatically extracts ZIP, creates folders, and distributes EOS files to appropriate locations

Usage: 
    python parse_eos_files.py           # Interactive mode
    python parse_eos_files.py --auto    # Automatic mode (no prompts, uses COPY)
"""

import os
import shutil
import zipfile
import sys
from datetime import datetime
from pathlib import Path

# Source directory - where EOS files are downloaded
SOURCE_DIR = r'G:\My Drive\00 - Trajanus USA\08-EOS-Files'

# Root directory for Trajanus USA
ROOT_DIR = r'G:\My Drive\00 - Trajanus USA'

# Folder mapping - where each file type should go
FOLDER_MAPPING = {
    'Technical_Journal': '07-Session-Journal/Technical-Journals',
    'Personal_Diary': '07-Session-Journal/Personal-Diaries',
    'Operational_Journal': '07-Session-Journal/Operational-Journals',
    'Trajanus_Project_Diary': '07-Session-Journal/Project-Diaries',
    'Session_Summary': '07-Session-Journal/Session-Summaries',
    'Code_Repository': '07-Session-Journal/Code-Repositories',
    'Next_Session_Handoff': '07-Session-Journal/Session-Handoffs',
}

# Files to keep in 08-EOS-Files (don't move)
KEEP_IN_EOS = [
    'EOS_DOWNLOAD_CHECKLIST',
    'EOS_CONVERSION_PROTOCOL',
    'FILE_CONVERSION_OPTIONS_GUIDE',
    'TRAJANUS_FILE_STRUCTURE_MAP'
]


def find_and_extract_zip():
    """Find today's ZIP file and extract it"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    print("\n" + "="*80)
    print("SEARCHING FOR ZIP FILE")
    print("="*80 + "\n")
    
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ ERROR: Source directory not found: {SOURCE_DIR}")
        return False
    
    # Find ZIP file
    zip_file = None
    for filename in os.listdir(SOURCE_DIR):
        if filename.endswith('.zip') and today in filename:
            zip_file = os.path.join(SOURCE_DIR, filename)
            print(f"✓ Found ZIP: {filename}")
            break
    
    if not zip_file:
        print(f"⚠ No ZIP file found for {today}")
        print("Looking for loose files instead...\n")
        return False
    
    # Extract ZIP
    try:
        print(f"\nExtracting to: {SOURCE_DIR}")
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            # List contents
            file_list = zip_ref.namelist()
            print(f"\nContents ({len(file_list)} files):")
            for f in file_list[:10]:  # Show first 10
                print(f"  - {f}")
            if len(file_list) > 10:
                print(f"  ... and {len(file_list) - 10} more")
            
            # Extract all
            zip_ref.extractall(SOURCE_DIR)
            print(f"\n✓ Extracted {len(file_list)} files successfully")
        
        # Optional: Move ZIP to archive subfolder
        archive_dir = os.path.join(SOURCE_DIR, 'archives')
        if not os.path.exists(archive_dir):
            os.makedirs(archive_dir)
        
        archive_path = os.path.join(archive_dir, os.path.basename(zip_file))
        shutil.move(zip_file, archive_path)
        print(f"✓ Archived ZIP to: archives/{os.path.basename(zip_file)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error extracting ZIP: {e}")
        return False


def create_folders():
    """Create all necessary folders if they don't exist"""
    print("\n" + "="*80)
    print("CREATING FOLDER STRUCTURE")
    print("="*80 + "\n")
    
    created = []
    for folder_path in FOLDER_MAPPING.values():
        full_path = os.path.join(ROOT_DIR, folder_path)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
            created.append(folder_path)
            print(f"✓ Created: {folder_path}")
        else:
            print(f"  Exists: {folder_path}")
    
    if created:
        print(f"\n✓ Created {len(created)} new folders")
    else:
        print("\n✓ All folders already exist")
    
    return len(created)


def find_todays_files():
    """Find all files from today in the EOS folder"""
    today = datetime.now().strftime('%Y-%m-%d')
    found_files = []
    
    print("\n" + "="*80)
    print(f"SCANNING FOR FILES: {today}")
    print("="*80 + "\n")
    
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ ERROR: Source directory not found: {SOURCE_DIR}")
        return found_files
    
    print(f"Scanning: {SOURCE_DIR}\n")
    
    for filename in os.listdir(SOURCE_DIR):
        # Skip if not from today
        if today not in filename:
            continue
        
        # Skip if it's a reference document (should stay in EOS)
        if any(keep in filename for keep in KEEP_IN_EOS):
            print(f"⊗ Keeping in EOS: {filename}")
            continue
        
        # Only process markdown files
        if not (filename.endswith('.md') or filename.endswith('.txt')):
            continue
        
        # Determine file type
        file_type = None
        for pattern in FOLDER_MAPPING.keys():
            if pattern in filename:
                file_type = pattern
                break
        
        if file_type:
            found_files.append({
                'filename': filename,
                'type': file_type,
                'source_path': os.path.join(SOURCE_DIR, filename),
                'dest_folder': FOLDER_MAPPING[file_type]
            })
            print(f"✓ Found {file_type}: {filename}")
        else:
            print(f"⚠ Unknown type: {filename}")
    
    print(f"\n✓ Found {len(found_files)} files to distribute")
    return found_files


def distribute_files(files, move=False):
    """
    Distribute files to their appropriate folders
    
    Args:
        files: List of file dictionaries
        move: If True, move files. If False, copy files (safer)
    """
    print("\n" + "="*80)
    print(f"DISTRIBUTING FILES ({'MOVE' if move else 'COPY'} mode)")
    print("="*80 + "\n")
    
    success_count = 0
    error_count = 0
    
    for file_info in files:
        try:
            dest_folder = os.path.join(ROOT_DIR, file_info['dest_folder'])
            dest_path = os.path.join(dest_folder, file_info['filename'])
            
            print(f"Processing: {file_info['filename']}")
            print(f"  → {file_info['dest_folder']}")
            
            # Check if destination already exists
            if os.path.exists(dest_path):
                print(f"  ⚠ File already exists at destination")
                # Create backup
                backup_path = dest_path + '.backup'
                shutil.copy2(dest_path, backup_path)
                print(f"  ✓ Created backup: {os.path.basename(backup_path)}")
            
            # Copy or move file
            if move:
                shutil.move(file_info['source_path'], dest_path)
                print(f"  ✓ Moved successfully")
            else:
                shutil.copy2(file_info['source_path'], dest_path)
                print(f"  ✓ Copied successfully")
            
            success_count += 1
            print()
            
        except Exception as e:
            print(f"  ❌ Error: {e}\n")
            error_count += 1
    
    return success_count, error_count


def main():
    """Main execution function"""
    # Check for automatic mode
    auto_mode = '--auto' in sys.argv
    
    print("\n" + "="*80)
    print("EOS FILE PARSER & DISTRIBUTOR - Trajanus USA")
    if auto_mode:
        print("(AUTOMATIC MODE)")
    print("="*80)
    
    # Step 1: Find and extract ZIP file
    zip_extracted = find_and_extract_zip()
    
    # Step 2: Create folder structure
    folders_created = create_folders()
    
    # Step 3: Find today's files
    files = find_todays_files()
    
    if not files:
        print("\n⚠ No files to process. Exiting.")
        return
    
    # Step 4: Determine distribution mode
    if auto_mode:
        # Automatic mode: Always use COPY
        move_files = False
        print("\n✓ Using COPY mode (automatic)")
    else:
        # Interactive mode: Ask user
        print("\n" + "="*80)
        print("DISTRIBUTION OPTIONS")
        print("="*80)
        print("\n1. COPY files (keeps originals in 08-EOS-Files) - RECOMMENDED")
        print("2. MOVE files (removes from 08-EOS-Files)")
        print("\nWhat would you like to do? [1/2]: ", end='')
        
        choice = input().strip()
        move_files = (choice == '2')
        
        if move_files:
            print("\n⚠ WARNING: This will MOVE files (remove from 08-EOS-Files)")
            print("Are you sure? [y/N]: ", end='')
            confirm = input().strip().lower()
            if confirm != 'y':
                print("\n✓ Cancelled. Using COPY mode instead.")
                move_files = False
    
    # Step 5: Distribute files
    success, errors = distribute_files(files, move=move_files)
    
    # Step 6: Summary
    print("=" * 80)
    print("DISTRIBUTION COMPLETE")
    print("=" * 80)
    print(f"\n✓ Files processed: {success}/{len(files)}")
    if errors > 0:
        print(f"❌ Errors: {errors}")
    if folders_created > 0:
        print(f"✓ Folders created: {folders_created}")
    
    print("\n" + "="*80)
    print("FILES ARE NOW ORGANIZED BY TYPE")
    print("="*80)
    print("\nFolder structure:")
    for file_type, folder in FOLDER_MAPPING.items():
        print(f"  {file_type} → {folder}")
    
    if zip_extracted:
        print("\n✓ ZIP file extracted and archived")
    print("✓ Session files organized and ready for conversion")
    print("\nNext step: Run CONVERT_ALL_FILES.ps1 to convert to Google Docs\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✓ Operation cancelled by user")
    except Exception as e:
        print(f"\n\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
