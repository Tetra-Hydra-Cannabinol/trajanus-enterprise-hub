# EOS AUTOMATION - QUICK START GUIDE

## 🎯 COMPLETE WORKFLOW (ONE COMMAND!)

### What You Do:
1. Download the session files ZIP to: `G:\My Drive\00 - Trajanus USA\08-EOS-Files\`
2. Open PowerShell
3. Run ONE command

### The Command:
```powershell
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center"
.\EOS_AUTOMATION_MASTER.ps1
```

### What Happens Automatically:
✅ Finds today's ZIP file in 08-EOS-Files  
✅ Extracts all files  
✅ Archives the ZIP to 08-EOS-Files/archives/  
✅ Creates folder structure in 07-Session-Journal:
   - Technical-Journals/
   - Personal-Diaries/
   - Operational-Journals/
   - Project-Diaries/
   - Session-Summaries/
   - Code-Repositories/
   - Session-Handoffs/  
✅ Distributes files by type to correct folders  
✅ Converts ALL files to Google Docs format  
✅ Plays success beep  

### Result:
🎉 Next Claude session has complete access to all files!

---

## 📁 FILE LOCATIONS

**Scripts:** `G:\My Drive\00 - Trajanus USA\00-Command-Center\`
- EOS_AUTOMATION_MASTER.ps1 ⭐⭐ (RUN THIS ONE)
- parse_eos_files.py
- CONVERT_ALL_FILES.ps1
- convert_office_to_google.py
- convert_single_md.py
- living_documents_appender.py
- scan_for_unconverted.ps1

**Download ZIP here:** `G:\My Drive\00 - Trajanus USA\08-EOS-Files\`

**Organized files go here:** `G:\My Drive\00 - Trajanus USA\07-Session-Journal\`

---

## ⚡ THAT'S IT!

Download ZIP → Run script → Done

No manual unzipping, no manual file moving, no manual conversion.

**Total time: 30-60 seconds**

---

## 🔧 TROUBLESHOOTING

**"ZIP not found"**
- Make sure ZIP is in 08-EOS-Files folder
- Make sure filename contains today's date (YYYY-MM-DD)

**"Python not found"**
- Add Python to PATH
- Or use full path: `python.exe "full\path\to\parse_eos_files.py" --auto`

**"Permission denied"**
- Run PowerShell as Administrator
- Or: Right-click script → Run as Administrator

**"Script execution disabled"**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📝 MANUAL MODE (If You Want Control)

If you want to run steps individually:

```powershell
# Step 1: Parse (with prompts)
python parse_eos_files.py

# Step 2: Convert
.\CONVERT_ALL_FILES.ps1
```

But the master script does both automatically!

---

**THIS IS THE SYSTEM WORKING AS DESIGNED**
