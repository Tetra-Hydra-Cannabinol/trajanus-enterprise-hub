# Trajanus Command Center - Change Log

## Purpose
Track significant changes, decisions, and lessons learned across development sessions. This is a living document that helps prevent repeated mistakes and provides context for future AI assistants.

---

## 2025-12-13 - Supabase Integration Failure (CRITICAL INCIDENT)

### What Happened
Attempted to integrate Supabase Knowledge Base browser into QCM workspace. Multiple cascading failures resulted in broken app that couldn't launch.

### Timeline
1. Modified main.js to add Supabase IPC handlers
2. Modified preload.js to expose Supabase methods
3. Modified index.html to add Supabase KB browser tab
4. Assumed RPC functions existed (`list_knowledge_sources`, `search_by_text`, `get_url_content`)
5. Got 401 errors - functions didn't exist
6. Tried to fix by switching to direct table queries
7. Added `@supabase/supabase-js` to package.json dependencies
8. Tried `npm install` - failed with TAR_ENTRY_ERROR (Google Drive locking)
9. Tried to delete node_modules to clean install - Google Drive blocked deletion
10. Corrupted node_modules/.bin directory
11. Corrupted node_modules/electron/package.json
12. App wouldn't launch - "electron is not recognized"

### Root Causes
1. **Assumed RPC Functions Existed** - Wrote integration code without verifying database schema first
2. **npm on Google Drive** - Attempted `npm install` which fails due to file locking
3. **Tried to Delete node_modules** - Google Drive locking prevented proper deletion, caused corruption
4. **No Backup Before Changes** - Modified working code without creating backup first
5. **Didn't Test Standalone** - Should have created test-supabase.js to verify queries work

### Lessons Learned
1. **ALWAYS verify database schema** before writing integration code
2. **NEVER run npm install on Google Drive** - use existing node_modules only
3. **NEVER delete node_modules on Google Drive** - will cause corruption
4. **ALWAYS backup before major changes** - especially index.html and main.js
5. **Test standalone before integrating** - create test scripts first
6. **Use knowledge base tools** - could have found previous Supabase discussions

### Recovery Actions
1. Restored index.html from backup: `index_ARCHIVE_2025-12-12_1700_BeforeFunctionRename.html`
2. Restored main.js from archive: `Archive/Trajanus_COMPLETE_Archive_2025-12-07/main.js`
3. Manually created node_modules/.bin/electron.cmd shim
4. Created minimal node_modules/electron/package.json
5. App still won't launch - electron binary missing from dist folder
6. **RESOLVED 2025-12-14:** Electron binary restored via local npm install and copy back

### Files Affected
- main.js (restored to clean state)
- preload.js (still has Supabase stubs - harmless)
- index.html (restored to clean state)
- package.json (has Supabase dependency - harmless)
- node_modules/electron (corrupted - needs full reinstall)

### Going Forward
- Supabase integration will be done properly:
  1. Verify schema with direct Supabase query
  2. Create standalone test script
  3. Backup working files
  4. Implement in main.js
  5. Test before modifying index.html

---

## 2025-12-15 - TKB Supabase Browser Implementation (SUCCESS)

### What Changed
Implemented TKB Browser modal to browse and search 1,805 documents in Supabase knowledge base directly from the Electron app.

### Implementation
1. **Re-added KB IPC handlers to main.js** (lines 247-333)
   - 7 handlers: kb:search, kb:listSources, kb:getByUrl, kb:browseBySource, kb:getRecent, kb:getCategories, kb:testConnection
   - All wrap kbService functions from services/kb-service.js

2. **Added window.kb API to preload.js** (lines 91-137)
   - Exposes 7 KB methods to renderer process
   - search, listSources, getByUrl, browseBySource, getRecent, getCategories, testConnection

3. **Created openTKBBrowser() in index.html** (lines 6530-6904)
   - Dynamic modal creation (same pattern as Living Docs Browser)
   - Brown/orange theme (#9B7E52, #7B6142)
   - Search input with Enter key support
   - Category dropdown populated from Supabase
   - Document list grouped by source category
   - Document viewer modal with content display
   - Copy content to clipboard functionality

4. **Updated Search KB button** (line 2421-2426)
   - Changed onclick from placeholder to openTKBBrowser()
   - Updated description to "Browse 1,805 documents"

### Functions Created
- `openTKBBrowser()` - Main modal opener
- `closeTKBBrowser()` - Close modal
- `loadTKBSources()` - Load all documents from Supabase
- `loadTKBCategories()` - Populate category dropdown
- `searchTKB()` - Search using window.kb.search()
- `renderTKBDocs(docs)` - Render document list
- `viewTKBDocument(url)` - Load and display document content
- `closeTKBDocViewer()` - Close document viewer
- `copyTKBContent()` - Copy document content

### Files Modified
- `main.js` - Added KB IPC handlers (87 lines)
- `preload.js` - Added window.kb API (47 lines)
- `index.html` - Added TKB Browser functions (~380 lines), updated button

### Testing
- App starts successfully with "Trajanus Enterprise Hub - Main process initialized"
- Supabase credentials verified in .env
- Uses existing kb-service.js (created 2025-12-14)

---

## 2025-12-14 - TASK-010: KB IPC Integration (SUCCESS)

### What Changed
Implemented full Supabase Knowledge Base integration via Electron IPC. The app can now directly query the KB without relying on MCP.

### Implementation
1. **Created KB Service Module:** `services/kb-service.js`
   - Loads .env manually (no dotenv package - Google Drive npm issue)
   - Provides 7 KB functions: search, listSources, getByUrl, browseBySource, getRecent, getSourceCategories, testConnection
   - Uses RPC functions with direct query fallback

2. **Added IPC Handlers to main.js:**
   - `kb:search` - Search knowledge base
   - `kb:listSources` - List all sources
   - `kb:getByUrl` - Get document by URL
   - `kb:browseBySource` - Browse by category
   - `kb:getRecent` - Get recent documents
   - `kb:getCategories` - Get source categories
   - `kb:testConnection` - Test connection

3. **Exposed API in preload.js:**
   - `window.kb` object with all KB methods

4. **Created Test Script:** `test-kb-ipc.js`
   - 6 tests, all passing

### Additional Fix
- **node_modules corruption:** Found 327 corrupted package.json files (0 bytes) from Dec 13 incident
- **Solution:** Rebuilt entire node_modules locally at `C:\temp\electron-fix`, renamed corrupted folder, copied fresh node_modules to Google Drive

### Files Created
- `services/kb-service.js` - KB service module
- `test-kb-ipc.js` - Integration test script

### Files Modified
- `main.js` - Added KB IPC handlers (~340 lines now)
- `preload.js` - Added window.kb API (~160 lines now)
- `.claude.md` - Updated documentation

### Test Results
```
KB SERVICE INTEGRATION TESTS
PASSED: 6
FAILED: 0
All tests passed! KB integration is working.
```

### Lessons Learned
1. **Check node_modules health** - Many package.json files were 0 bytes from Dec 13
2. **Local npm install works** - Can rebuild on local drive and copy to Google Drive
3. **Manual .env loading** - Works without dotenv package dependency

---

## 2025-12-14 - Added Startup Log Message

### What Changed
Added console.log statement to display version info on app launch.

### Implementation
- Modified `main.js` line 41-44
- Changed `app.whenReady().then(createWindow)` to arrow function block
- Added `console.log('Trajanus Hub v1.0 starting...');` before `createWindow()`

### Files Modified
- `main.js` - Added startup log in ready handler

### Testing
- Ran `npm start` - Message appears in terminal before window opens
- App launches normally, no errors

---

## 2025-12-14 - TASK-008: Verified Supabase Schema (SUCCESS)

### What Changed
Verified Supabase knowledge base schema, data, and RPC functions.

### Key Findings
- **Table:** `knowledge_base` (single table design, as intended)
- **Rows:** 1,805 total, 84 unique documents
- **Embeddings:** 99.9% coverage (vector 1536 dimensions)
- **RPC Functions:** All 4 working
  - match_knowledge_base (vector search)
  - list_knowledge_sources
  - search_by_text (full-text)
  - get_url_content

### Data Distribution
- Session History: 420 rows
- Living Documents: 351 rows
- Core Protocols: 216 rows

### Schema Status
- ✅ Production ready
- ✅ Indexes configured
- ✅ RLS policies active

### Files Created
- `TASK-005_Supabase_Schema_Report.md` - Full verification report
- `C:\temp\electron-fix\test-supabase-schema.py` - Test script
- `C:\temp\electron-fix\test-supabase-detailed.py` - Detailed test script

### Recommendations
- Schema is solid, proceed with IPC integration
- Consider adding OpenAI key for vector search

---

## 2025-12-14 - TASK-007: Fixed Trajanus KB MCP (SUCCESS)

### What Changed
Fixed the trajanus-kb MCP server that was failing to connect.

### Root Causes Identified
1. **Truncated Supabase URL** - .env had `iaxtwrswinygwwwd.supabase.co` but should be `iaxtwrswinygwwwdkvok.supabase.co`
2. **Missing OpenAI API Key** - Original script required OpenAI for embeddings
3. **Wrong env var name** - Script used `SUPABASE_SERVICE_KEY` but .env has `SUPABASE_ANON_KEY`
4. **.env path issue** - Script ran from 05-Scripts but .env in parent directory

### Fixes Applied
1. **Fixed Supabase URL** in .env (decoded JWT to find correct ref)
2. **Rewrote MCP server** to use text search instead of vector embeddings
3. **Fixed env var name** to use `SUPABASE_ANON_KEY`
4. **Fixed .env path** loading using pathlib
5. **Added UTF-8 encoding** for Windows compatibility

### Testing Results
- Connection test: PASS
- Search test: PASS (found 3 results for "QCM workflow")
- MCP list shows: `trajanus-kb: ✓ Connected`

### Files Modified
- `.env` - Fixed Supabase URL
- `05-Scripts/kb_mcp_server.py` - Simplified (no OpenAI needed)

### Lessons Learned
1. **Decode JWT to verify credentials** - JWT contains the correct Supabase ref
2. **Text search works without embeddings** - Can use ilike for basic search
3. **Check .env path when running from subdirectory** - Use pathlib for reliable paths

---

## 2025-12-14 - TASK-002: Electron Fix + Playwright MCP (SUCCESS)

### What Changed
Fixed corrupted Electron installation and set up Playwright MCP for visual validation.

### Electron Fix
**Problem:** node_modules/electron corrupted from Dec 13 incident - binary missing

**Solution:**
1. Created temp directory: `C:\temp\electron-fix`
2. Created minimal package.json with electron ^28.0.0
3. Ran `npm install` on local drive (not Google Drive!)
4. Copied fresh electron folder to Google Drive
5. Verified with `npm start` - SUCCESS

**Key Insight:** Can run npm on local drive, then copy results to Google Drive. This works!

### Playwright MCP Setup
**Installation:**
```bash
claude mcp add playwright -s user npx @playwright/mcp@latest
```

**Verification:**
```bash
claude mcp list
# Shows: playwright: npx @playwright/mcp@latest - Connected
```

**Electron Testing:**
- Playwright MCP is for browser control, not Electron apps
- Created custom test script using Playwright's `_electron.launch()` API
- Installed Playwright at `C:\temp\electron-fix`
- Successfully captured 5 screenshots of running app

### Files Created
- `playwright-research.md` - Research findings
- `playwright-validation-workflow.md` - How to use for UI validation
- `test-playwright-electron.js` - Screenshot test script
- `screenshots/` - Directory with test screenshots

### Screenshots Captured
- main-window.png
- qcm-workspace.png
- viewport-desktop.png (1920x1080)
- viewport-laptop.png (1366x768)
- viewport-tablet-landscape.png (1024x768)

### Lessons Learned
1. **npm install works on local drive** - Copy results to Google Drive after
2. **Playwright MCP vs Playwright Electron API** - MCP for browsers, `_electron` API for Electron apps
3. **Test scripts need Playwright locally** - Installed at C:\temp\electron-fix, run from there

---

## 2025-12-14 - Infrastructure Foundation Day (TASK-001)

### What We Built
Created proper orchestration framework for AI-augmented development:
1. .claude.md context system - Persistent project knowledge - COMPLETE
2. changelog.md - Decision log and lessons learned - COMPLETE
3. plan.md - Task tracking - COMPLETE
4. Playwright MCP - Visual validation - COMPLETE
5. My Developer workflow - Planner + Developer pattern (pending)
6. Sub-agent library (pending)
7. Command library (pending)

### Why This Matters
- **Before:** Ad-hoc development, excessive grep operations, repeated mistakes
- **After:** Context-driven, validated, systematic development

### Expected Outcomes
- 90% reduction in grep operations (context in .claude.md)
- No repeated mistakes across sessions (lessons in changelog.md)
- Seamless handoffs between Claude instances
- Professional development workflow

### Files Created
- `.claude.md` - Main project context (comprehensive)
- `changelog.md` - This file
- `plan.md` - Task tracking

### Architecture Decision
- **No separate workspace directories** - All workspaces (Developer, PM, QCM) are within index.html
- **Single-file UI approach** - Easier to backup/restore, no build step required
- **Documented in .claude.md** - Quick reference section for finding code

---

## 2025-12-12 - Function Rename Session

### What Changed
Renamed functions in index.html for clarity. Last known working state before Supabase attempt.

### Backup Created
`index_ARCHIVE_2025-12-12_1700_BeforeFunctionRename.html`

### Status
This is the recovery point used after Dec 13 failure.

---

## 2025-12-11 - Developer Project Integration

### What Changed
Added Developer Project workspace with enhanced functionality.

### Backups Created
- `index_BACKUP_2025-12-11_1952_PreDeveloperProject.html`
- `index_2025-12-11_2029_DeveloperProject_Complete.html`

---

## 2025-12-07 - Complete Archive Created

### What Changed
Created full archive of working project state.

### Location
`Archive/Trajanus_COMPLETE_Archive_2025-12-07/`

### Contents
- main.js (clean, no Supabase)
- preload.js
- index.html

### Importance
This archive was used to restore main.js after Dec 13 failure.

---

## Template for Future Entries

### YYYY-MM-DD - [Change Title]

**What Changed:** [Brief description]

**Why:** [Reasoning for change]

**Files Affected:** [List of files]

**Backup Created:** [Backup filename if applicable]

**Testing Done:** [How it was verified]

**Issues Found:** [Any problems discovered]

**Lessons:** [What we learned]

**References:** [Related files, commits, sessions]

---

## Quick Reference: Common Mistakes to Avoid

| Mistake | Consequence | Prevention |
|---------|-------------|------------|
| npm install on Google Drive | TAR_ENTRY_ERROR, corruption | Never do it. Copy to local drive first |
| Delete node_modules on GDrive | File locks, partial deletion | Never do it. Rename instead if needed |
| No backup before changes | Lost working state | Always backup index.html and main.js |
| Assume DB schema | 401/404 errors | Query information_schema first |
| Skip standalone testing | Integration bugs | Create test script first |

---

**Last Updated:** 2025-12-15
**Maintained By:** Claude Code
