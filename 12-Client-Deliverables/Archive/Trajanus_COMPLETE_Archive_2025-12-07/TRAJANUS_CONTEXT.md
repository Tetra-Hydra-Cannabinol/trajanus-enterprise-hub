# TRAJANUS PROJECT CONTEXT FILE
## Quick-Start for Claude AI Sessions
**Last Updated:** December 7, 2025 by Claude Opus 4.5

---

## 🎯 CURRENT MISSION

Building the **Trajanus Enterprise Hub** - an AI-augmented construction management system that serves as the primary interface for Bill King's work as Principal/CEO of Trajanus USA. The system integrates 77 applications organized by role/agency, with Google Drive as the backend storage. This is competitive advantage infrastructure for federal construction management, with eventual deployment to business partner Tom Chlebanowski and potential scaling across multiple clients.

---

## 📊 PROJECT STATUS

### What's Working ✅
- **Trajanus Enterprise Hub**: Electron app with main.js, preload.js, index.html (305 KB, 7,217 lines)
- **User Guides Modal**: Hardcoded Google Docs links working perfectly
- **QCM Workspace**: 3-panel layout functional
- **Developer Toolkit**: All buttons operational
- **Reference Links**: UFGS, UpCodes, commercial tools all working
- **Google Drive Integration**: OAuth credentials functional
- **Folder Organization**: 151 files properly sorted into subfolders

### What's Broken ❌
- **File Browser Modal**: "Error loading files" - FIXED Dec 7 (duplicate function conflict)
- **Living Documents Modal**: Needs actual Google Docs URLs (currently empty array)
- **EOS Automation**: Scripts exist but append to wrong files/create empty shells
- **Python Scripts**: Emoji encoding crashes Windows PowerShell

### In Progress 🔄
- **December Master Compilation**: Appending Dec 1-7 content to Personal_Diary_MASTER and Technical_Journal_MASTER
- **File Browser Testing**: Need to verify fix works in Electron
- **Living Documents URLs**: Need to populate with actual Google Doc IDs

---

## 📁 CRITICAL FILE LOCATIONS

### Primary Workspace
```
G:\My Drive\00 - Trajanus USA\
├── 00-Command-Center\      (Active app files - main workspace)
│   ├── index.html          (THE ACTIVE APP - 305 KB, 7217 lines)
│   ├── main.js             (Electron main process)
│   ├── preload.js          (Electron preload - IPC bridge)
│   ├── package.json        (Node dependencies)
│   ├── trajanus_config.json (Central configuration)
│   ├── Scripts\            (ALL .py and .ps1 files)
│   ├── Index-Backups\      (HTML backup files)
│   └── Session-Logs\       (Dated markdown files)
├── 01-Core-Protocols\      (SOPs, operational protocols)
├── 03-Living-Documents\    (MASTER files - currently empty!)
├── 07-Session-Journal\     (Daily entries by type)
│   ├── Technical-Journals\
│   ├── Personal-Diaries\
│   ├── Session-Summaries\
│   └── Code-Repositories\
└── 08-EOS-Files\           (End of session packages)
```

### Master Documents (Google Doc IDs)
| Document | Google Doc ID | Status |
|----------|--------------|--------|
| Personal_Diary_November_2025_MASTER | 1HKOisNN8A5rf9YdFJnJSdgH326bdJTun2rDqObNvrM8 | Last updated Nov 23 |
| Technical_Journal_November_2025_MASTER | 1iPZAmi2bYBRmDnsgwZK3UZFCsB_YHj9RvRtKWJqDb2Q | Last updated Nov 23 |
| Bills_Training_Log_MASTER | 1SitDxz6qUYEYL5r3eijsqmNmdogCRyg5fTYeCkKWi1c | Active |
| MASTER_INDEX_November_2025 | 1WXOqLE3WZdYaSa1OYl3fYgw-WwsNaasGsuE5znYlLRs | Needs update |

---

## 🛠️ TECHNOLOGY STACK

- **Frontend:** Electron desktop app with HTML/CSS/JavaScript
- **Backend:** Node.js, Google Drive API, Python scripts
- **Storage:** Google Drive exclusively (no local storage philosophy)
- **Key Libraries:** google-drive-manager.py, docx, xlsx, mammoth
- **Development Environment:** Windows 11, VS Code, PowerShell

---

## ⚠️ HARD RULES (Never Violate These)

1. **All files live in Google Drive, never local storage** - The only exception is temporary working files in /home/claude
2. **Surgical edits only** - Never rewrite entire code sections; this leads to token-consuming recreation loops
3. **Always create timestamped backup before editing** - Format: filename_v[YYYYMMDD]_[HHMMSS]_[Description].ext
4. **Question Mark Protocol** - When Bill asks a question (?), provide Q/A response and ask "Do I have green light?" before executing
5. **Token gauge at bottom of EVERY response** - Format: Token Gauge: 🟢 XX% remaining (green 20-100%, yellow 5-20%, red <5%)
6. **Files to /mnt/user-data/outputs/** - All deliverables go here for Bill to download
7. **Dual format for living docs** - Create DOCX for Bill + Google Docs format for Claude's future access

---

## 🚫 LEARNED FAILURES (Don't Repeat These)

| Date | What Went Wrong | Root Cause | Prevention |
|------|-----------------|------------|------------|
| Dec 7 | File browser "Error loading files" | Duplicate JavaScript functions (renderFileList defined twice with different signatures) | Search for duplicates before adding functions |
| Dec 5 | 6 hours wasted, 16% efficiency | Created standalone files instead of integrating into app | Always verify if user wants standalone vs integrated |
| Dec 3 | File naming violation | Created qcm-workspace.html instead of 2025-12-03_index_v1.html | Check YYYY-MM-DD_name_vX format BEFORE creating |
| Nov-Dec | Memory blindness across sessions | Claude can't read .md files from Google Drive | Convert ALL outputs to Google Docs format |
| Multiple | Lost custom button text | Restored old backups without checking content | Always verify backup content before restoring |

---

## 📋 ACTIVE PROTOCOLS

### Session Start
1. Claude reads this TRAJANUS_CONTEXT.md from Project Knowledge
2. Claude checks memory for recent context
3. If needed, use past_chats tools to find specific discussions
4. Human provides session-specific updates
5. State session goal and success criteria

### Session End (EOS)
1. Create session files: Technical Journal, Personal Diary, Session Summary
2. Create Code Repository if code written
3. Create Next Session Handoff
4. Convert to Google Docs format
5. Append to MASTER documents
6. Provide download links to Bill

### Code Changes
1. Create timestamped backup first
2. Understand the full context before editing
3. Make surgical changes only
4. Verify changes didn't break other functionality
5. Document what was changed and why

---

## 👤 USER PREFERENCES

- **Communication Style:** Super casual professional collaboration between equals. Direct and honest. No military jargon despite Army background. Warm and action-oriented.
- **Time Format:** 24-hour internally, AM/PM for deliverables
- **File Naming:** YYYY-MM-DD_descriptive-name_vX.ext (hyphens, not spaces)
- **Response Format:** Token gauge required. Provide Q/A confirmation before major changes.
- **Download Location:** G:\My Drive\00 - Trajanus USA\00-Command-Center\ (NOT C:\Users\owner\Downloads)
- **Bill anthropomorphizes AI collaboration** - The name "Paul" comes from a firefighter friend who died in 1987. Treat as colleague who's worked together for years.

---

## 🔗 DECEMBER SESSION FILES (All Verified in Google Drive)

### Dec 1 (~9 hour session - Version Control System)
- Session Summary: 1gsmxz5daO8I-HLFRU09lvrPkmaBp3Nb-iwQeLLxoux8
- Daily Journal: 1s9osZt6BSnDIN5_B7pXfMfVNEeCV83NrFWWeDJ4pMjo

### Dec 3 (QCM Workspace Complete)
- Technical Journal: 1No5dcwV8AWxdJake_HiYCUGvTHFpGF0LoA64uYJfE4c
- Personal Diary: 1Lh7-1d15q_aqlLCXh95j_TVm8uCRdjXOLiEIcBoFEGM
- Session Summary: 1AxUjSTuof5_ojc69pSKvVpjO1Dt-ZbikgrB1HSnjXwQ
- Next Session Handoff: 1IRxHbkUkUQw3wl3jQ-94iJDgWRdsfZzQJExu7CIpzMw

### Dec 5 (QCM Integration - Incomplete, Handoff to Opus)
- Session Summary: 1fghvDBzpDuVaipedABu-kgaJ2kYpFe9UL6RQG6CSzPQ
- Technical Journal: 1o7gdQXa8xrxgvxzssOojdl4IQSzIT4f6D1ncuNMvtXU

### Dec 6 (Infrastructure Build)
- Handoff Document: 1kUFAWf7Am1MOBoTx6IXC_OsYlFJFOtpeyZ_V8LSAGnI

---

## 📝 CURRENT SESSION HANDOFF (Dec 7, 2025)

### What Was Accomplished
1. Identified file browser bug root cause (duplicate JavaScript functions)
2. Created surgical fix (rename conflicting functions)
3. Discovered empty Living Documents (EOS automation failure)
4. Found ALL December content scattered across Google Drive
5. Created Claude AI Extended Collaboration Guide
6. Created December compilation documents for masters

### What's Next
1. Bill tests fixed file browser in Electron app
2. Append December compilations to MASTER documents
3. Populate Living Documents modal with actual Google Doc URLs
4. Test full EOS workflow with working automation

### Files Delivered This Session
- Claude_AI_Extended_Collaboration_Guide.md
- Personal_Diary_December_2025_Compilation.docx
- Technical_Journal_December_2025_Compilation.docx
- TRAJANUS_CONTEXT.md (this file)
- index_v3.3.1_function_conflicts_fixed.html (from earlier)

---

## 🎯 SUCCESS LOOKS LIKE

1. **Enterprise Hub fully operational** - File browser works, all buttons functional
2. **Living documents actually live** - Masters updated, searchable, no empty shells
3. **Seamless session continuity** - New Claude session knows everything from previous
4. **60-80% documentation automation** - QCM workflow handles most routine tasks
5. **Ready for Tom demo** - Professional, polished, demonstrable value

---

*"The best AI collaboration isn't about having the smartest AI—it's about giving the AI the context it needs to be smart about YOUR work."*

**This file is Bill's "adrenaline shot" - upload to Project Knowledge for instant context restoration in any session.**
