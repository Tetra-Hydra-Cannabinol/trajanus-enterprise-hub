"""
Audit 00 - Trajanus USA folder structure
Identify duplicates and numbering issues
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from google_drive_manager import GoogleDriveManager

print("\n" + "="*60)
print("AUDITING TRAJANUS USA FOLDER STRUCTURE")
print("="*60 + "\n")

# Connect
drive = GoogleDriveManager(
    credentials_path='../credentials/credentials.json',
    token_path='../credentials/token.json'
)

# Find Trajanus USA
trajanus_id = drive.find_folder_by_path("00 - Trajanus USA")

# List all folders
print("Current folder structure:\n")
folders = drive.service.files().list(
    q=f"'{trajanus_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
    fields="files(id, name)",
    orderBy="name"
).execute()

items = folders.get('files', [])

# Parse and display
numbered = {}
for item in items:
    name = item['name']
    folder_id = item['id']
    
    # Extract number
    if name[:2].isdigit():
        num = int(name[:2])
        if num not in numbered:
            numbered[num] = []
        numbered[num].append({'name': name, 'id': folder_id})

# Show structure
for num in sorted(numbered.keys()):
    folders = numbered[num]
    if len(folders) > 1:
        print(f"❌ DUPLICATE {num:02d}:")
        for f in folders:
            print(f"   - {f['name']}")
    else:
        print(f"✓  {folders[0]['name']}")

print("\n" + "="*60)
print("ISSUES IDENTIFIED:")
print("="*60)

# Find duplicates
dupes = [num for num, folders in numbered.items() if len(folders) > 1]
if dupes:
    print(f"\nDuplicate numbers: {', '.join([f'{d:02d}' for d in dupes])}")
else:
    print("\n✓ No duplicate numbers")

# Find gaps
all_nums = sorted(numbered.keys())
if all_nums:
    expected = list(range(all_nums[0], all_nums[-1] + 1))
    gaps = [n for n in expected if n not in all_nums]
    if gaps:
        print(f"Missing numbers: {', '.join([f'{g:02d}' for g in gaps])}")
    else:
        print("✓ No gaps in numbering")

print("\nTotal folders: " + str(len(items)))
print()
