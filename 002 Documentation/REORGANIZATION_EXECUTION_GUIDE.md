# TRAJANUS DRIVE REORGANIZATION - EXECUTION GUIDE

**Script:** `reorganize_trajanus_drive.py`  
**Purpose:** Complete folder structure reorganization with Living Documents system  
**Created:** December 4, 2025

---

## WHAT THIS SCRIPT DOES

### Phase 1: Renames Folders
- `05-Scripts` → `04-Scripts`
- `PM-Toolbox` → `10-PM-Toolbox`
- `Personal` → `11-Personal`
- `Credentials` → `12-Credentials`

### Phase 2: Creates New Folders
- `03-Living-Documents/` (main folder)
- `05-Archives/` (consolidation folder)

### Phase 3: Creates Living Documents Structure
Creates 11 document type folders, each with Daily_Entries subfolder:

```
03-Living-Documents/
├── Operational_Journal_Daily_Entries/
├── Technical_Journal_Daily_Entries/
├── Personal_Diary_Daily_Entries/
├── Code_Repository_Daily_Entries/
├── Bills_POV_Updates_Daily_Entries/
├── Users_Guide_Daily_Entries/
├── Enterprise_Hub_Version_Log_Daily_Entries/
├── Website_Code_Versions_Daily_Entries/
├── Protocol_Violations_Daily_Entries/
├── Active_Commitments_Daily_Entries/
└── Master_File_Architecture_Daily_Entries/
```

### Phase 4: Creates Archive Structure
```
05-Archives/
├── AI-Projects/
├── FILE-RECOVERY-1109-1315/
└── Chat-Files/
```

---

## FINAL FOLDER STRUCTURE

```
00 - Trajanus USA/
├── 00-Command-Center/              [Existing]
├── 01-Core-Protocols/              [Existing]
├── 02-Templates/                   [Existing]
├── 03-Living-Documents/            [NEW - 11 types + 11 Daily_Entries folders]
├── 04-Scripts/                     [Renamed from 05-Scripts]
├── 05-Archives/                    [NEW - 3 subfolders]
├── 06-Project-State/               [Existing]
├── 07-Session-Journal/             [Existing]
├── 08-EOS-Files/                   [Existing]
├── 09-Active-Projects/             [Existing]
├── 10-PM-Toolbox/                  [Renamed from PM-Toolbox]
├── 11-Personal/                    [Renamed from Personal]
└── 12-Credentials/                 [Renamed from Credentials]
```

**Total folders created: 30+**
- 13 main folders (00-12)
- 11 Living Documents Daily_Entries folders
- 3 Archive subfolders
- Plus MASTER files (created later)

---

## HOW TO RUN

### Step 1: Copy Script to Command Center
```powershell
# Navigate to Command Center
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center"

# Download the script from Claude outputs
# (Copy reorganize_trajanus_drive.py to this folder)
```

### Step 2: Verify Credentials
```powershell
# Make sure these files exist:
dir credentials.json
dir token.json
```

### Step 3: Run the Script
```powershell
python reorganize_trajanus_drive.py
```

### Expected Output
```
============================================================
TRAJANUS DRIVE REORGANIZATION
============================================================

Authenticating...
✓ Authenticated successfully

Finding Trajanus USA folder...
✓ Found Trajanus USA root folder

STEP 1: Renaming folders without prefixes
✓ Renamed folder to: 04-Scripts
✓ Renamed folder to: 10-PM-Toolbox
✓ Renamed folder to: 11-Personal
✓ Renamed folder to: 12-Credentials

STEP 2: Creating main folder structure
✓ Created folder: 03-Living-Documents
✓ Created folder: 05-Archives
Folder '00-Command-Center' already exists
...

STEP 3: Creating Living Documents structure (11 types)
Creating Operational_Journal structure...
✓ Created folder: Operational_Journal_Daily_Entries
Creating Technical_Journal structure...
✓ Created folder: Technical_Journal_Daily_Entries
...

STEP 4: Creating Archives structure
✓ Created folder: AI-Projects
✓ Created folder: FILE-RECOVERY-1109-1315
✓ Created folder: Chat-Files

============================================================
REORGANIZATION COMPLETE
============================================================

✓ Main folders: 13
✓ Living Documents types: 11
✓ Daily entry folders: 11
✓ Archive folders: 3

NEXT STEPS:
1. Manually move files from old folders to renamed folders if needed
2. Run Living Documents population script to create MASTER files
3. Begin daily entry creation process
```

---

## SAFETY FEATURES

✅ **No Data Loss:** Script only creates/renames folders, never deletes files  
✅ **Duplicate Detection:** Checks if folders exist before creating  
✅ **Error Handling:** Continues if individual operations fail  
✅ **Existing Files:** Preserves all files in existing folders  
✅ **Rollback Safe:** Can manually undo renames in Google Drive if needed

---

## POST-EXECUTION TASKS

### Manual File Organization (Optional)
After script runs, you may want to:
1. Move archive files to `05-Archives/` subfolders
2. Verify renamed folders contain correct files
3. Move any misplaced documents to proper locations

### Next Script to Run
After this completes, run:
```powershell
python create_living_documents_masters.py
```
This will create all 11 MASTER files with proper templates.

---

## TROUBLESHOOTING

**Error: "Could not find '00 - Trajanus USA' folder"**
- Check that folder name is exactly "00 - Trajanus USA"
- Verify you have access to the folder

**Error: "Authentication failed"**
- Delete token.json and re-run
- Verify credentials.json is valid

**Error: "Permission denied"**
- Ensure you have edit access to Trajanus USA folder
- Check Google Drive API is enabled

**Folders not appearing?**
- Refresh Google Drive in browser
- Wait 30 seconds for sync
- Check "Shared with me" if folder is shared

---

## VERIFICATION CHECKLIST

After running script, verify:
- [ ] All folders 00-12 exist and are numbered
- [ ] 03-Living-Documents has 11 Daily_Entries subfolders
- [ ] 05-Archives has 3 subfolders
- [ ] Old folder names (PM-Toolbox, Personal, etc.) are gone
- [ ] All existing files still accessible
- [ ] No files were deleted

---

## DOCUMENTATION UPDATE

After successful execution, update:
1. **Operational_Journal_MASTER.md** - Add folder reorganization entry
2. **Master_File_Architecture_MASTER.md** - Update complete structure
3. **Technical_Journal_MASTER.md** - Document script execution details

---

**Questions? Issues? Document in Protocol_Violations if anything unexpected happens.**
