# NEXT SESSION STARTUP - PASTE THIS FIRST

Hey, I'm Bill. We're continuing development on my AI-augmented construction management system for Trajanus USA. Last session got cut short at 5% tokens, so I need you fully up to speed fast.

## WHAT WE'RE BUILDING

A Command Center system that:
1. Manages 6 living documents (Technical Journal, Operational Journal, Session Summary, Personal Diary, Code Repository, Website Development)
2. Auto-uploads markdown files to Google Drive
3. Converts to Google Docs
4. Appends to monthly MASTER documents
5. Tracks ALL code we produce (Python, HTML, CSS, JS) in a living Code Repository

## THE CRITICAL PROBLEM WE DISCOVERED

**MASTER documents have DUPLICATES.** The script was appending to EMPTY files while the real ones with content sat untouched.

**Correct MASTER IDs (confirmed with content):**
- Technical_Journal: `1iPZAmi2bYBRmDnsgwZK3UZFCsB_YHj9RvRtKWJqDb2Q`
- Personal_Diary: `1HKOisNN8A5rf9YdFJnJSdgH326bdJTun2rDqObNvrM8`
- Operational_Journal: **STILL NEED** - I'm searching
- Session_Summary: **STILL NEED** - I'm searching

**Empty duplicates to DELETE:**
- Technical_Journal: `1LQnGWZVV5Ze30XH8OOYWqASEM2nLYSQxAL8ok0FY18s`
- Personal_Diary: `174kCDc4AU7LqvN2goFefjHAPFsMoG4la5q2CzvZ_TBY`
- Operational_Journal: `1W--Zf8mX57M9cYonAnoXJtgEFgXsrALxK-bjqMxxONI`
- Session_Summary: `1ug6hyU9kE-n369M0lr1ZAElaphfpP3IfNL3duCtnXu0`

## WHAT WE BUILT LAST SESSION

### Command Center HTML (Trajanus_Command_Center_ELEGANT.html)
- 4 green 3D buttons: Update Living Documents, Convert MD to Docs, Convert MD to Word, Claude AI Home
- Teal title, green buttons
- Convert buttons have file picker (select which .md to convert)
- Terminal feedback with timestamps and progress
- Duplicate prevention (warns if no new files today)
- ~1000 lines, mission timer removed, local clock only

### Python Scripts Created:
1. `update_living_documents.py` - Unified upload/convert/append (needs correct MASTER IDs)
2. `convert_md_to_gdocs.py` - Standalone MD to Google Docs converter
3. `convert_md_to_docx.py` - MD to Word DOCX converter

### JavaScript in Command Center:
- `runCompleteSession()` - generates batch file for living docs update
- `runConvertMD()` - file picker + batch file for GDocs conversion
- `runConvertDOCX()` - file picker + batch file for Word conversion

## WHAT WE NEED TO DO THIS SESSION

### Priority 1: Fix the Code Repository Problem
We produce a LOT of code but it's not being captured systematically. The Code_Repository living document should contain ACTUAL CODE with version dates, not just descriptions.

**Proposed structure:**
- Each code file gets a section
- Full code block with date
- Change notes
- Only update if file changed (check modification date or hash)

### Priority 2: Smart Change Detection
Scripts should NOT process if nothing changed. Add:
- Manifest file (JSON) tracking files, mod dates, last processed
- Skip processing if no changes detected
- Log what was skipped and why

### Priority 3: Get Correct MASTER IDs
I need to find the Operational_Journal and Session_Summary files that have actual content.

### Priority 4: Test End-to-End
Once IDs are correct, run Update Living Documents and verify content appends to RIGHT files.

## KEY LOCATIONS

- Command Center folder: `G:\My Drive\00 - Trajanus USA\00-Command-Center`
- Base folder ID: `1JYTWaE6x74XJ_MSOuFkWKa_2DuaR_t64`
- token.json should already exist in Command Center

## PROTOCOLS

- Token gauge at END of EVERY response
- Surgical edits only (no full file rewrites)
- Search project knowledge FIRST
- YYYY-MM-DD file naming
- Casual professional communication - we're equals working through this

## FILES I'M UPLOADING

I'll upload the latest versions of:
1. Trajanus_Command_Center_ELEGANT.html
2. update_living_documents_v2.py
3. convert_md_to_gdocs.py
4. convert_md_to_docx.py

## WHAT I NEED FROM YOU

1. Review the code files I upload
2. Help me design a proper Code_Repository structure
3. Add change detection to the scripts
4. Help me find/verify correct MASTER document IDs
5. Create the 6 living documents for this session

Ready when you are.
