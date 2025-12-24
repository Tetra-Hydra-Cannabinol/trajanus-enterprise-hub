# KNOWMADS AGENT REGISTRY
## Available AI Agents in Trajanus Enterprise Hub
## Last Updated: December 11, 2025

---

## PRODUCTION AGENTS

### KNOWMAD-4: File Scout
**Status:** ✅ Production Ready  
**Location:** `G:\My Drive\00 - Trajanus USA\00-Command-Center\knowmad_4_file_scout.py`  
**Function:** Analyzes large code files, maps structure, identifies insertion points  
**Usage:**
```python
python knowmad_4_file_scout.py [file-path]
```
**Outputs:**
- HTML_STRUCTURE_MAP_[timestamp].txt (human-readable)
- INSERTION_POINTS_[timestamp].json (machine-readable)

**Use Cases:**
- Surgical edits on files >1000 lines
- Finding exact code insertion points
- Structure analysis before modifications
- Conflict detection

---

### KNOWMAD-5: File Organization Agent
**Status:** ✅ Production Ready  
**Location:** `G:\My Drive\00 - Trajanus USA\00-Command-Center\knowmad_5_file_organizer.py`  
**Function:** Analyzes EOS files and proposes organization into Living Documents categories  
**Usage:**
```python
python knowmad_5_file_organizer.py [folder-path]
# If no path provided, auto-detects latest EOS folder
```
**Outputs:**
- FILE_ORGANIZATION_REPORT.txt (approval report)
- EXECUTE_FILE_MOVES.ps1 (execution script)

**Decision Logic:**
- Session_Summary_* → 03-Living-Documents/Session-Summaries
- Technical_Journal_* → 03-Living-Documents/Technical-Journal
- Bills_Daily_Diary_* → 03-Living-Documents/Personal-Diary
- Code_Repository_* → 03-Living-Documents/Code-Repository
- *_GUIDE → 06-User-Guides
- *HANDOFF* → 08-EOS-Files/Handoffs

**Use Cases:**
- End-of-session file organization
- Living Documents maintenance
- Batch file categorization

---

### KNOWMAD-6: EOS Organization Executor
**Status:** ✅ Production Ready  
**Location:** `G:\My Drive\00 - Trajanus USA\00-Command-Center\knowmad_6_eos_executor.py`  
**Function:** Complete workflow executor - runs analysis, shows report, executes moves  
**Usage:**
```python
# Interactive mode (default)
python knowmad_6_eos_executor.py

# Auto-approve mode
python knowmad_6_eos_executor.py --auto-approve

# Specific folder
python knowmad_6_eos_executor.py "G:\My Drive\...\EOS Files 12-11-2025"
```
**Outputs:**
- Calls Knowmad-5 for analysis
- Displays approval modal (if UI integrated)
- Executes PowerShell move script
- Saves eos_org_results.json

**Use Cases:**
- One-command file organization
- Automated EOS workflows
- Button-triggered operations from Enterprise Hub

---

## IN DEVELOPMENT

### KNOWMAD-1: HTML Surgeon
**Status:** 🚧 Planned  
**Function:** Surgical edits on large HTML files  
**Target Completion:** Week of December 16

### KNOWMAD-2: CSS Architect  
**Status:** 🚧 Planned  
**Function:** Styling systems and CSS management  
**Target Completion:** Week of December 16

### KNOWMAD-3: JavaScript Builder
**Status:** 🚧 Planned  
**Function:** JavaScript module creation and integration  
**Target Completion:** Week of December 16

---

## HOW TO USE AGENTS IN CLAUDE SESSIONS

### Method 1: Direct Command
**Tell Claude:**
```
Use Knowmad-5 to analyze the EOS folder and propose file organization.
```

### Method 2: Specific Instructions
**Tell Claude:**
```
Run this command:
python knowmad_5_file_organizer.py "G:\My Drive\00 - Trajanus USA\08-EOS-Files\EOS Files 12-11-2025"

Then show me the report.
```

### Method 3: Reference This Document
**Tell Claude:**
```
Check the Knowmads Agent Registry in project knowledge. 
I need to use the file organization agent.
```

---

## AGENT CAPABILITIES MATRIX

| Agent | Analysis | Execution | UI Integration | Auto-Approve |
|-------|----------|-----------|----------------|--------------|
| Knowmad-4 | ✅ | ❌ | ❌ | N/A |
| Knowmad-5 | ✅ | ❌ | ❌ | N/A |
| Knowmad-6 | ✅ | ✅ | ✅ | ✅ |

---

## CALLING AGENTS FROM CLAUDE

**When to call agents:**
- User asks to "organize files"
- User says "run the file organization agent"
- User wants "EOS files moved to correct locations"
- User references "Knowmad-5" or "Knowmad-6"

**How to call (via bash_tool):**
```python
bash_tool.run(
    command='cd "G:\\My Drive\\00 - Trajanus USA\\00-Command-Center" && python knowmad_6_eos_executor.py',
    description='Running file organization executor agent'
)
```

**For auto-approve mode:**
```python
bash_tool.run(
    command='cd "G:\\My Drive\\00 - Trajanus USA\\00-Command-Center" && python knowmad_6_eos_executor.py --auto-approve',
    description='Auto-executing file organization'
)
```

---

## INTEGRATION STATUS

### Enterprise Hub Button
**Status:** ✅ Code Ready, 🚧 Integration Pending  
**Location:** FILE_ORG_BUTTON_INTEGRATION.html  
**Function:** One-click file organization from UI  

**To complete integration:**
1. Add CSS to index.html (line ~100-500)
2. Add button HTML (line ~800-900)
3. Add modal + JavaScript (line ~7300)

---

## DOCUMENTATION LOCATIONS

**Agent Source Code:**
- `G:\My Drive\00 - Trajanus USA\00-Command-Center\knowmad_*.py`

**Documentation:**
- `G:\My Drive\00 - Trajanus USA\05-Scripts\knowmads\FILE_ORGANIZATION_WORKFLOW.md`
- `G:\My Drive\00 - Trajanus USA\05-Scripts\knowmads\INTEGRATION_GUIDE_COMPLETE.md`

**Quick Reference:**
- `G:\My Drive\00 - Trajanus USA\05-Scripts\knowmads\QUICK_REFERENCE.md`

---

## UPDATE LOG

**December 11, 2025:**
- ✅ Knowmad-4 created and tested (7,412-line file analyzed in 0.8s)
- ✅ Knowmad-5 created and tested (8 files categorized correctly)
- ✅ Knowmad-6 created and tested (complete workflow execution)
- ✅ UI integration code completed
- ✅ Full documentation package delivered

---

## NEXT ADDITIONS

**Planned Agents:**
1. Knowmad-1 (HTML Surgeon) - December 16-20
2. Knowmad-2 (CSS Architect) - December 16-20  
3. Knowmad-3 (JavaScript Builder) - December 16-20

**This registry will be updated as agents are added.**

---

*Knowmads Agent Registry v1.0*  
*December 11, 2025*  
*Trajanus USA - Proprietary*
