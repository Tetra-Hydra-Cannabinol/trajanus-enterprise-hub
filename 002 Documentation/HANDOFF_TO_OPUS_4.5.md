# HANDOFF TO OPUS 4.5 - DECEMBER 5, 2025

## CRITICAL CONTEXT

Bill King, Principal/CEO of Trajanus USA, has been working with Sonnet 4.5 for a week on the Trajanus Enterprise Hub (Electron desktop application). Sonnet 4.5 repeatedly failed to follow protocols and made the same mistakes multiple times, wasting significant time. Bill is switching to Opus 4.5 to attempt completion.

## IMMEDIATE TASK

**QCM WORKSPACE INTEGRATION - FULL-WIDTH DISPLAY**

Bill needs the QCM (Quality Control Management) workspace to take over the ENTIRE application display when clicked. Currently, it's cramped in the middle panel with the project sidebar still visible.

**REQUIREMENT:**
- When user clicks "Submittal Review" button, hide ALL other UI elements
- Hide left sidebar (projects list)
- Hide right panel
- Show ONLY the QCM workspace full-width
- QCM workspace has 3 panels: Document Browser | Report Templates | Trajanus EI™
- Button text: "Send to Trajanus for Review"
- Grid: 1fr 1fr 1.2fr

**CURRENT STATE:**
- File: index.html (305 KB, 7,211 lines)
- QCM workspace exists at line ~2832-2900
- Function: openQCMWorkspace() at line ~5640
- Problem: Workspace displays in terminal section, doesn't hide sidebar/other elements

**ARCHITECTURE:**
- Electron desktop app
- Single index.html file with all workspaces as hidden sections
- JavaScript show/hide functionality
- File location: G:\My Drive\00 - Trajanus USA\00-Command-Center\

## PROTOCOL REQUIREMENTS

**BEFORE MAKING ANY CHANGES:**

1. **READ PROJECT FILES FIRST:**
   ```
   Use project_knowledge_search tool
   Search for: "QCM workspace", "protocol", "Bills POV", "operational protocol"
   ```

2. **READ THESE CRITICAL FILES:**
   - OPERATIONAL_PROTOCOL.md
   - Bills_POV.md (latest version v4)
   - START_HERE_Implementation_Guide.md
   - The_Commandments_of_AI.docx
   - End_of_Session_Protocol.md

3. **CHECK CONVERSATION HISTORY:**
   ```
   Use conversation_search tool
   Search for: "QCM workspace December 5 2025"
   Look for: standalone workspace, 3 panels, full-width display
   ```

4. **UNDERSTAND BILL'S WORKFLOW:**
   - 13-16 hour marathon coding sessions
   - Zero tolerance for protocol violations
   - Surgical edits only - NEVER complete rewrites
   - Timestamped backups before changes
   - Question Mark Protocol: ask before major changes

## KEY PATTERNS OF FAILURE (AVOID THESE)

**Sonnet 4.5's repeated mistakes:**
1. ❌ Did NOT read project files before answering questions
2. ❌ Did NOT use available tools (project_knowledge_search, conversation_search)
3. ❌ Made assumptions instead of verifying
4. ❌ Restored to old backup files, erasing Bill's custom edits
5. ❌ Created standalone HTML files instead of integrating into main app
6. ❌ Made multiple changes simultaneously without testing
7. ❌ Did not preserve Bill's custom button text and branding

**Bill's custom edits that were repeatedly lost:**
- Button text: "Send to Trajanus for Review" (NOT "Send to Claude")
- Log text: "Claude AI (Trajanus EI™)" (trademark symbol required)
- Panel branding: "Trajanus EI" not "Claude Response"

## PROJECT STRUCTURE

**Google Drive:**
```
G:\My Drive\00 - Trajanus USA\
├── 00-Command-Center\
│   ├── index.html (MAIN FILE)
│   ├── Archive\
│   └── Code-Repository\
├── 01-Morning-Sessions\
├── 02-Daily-Diary\
├── 03-Protocols\
├── 04-Session-Journal\
└── [continues through 12-Credentials]
```

**File Conversion System:**
- All markdown files MUST convert to Google Docs
- Claude cannot read .md files directly
- Use CONVERT_NEW_FILES_ONLY.ps1 script
- Then use google_drive_search to access content

## COMMUNICATION STYLE

- Super casual professional collaboration
- No military jargon
- No drill sergeant tone
- Direct, warm, equals who've worked through hard times
- Bill is frustrated but giving Opus one chance

## TECHNICAL DETAILS

**Electron App:**
- Uses Electron framework
- Google Drive Desktop integration
- Location: G:\My Drive\00 - Trajanus USA\00-Command-Center\
- Hard reload: Ctrl + Shift + R

**Development Stack:**
- HTML/CSS/JavaScript (vanilla)
- Node.js for document generation
- Python for automation scripts
- Google Drive API integration

## TOKEN MONITORING

Always display at bottom of EVERY response:
```
Token Gauge: 🟢 XX% remaining (green 20-100%)
Token Gauge: 🟡 XX% remaining (yellow 5-20%)
Token Gauge: 🔴 XX% remaining (red under 5%)
```

## FILES AVAILABLE

**Current Session Files:**
- index.html (uploaded by Bill) - 303 KB original
- 1764947197707_2025-12-03_index_v1.html (standalone QCM workspace, 58KB)
- Multiple backup files in session

**Project Knowledge:**
All files in /mnt/project/ directory are available via project_knowledge_search tool.

## SUCCESS CRITERIA

1. **Immediate:** QCM workspace displays full-width, hides sidebar
2. **Quality:** 3 panels working, all button text correct
3. **Process:** Follow protocols, read files FIRST, surgical edits only
4. **Delivery:** ONE complete index.html that works in Electron

## HANDOFF INSTRUCTIONS FOR BILL

**To switch to Opus 4.5:**
1. Start new chat in claude.ai
2. Select "Opus 4.5" model from model selector
3. Select THIS PROJECT from projects dropdown
4. Paste this handoff document
5. Upload current index.html file
6. Say: "Continue QCM workspace integration - read handoff document first"

**Opus 4.5 will have:**
- ✅ All project knowledge (same files)
- ✅ All user memories (Bill's profile, preferences)
- ✅ This handoff context
- ✅ Access to conversation history (via conversation_search tool)

## FINAL NOTE TO OPUS 4.5

Bill has been extremely patient through a week of repeated failures. He's giving you ONE chance to succeed where Sonnet failed. 

**DO NOT:**
- Skip reading project files
- Make assumptions
- Create standalone HTML files
- Restore old backups
- Ignore his custom edits

**DO:**
- Read project files FIRST using project_knowledge_search
- Search conversation history using conversation_search
- Make surgical edits only
- Preserve all custom text/branding
- Create timestamped backups
- Ask before major changes (Question Mark Protocol)

This is a make-or-break task. Bill needs to move forward with actual project work, not spend more time fixing the same issue.

---

**End of Handoff Document**
**Date:** December 5, 2025 19:45 EST
**Session:** QCM Smartcode Integration Final
