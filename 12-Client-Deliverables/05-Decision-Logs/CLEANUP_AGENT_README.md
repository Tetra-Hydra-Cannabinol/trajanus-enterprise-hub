# GOOGLE DRIVE CLEANUP AGENT
**Version:** 1.0  
**Date:** December 11, 2025  
**Purpose:** Safe, automated Google Drive organization and cleanup

---

## WHAT IT DOES

**✅ SCAN OPERATIONS (Safe, Read-Only):**
- Detect duplicate files (by name and by content)
- Find files needing conversion to Google Docs
- Identify misplaced files
- Validate folder structure
- Generate complete inventory
- Calculate statistics

**🔒 SAFE MODE (Default):**
- **NO DELETIONS** without your approval
- **NO MOVES** without your approval
- **NO CHANGES** - only reports
- Creates detailed reports for review
- You decide what to do

---

## QUICK START

### 1. Install (One-Time Setup)

```bash
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center\05-Scripts"

# Copy the agent files here:
# - gdrive_cleanup_agent.py
# - cleanup_config.json
# - RUN_CLEANUP_AGENT.bat

# No additional packages needed - uses existing Google Drive setup
```

### 2. Run Your First Scan

**Option A: Double-click to run in background**
```
Double-click: RUN_CLEANUP_AGENT.bat
```

This opens a new window and starts scanning. You can minimize it and keep working.

**Option B: Command line**
```bash
python gdrive_cleanup_agent.py --mode scan
```

### 3. Review the Reports

After scan completes (5-10 minutes for ~1000 files):
```
cleanup_report_20251211_143022.json  (machine-readable)
cleanup_report_20251211_143022.txt   (human-readable)
```

Open the .txt file to see:
- All duplicate files found
- Files needing conversion
- Misplaced files
- Complete statistics

---

## USAGE MODES

### MODE 1: SCAN (Default - Safe)

```bash
python gdrive_cleanup_agent.py --mode scan
```

**What it does:**
- Scans entire Google Drive folder structure
- Detects all issues
- Creates comprehensive reports
- **Makes NO changes**

**Time:** 5-10 minutes for ~1000 files  
**Safe:** Yes - read-only

### MODE 2: REPORT (View Previous Scan)

```bash
python gdrive_cleanup_agent.py --mode report
```

**What it does:**
- Loads most recent scan results
- Displays summary
- **Makes NO changes**

**Time:** Instant  
**Safe:** Yes - read-only

### MODE 3: EXECUTE (Not Yet Implemented)

```bash
python gdrive_cleanup_agent.py --mode execute --dry-run
```

**Future feature for:**
- Converting files to Google Docs
- Moving misplaced files
- Handling duplicates

**Current status:** Use reports to manually execute changes

---

## WHAT YOU'LL FIND

### 1. DUPLICATE FILES

**By Name:**
```
📁 Session_Summary_2025-11-30.md (3 copies)
   └─ 07-Session-Journal/Session_Summary_2025-11-30.md
   └─ 08-EOS-Files/Session_Summary_2025-11-30.md
   └─ 09-Archive/Session_Summary_2025-11-30.md
```

**By Content:**
```
Identical files with different names:
- report_v1.docx
- report_final.docx
- report_FINAL_FINAL.docx
```

### 2. FILES NEEDING CONVERSION

```
📄 OPERATIONAL_PROTOCOL.md (.md)
   Location: 01-Core-Protocols/OPERATIONAL_PROTOCOL.md
   Convert to: Google Docs
   Reason: Claude can read Google Docs but not .md from Drive

📄 Session_Summary_2025-12-10.docx (.docx)
   Location: 07-Session-Journal/Session_Summary_2025-12-10.docx
   Convert to: Google Docs
   Reason: Better accessibility and collaboration
```

### 3. MISPLACED FILES

```
📂 session_summary_nov30.md
   Current: 08-EOS-Files/
   Suggested: 07-Session-Journal/
   Reason: Contains "session" in name

📂 google_drive_manager.py
   Current: 00-Command-Center/
   Suggested: 05-Scripts/
   Reason: Python script file
```

### 4. FOLDER INVENTORY

```
01-Core-Protocols/
   Files: 12
   Subfolders: 0
   Types: .docx (8), .md (4)
   Size: 2.3 MB

05-Scripts/
   Files: 23
   Subfolders: 2
   Types: .py (20), .txt (2), .json (1)
   Size: 1.1 MB
```

---

## RUNNING IN BACKGROUND

### Method 1: Batch File (Recommended)

**RUN_CLEANUP_AGENT.bat** (included):
```batch
@echo off
echo Starting Google Drive Cleanup Agent...
echo This will run in the background. You can minimize this window.
echo.
python gdrive_cleanup_agent.py --mode scan
echo.
echo Scan complete! Press any key to close this window.
pause
```

**Usage:**
1. Double-click `RUN_CLEANUP_AGENT.bat`
2. Window opens and starts scanning
3. Minimize the window
4. Keep working in Claude
5. Check back in 5-10 minutes for results

### Method 2: Windows Task Scheduler

**Schedule weekly automatic scans:**

1. Open Task Scheduler
2. Create Basic Task
3. Name: "Trajanus Drive Cleanup"
4. Trigger: Weekly, Sunday, 8:00 PM
5. Action: Start Program
   - Program: `python`
   - Arguments: `gdrive_cleanup_agent.py --mode scan`
   - Start in: `G:\My Drive\00 - Trajanus USA\00-Command-Center\05-Scripts`
6. Finish

Now it runs automatically every week!

---

## SAFETY FEATURES

**🔒 MULTIPLE LAYERS OF PROTECTION:**

1. **Read-Only by Default**
   - Scan mode makes NO changes
   - Only reads and reports

2. **No Auto-Delete**
   - Nothing deleted without your explicit approval
   - Max deletions set to 0 in config

3. **Dry-Run Mode**
   - Test all operations before executing
   - See what WOULD happen

4. **Backup Before Action**
   - Future: Creates backup before any changes
   - Reversible operations

5. **Confirmation Required**
   - Manual review of all proposed changes
   - You decide what to execute

---

## CONFIGURATION

Edit `cleanup_config.json` to customize:

```json
{
  "safe_mode": true,              // Require approval for changes
  "auto_approve": false,           // Never auto-approve deletions
  "duplicate_strategy": "report_only",  // Only report, don't delete
  "max_deletions_per_run": 0,     // Zero deletions allowed
  "dry_run_default": true          // Always dry-run first
}
```

### Folder Mapping Rules

```json
"folder_mappings": {
  "session": "07-Session-Journal",
  "protocol": "01-Core-Protocols",
  "script": "05-Scripts",
  "eos": "08-EOS-Files"
}
```

Files with these keywords get suggested for these folders.

---

## REPORTS EXPLAINED

### JSON Report (Machine-Readable)

```json
{
  "scan_date": "2025-12-11T14:30:22",
  "statistics": {
    "total_files": 856,
    "total_folders": 42,
    "total_size_mb": 234.5,
    "duplicates": 23,
    "needs_conversion": 67
  },
  "duplicates": [...],
  "needs_conversion": [...],
  "misplaced_files": [...]
}
```

**Use:** Import into other tools, process programmatically

### TXT Report (Human-Readable)

```
STATISTICS
-------------------
Total Files: 856
Total Folders: 42
Total Size: 234.5 MB
Duplicates: 23
Need Conversion: 67

DUPLICATE FILES
-------------------
[Details...]

FILES NEEDING CONVERSION
-------------------
[Details...]
```

**Use:** Read and review, print, share with team

---

## TAKING ACTION

**After reviewing reports, you can:**

### 1. Convert Files Manually

For each file in "needs_conversion":
1. Open the file in Google Drive
2. File → Save as Google Docs/Sheets/Slides
3. Delete the original (optional)

**Or use batch conversion script:**
```bash
python batch_convert_to_gdocs.py --report cleanup_report_*.json
```

### 2. Move Misplaced Files

For each file in "misplaced_files":
1. Open file in Google Drive
2. Right-click → Move to
3. Select suggested folder

**Or approve agent to move:**
```bash
python gdrive_cleanup_agent.py --mode execute --action move --dry-run
# Review proposed moves
python gdrive_cleanup_agent.py --mode execute --action move
```

### 3. Handle Duplicates

**Strategy options:**

**Keep Newest:**
- Compare modified dates
- Keep most recent version
- Delete older copies

**Keep by Location:**
- Keep file in "correct" folder
- Delete from other locations

**Manual Review:**
- Open each duplicate
- Compare content
- Decide which to keep

---

## TYPICAL WORKFLOW

**Weekly Routine:**

**Sunday Evening (10 minutes):**
1. Run cleanup scan
2. Review reports while having coffee
3. Note issues to fix
4. Make notes in cleanup checklist

**During Week (5-10 minutes/day):**
1. Convert 5-10 files to Google Docs
2. Move 3-5 misplaced files
3. Review 1-2 duplicate sets

**Result:**
- Cleaner Drive every week
- Better organization over time
- No massive cleanup sessions needed
- Continuous improvement

---

## TROUBLESHOOTING

### Scan Taking Too Long

**Problem:** Scan runs for 30+ minutes

**Solution:**
- Reduce base folder scope
- Exclude Archive folder: `"exclude_folders": ["09-Archive"]`
- Increase `pageSize` in code

### Can't Find Base Folder

**Problem:** "Could not find folder: 00 - Trajanus USA"

**Solution:**
- Check folder name spelling
- Use `--base-folder "Exact Name"` argument
- Verify folder not in Trash

### Authentication Errors

**Problem:** "Authentication failed"

**Solution:**
1. Delete `credentials/token.json`
2. Run agent again
3. Re-authorize in browser
4. Token regenerated

### Empty Reports

**Problem:** Reports show zero files

**Solution:**
- Check base_folder_id found correctly
- Verify folder has files
- Check folder not empty in Drive web interface

---

## ADVANCED USAGE

### Custom Scan Location

```bash
python gdrive_cleanup_agent.py --base-folder "Different Folder Name"
```

### Scan Specific Subfolder

Edit code to set different `base_folder_id`

### Export to CSV

```python
import json
import csv

with open('cleanup_report_*.json') as f:
    data = json.load(f)

with open('duplicates.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Count', 'Locations'])
    for dup in data['duplicates']['by_name']:
        writer.writerow([dup['name'], dup['count'], '; '.join(dup['locations'])])
```

---

## FUTURE ENHANCEMENTS

**Planned for v2.0:**
- ✅ Execute mode with dry-run
- ✅ Automatic file conversion
- ✅ Automatic file moving
- ✅ Duplicate resolution automation
- ✅ Scheduling and monitoring
- ✅ Email reports
- ✅ Web dashboard

**Requested by Bill:**
- ✅ Background operation
- ✅ Safe mode (no deletions)
- ✅ Comprehensive reports
- ✅ Conversion detection
- ✅ Misplaced file detection

---

## SUPPORT

**Questions or Issues:**
- Review this README
- Check configuration in cleanup_config.json
- Review generated reports
- Test with --dry-run first

**Contact:**
- Bill King, Trajanus USA
- Session documentation in knowledge base

---

## VERSION HISTORY

**v1.0 (2025-12-11):**
- Initial release
- Full scan capabilities
- Duplicate detection
- Conversion detection
- Folder validation
- Comprehensive reporting
- Safe mode only (no execute yet)

---

**REMEMBER:** This agent is designed to HELP, not to automatically change things. You remain in full control. Review all reports before taking any action.

**SAFE, SMART, SYSTEMATIC** 🔒📊✅
