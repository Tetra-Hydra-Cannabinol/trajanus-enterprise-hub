"""
Create 13-Knowledge-Base Structure
Uses existing google_drive_manager.py that already works
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google_drive_manager import GoogleDriveManager

print("\n" + "="*60)
print("CREATING TRAJANUS KNOWLEDGE BASE")
print("="*60 + "\n")

# Initialize (uses your existing working auth)
print("Connecting to Google Drive...")
drive = GoogleDriveManager(
    credentials_path='../credentials/credentials.json',
    token_path='../credentials/token.json'
)
print("✓ Connected\n")

# Find Trajanus USA folder
print("Finding '00 - Trajanus USA'...")
trajanus_id = drive.find_folder_by_path("00 - Trajanus USA")
if not trajanus_id:
    print("❌ Folder not found")
    exit(1)
print("✓ Found\n")

# Create main folder
print("Creating 13-Knowledge-Base...")
kb_id = drive.create_folder("13-Knowledge-Base", trajanus_id)
print("✓ Created\n")

# Structure
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

print("Creating folders...")
for name, subs in folders.items():
    parent_id = drive.create_folder(name, kb_id)
    print(f"  ✓ {name}")
    for sub in subs:
        drive.create_folder(sub, parent_id)
        print(f"    ✓ {name}/{sub}")

print("\n" + "="*60)
print("✅ DONE!")
print("="*60)
print("\nRefresh File Explorer to see: 13-Knowledge-Base\n")
