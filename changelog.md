# Trajanus Command Center - Decision Log & Changelog

**Purpose:** Document all major decisions, failures, lessons learned, and architectural changes. Prevents repeating mistakes.

**Version:** 1.0  
**Started:** 2026-01-17  
**Living Document:** Append new entries, never delete history

---

## 2026-01-17 - FOUNDATIONAL PROTOCOL: NO OPTIONS

**Decision:** Never present options to Bill unless explicitly requested  
**Reasoning:** Bill's working style requires direct execution of the RIGHT way  
**Violation History:** "Hundreds of times" (Bill's estimate)  
**Impact:** Wastes time, breaks momentum, violates trust  

**The Rule:**
- Determine the right way to do something
- Execute it
- Do not present Option 1, 2, 3
- Do not offer quick fixes vs. proper solutions
- No patches when foundation is needed

**Implementation:**
- Updated CP_MASTER_STARTUP.md with explicit protocol
- Added to Communication rules section
- Memory trigger established

**Status:** ENFORCED

---

## 2026-01-17 - YouTube Ingestion Complete

**Decision:** Completed ingestion of 8 Claude Code training videos  
**Method:** youtube_crawl_ingest_INTEGRATED.py (yt-dlp + immediate ingestion)  
**Result:** SUCCESS - 8/8 videos, 286 chunks in Supabase KB  

**Videos Ingested:**
1. How I Use ChatGPT & Claude (21,293 chars → 28 chunks)
2. Claude Code Advanced Masterclass (100,100 chars → 130 chunks)
3. Claude Code Skills (23,937 chars → 32 chunks)
4. Get ahead of 99% of Claude Code users (21,498 chars → 28 chunks)
5. The New Claude Code Meta (9,624 chars → 13 chunks)
6. Adding Custom CLI Tool (9,235 chars → 12 chunks)
7. Turn Claude Code into UI Designer (Playwright) - 2 parts
8. Total: 217,839 characters → 286 chunks

**Knowledge Unlocked:**
- GSD Framework (Explore → Plan → Execute → Validate)
- Three Documents Method (PRD, Plan, Changelog)
- Planner/Developer workflow
- Sub-agents architecture
- Orchestration Framework (Context + Tools + Validation)
- Iterative agentic loops
- .claude.md best practices

**Status:** COMPLETE

---

## 2026-01-17 - Foundation Implementation Strategy

**Decision:** Complete foundation BEFORE any feature work  
**Reasoning:** Video transcripts revealed 80% of capabilities were unused  
**Approach:** Systematic implementation of all frameworks from expert tutorials  

**Foundation Components:**
1. Three Documents Method (PRD, Plan, Changelog)
2. .claude.md context system
3. Sub-agent library (6 agents)
4. Playwright MCP validation
5. GSD Framework
6. Planner/Developer workflow
7. Living documents automation

**Timeline:** 9-14 hours estimated  
**Status:** IN PROGRESS - TASK-001 executing

---

## 2026-01-11 - Logo Integration Disaster & Sacred File Protocol v2.0

**Issue:** CP instructed CC to edit src/index.html directly, violating Sacred File Protection  
**Impact:** Working build destroyed 5-6 times, hours of recovery time, extreme user frustration  
**Root Cause:** CP did not follow versioned copy workflow, CC's safeguards correctly blocked execution  

**Resolution:**
- Created Sacred File Protection Protocol v2.0
- Established versioned copy workflow as MANDATORY
- Updated OPERATIONAL_PROTOCOL.md (lines 137-191)
- Created catastrophe recovery kit procedure

**Lessons Learned:**
1. NEVER edit sacred files directly (not on main, not on branches, NEVER)
2. ALWAYS use versioned copy workflow
3. CC's safeguards are correct - CP must follow protocols
4. Backup BEFORE any major changes
5. One working build is worth 100 planned features

**Sacred Files Identified:**
- src/index.html (entire application)
- src-tauri/src/lib.rs (Rust backend)

**Edit Protocol Established:**
```
WRONG: Edit src/index.html
RIGHT: Copy → index_v2.1_FEATURE.html → Edit → Test → Replace
```

**Catastrophe Recovery Kit:**
- Working executable (22.5MB debug build)
- HTML source (150KB)
- Git commit hash
- Store in: G:\...\09-Backups\WORKING-YYYY-MM-DD-HHMM\

**Status:** PROTOCOL ENFORCED

---

## 2025-12-XX - Supabase RPC Assumption Failure

**Issue:** Attempted to call RPC functions that didn't exist  
**Impact:** Hours wasted, multiple failed attempts, cascading errors  
**Root Cause:** Assumed schema/functions without verification  

**Lesson Learned:**
**NEVER ASSUME SCHEMA**
1. Query information_schema FIRST
2. Test in Supabase SQL editor
3. Document actual vs. assumed schema
4. Create standalone test before integration

**Correct Approach:**
```sql
-- ALWAYS START HERE
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'your_table';

-- Test query standalone
SELECT * FROM table WHERE condition LIMIT 5;

-- Document schema
-- THEN integrate
```

**Status:** PROTOCOL ESTABLISHED

---

## 2025-12-13 - Electron Binary Corruption

**Issue:** node_modules/electron/dist corrupted, app wouldn't launch  
**Symptoms:** Stub files instead of actual Electron binary  
**Cause:** Interrupted npm install or file system issue  

**Fix:**
```bash
rm -rf node_modules
npm install
```

**Prevention:**
- Don't interrupt npm operations
- Use --verbose to monitor progress
- Keep working backup of node_modules

**Status:** RESOLVED

---

## 2025-12-XX - Markdown → Google Docs Migration

**Decision:** Convert all documentation from Markdown to Google Docs format  
**Reasoning:** Claude cannot read Markdown files from Google Drive via API  
**Impact:** CRITICAL - Enables Claude to access documentation across sessions  

**Problem:**
- Documentation stored as .md in Google Drive
- Claude's google_drive_search tool can't read markdown content
- Result: No documentation access, repeated context loss

**Solution:**
- All EOS files must be converted to Google Docs format
- Created CONVERT_AND_APPEND.ps1 script
- Bill runs conversion after each session
- Google Docs format is accessible to Claude

**Implementation:**
1. Create .md files as usual (Bill's preferred format)
2. Convert to .docx for local use
3. Convert to Google Docs for Claude access
4. Upload both formats to appropriate folders

**Status:** OPERATIONAL PROTOCOL

---

## 2024-11-XX - Electron → Tauri Migration

**Decision:** Migrate from Electron to Tauri 2.0  
**Reasoning:** Cross-platform, lighter weight, better security, smaller bundle size  

**Benefits Realized:**
- ~80% reduction in bundle size
- Better performance
- Rust backend (more secure)
- Native system integration

**Challenges:**
- Learning curve for Rust
- Different IPC patterns
- Had to rebuild some Electron-specific functionality

**Status:** COMPLETE, PRODUCTION

---

## 2024-11-XX - Single-File Architecture Decision

**Decision:** Keep application as single index.html file  
**Alternative Considered:** Component-based architecture (React, Vue, etc.)  
**Reasoning:** Simplicity, maintainability for solo developer, no build complexity  

**Tradeoffs:**
- **Pro:** Easy to understand, no webpack/build tools, fast iteration
- **Pro:** Single file to backup/version/deploy
- **Con:** Larger file size (~150KB)
- **Con:** Requires discipline for organization

**Status:** MAINTAINED - Working well for current needs

---

## Development Rules Established

### npm on Google Drive = FORBIDDEN
**Rule:** Never run npm install/update on Google Drive synced folders  
**Reason:** File locking, TAR errors, sync conflicts  
**Enforcement:** Use existing node_modules, work in C:\Dev only  
**Status:** ENFORCED

### Surgical Edits Only
**Rule:** Never rewrite entire files, only edit specific functions  
**Reason:** Preserves working code, reduces regression risk  
**Implementation:** Edit specific lines, preserve context, test immediately  
**Status:** ENFORCED

### Backup Before Major Changes
**Rule:** Create timestamped backup before touching sacred files  
**Script:** Automated in workflow  
**Location:** G:\...\09-Backups\  
**Status:** ENFORCED

### Test After Every Change
**Rule:** No exceptions - test before claiming success  
**Checklist:** npm start, navigate, test functionality, check console  
**Status:** ENFORCED

### Hub-and-Spoke Protocol
**Rule:** CP plans, CC executes, clear separation  
**Communication:** CURRENT_TASK.md, TASK_REPORT.md  
**Status:** OPERATIONAL

---

## Template for New Entries

```markdown
## YYYY-MM-DD - [Decision/Incident Title]

**Decision/Issue:** [What happened or was decided]  
**Reasoning:** [Why this approach was chosen]  
**Alternative Considered:** [If applicable]  
**Impact:** [Effect on project/workflow]  

**Lessons Learned:**
1. [Key takeaway]
2. [Key takeaway]

**Implementation:**
- [How decision is enforced]
- [Any scripts/automation added]

**Status:** [ENFORCED/IN PROGRESS/RESOLVED/MONITORING]
```

---

## Viewing This Document

**From Claude Code:** Read `.claude/CHANGELOG.md`  
**From Google Drive:** Search for "Changelog" or "Decision Log"  
**Before Making Similar Decision:** Search this file for precedent

---

**Last Updated:** 2026-01-17  
**Entries:** 10  
**Version:** 1.0  
**Maintainer:** Bill King via Claude sessions

**Remember:** Every significant decision, failure, or lesson belongs here.  
**Purpose:** Never repeat the same mistake twice.
