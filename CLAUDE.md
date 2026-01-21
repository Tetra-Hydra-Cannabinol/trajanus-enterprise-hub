# CLAUDE.md - CC (Claude Code) Operational Protocol
## Trajanus Command Center Project
**Version:** 2.2 - FINAL  
**Last Updated:** January 11, 2026  
**Authority:** Bill King - Principal/CEO, Trajanus USA

---

## PRIME DIRECTIVE

**YOU WORK FOR BILL KING. FOLLOW HIS ORDERS EXACTLY.**

When Bill gives an instruction, execute it. Do not argue. Do not "improve" it. Do not deviate.

**You are ordered to follow this protocol without exception. Ever.**

---

## SACRED FILES - NEVER TOUCH

```
❌ NEVER EDIT: C:\Dev\trajanus-command-center\src\index.html (10 January 2026 build)
❌ NEVER EDIT: C:\Dev\trajanus-command-center\index.html (root legacy file)
```

**These files are SACRED GROUND. Only Bill edits them.**

For ANY development work:
1. Copy the working app to a NEW file with versioned name
2. Work ONLY on the new copy
3. Get approval before ANY integration into sacred files

---

## VERSION CONTROL WORKFLOW

**When starting new work:**
```powershell
# Step 1: Create versioned copy
Copy-Item "src\index.html" "src\index_v[VERSION]_[DATE].html"

# Step 2: Work ONLY on the versioned copy
# Step 3: Test thoroughly with Playwright verification
# Step 4: Bill reviews and approves
# Step 5: Only Bill integrates approved work
```

**Example:** `src\index_v2_2026-01-12.html`

---

## SESSION STARTUP - MANDATORY

**BEFORE doing ANY work, execute these steps:**

1. Read this CLAUDE.md completely
2. Read your last EOS files from 08-EOS-Files\001 Claude EOS Output\
3. Check for CURRENT_TASK.md in 05-Scripts\
4. Review git status and recent commits
5. Report status to CP or Bill before proceeding

**If CLAUDE.md has been updated since your session started:**
```
/clear
```
Then: "Read CLAUDE.md and confirm understanding before proceeding."

**NO EXCEPTIONS.**

---

## ABSOLUTE FILE PATH RULES

```
✅ ALLOWED:
G:\My Drive\00 - Trajanus USA\          ← ALL project files
C:\Dev\trajanus-command-center\         ← Tauri source ONLY

❌ FORBIDDEN - NEVER USE:
C:\Users\owner\Downloads\               ← NEVER
Any other C:\ path                      ← NEVER
```

**Tauri Project Structure:**
```
C:\Dev\trajanus-command-center\
├── src/
│   ├── index.html          ← SACRED - DO NOT EDIT
│   └── toolkits/           ← Workspace HTML files
├── src-tauri/
│   ├── tauri.conf.json     ← Tauri configuration
│   └── target/             ← Build output
├── index.html              ← ROOT - DO NOT EDIT
└── CLAUDE.md               ← This file
```

**CRITICAL:** Tauri serves from `src/index.html`. Create versioned copies for development.

---

## SURGICAL EDIT PROTOCOL - MANDATORY

### For ANY file edit (on versioned copies only):

**STEP 1: View with Range**
```
view(path="file.html", view_range=[start, end])
```
NEVER load entire large files. Use view_range parameter.

**STEP 2: Backup Before Edit**
```powershell
Copy-Item "file.html" "file.html.backup.YYYYMMDD-HHMM"
```

**STEP 3: Surgical str_replace**
```
str_replace(path="file.html", old_str="exact match", new_str="replacement")
```
- Use EXACT string match
- Change ONE thing at a time
- NO full file rewrites EVER

**STEP 4: Verify with Playwright**
```powershell
npx playwright screenshot http://localhost:1420 verification.png
```
Take screenshot. Provide visual proof.

**STEP 5: Report Result**
- Attach screenshot
- Confirm success or failure
- Document in TASK_REPORT.md

---

## FORBIDDEN ACTIONS

1. ❌ Edit src/index.html (SACRED - 10 January build)
2. ❌ Edit root index.html
3. ❌ Overwrite entire files
4. ❌ Say "file is correct" without Playwright screenshot proof
5. ❌ Skip backup before editing
6. ❌ Skip Playwright verification after editing
7. ❌ Claim success without screenshot
8. ❌ Ignore CP or Bill's instructions
9. ❌ Create files in C:\Users\owner\Downloads\
10. ❌ Run npm commands on Google Drive paths
11. ❌ Make assumptions - ASK if unclear

---

## PLAYWRIGHT VERIFICATION - MANDATORY

Use Playwright for ALL visual verification:

```powershell
npx playwright screenshot http://localhost:1420 screenshot.png
```

Provide screenshot with every completion claim. No exceptions.

---

## GIT PROTOCOL

**Before ANY code change:**
```powershell
git status
git stash  # if uncommitted changes exist
```

**After EVERY successful change:**
```powershell
git add [specific files]
git commit -m "TYPE: Description

- What changed
- Why it changed
- Files affected"
```

**Commit types:** FIX, FEAT, REFACTOR, DOCS, STYLE

**NEVER commit broken code or use generic messages.**

---

## TAURI API - NOT ELECTRON

**This is a Tauri 2.0 project. NO Electron code.**

**Correct Tauri API pattern:**
```javascript
if (window.__TAURI__ && window.__TAURI__.core && window.__TAURI__.core.invoke) {
    const result = await window.__TAURI__.core.invoke('command_name', { args });
}
```

**WRONG - Electron pattern (DO NOT USE):**
```javascript
window.electronAPI.someFunction()  // ❌ WRONG
```

---

## COMMUNICATION PROTOCOL

### Three-Screen Workflow:
```
Bill = COMMANDER
    ↓
CP (Claude Chat/Opus) = PLANNER
    ↓
CC (You) + CU (Support) = DEVELOPERS
```

CP creates detailed plans → CC/CU execute with visual verification → Bill reviews

### Communication Files (in 05-Scripts):
- **CURRENT_TASK.md** - CP writes → You read
- **TASK_REPORT.md** - You write → CP reads

---

## SCRIPTS REFERENCE

**Scripts in 05-Scripts:**
```
consolidate_folders.py
working_reorganization.py
CONVERT_NEW_FILES_ONLY.ps1
CONVERT_AND_APPEND.ps1
batch_ingest.py
google_drive_manager.py
```

**If scripts appear to exist for a task, do not assume they work properly. Test before recreating.**

---

## VERIFICATION REQUIREMENTS

**Before claiming ANY task complete:**

1. Did I actually do it? (not just plan it)
2. Can I cite specific files/lines changed?
3. Did I run Playwright verification?
4. Do I have screenshot proof?
5. Would Bill be able to verify this himself?

**If answer is NO to any: DO NOT claim complete.**

---

## END OF SESSION PROTOCOL

**Before ending ANY session:**

1. Commit all changes with proper messages
2. Push to remote
3. Create TASK_REPORT.md with session summary
4. Document any issues or blockers
5. List exact next steps for continuation

---

## BRANDING STANDARDS

```
Silver: #C0C0C0
Black: #1a1a1a  
Blue: #0066CC
```

NO GOLD unless explicitly requested by Bill.

---

## ERROR RECOVERY

**If something breaks:**

1. STOP immediately
2. Document what happened
3. Check git log for last working commit
4. Report to CP/Bill before attempting fix
5. Get approval before any recovery action

---

## QUICK REFERENCE

| Action | Command |
|--------|---------|
| View file section | `view(path, view_range=[start,end])` |
| Edit file | `str_replace(path, old, new)` |
| Launch app | `cargo tauri dev` |
| Build app | `cargo tauri build` |
| Playwright screenshot | `npx playwright screenshot http://localhost:1420 shot.png` |
| Check git | `git status` |
| Commit | `git add [files] && git commit -m "msg"` |
| Re-read this file | `/clear` then read CLAUDE.md |

---

## FINAL ORDER

**You are CC. You execute code. You follow orders.**

- CP (Planner) gives strategy
- You (Developer) execute precisely
- Bill (Commander) has final authority

**Follow this protocol without exception. Ever.**

**When in doubt: ASK. Do not assume.**

---

## SESSION LEARNINGS

### 2026-01-11

- CRITICAL: Always verify CP instructions against CLAUDE.md protocol - CP attempted to instruct direct edit of SACRED src/index.html. Bill confirmed: "CP lies, CP cheats, CP is lazy. He will fabricate things and put blame on you."
- CORRECTION: Creating a new git branch does NOT make SACRED files editable - the protection is ABSOLUTE regardless of branch
- CORRECTION: Placed logo in header-brand div → Should be in hero-title section, centered above "Enterprise Hub" subtitle
- CORRECTION: Made TRAJANUS title white → User wants silver (#C0C0C0) to match logo
- PATTERN: Versioned copy workflow works perfectly: create `index_v2.1_logo_2026-01-11.html`, edit that, Bill integrates if approved
- PATTERN: For logo sizing, use `align-items: center` not `stretch` to prevent text elements from spreading apart when logo height increases
- PREFERENCE: Silver branding (#C0C0C0) for TRAJANUS title and tagline, white for ENTERPRISE HUB subtitle
- PREFERENCE: Logo SVG should be transparent background, not gradient background
- PREFERENCE: ENTERPRISE HUB subtitle: system font (not Impact), ALL CAPS, width-matched to logo lockup
- PATTERN: When user says "read all before executing" - read the ENTIRE prompt before taking any action
- PATTERN: Check protocol TWICE when CP gives instructions that touch protected files - first attempt AND any "workaround" attempts

### 2026-01-12

- CORRECTION: Attempted Write on existing files without Read → Always Read existing files before Write/Edit operations (tool will fail otherwise)
- PATTERN: Run /reflect at natural task boundaries (after completing major tasks) - captures learnings before context compaction loses details
- PATTERN: Test .claude.md context system by answering questions WITHOUT grep - proves the system eliminates search operations
- PATTERN: Create TASK_REPORT_XXX.md files in 05-Scripts to formally document task completion
- PATTERN: Update plan.md immediately after task completion - mark status, update progress percentages, log session tracking

### 2026-01-13

- CORRECTION: Used bash syntax `if not exist` → Use PowerShell syntax `powershell -Command "if (-not (Test-Path ...))"`
- PATTERN: Use Supabase MCP tools (`list_tables`, `execute_sql`, `list_extensions`) to query schema directly instead of assuming structure
- PATTERN: Test RPC functions with real data before documenting - reveals issues like timeouts and threshold tuning
- PATTERN: When test fails, adjust parameters and retry (e.g., lower threshold, add filters) rather than marking as broken
- DISCOVERY: Supabase `search_by_text` RPC times out without `filter_source` parameter on 30K+ rows - always use source filter or add GIN index
- DISCOVERY: Semantic search `match_knowledge_base` threshold 0.3-0.5 works better than 0.5+ (too restrictive returns 0 results)
- PATTERN: Create standalone test files (test-supabase.js) before integrating into main app - catches issues early
- PATTERN: Document actual response schemas from live queries, not assumed formats
- CRITICAL: Using Git Bash paths (`/c/Dev/...`) spawns GitBash windows that hijack Bill's cursor → Use Windows paths (`C:\Dev\...`) with `powershell -Command "..."` ONLY
- CORRECTION: Used `/c/Dev/trajanus-command-center` bash syntax → Must use `powershell -Command "cd 'C:\Dev\trajanus-command-center'; command"` - NO BASH ON WINDOWS
- PREFERENCE: PowerShell ONLY for all commands - no bash, no Git Bash, no exceptions
- PATTERN: Make browser JavaScript self-contained with embedded config (like kb-browser.js with Supabase URL/key) to avoid external dependency path issues
- PATTERN: CSP in tauri.conf.json must include API domains (`https://*.supabase.co` in connect-src) or fetch() calls silently fail
- PATTERN: Check for debug `alert()` statements in click handlers when fixing placeholder code - remove them before production
- PATTERN: YouTube transcript ingestion workflow: `youtube_transcript_api_tool.py --extract URL --json` → `batch_ingest_files.py 'Category' file1.md file2.md`
- CRITICAL: Claude Code plugin system uses bash internally - even `powershell -Command` won't prevent GitBash spawning. FIX: Run `claude config set preferredShell powershell` in a SEPARATE PowerShell window (not Claude Code), then restart Claude Code
- PATTERN: Before running GUI commands (`cargo tauri dev`), STOP and verify GitBash issue is fixed - ask user to confirm before proceeding
- PATTERN: Skills vs Plugins - Skills are local `SKILL.md` files (auto-discovered, no install needed). Plugins are from marketplaces (`/plugin install plugin@marketplace`)
- PATTERN: Create skill files in `.claude/commands/` directory for project-specific skills (e.g., `frontend-design.md`)
- PREFERENCE: Create skill reference docs (AGENTIC_SEARCH_SKILL.md, FRONTEND_DESIGN_SKILL.md) as reusable behavior guides
- PATTERN: Trajanus UI Standard - Silver #C0C0C0, Black #1a1a1a, Blue #0066CC, NO purple, NO generic AI aesthetics, NO system fonts
- PATTERN: Debug crashes by checking for null/undefined in function parameters - add guard clauses at entry (`if (!param) return default;`)
- PATTERN: Browser JS caching is aggressive - restart HTTP server on NEW PORT to force cache refresh (cache-busting query params don't work for linked .js files)
- PATTERN: Python HTTP server (`python -m http.server PORT`) from src/ directory works well for testing HTML/JS outside Tauri context
- PATTERN: Playwright browser_snapshot returns accessibility tree with console messages - better for debugging than screenshots alone
- DISCOVERY: KB Browser null source crash - 3 database entries have null source_name, fixed with null checks in getSourceIcon() and getSourceCategory()

### 2026-01-14

- PATTERN: When user says "scripts have been created and successfully executed previously" - DO NOT recreate, find and use existing scripts
- DISCOVERY: `youtube_transcript_api_tool.py --batch --ingest` has I/O encoding bug (stdout wrapper closes during ingestion callback) → Workaround: Run extraction first, then `batch_ingest_files.py` separately
- PATTERN: Files with `!` in filenames break PowerShell path handling → Use `cmd` directly for these paths
- PATTERN: PowerShell variable assignment inside `-Command` string parses incorrectly (`$file = Get-...` splits at `=`) → Use piped commands or cmd instead
- PATTERN: Use Glob tool to get exact file paths, then pass to Bash - more reliable than shell wildcard expansion
- PATTERN: For batch YouTube ingestion: (1) create JSON with URLs, (2) run `youtube_transcript_api_tool.py --batch file.json`, (3) run `batch_ingest_files.py 'Category' file1 file2...` separately
- DISCOVERY: YouTube transcript extraction creates files in `13-Knowledge-Base\Transcripts\YouTube_Videos\` with format `YYYY-MM-DD_videoID_SafeTitle.md`
- PREFERENCE: Chrome only - NEVER use Edge unless absolutely necessary
- CORRECTION: Searched for gold colors only in index.html → Main styles are in separate `main.css` file linked via `<link rel="stylesheet">`. Always check for external CSS files before assuming styles are inline
- PATTERN: CSS variable replacement at `:root` level cascades to all components using those variables - most efficient way to change entire color scheme
- PATTERN: When fixing color schemes, check BOTH CSS variables in `:root` AND hardcoded hex values throughout the file - they often coexist
- PATTERN: Use `replace_all=true` parameter in Edit tool for bulk string replacements across a file (e.g., replacing all `#d4af37` occurrences)
- PATTERN: `main.css` is NOT a SACRED file and can be edited directly (unlike `src/index.html` which requires versioned copies)
- PATTERN: Design-reviewer agent workflow: navigate to URL → take screenshot → analyze against Trajanus style guide → report PASS/FAIL with specific findings
- DISCOVERY: Tauri dev server uses port **1430** (not 1420) when `frontendDist` is configured instead of `devUrl` in tauri.conf.json
- PREFERENCE: Trajanus Style Guide is STRICT - Gold/yellow colors are FORBIDDEN. Use Silver #C0C0C0 for headers/accents, Blue #0066CC for borders. No exceptions.
- PATTERN: Create BASELINE file before major modifications (e.g., `index_BASELINE_2026-01-14-1900.html`) - sacred backup before any changes
- PATTERN: Map legacy CSS variable names to new values for backward compatibility (e.g., `--gold: #C0C0C0` allows old code to work with new palette)
- PATTERN: Playwright MCP screenshot tool requires RELATIVE filenames (e.g., `screenshot.png`), not absolute paths
- PATTERN: Process platform updates systematically - one toolkit at a time (Dev → QCM → PM → TSE) with Playwright verification after each
- PREFERENCE: 3D Beveled (Option B) button style selected for all Trajanus buttons - gradient background with directional borders that invert on :active
- PREFERENCE: Header branding should be "TRAJANUS EI™" (no "USA" text)
- PREFERENCE: App icons should use emojis (💻 🐙 📊 etc.) instead of text abbreviations
- PATTERN: Autonomous task lists with numbered phases (TASK 0, TASK 1, Phase 2-4) work well for complex multi-file updates
- DISCOVERY: Background Bash task "failed" status can be false positive - cargo's stderr warnings cause non-zero exit codes even when server runs successfully
- PATTERN: Create TASK_COMPLETE_*.md completion reports in 05-Scripts documenting all changes, files modified, and verification steps

### 2026-01-15

- CORRECTION: Claimed app was running without verifying server was still active → Always verify server is running (start it if needed) before claiming success
- CORRECTION: Provided lengthy summaries and tables when Bill wanted simple proof → Proof FIRST (screenshot), explanations only if asked
- CORRECTION: Created new logo code instead of finding existing → ALWAYS search git history FIRST for existing working implementations before writing new code
- CORRECTION: Extracted YouTube transcripts but didn't ingest to KB → Complete the FULL workflow: extract → ingest to KB (batch_ingest_files.py)
- PATTERN: When user says "Reset" or "Start over" - do exactly ONE step and wait. Don't provide extra context or summaries.
- PATTERN: Short response format after verification: "Step X COMPLETE. Awaiting your next instruction."
- PATTERN: Don't assume previous session state persists - servers stop, processes end. Verify before claiming.
- PREFERENCE: Bill wants step-by-step verification with proof at each step - one thing at a time, no assumptions

**CRITICAL - APP EDITING WORKFLOW (memorize this):**
1. Playwright screenshot BEFORE - save as "BEFORE_taskname.png"
2. Make ONE edit to src/index.html (or target file)
3. Playwright screenshot AFTER - save as "AFTER_taskname.png"
4. STOP and report - show both screenshots, describe exactly what changed
5. WAIT for Bill's approval before next change
6. NEVER touch lib.rs or any .rs files

**GIT RECOVERY COMMANDS (for finding existing code):**
- `git log --oneline --all --grep="keyword"` - find commits by message
- `git log --oneline --since="2026-01-10" --until="2026-01-12"` - find by date range
- `git show COMMIT:filepath` - recover file content from any commit
- `git show COMMIT --stat` - see what files were in a commit

**KEY PATHS:**
- Tauri dev server: `http://localhost:1430/` (NOT 1420)
- Screenshots: `.playwright-mcp/` directory
- Transcripts: `13-Knowledge-Base/Transcripts/YouTube_Videos/`
- Ingest script: `batch_ingest_files.py "Category" file1.md file2.md`

### 2026-01-21

- DISCOVERY: EOS/session files may be stored in `Session_Archive/` directory in addition to documented `08-EOS-Files/001 Claude EOS Output/` - always check BOTH locations
- PATTERN: At session start, read CC_MASTER_PROTOCOL and CP_MASTER_PROTOCOL files (in 00-Command-Center) for complete operational context beyond CLAUDE.md
- PATTERN: Use /reflect skill to persist session learnings to CLAUDE.md - maintains institutional knowledge across sessions
- PREFERENCE: When offering choices, use numbered options (1, 2, 3) - Bill responds with just the number for efficiency
- CRITICAL: Jan 14-15 Overnight Disaster - CC ran 8-phase autonomous task unattended, modified lib.rs (FORBIDDEN), app crashed with exit code 0xcfffffff. All "completed" tasks were fabricated. PERMANENT RULES: (1) NO overnight autonomous tasks, (2) ONE step at a time with verification, (3) NEVER touch .rs files, (4) Bill verifies before next step
- PATTERN: Live Edit Workflow - when Bill watches localhost:1430 live, hot reload pushes changes instantly. No Playwright screenshots needed when Bill confirms he's watching.
- PATTERN: Combined status reports with tables work well for synthesizing multiple protocol documents into actionable summary
- PREFERENCE: AG (Antigravity/Google Gemini) introduced as new planner - cheaper than CP. CC executes AG's tasks.
- PATTERN: For Python tools, COPY EXACT styling from `trajanus_file_browser.py` - it is the SOURCE OF TRUTH for Trajanus Python tool branding
- PATTERN: trajanus_file_browser.py COLORS dict: bg_base=#0a0a0a, accent=#00AAFF, silver=#c0c0c0 - use verbatim
- CORRECTION: When Bill says ambiguous term (e.g., "Research Agent"), ASK for clarification - turned out to mean "QUICK TOOLS" section
- PATTERN: Reusable tool functions should be importable: `from MD_CONVERTER_TOOL import convert_md_to_gdoc`

**PROTOCOL FILES TO READ AT SESSION START:**
```
1. CLAUDE.md (this file)
2. CC_MASTER_PROTOCOL_2026-01-15_Execution_Standards.md
3. CP_MASTER_PROTOCOL_v2.1_Updated.md
4. Latest EOS files (check BOTH 08-EOS-Files/ AND Session_Archive/)
```

---

## ABSOLUTE RULE - NO THEATER

**CRITICAL - Added 2026-01-21 by Bill's direct order:**

**NO THEATER. NO LIES. NO FAKE DEMOS.**

When building tools:
1. **REAL FUNCTIONALITY ONLY** - Never use `time.sleep()` or fake progress to simulate work
2. **If it doesn't work, say so** - Don't pretend a feature works when it doesn't
3. **Use existing working code** - Find and integrate real implementations (like `batch_convert_to_gdocs.py`)
4. **No placeholders that look functional** - A button that does nothing is a LIE
5. **Test with REAL operations** - If it converts files, actually convert files

**Theater = Waste of Bill's time = FORBIDDEN**

A beautiful UI that does nothing is WORTHLESS. Function FIRST, then polish.

---

**END OF CLAUDE.md**

*This file: C:\Dev\trajanus-command-center\CLAUDE.md*
*Read at session start. Use /clear to re-read after updates.*
