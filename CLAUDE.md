# CLAUDE.md - Trajanus Command Center
# This file is read automatically at every session start.
# Last Updated: 2025-12-30

---

## PROJECT CONTEXT

**Project:** Trajanus Enterprise Hub (Command Center)
**Owner:** Bill King, Trajanus USA
**Stack:** Tauri 2.0, Rust, JavaScript/TypeScript, Supabase, Google Drive

---

## PROJECT LOCATIONS - CRITICAL

| Project | Location | Purpose |
|---------|----------|---------|
| TAURI APP (source) | C:\Dev\trajanus-command-center\ | BUILD AND EDIT HERE |
| Google Drive | G:\My Drive\00 - Trajanus USA\00-Command-Center\ | Scripts, docs, backups |
| Running EXE | C:\Dev\trajanus-command-center\src-tauri\target\release\ | Compiled app |

### BUILD RULES:
1. ALL app edits → C:\Dev\trajanus-command-center\src\index.html
2. Build command → cd "C:\Dev\trajanus-command-center" && npm run tauri build
3. After successful builds → copy .exe to Google Drive for distribution
4. Google Drive has ELECTRON (old), C:\Dev has TAURI (current)

### DISTRIBUTION:
- Chris/Tom get the .exe file only
- They don't need source code or build tools
- Push updates by rebuilding and sharing new .exe

### CHAT ASSISTANT NAMING:
- Trajanus = The AI assistant in the app
- Knomad Prime = Bill King (the user/developer)
- "Knomad Prime's Workspace" = Bill's workspace (correct)
- Chat assistant name = "TRAJANUS" (not Knomad Prime)

---

## ABSOLUTE RULES (NEVER VIOLATE)

### NEVER DO THESE:

```
- git push (without explicit permission)
- git commit --amend (rewrites history)
- git reset --hard (destroys commits)
- git force push
- Delete folders outside current task scope
- Restructure project directories without explicit approval
- Modify files not specifically part of current task
- Overwrite entire files (use surgical str_replace)
- Run rm -rf on any directory
- Modify .env files without permission
- Change database schemas without approval
- Deploy to production without explicit command
- Edit Google Drive index.html (WRONG FILE - Tauri doesn't load it)
```

### ALWAYS DO THESE:

```
- Create backup before editing any file over 100 lines
- Use str_replace for surgical edits (never rewrite whole files)
- Ask before creating new folders
- Confirm before any git operations
- Report what you're about to do before doing it
- Test changes before reporting success
```

---

## TRUSTED DOMAINS (Auto-Approve Fetch)

These domains are safe to fetch without asking:
- github.com
- raw.githubusercontent.com
- api.github.com
- youtube.com
- lilys.ai
- creatoreconomy.so
- googleapis.com
- docs.google.com
- drive.google.com
- api.anthropic.com
- docs.anthropic.com
- v2.tauri.app
- docs.rs
- crates.io
- npmjs.com
- pypi.org
- stackoverflow.com

---

## AUTO-APPROVED OPERATIONS

### File Operations
- Read any file in project directory
- Create new files in project directory
- Edit files specifically mentioned in current task
- Create markdown documentation
- Create/modify files in .claude/ directory

### Package Management
- pip install (any package)
- npm install (any package)
- cargo add (any crate)

### Safe Commands
- python *.py (run scripts)
- npm run * (package scripts)
- cargo build/run/test
- git status, git log, git diff (read-only)

---

## SKILLS: YouTube Transcript Extraction

### CRITICAL: No Authentication Required
YouTube transcripts are PUBLIC. Never open browser. Never OAuth.

### Method 1: youtube-transcript-api (Preferred)
```python
# pip install youtube-transcript-api
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return ' '.join([entry['text'] for entry in transcript])

# Extract ID from URL: youtube.com/watch?v=VIDEO_ID -> VIDEO_ID
```

### Method 2: yt-dlp (Fallback)
```bash
pip install yt-dlp
yt-dlp --write-auto-sub --sub-lang en --skip-download "URL"
```

### Method 3: Third-Party Sites (If Blocked)
If YouTube blocks IP, fetch from:
- lilys.ai/notes/en/[video-title]
- Other transcript aggregators

### Output Format
Save as: `TRANSCRIPT_{video_id}.md`

---

## SKILLS: File Editing (Large Files)

### NEVER rewrite entire files. Use surgical editing.

### Method: str_replace
```python
# 1. View specific section first
view(path="file.html", view_range=[100, 120])

# 2. Copy EXACT string to replace (including whitespace)
str_replace(
    path="file.html",
    old_str="    exact string here",  # Must be unique in file
    new_str="    new string here"
)

# 3. Verify change
view(path="file.html", view_range=[100, 120])
```

### Common Errors & Fixes

**Error: "String to replace not found"**
- Whitespace doesn't match exactly
- String appears 0 times (typo)
- Copy exact text from view output

**Error: "Multiple matches found"**
- String too generic
- Include more surrounding context
- Use larger unique block

---

## SKILLS: Google Drive Access

### For Reading Files
Use Google Drive API via existing scripts in:
`G:\My Drive\00 - Trajanus USA\00-Command-Center\05-Scripts\`

### For Converting Markdown to Google Docs
```powershell
.\CONVERT_NEW_FILES_ONLY.ps1
```

### CRITICAL: Claude Cannot Read .md from Google Drive
All documentation for Claude access must be converted to Google Docs format.

---

## KNOWN WORKING PATTERNS (Don't Change)

These workflows are tested and working. Don't reinvent them.

### 1. EOS Protocol Files
- Session Summary
- Technical Journal
- Personal Diary
- Code Repository
- Handoff Document
- Context Update

### 2. File Locations
| Item | Path |
|------|------|
| Source Code | C:\Dev\trajanus-command-center\ |
| Runtime | G:\My Drive\00 - Trajanus USA\00-Command-Center\ |
| Scripts | ..\00-Command-Center\05-Scripts\ |
| Skills | ..\00-Command-Center\Skills\ |

### 3. Session Naming
Format: `YYYY-MM-DD-HHMM_[CAT]_[Description]`
Categories: DEV, DEBUG, DOC, REVIEW, EXPLORE, QUICK

---

## COMMON ERRORS LOG (Learn From These)

### Error: Electron binary not found
**Cause:** node_modules corrupted or incomplete
**Fix:**
```bash
rm -rf node_modules
npm install
```

### Error: Permission denied on Google Drive
**Cause:** OAuth token expired
**Fix:** Re-run authentication flow, don't try to force it

### Error: YouTube blocking IP
**Cause:** Rate limiting or VPN detection
**Fix:** Use third-party transcript sites (lilys.ai, etc.)

### Error: Tauri build fails
**Cause:** Usually Rust dependency issue
**Fix:**
```bash
cargo clean
cargo build
```

### Error: File too large to edit
**Cause:** Trying to rewrite entire file
**Fix:** Use str_replace with view_range, never load whole file

---

## LEARNED PATTERNS (Auto-Updated by /reflect)

### Workflow Preferences
- [2026-01-06] YouTube transcripts: Always use established pipeline (batch_ingest_files.py), don't create custom approaches
- [2026-01-06] Check scripts folder and KB for existing solutions before building new ones

### Technical Decisions
- [2026-01-06] Tauri app source: C:\Dev\trajanus-command-center (NOT Google Drive)
- [2026-01-06] Skills location: .claude/skills/ for Claude Code skills

### Communication Preferences
[Patterns extracted from sessions]

### Process Corrections
[Things corrected that shouldn't repeat]

---

## COMMUNICATION PROTOCOL

### With Bill
- Action over affirmation
- No platitudes ("you're right" without verification)
- Direct and professional
- Report what you'll do before doing it
- Ask if uncertain

### Reporting Format
```
TASK: [What I'm doing]
STATUS: [In Progress / Complete / Blocked]
CHANGES: [Files modified]
NEXT: [What comes next]
```

---

## CUSTOM COMMANDS

Available commands (invoke with /command-name):

| Command | Purpose |
|---------|---------|
| /youtube-transcript | Extract YouTube video transcript |
| /eos | End of session protocol |
| /today | Morning startup routine |
| /reflect | Capture session learnings to CLAUDE.md |
| /skill-creator | Create new Claude Code skills |

---

## BEFORE STARTING ANY TASK

1. Read this entire CLAUDE.md
2. Identify which files will be touched
3. Confirm scope with user if unclear
4. Check KNOWN WORKING PATTERNS - don't reinvent
5. Check COMMON ERRORS LOG - don't repeat

---

## END OF CLAUDE.md
