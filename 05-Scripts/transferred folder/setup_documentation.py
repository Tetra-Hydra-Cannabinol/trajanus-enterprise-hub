"""
COMMAND CENTER DOCUMENTATION SETUP
Automatically organizes all documentation files into proper folder structure
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# Base paths
COMMAND_CENTER = Path(r"G:\My Drive\00 - Trajanus USA\00-Command-Center")
DOWNLOADS = Path(r"G:\My Drive\00 - Trajanus USA\00-Command-Center")  # Where files download

# Folder structure
FOLDERS = {
    "01-Core-Protocols": COMMAND_CENTER / "01-Core-Protocols",
    "02-Templates": COMMAND_CENTER / "02-Templates",
    "03-Session-Files": COMMAND_CENTER / "03-Session-Files",
    "04-Documentation": COMMAND_CENTER / "04-Documentation",
    "05-Scripts": COMMAND_CENTER / "05-Scripts",
    "06-Archive": COMMAND_CENTER / "06-Archive"
}

# File routing rules
FILE_ROUTES = {
    "04-Documentation": [
        "DEVELOPMENT_WORKFLOW.md",
        "ADDING_UTILITY_BUTTONS.md",
        "DEVELOPER_UTILITIES_CONFIG.md",
        "DEVELOPER_UTILITIES_QUICK_REF.md",
        "CODING_EDUCATION_GUIDE.md",
        "CODING_CHEAT_SHEET.md",
        "LEARNING_TRAINING_SUMMARY.md"
    ],
    "05-Scripts": [
        "get_user_guide_urls.py"
    ]
}

def create_folder_structure():
    """Create all required folders if they don't exist"""
    print("\n" + "="*60)
    print("CREATING FOLDER STRUCTURE")
    print("="*60)
    
    for folder_name, folder_path in FOLDERS.items():
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created: {folder_name}")
        else:
            print(f"  Exists: {folder_name}")

def organize_files():
    """Move files to their proper locations"""
    print("\n" + "="*60)
    print("ORGANIZING FILES")
    print("="*60)
    
    moved_count = 0
    
    for destination_folder, filenames in FILE_ROUTES.items():
        dest_path = FOLDERS[destination_folder]
        
        for filename in filenames:
            # Check common source locations
            source_locations = [
                DOWNLOADS / filename,
                COMMAND_CENTER / filename,
                Path.cwd() / filename
            ]
            
            for source in source_locations:
                if source.exists():
                    dest_file = dest_path / filename
                    
                    # Backup if file exists
                    if dest_file.exists():
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        backup = dest_path / f"{filename}.{timestamp}.bak"
                        shutil.copy2(dest_file, backup)
                        print(f"  Backed up: {filename}")
                    
                    # Move file
                    shutil.copy2(source, dest_file)
                    print(f"✓ Moved: {filename} → {destination_folder}")
                    moved_count += 1
                    break
            else:
                print(f"✗ Not found: {filename}")
    
    print(f"\nMoved {moved_count} files")

def create_readme():
    """Create README in Documentation folder"""
    readme_path = FOLDERS["04-Documentation"] / "README.md"
    
    content = """# COMMAND CENTER DOCUMENTATION

## Reference Guides

### Development
- **DEVELOPMENT_WORKFLOW.md** - How to build features (the proven process)
- **ADDING_UTILITY_BUTTONS.md** - How to add new utility buttons

### Configuration
- **DEVELOPER_UTILITIES_CONFIG.md** - Setup instructions for utilities
- **DEVELOPER_UTILITIES_QUICK_REF.md** - Visual quick reference

### Learning Resources
- **CODING_EDUCATION_GUIDE.md** - 12-week learning roadmap
- **CODING_CHEAT_SHEET.md** - Printable syntax reference
- **LEARNING_TRAINING_SUMMARY.md** - Implementation details

## Usage

These are reference documents for development and learning.

- **For Development:** Read DEVELOPMENT_WORKFLOW.md first
- **For Learning:** Start with CODING_EDUCATION_GUIDE.md
- **For Quick Reference:** Use CODING_CHEAT_SHEET.md

All documents are in Markdown format. Open with VS Code or any text editor.
"""
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✓ Created README in Documentation folder")

def verify_structure():
    """Verify all folders and files are in place"""
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    # Check folders
    print("\nFolders:")
    for folder_name, folder_path in FOLDERS.items():
        status = "✓" if folder_path.exists() else "✗"
        print(f"{status} {folder_name}")
    
    # Check files
    print("\nDocumentation Files:")
    doc_folder = FOLDERS["04-Documentation"]
    for filename in FILE_ROUTES["04-Documentation"]:
        file_path = doc_folder / filename
        status = "✓" if file_path.exists() else "✗"
        print(f"{status} {filename}")
    
    print("\nScript Files:")
    script_folder = FOLDERS["05-Scripts"]
    for filename in FILE_ROUTES["05-Scripts"]:
        file_path = script_folder / filename
        status = "✓" if file_path.exists() else "✗"
        print(f"{status} {filename}")

def main():
    """Run complete setup"""
    print("\n" + "="*60)
    print("COMMAND CENTER DOCUMENTATION SETUP")
    print("="*60)
    print(f"Base Path: {COMMAND_CENTER}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Step 1: Create folders
        create_folder_structure()
        
        # Step 2: Organize files
        organize_files()
        
        # Step 3: Create README
        create_readme()
        
        # Step 4: Verify
        verify_structure()
        
        print("\n" + "="*60)
        print("✓ SETUP COMPLETE")
        print("="*60)
        print("\nNext steps:")
        print("1. Verify files are in correct folders")
        print("2. Test the Command Center app")
        print("3. Demo to Tom")
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        raise

if __name__ == "__main__":
    main()
