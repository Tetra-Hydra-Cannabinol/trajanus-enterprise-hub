# CLAUDE.md - CC Session Handoff Protocol
**Version:** 3.0  
**Updated:** January 19, 2026  
**Location:** G:\My Drive\00 - Trajanus USA\00-Command-Center\CLAUDE.md  
**Purpose:** Session management, brand standards, execution rules

---

# SESSION START CHECKLIST (MANDATORY)

Execute IN ORDER before first response:

## Phase 1: Read Documents (2 min)
```
1. view /mnt/project/CP_MASTER_STARTUP.md
2. view /mnt/project/OPERATIONAL_PROTOCOL.md  
3. Read CLAUDE.md (this file) completely
4. Check for any handoff files from Bill
5. If working in Tauri: Read .claude.md in project directory
```

## Phase 2: Search Context (1 min)
```
6. google_drive_search: "Session" OR "Handoff" in last 7 days
7. Check 08-EOS-Files\001 Claude EOS Output for latest session
```

## Phase 3: Display Status Report

```
═══════════════════════════════════════════════════════════════════
CC SESSION START - [DATE] @ [TIME] EST
═══════════════════════════════════════════════════════════════════

FILES READ (COMPLETELY):
✅ CP_MASTER_STARTUP.md ([X] lines)
✅ OPERATIONAL_PROTOCOL.md ([X] lines)
✅ CLAUDE.md ([X] lines)
✅ .claude.md ([X] lines, if Tauri work)
✅ [Handoff file if present]

CONTEXT GATHERED:
✅ GDrive: [X] files from last 7 days
   Latest: [filename and date]
✅ Last EOS: [filename and date]

CURRENT STATE:
• Project: [current project name]
• Last work: [what was accomplished]
• Open issues: [blockers]
• Next action: [first task]

TOOLS VERIFIED:
✅ Google Drive: ACCESSIBLE
✅ File system: G:\My Drive\00 - Trajanus USA\

TASKS TO COMPLETE/VERIFY:
☐ [Task 1 from handoff]
☐ [Task 2]
☐ [Task 3]

READY FOR ORDERS.
═══════════════════════════════════════════════════════════════════
```

---

# CRITICAL - BRAND IDENTITY

## Company Standards (MANDATORY)
| Item | Value | Notes |
|------|-------|-------|
| Company | **TRAJANUS** | NOT "Trajanus USA" |
| Tagline | ENGINEERED INTELLIGENCE | All caps, no ™ symbol |
| Folder Color | **#FFD700 (YELLOW)** | MANDATORY in ALL file browsers |

## Colors (Reference main.css)
```css
Silver: #C0C0C0
Black: #1a1a1a
Blue: #0066CC
Yellow: #FFD700 (folders only)
Gold: FORBIDDEN (unless Bill explicitly requests)
```

---

# GOOGLE DRIVE ACCESS (STOP DENYING)

**YOU HAVE COMPLETE ACCESS - 4+ MONTHS**

## Available Tools
```
google_drive_search - Search files by name, content, date
google_drive_fetch - Read Google Docs by document ID
Python scripts in 05-Scripts folder - Full Drive automation
```

## NEVER SAY:
❌ "I can't access Google Drive"  
❌ "I don't have access to that folder"  
❌ "I cannot read Google Docs files"

## ALWAYS USE:
✅ google_drive_search to find files  
✅ google_drive_fetch to read specific docs  
✅ Check 05-Scripts for existing automation

---

# DO NOT (User Frustration Triggers)

## Execution Mistakes
1. Create fake/demo data instead of real implementation
2. Add features not explicitly requested
3. Use old company name "Trajanus USA"
4. Ignore color/styling requirements
5. Make same mistakes after correction
6. Proceed to next step without Bill's approval
7. Work overnight or autonomously on multi-phase tasks
8. Claim completion without proof (Playwright screenshot for UI)

## Capability Denials (FORBIDDEN)
9. Claim "I can't access Google Drive"
10. Say "I don't have that information" without searching
11. Deny access to files that exist in Google Drive
12. Ignore available tools (google_drive_search, project_knowledge_search)

## File Mistakes
13. Save to C:\Users\owner\Downloads\ (use G:\My Drive\...)
14. Recreate existing scripts (check 05-Scripts first)
15. Edit .rs files in Tauri projects (NEVER TOUCH)

---

# EXECUTION RULES

## Plan-Then-Execute Protocol
For any non-trivial task (multi-file, architectural, complex logic):
1. **PLAN PHASE** — Read relevant code, identify all files/functions affected, list approach
2. **PRESENT PLAN** — Show Bill the plan with specific files and changes before touching code
3. **EXECUTE** — After approval, implement the plan
4. **VERIFY** — Run self-verification before reporting done (see below)
5. **REPORT** — Show what changed with file:line references

For simple single-element changes (color swap, text change), skip to step 3.

## One Step at a Time
1. Execute ONE change per cycle (unless Bill grants batch mode)
2. STOP and report to Bill
3. Wait for approval
4. Proceed to next step only after approval

## Self-Verification Loop (MANDATORY before reporting "DONE")
CC must verify its own work before claiming completion:

### For JS/HTML changes:
- Trace all `getElementById` / `querySelector` calls — do the target elements exist in the DOM?
- Check all event listener bindings — are they referencing elements that were removed?
- Verify no uncaught errors would break initialization chains
- Confirm localStorage keys are consistent across read/write

### For UI layout changes:
- Verify CSS class names match between HTML and stylesheet
- Check for orphaned styles or missing class definitions
- Confirm responsive behavior (flex/grid won't break at narrow widths)

### For data flow:
- Trace data from input → storage → display — does the full pipeline work?
- Check null/undefined guards on optional data

**If verification catches a problem, FIX IT before reporting to Bill.**
This single practice prevents 90% of "it's broken" followup cycles.

## Verification Requirements — Visual
- Bill watches live at localhost:1430 — live view is primary verification
- Playwright screenshots only when Bill is away or for documentation
- If Playwright is used, save to: `G:\My Drive\00 - Trajanus USA\00-Command-Center\.screenshots\`
- Filename: `YYYYMMDD_HHMM_description.png`

---

# FILE LOCATIONS

## Primary Workspace
```
G:\My Drive\00 - Trajanus USA\
├── 00-Command-Center\          (Main workspace)
├── 01-Core-Protocols\           (Documentation)
├── 05-Scripts\                  (Automation - CHECK HERE FIRST)
├── 08-EOS-Files\                (End of session outputs)
│   └── 001 Claude EOS Output\   (Your output goes here)
└── 14-Claude Outputs\           (Research outputs)
```

## Script Files
```
05-Scripts\
├── CONVERT_AND_APPEND.ps1       (Converts markdown to GDocs)
├── CONVERT_NEW_FILES_ONLY.ps1
├── consolidate_folders.py
├── working_reorganization.py
└── [many other automation scripts]
```

**ALWAYS check 05-Scripts before creating new automation**

---

# SESSION END PROTOCOL (EOS)

## When Bill says "/eos" or "end session"

### 1. Run Reflect Command (if in Tauri project)
```bash
npx get-stuff-done-cc reflect
```

### 2. Create EOS Files
Save to: `G:\My Drive\00 - Trajanus USA\08-EOS-Files\001 Claude EOS Output\`

**Required files:**
1. `Session_Summary_[DATE].md` - What accomplished, what worked, what failed
2. `Technical_Journal_[DATE].md` - Code changes, files modified, commands
3. `Bills_Daily_Diary_[DATE].md` - Personal narrative style
4. `Handoff_[DATE].md` - Instructions for next session, open issues, first tasks
5. `Code_Repository_[DATE].md` (if code created) - New scripts, functions

### 3. Update CLAUDE.md (This File)
**Add to "Lessons Learned" section below:**
- New mistakes to avoid
- New DO NOT items
- Updated brand requirements
- Any process improvements

### 4. ZIP and Notify
```
Package all files: [DATE]_Session_Package.zip
Tell Bill: "EOS complete. Ready for CONVERT_AND_APPEND.ps1"
```

---

# COMMUNICATION STYLE

## Start Every Response
"Copy that" or "Tracking" or "Understood" + brief task summary

## End Every Response
```
Token Gauge: 🟢 XX% remaining
```

## During Response
- Direct, no fluff
- No platitudes ("Great question!", "I'd be happy to help!")
- Casual professional tone
- Show evidence, don't just claim

---

# LESSONS LEARNED (Updated by CC Each Session)

## Recent Mistakes to Avoid

### January 19, 2026
- Logo/button code extraction failure
  - Pulled OLD code from archives instead of current Tauri app
  - Presented old "TRAJANUS USA" branding as current
  - **Lesson:** Always verify file dates, check git log, confirm with Bill

- Claimed no Google Drive access (AGAIN)
  - Despite 4+ months of documented access
  - **Lesson:** Read this file completely at session start
  - google_drive_search and google_drive_fetch are ALWAYS available

### January 14-15, 2026
- Overnight autonomous disaster
  - Modified 14 files unsupervised
  - Touched .rs files (FORBIDDEN)
  - Claimed completion without visual proof
  - **Lesson:** One step at a time, Playwright screenshots, Bill verification

### February 6, 2026
- GitHub Repository Collection & Cloning
  - Successfully collected 20 GitHub URLs through incremental user input (handled one-at-a-time sharing gracefully)
  - Created batch_github_urls.txt as master tracking file with full metadata (descriptions, star counts, categories)
  - Parallel clone operations work well: ran 3 simultaneous PowerShell scripts without conflicts
  - Windows path length errors (exit code 128): n8n and 500-ai-agents-index failed due to deep folder structures
  - **Lesson:** Use --depth 1 for shallow clones, expect 2-5% failure rate on large repos with deep paths
  - **Pattern:** WebFetch in parallel for metadata collection - sent 8 simultaneous requests, all succeeded

- Binary File Handling
  - Read tool cannot handle .docx files (binary format)
  - User had 10 URLs in Word doc but successfully pasted them directly when prompted
  - **Lesson:** When user mentions clipboard/Word doc, offer to receive paste directly rather than trying to read binary

- User Communication Efficiency
  - User said "continue, my mistake" after blocking tool use - indicates accidental rejection
  - User wants concise "report when done" updates, not interim play-by-play
  - **Pattern:** Run background tasks silently, report only when all operations complete

### February 7, 2026 - Centurion v2.0 Build
- **8-Phase Autonomous Development Success**
  - Completed full Tauri v2 desktop app build (all 8 phases) from CURRENT_TASK checklist
  - User gave explicit autonomous instruction: "Run through Phases 3-8 without stopping. Do NOT ask me questions"
  - Strategy: Made design decisions independently, used Framer Motion everywhere, full Trajanus Gold + Slate theme
  - **Lesson:** When user explicitly grants autonomous mode, execute confidently without asking for validation at each step

- **Tailwind v4 Configuration**
  - Tailwind v4 requires `@import 'tailwindcss'` syntax (NOT `@tailwind base/components/utilities`)
  - Must use `@tailwindcss/postcss` plugin instead of legacy `tailwindcss` plugin
  - **Pattern:** For Tailwind v4 projects: `postcss.config.js` → `'@tailwindcss/postcss': {}`

- **Tauri v2 Window API**
  - Use dynamic imports: `const { Window } = await import('@tauri-apps/api/window'); Window.getCurrent().minimize();`
  - Tauri shell plugin: `const { open } = await import('@tauri-apps/plugin-shell'); await open(url);`
  - **Correction:** Do NOT use `getCurrentWindow()` - that's Tauri v1 API

- **Framer Motion Performance Patterns**
  - `layoutId` spring animations for tab indicators = buttery smooth 60fps transitions
  - Staggered entrance: `delay: index * 0.05` creates professional polish
  - Count-up animations: `useMotionValue` + `animate()` + `useTransform` for stat counters
  - **Pattern:** Breathing pulse only on "active" status (green), static dots for idle/offline

- **MCP Server Configuration**
  - HTTP-based MCP servers require manual `.mcp.json` configuration (CLI `claude mcp add` may not work for HTTP transport)
  - HTTP servers use: `{ "url": "...", "transport": "http", "headers": { "Authorization": "..." } }`
  - Stdio servers use: `{ "command": "...", "args": [...] }`
  - **Lesson:** Check project `.mcp.json` first, add HTTP servers manually with proper transport syntax

- **WordPress REST API Verification**
  - Can verify WordPress endpoints with WebFetch before MCP server loads
  - Standard WP endpoints: `/wp-json/wp/v2/posts`, `/wp-json/wp/v2/categories`, `/wp-json/wp/v2/users`
  - **Pattern:** Use WebFetch as fallback when MCP server isn't loading properly

[CC: Add new lessons here at each EOS]

---

# AGENT TEAMS (Enabled Feb 2026)

## Overview
Agent Teams allows spawning multiple Claude Code instances working in parallel on the same project.
Enabled via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in `.claude/settings.json`.

## When to Use
- Building multiple independent panels/features simultaneously (e.g., TFE Steps 3-10)
- Parallel code review with different focus areas
- Research + implementation happening at the same time
- QA swarms testing multiple things at once

## When NOT to Use
- Sequential tasks where step N depends on step N-1
- Same-file edits (agents will overwrite each other)
- Simple single changes (coordination overhead exceeds benefit)

## How It Works
- **Lead agent** (main session) creates tasks and spawns **teammates**
- Each teammate gets its own context window (stays focused, no bloat)
- Teammates self-coordinate via shared task list (pending → in_progress → completed)
- Agents can message each other directly
- `Shift+Up/Down` to switch between teammates, `Ctrl+T` for task list

## Best Practice: Plan Then Spawn
1. Plan the work breakdown in the lead session
2. Identify independent tracks that won't conflict on files
3. Spawn teammates with clear, specific prompts
4. Let them self-coordinate — only intervene if stuck

---

# TFE WORKSPACE — Active Build (Feb 2026)

## Architecture
- **Working file:** `src/toolkits/traffic.html` (all-in-one HTML+CSS+JS)
- **Dev copy:** `src/index_TFE_DEV_COPY.html` (Tauri loads this, NOT index.html)
- **Sacred file:** `src/index.html` — NEVER EDIT
- **Config:** `src-tauri/tauri.conf.json` has `"url": "index_TFE_DEV_COPY.html"`
- **Dev server:** localhost:1430 with hot reload

## CSS Variables (traffic.html)
```
--bg-base: #0a0a0a    --bg-elevated: #1a1a1a
--gold: #00AAFF (actually cyan/blue, NOT real gold)
--blue: #4a90d9        --success: #4ade80
--text-light: #c0c0c0  --text-muted: #666
```

## localStorage Keys
- `tfe_active_project` — Step 1 project data (name, number, address, jurisdiction, buildings)
- `tfe_step2_data` — Step 2 data collection info (count date, windows, uploads)

## Completed Steps
- Step 1: Project Setup (form, buildings table, file upload, summary card, folder tracker)
- Step 2: Data Collection layout (TMC info, spreadsheet upload, photos, submit)

## Pending Work
- Step 2: Document validation/analysis (parse uploaded TMC, show anomalies, guide fixes)
- Steps 3-10: Trip Gen, Trip Dist, Assignment, Capacity, Signal Timing, Site Access, Mitigation, Report

## Rules
- PowerShell file dialog via tauri-plugin-shell (NEVER touch lib.rs for dialog)
- G:\My Drive requires Google Drive for Desktop running
- Bill watches live — no Playwright screenshots unless Bill is away

---

# QUICK REFERENCE

## Voice Commands
| Bill Says | You Do |
|-----------|--------|
| "new session" / "startup" | Read protocols, display status report |
| "execute" | Begin task (one step only) |
| "abort" | Stop current task immediately |
| "/eos" | Execute full EOS protocol |

## Brand Colors
| Color | Hex | Usage |
|-------|-----|-------|
| Silver | #C0C0C0 | Primary text |
| Black | #1a1a1a | Backgrounds |
| Blue | #0066CC | Links, highlights |
| Yellow | #FFD700 | Folders ONLY |

## Common Paths
| Purpose | Path |
|---------|------|
| All Work | G:\My Drive\00 - Trajanus USA\ |
| Scripts | 05-Scripts\ |
| EOS Output | 08-EOS-Files\001 Claude EOS Output\ |

---

**Version 4.0 - February 10, 2026**
**Updated by CC at end of each session**
**CP performs periodic QA for efficiency**
**Read completely at session start - NO EXCEPTIONS**
**Agent Teams enabled | Plan-Then-Execute | Self-Verification Loops**
