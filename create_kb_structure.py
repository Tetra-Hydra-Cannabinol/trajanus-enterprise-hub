"""
Create 13-Knowledge-Base Folder Structure
Uses Google Drive API to properly create folders
Author: Claude
Date: December 9, 2025
"""

import os
import sys

# Add parent directory to path to import google_drive_manager
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google_drive_manager import GoogleDriveManager

def create_knowledge_base_structure():
    """Create complete 13-Knowledge-Base folder structure in Google Drive"""
    
    print("\n" + "="*60)
    print("CREATING TRAJANUS KNOWLEDGE BASE FOLDER STRUCTURE")
    print("="*60 + "\n")
    
    # Initialize Drive Manager
    print("Authenticating with Google Drive...")
    drive = GoogleDriveManager()
    print("✓ Authenticated\n")
    
    # Find the "00 - Trajanus USA" folder
    print("Finding '00 - Trajanus USA' folder...")
    trajanus_folder_id = drive.find_folder_by_path("00 - Trajanus USA")
    if not trajanus_folder_id:
        print("❌ ERROR: Could not find '00 - Trajanus USA' folder")
        return False
    print(f"✓ Found folder (ID: {trajanus_folder_id})\n")
    
    # Create main Knowledge Base folder
    print("Creating main folder...")
    kb_folder_id = drive.create_folder("13-Knowledge-Base", parent_folder_id=trajanus_folder_id)
    if not kb_folder_id:
        print("❌ ERROR: Could not create 13-Knowledge-Base folder")
        return False
    print("✓ Created: 13-Knowledge-Base\n")
    
    # Define folder structure
    folders = {
        "01-Building-Codes": ["NFPA-70", "IBC-2021", "UFC"],
        "02-USACE-Standards": ["Engineer-Regulations", "Engineer-Pamphlets"],
        "03-Project-History": ["2024-Q4", "2025-Q1"],
        "04-Technical-Decisions": ["Architecture", "Rejected-Approaches", "Design-Patterns"],
        "05-Code-Repository": ["Working-Examples", "Failed-Attempts"],
        "06-Protocols-Preferences": [],
        "07-Training-Materials": [],
        "08-Software-Documentation": ["Procore", "Primavera-P6", "RMS-3.0"],
        "09-Product-Data": ["Electrical", "Structural", "Mechanical"]
    }
    
    # Create all folders
    print("Creating subfolders...")
    for parent_name, subfolders in folders.items():
        # Create parent folder
        parent_id = drive.create_folder(parent_name, parent_folder_id=kb_folder_id)
        if parent_id:
            print(f"  ✓ {parent_name}")
            
            # Create subfolders
            for subfolder_name in subfolders:
                subfolder_id = drive.create_folder(subfolder_name, parent_folder_id=parent_id)
                if subfolder_id:
                    print(f"    ✓ {parent_name}/{subfolder_name}")
                else:
                    print(f"    ❌ Failed: {parent_name}/{subfolder_name}")
        else:
            print(f"  ❌ Failed: {parent_name}")
    
    print("\n" + "="*60)
    print("✅ FOLDER STRUCTURE CREATED SUCCESSFULLY!")
    print("="*60)
    print("\nLocation: G:\\My Drive\\00 - Trajanus USA\\13-Knowledge-Base\\")
    print("\nRefresh Google Drive in File Explorer to see folders.")
    print("\n")
    
    return True

if __name__ == "__main__":
    try:
        success = create_knowledge_base_structure()
        if success:
            print("✓ Done. Ready for next step (Supabase setup).")
        else:
            print("❌ Failed. Check error messages above.")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
