# GOOGLE DRIVE UPLOADER - SETUP & USAGE GUIDE

## ONE-TIME SETUP

### Step 1: Install Python Packages

Open PowerShell in your Command Center folder:

```powershell
cd "G:\My Drive\Trajanus USA\00_Command_Center"
pip install google-auth google-auth-oauthlib google-api-python-client
```

### Step 2: Verify Credentials

Make sure these files are in the folder:
- `credentials.json` ✅
- `token.json` ✅
- `upload_session_docs.py` ✅

### Step 3: Test the Connection

```powershell
python upload_session_docs.py
```

If it says "Connected to Google Drive" - you're ready!

---

## USAGE

### Upload All Session Documents

From the Command Center folder:

```powershell
python upload_session_docs.py
```

This will automatically:
1. Find all .md, .txt, and .html files
2. Create today's date folder in Session Summaries
3. Upload everything
4. Give you links to view the files

### Upload Specific Files

```powershell
python upload_session_docs.py file1.md file2.txt file3.html
```

### Upload from Another Location

```powershell
python upload_session_docs.py "C:\Downloads\session_summary.md"
```

---

## WHERE FILES GO

```
Google Drive:
└── Trajanus USA
    └── AI Projects
        └── 01_Documentation
            └── Session Summaries
                └── 2025-11-23          ← Today's folder
                    ├── SESSION_SUMMARY_2025-11-22_FINAL.md
                    ├── TECHNICAL_JOURNAL_ENTRY_2025-11-22_FINAL.md
                    ├── SESSION_DIARY_2025-11-22_FINAL.md
                    └── ... (all uploaded files)
```

Each day gets its own folder (YYYY-MM-DD format).

---

## INTEGRATING WITH CLAUDE

### At End of Each Session:

1. Claude creates session documents
2. You download them (or Claude saves to outputs folder)
3. Move files to Command Center folder
4. Run: `python upload_session_docs.py`
5. Done! Everything's in Drive, organized by date

### Future Enhancement:

We can automate this further so Claude triggers the upload automatically.

---

## TROUBLESHOOTING

### "No module named google.auth"
Run: `pip install google-auth google-auth-oauthlib google-api-python-client`

### "Token expired"
The script auto-refreshes tokens. If it fails, delete `token.json` and re-authenticate.

### "Trajanus USA folder not found"
Make sure you're using the same Google account that has the Trajanus USA folder.

### "Permission denied"
Make sure the credentials.json is from the same Google Cloud project with Drive API enabled.

---

## WHAT THIS ENABLES

**Before:**
1. Claude creates documents
2. You download each one
3. Open Google Drive in browser
4. Navigate to correct folder
5. Upload each file
6. Repeat 5x per session

**After:**
1. Claude creates documents
2. Run one command: `python upload_session_docs.py`
3. Done!

**Time saved:** ~5 minutes per session
**Errors eliminated:** No more misplaced files
**Organization:** Automatic date-based filing

---

## NEXT STEPS

Once this works, we can:

1. **Automate from Claude** - Claude runs the upload directly
2. **Real-time sync** - Documents appear in Drive as Claude creates them
3. **Bidirectional sync** - Edit in Drive, Claude sees changes
4. **Full integration** - Command Center interface manages everything

This is the foundation. Let's test it and make sure it works perfectly.
