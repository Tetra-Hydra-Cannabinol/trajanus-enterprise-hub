# TRAJANUS COMMAND CENTER - USER GUIDE
## Complete Reference for AI-Augmented Construction Management System

**Version:** 1.1.0  
**Last Updated:** November 25, 2025  
**Status:** Production Ready  
**Author:** Bill King & Claude AI

---

## TABLE OF CONTENTS

1. [System Overview](#system-overview)
2. [Getting Started](#getting-started)
3. [Interface Guide](#interface-guide)
4. [Version Control Workflow](#version-control-workflow)
5. [Living Documents System](#living-documents-system)
6. [Session Management](#session-management)
7. [Project Browser](#project-browser)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)
10. [Technical Reference](#technical-reference)

---

## SYSTEM OVERVIEW

### What is the Command Center?

The Trajanus Command Center is a web-based application that serves as the central hub for AI-augmented construction project management. It integrates:

- **Session Management** - Automated documentation and closeout procedures
- **Living Documents** - Continuous knowledge capture across Claude sessions
- **Project Browser** - Google Drive integration for file management
- **Development Tools** - Markdown conversion, batch operations, automation
- **Version Control** - Git-backed with local timestamped backups

### Core Philosophy

**"The methodology itself is the intellectual property."**

Every session with Claude generates documentation that becomes a permanent knowledge asset. The Command Center automates this process, turning daily work into competitive advantage.

### System Requirements

- **Operating System:** Windows 10/11 (PowerShell 5.1+)
- **Browser:** Chrome, Edge, or Firefox (latest versions)
- **Google Account:** With Drive API access
- **Git:** For version control (optional but recommended)
- **Python 3.8+:** For automation scripts

---

## GETTING STARTED

### Initial Setup

#### 1. File Structure

Your Command Center folder should be organized as follows:

```
G:\My Drive\00 - Trajanus USA\00-Command-Center\
│
├── index.html                          # Main Command Center file
├── save-version.ps1                    # Quick save script
├── archive-today.ps1                   # End-of-day archive script
│
├── Archive\
│   ├── 2025-11-24\                    # Daily archives
│   ├── 2025-11-25\
│   └── HTML-Versions\                 # Long-term backups
│
├── Credentials\
│   ├── credentials.json               # Google OAuth credentials
│   └── token.json                     # Authentication token
│
├── Scripts\
│   ├── upload_session_docs.py         # Upload session files
│   ├── update_master_docs_v2.py       # Update MASTER docs
│   └── project_browser.py             # Drive file browser
│
└── Session-Archives\
    ├── 2025-11-24\                    # Daily session documents
    └── 2025-11-25\
```

#### 2. Desktop Shortcut

**Create shortcut to index.html:**

1. Right-click Desktop → New → Shortcut
2. Target: `G:\My Drive\00 - Trajanus USA\00-Command-Center\index.html`
3. Name: "Trajanus Command Center"

**Or use PowerShell:**
```powershell
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut("$env:USERPROFILE\Desktop\Trajanus Command Center.lnk")
$shortcut.TargetPath = "G:\My Drive\00 - Trajanus USA\00-Command-Center\index.html"
$shortcut.Save()
```

#### 3. Google Drive Authentication

Run once to authenticate:
```powershell
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center\Scripts"
python upload_session_docs.py
# Follow browser OAuth prompts
```

This creates `token.json` in the Credentials folder.

---

## INTERFACE GUIDE

### Sidebar Navigation

The left sidebar contains three main sections:

#### Developer Projects
- **Command Center** - Session management and automation
- **Website Builder** - Trajanus-USA.com development
- **PM Toolkit** - Project Manager resources
- **QCM Toolkit** - Quality Control Manager tools
- **Safety Toolkit** - SSHO documentation
- **Route Optimizer** - Store visit optimization
- **Traffic Study** - Transportation engineering
- **Memory/Resources** - Knowledge base and protocols

#### Working Projects
- **PM Working** - Active PM tasks
- **QCM Working** - Active QCM tasks
- **SSHO Working** - Active safety work

#### Quick Access
- **Claude AI** - Opens claude.ai
- **Google Drive** - Opens Drive in browser
- **Resources & Codes** - Industry standards

### Main Content Area

**Header:**
- Project title and breadcrumb navigation
- Live clock display

**Workspace:**
- Tools section with action buttons
- Project resources and links
- Terminal for command output

**Status Bar:**
- Google Drive connection status
- Platform information
- Version number

### Terminal

Multi-tab terminal at bottom of screen:
- View command output
- Multiple terminal tabs
- Clear and refresh functions
- Real-time status updates

---

## VERSION CONTROL WORKFLOW

### The Dual-System Approach

**Git Repository (Primary):**
- Full version history with commit messages
- Professional standard for collaboration
- Rollback to any previous state

**Local Archives (Safety Net):**
- Timestamped snapshots during development
- Quick recovery without Git commands
- Same-day rollback capability

### Daily Workflow

#### During Active Development

**1. Make Changes**
Edit `index.html` in your preferred editor (VS Code recommended)

**2. Save Timestamped Version**
```powershell
.\save-version.ps1
```

Optional: Add description
```powershell
.\save-version.ps1 "fixed session buttons"
.\save-version.ps1 "added project browser"
```

**Output:**
```
✓ Version saved!
  File: index_2025-11-25_1430.html
  Size: 104.2 KB
  Time: 14:30:15
```

**3. Test Changes**
Open in browser, verify functionality

**4. Git Commit (Major Milestones)**
```powershell
git add index.html
git commit -m "Implemented session management automation"
git push
```

#### End of Day

**1. Run Archive Script**
```powershell
.\archive-today.ps1
```

**What it does:**
- Lists all today's timestamped files
- Asks for confirmation
- Moves files to `Archive/YYYY-MM-DD/` folder
- Checks for archives older than 30 days
- Offers to delete old archives

**Example output:**
```
================================
End of Day Archive
================================

Found 5 file(s) from today:

  • index_2025-11-25_0900.html
    103.2 KB | Modified: 09:00:15
  • index_2025-11-25_1130.html
    104.1 KB | Modified: 11:30:42
  • index_2025-11-25_1430.html
    104.2 KB | Modified: 14:30:15

Archive these files? (Y/N): Y

Archiving...
  ✓ Archived: index_2025-11-25_0900.html
  ✓ Archived: index_2025-11-25_1130.html
  ✓ Archived: index_2025-11-25_1430.html

================================
Archive Complete!
================================

Files archived: 3
Total size: 0.31 MB
Location: Archive\2025-11-25\
```

**2. Run Session Closeout**
Follow the [Session Management](#session-management) protocol

**3. Git Commit End-of-Day State**
```powershell
git add .
git commit -m "EOD 2025-11-25: [summary of day's work]"
git push
```

### Version Recovery

#### Restore from Today's Timestamp
```powershell
# List today's archives
ls "Archive\2025-11-25\"

# Copy specific version back
copy "Archive\2025-11-25\index_2025-11-25_1130.html" index.html
```

#### Restore from Git
```powershell
# See commit history
git log --oneline

# Restore specific commit
git checkout <commit-hash> index.html

# Or reset to previous commit
git reset --hard HEAD~1
```

### Git Best Practices

**Commit Messages:**
- Use present tense: "Add feature" not "Added feature"
- Be specific: "Fix session button CSS" not "Fix bug"
- Reference issues if applicable

**Commit Frequency:**
- After completing a feature
- Before making risky changes
- At end of each session
- Minimum once per day

**Branch Strategy (Future):**
```
main          - Production stable version
development   - Active development work
feature/*     - Specific feature branches
hotfix/*      - Emergency fixes
```

### Archive Maintenance

**Keep Archives For:**
- Current month: All files
- Previous 1-3 months: Weekly snapshots
- Older than 3 months: Monthly snapshots
- Critical versions: Permanent

**Cleanup Strategy:**
```powershell
# archive-today.ps1 automatically offers to delete >30 day archives
# Manual cleanup if needed:
Remove-Item "Archive\2024-10-*" -Recurse -Force
```

---

## LIVING DOCUMENTS SYSTEM

### The Six Living Documents

1. **Session Summary** - High-level overview of session accomplishments
2. **Technical Journal** - Code changes, bugs, technical decisions
3. **Code Repository** - HTML file state, version tracking
4. **Operational Journal** - Process improvements, workflow changes
5. **Personal Diary** - User reflections and observations (optional)
6. **Website Development** - Trajanus-USA.com progress and documentation

### Document Flow

```
Claude Session
    ↓
Generate .md files (6 documents)
    ↓
Download to Command Center folder
    ↓
Run automation (upload_session_docs.py)
    ↓
Upload to Google Drive (dated archive)
    ↓
Append to MASTER documents
    ↓
Update last-modified timestamps
```

### MASTER Documents

Located in Google Drive: `00 - Trajanus USA/00-Command-Center/Living-Documents/`

**Naming Convention:**
- `Session_Summaries_November_2025_MASTER`
- `Technical_Journal_November_2025_MASTER`
- `Code_Repository_November_2025_MASTER`
- `Operational_Journal_November_2025_MASTER`
- `Personal_Diary_November_2025_MASTER`
- `Website_Development_November_2025_MASTER`

**Structure:**
- Monthly documents (new document each month)
- Entries appended with timestamp headers
- Full history of all sessions

### Using the Living Documents Tools

#### Update Living Documents (Complete Workflow)
```
Button: "Update Living Documents"
Function: runUpdateLivingDocs()
```

**What it does:**
1. Prompts for .md file selection
2. Uploads to dated archive folder in Drive
3. Converts .md to Google Docs format
4. Appends content to appropriate MASTER docs
5. Updates timestamps

**When to use:** After every Claude session (part of EOS protocol)

#### Convert MD to Docs
```
Button: "Convert MD to Docs"
Function: runConvertMD()
```

Converts selected .md files to Google Docs without appending to MASTERs.

**When to use:** Creating standalone Google Docs from markdown

#### Convert MD to Word
```
Button: "Convert MD to DOCX"
Function: runConvertDOCX()
```

Converts selected .md files to Word .docx format.

**When to use:** Creating Word documents for formal deliverables

#### Setup Living Documents (ONE-TIME)
```
Button: "Setup Living Documents"
Function: runSetupDocs()
```

Creates all 10 MASTER documents (6 living docs × 2 for current + next month).

**When to use:** 
- Initial system setup
- Start of new month
- After major system reorganization

#### Batch Convert Folder
```
Button: "Batch Convert Folder"
Function: runBatchConvert()
```

Converts entire folder of .md files to Google Docs.

**When to use:** Migrating historical documentation

---

## SESSION MANAGEMENT

### Session Closeout Protocol (EOS)

**Required at end of EVERY Claude session.**

#### Phase 1: Document Creation

In Claude, request all 6 living documents:
- Session Summary
- Technical Journal
- Code Repository
- Operational Journal
- Personal Diary (optional)
- Website Development (if applicable)

Download all documents to Command Center folder.

#### Phase 2: Automation Execution

**Option A: Command Center Buttons**
1. Open Command Center
2. Click "Command Center" in sidebar
3. Click "Update Living Documents" button
4. Select all 6 .md files
5. Confirm execution

**Option B: PowerShell Manual**
```powershell
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center\Scripts"
python upload_session_docs.py
python update_master_docs_v2.py
```

#### Phase 3: Version Control

**Save current state:**
```powershell
.\save-version.ps1 "session complete"
```

**Git commit:**
```powershell
git add .
git commit -m "Session [date/time]: [brief summary]"
git push
```

#### Phase 4: Archive

**Run archive script:**
```powershell
.\archive-today.ps1
```

Confirm file archival when prompted.

### Session Startup Protocol

**For each new Claude session:**

#### 1. Upload Required Files
- `credentials.json`
- `token.json`
- Most recent Session Summary

#### 2. Opening Message Template
```
Continuing from [date] session. 

Priority tasks:
1. [Task 1]
2. [Task 2]
3. [Task 3]

Uploaded credentials and session summary. Ready to work.
```

#### 3. Review Context

Claude will search Google Drive for MASTER documents and review:
- Recent session summaries
- Technical journal entries
- Code repository state
- Operational notes

### Token Management

**Claude displays token gauge at end of every response:**
```
Token Gauge: 🟢 45% remaining
```

**Action thresholds:**
- **🟢 20-100%** - Continue work normally
- **🟡 10-20%** - Start planning session closeout
- **🟡 5-10%** - Begin EOS protocol immediately
- **🔴 <5%** - Emergency: Create Session Summary only

**Best practice:** Start EOS at 15% tokens remaining.

### Recovery Protocol

**If session crashes before EOS:**

1. **Assess what survived:**
   - Check for timestamped HTML versions
   - Check Downloads folder for any artifacts
   - Review browser history for recovery clues

2. **Create recovery session:**
   - Document what was lost
   - Document what survived
   - Reconstruct from code and memory

3. **Prevent future loss:**
   - Save versions more frequently
   - Run mid-session checkpoints
   - Keep timestamped backups current

4. **Reference:** See `RECOVERY_Session_2025-11-24.md` for real example

---

## PROJECT BROWSER

### Overview

The Project Browser integrates Google Drive file access directly into Command Center.

### Python Script: project_browser.py

**Location:** `Scripts/project_browser.py`

#### Commands

**List Known Projects:**
```powershell
python project_browser.py list-projects
```

Output: JSON list of configured project folders with file counts

**List Files in Folder:**
```powershell
python project_browser.py list-files <folder_id>
```

Output: JSON list of files with metadata (name, size, type, modified date)

**Download File:**
```powershell
python project_browser.py download <file_id> <local_path>
```

Downloads file to specified location. Auto-converts Google Docs formats.

**Scan for Projects:**
```powershell
python project_browser.py scan
```

Searches Drive for folders containing "Project", "Study", "Traffic", or "Command"

**Add Project:**
```powershell
python project_browser.py add-project <folder_id> [display_name]
```

Adds folder to known projects list (manual edit of script required)

### Integration (Future)

Modal file browser in Command Center interface:
- Click "Browse Projects" button
- Visual folder/file explorer
- Direct download to local machine
- Upload capabilities

---

## TROUBLESHOOTING

### Common Issues

#### "index.html not found"
**Cause:** Running scripts from wrong directory  
**Solution:** 
```powershell
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center"
```

#### "credentials.json not found"
**Cause:** Google OAuth files missing  
**Solution:** Check `Credentials/` folder, re-authenticate if needed

#### Git push fails
**Cause:** Repository not initialized or network issue  
**Solution:**
```powershell
git remote -v  # Verify remote exists
git push -u origin main  # Set upstream
```

#### Python script errors
**Cause:** Missing dependencies  
**Solution:**
```powershell
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client --break-system-packages
```

#### Archive script can't find files
**Cause:** Wrong date format or files already archived  
**Solution:** Check filename pattern matches `index_YYYY-MM-DD_HHMM.html`

#### Timestamped file not created
**Cause:** save-version.ps1 can't find index.html  
**Solution:** Verify `index.html` exists in Command Center root

### Emergency Procedures

#### System Completely Broken
1. Don't panic
2. Check Archive folder for last working version
3. Copy last working version to index.html
4. Test in browser
5. Document what broke in recovery session

#### Lost All Documentation
1. Recreate from Git history
2. Use Code Repository MASTER in Drive
3. Create recovery session documenting gap
4. Implement more frequent backups going forward

#### Claude Session Crash
1. Save any visible artifacts immediately
2. Screenshot critical information
3. Check phone app access (sometimes works when web doesn't)
4. Follow Recovery Protocol (see [Session Management](#session-management))
5. Document in Technical Journal

---

## BEST PRACTICES

### Daily Habits

**Morning:**
- [ ] Open Command Center
- [ ] Check Git status: `git status`
- [ ] Review yesterday's session summary
- [ ] Start new Claude session with proper context

**During Work:**
- [ ] Save version after major changes: `.\save-version.ps1`
- [ ] Commit to Git at logical milestones
- [ ] Test changes before saving
- [ ] Document as you go (notes for session summary)

**Evening:**
- [ ] Complete session closeout protocol
- [ ] Archive timestamped files: `.\archive-today.ps1`
- [ ] Git commit end-of-day state
- [ ] Review accomplishments

### Code Quality

**HTML/CSS:**
- Comment complex sections
- Use consistent indentation
- Test in multiple browsers
- Validate before committing

**JavaScript:**
- Add descriptive function comments
- Use meaningful variable names
- Handle errors gracefully
- Test all user interactions

**Python Scripts:**
- Follow PEP 8 style guide
- Add docstrings to functions
- Handle API errors properly
- Test with various inputs

### Documentation

**Session Summaries:**
- Be concise but complete
- List specific accomplishments
- Note any unresolved issues
- Provide context for next session

**Technical Journal:**
- Document WHY not just WHAT
- Include code snippets for major changes
- Note debugging steps that worked
- Reference line numbers

**Code Repository:**
- Track current state (working/broken/partial)
- List known bugs
- Note dependencies
- Provide rollback information

### Communication with Claude

**Effective Prompts:**
- Be specific about requirements
- Provide examples when possible
- Ask questions if unclear
- Confirm understanding before proceeding

**Context Management:**
- Upload required files at session start
- Reference past work explicitly
- Don't assume Claude remembers everything
- Use session summaries for continuity

**Token Awareness:**
- Check token gauge regularly
- Start EOS before hitting 10%
- Prioritize critical work early in session
- Break large tasks into multiple sessions

---

## TECHNICAL REFERENCE

### File Types

**.html** - Main Command Center interface  
**.ps1** - PowerShell automation scripts  
**.py** - Python automation scripts  
**.md** - Markdown documentation (session files)  
**.json** - Configuration and authentication files

### Key Scripts

| Script | Purpose | Location |
|--------|---------|----------|
| save-version.ps1 | Quick timestamped save | Root |
| archive-today.ps1 | End-of-day archive | Root |
| upload_session_docs.py | Upload to Drive archive | Scripts/ |
| update_master_docs_v2.py | Append to MASTERs | Scripts/ |
| project_browser.py | Drive file browser | Scripts/ |

### Google Drive API Scopes

```python
SCOPES = ['https://www.googleapis.com/auth/drive']
```

Full Drive access required for:
- File upload/download
- Folder creation
- Metadata reading
- Document conversion

### Git Commands Quick Reference

```powershell
# Check status
git status

# Stage changes
git add index.html
git add .  # All files

# Commit
git commit -m "Your message"

# Push to remote
git push

# View history
git log --oneline

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard all changes
git reset --hard HEAD
```

### PowerShell Tips

```powershell
# Change directory
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center"

# List files
ls
Get-ChildItem  # Verbose version

# Copy file
copy source.html destination.html

# Move file
move source.html destination.html

# Delete file
Remove-Item filename.html

# Create directory
mkdir FolderName

# Get current date
Get-Date -Format "yyyy-MM-dd_HHmm"
```

---

## APPENDIX A: KEYBOARD SHORTCUTS

**Command Center Interface:**
- `Ctrl + R` - Refresh page
- `F12` - Open browser DevTools
- `Ctrl + Shift + I` - Inspect element

**VS Code (editing HTML):**
- `Ctrl + S` - Save file
- `Ctrl + /` - Toggle comment
- `Ctrl + F` - Find
- `Ctrl + H` - Find and replace
- `Alt + Up/Down` - Move line up/down

---

## APPENDIX B: FOLDER STRUCTURE REFERENCE

```
Command Center Root/
│
├── index.html                          # PRODUCTION VERSION (run from Desktop shortcut)
├── save-version.ps1                    # Quick save during work
├── archive-today.ps1                   # End-of-day cleanup
│
├── Archive/                            # Historical versions
│   ├── 2025-11-24/                    # Daily archives
│   │   ├── index_2025-11-24_0900.html
│   │   ├── index_2025-11-24_1130.html
│   │   └── index_2025-11-24_1500.html
│   ├── 2025-11-25/
│   └── HTML-Versions/                  # Long-term backups
│       └── index_BACKUP_*.html
│
├── Credentials/                        # OAuth and auth tokens
│   ├── credentials.json               # Google OAuth client secrets
│   └── token.json                     # Active auth token
│
├── Scripts/                            # Python automation
│   ├── upload_session_docs.py         # Upload session .md files
│   ├── update_master_docs_v2.py       # Append to MASTER docs
│   └── project_browser.py             # Drive file browser
│
└── Session-Archives/                   # Session living documents
    ├── 2025-11-24/                    # Dated folders
    │   ├── Session_Summary_2025-11-24.md
    │   ├── Technical_Journal_2025-11-24.md
    │   ├── Code_Repository_2025-11-24.md
    │   ├── Operational_Journal_2025-11-24.md
    │   ├── Personal_Diary_2025-11-24.md
    │   └── Website_Development_2025-11-24.md
    └── 2025-11-25/
```

---

## APPENDIX C: GLOSSARY

**EOS** - End of Session protocol  
**MASTER Document** - Monthly consolidated living document in Google Drive  
**Session Summary** - High-level overview of Claude session accomplishments  
**Technical Journal** - Detailed log of code changes and technical decisions  
**Code Repository** - Documentation of HTML file state and version tracking  
**Operational Journal** - Process improvements and workflow documentation  
**Living Document** - Continuously updated document capturing ongoing work  
**Timestamped Save** - Version of index.html with YYYY-MM-DD_HHMM format  
**Command Center** - Main HTML interface (this application)  
**Token Gauge** - Display showing remaining Claude context window capacity

---

## SUPPORT & UPDATES

**This guide is a living document.**

Updates tracked in:
- Git commit history
- Code Repository living document
- Operational Journal entries

**For issues or improvements:**
Document in next Claude session for incorporation into guide.

---

**End of User Guide**  
**Version 1.1.0 - November 25, 2025**
