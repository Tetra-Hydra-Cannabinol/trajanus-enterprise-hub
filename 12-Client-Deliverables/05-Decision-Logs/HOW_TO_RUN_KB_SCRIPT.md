# RUN THIS TO CREATE KNOWLEDGE BASE FOLDERS

## STEP 1: Move the script

The script is in your Downloads: `create_kb_structure.py`

Move it to: `C:\trajanus-command-center\Scripts\`

## STEP 2: Run it

Open PowerShell:
```powershell
cd C:\trajanus-command-center\Scripts
python create_kb_structure.py
```

## What it does:

1. Authenticates with Google Drive (uses your credentials)
2. Finds "00 - Trajanus USA" folder
3. Creates "13-Knowledge-Base" folder inside it
4. Creates all 9 main folders
5. Creates all subfolders

## You'll see:

```
============================================================
CREATING TRAJANUS KNOWLEDGE BASE FOLDER STRUCTURE
============================================================

Authenticating with Google Drive...
✓ Authenticated

Finding '00 - Trajanus USA' folder...
✓ Found folder (ID: xxxxxxxxx)

Creating main folder...
✓ Created: 13-Knowledge-Base

Creating subfolders...
  ✓ 01-Building-Codes
    ✓ 01-Building-Codes/NFPA-70
    ✓ 01-Building-Codes/IBC-2021
    ✓ 01-Building-Codes/UFC
  ✓ 02-USACE-Standards
    ✓ 02-USACE-Standards/Engineer-Regulations
    ✓ 02-USACE-Standards/Engineer-Pamphlets
... (all folders)

============================================================
✅ FOLDER STRUCTURE CREATED SUCCESSFULLY!
============================================================

Location: G:\My Drive\00 - Trajanus USA\13-Knowledge-Base\

Refresh Google Drive in File Explorer to see folders.

✓ Done. Ready for next step (Supabase setup).
```

## If it fails:

Check that:
- You're in C:\trajanus-command-center\Scripts\
- credentials/credentials.json exists
- credentials/token.json exists (from previous Drive usage)
- Internet connection is working

## After success:

1. Refresh File Explorer (F5)
2. Open Google Drive folder
3. You'll see 13-Knowledge-Base with all subfolders
4. Move to next step: Supabase setup
