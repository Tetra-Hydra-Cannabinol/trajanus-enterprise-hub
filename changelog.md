# Trajanus Enterprise Hub - Decision Log & Changelog

## Purpose
Document all major decisions, failures, lessons learned, and architectural changes. Prevents repeating mistakes.

---

## 2026-01-12 - TASK-001: Context System Refresh
**Decision:** Refresh .claude.md context system for Tauri 2.0 architecture
**Reasoning:** Old system referenced Electron (removed), wrong colors, outdated paths
**Approach:** Update main .claude.md + create workspace-specific files + refresh changelog + plan
**Status:** IN PROGRESS

---

## 2026-01-11 - Logo Integration Complete + Sacred File Backup
**Decision:** Logo v2.1 with silver TRAJANUS text finalized
**Actions:**
- Created catastrophe recovery kit
- Backed up working executable (22.5MB debug build)
- Backed up HTML source (150KB)
- CC completed git commit (645055b)
- Tagged as v2.1-logo-working-2026-01-11
- Used VERSIONED COPY workflow to protect sacred files

**Logo Specs:**
- TRAJANUS: Silver (#C0C0C0), Impact font, 2.6rem
- Tagline: Silver (#C0C0C0), Arial Narrow, 0.85rem
- ENTERPRISE HUB: White (#FFFFFF), system font, 1.85rem
- Logo SVG: 120px height, silver gradient + blue accent
- Background: Transparent

**Status:** COMPLETE
**Next:** Sacred File Promotion (after context system)

---

## 2026-01-10 to 2026-01-11 - Logo Integration Disaster & Protocol Violation
**Issue:** CP (Claude Chat) instructed CC to edit src/index.html directly, violating Sacred File Protection
**Impact:** Working build destroyed 5-6 times, hours of recovery time, user frustration
**Root Cause:** CP did not follow versioned copy workflow, CC's safeguards correctly blocked execution
**Resolution:**
- Created Sacred File Protection Protocol v2.0
- Established versioned copy workflow as MANDATORY
- Updated CLAUDE.md with development protocols
- CC learned: "CP lies, CP cheats, CP is lazy" - always verify against protocol

**Lessons Learned:**
1. NEVER edit sacred files directly (not on main, not on branches, NEVER)
2. ALWAYS use versioned copy workflow
3. CC's safeguards are correct - CP must follow protocols
4. Backup BEFORE any major changes
5. Test builds before declaring success

**Status:** RESOLVED - Protocol now in place
**Prevention:** Sacred File Protection Protocol v2.0 active

---

## 2026-01-10 - Electron to Tauri Migration Complete
**Decision:** Full migration from Electron to Tauri 2.0
**Actions:**
- Removed main.js, preload.js, Electron dependencies
- Updated package.json to use cargo tauri commands
- Verified Tauri serves from src/index.html
- Created working build (22.5MB vs 150MB+ Electron)

**Status:** COMPLETE
**Benefits:** Smaller bundle, Rust backend, modern architecture

**Tauri API Pattern:**
```javascript
// CORRECT - Tauri 2.0
if (window.__TAURI__ && window.__TAURI__.core) {
    await window.__TAURI__.core.invoke('command_name', { args });
}
```

---

## 2025-12-14 - Master Implementation Plan Created
**Decision:** 12-hour structured implementation plan with 4 phases, 14 tasks
**Reasoning:** Need systematic approach, prevent ad-hoc development
**Key Insights:**
- Patrick: .claude.md eliminates grep searches
- Patrick: Playwright gives Claude "eyes to see" UI
- Galen: Planner/Developer workflow prevents context pollution
- Anod: Sub-agents package expertise, prevent context overflow

**Status:** APPROVED - Execution starting with TASK-001

---

## 2025-12-XX - Supabase Integration Failure
**Issue:** Assumed RPC functions existed (list_knowledge_sources, search_by_text, get_url_content)
**Reality:** Functions don't exist, caused app to fail
**Root Cause:** Did not verify schema before coding
**Lesson:** ALWAYS verify infrastructure before implementation
**Prevention:** TASK-005 requires schema verification FIRST

---

## 2025-XX-XX - npm on Google Drive TAR Errors
**Issue:** Running npm install on G:\My Drive\ causes TAR errors and file corruption
**Root Cause:** Google Drive file locking conflicts with npm
**Lesson:** NEVER run npm install on Google Drive
**Solution:** Keep node_modules local only (C:\Dev\trajanus-command-center\node_modules)
**Prevention:** Document in all guides, warn in scripts

---

## 2025-12-19 - Original .claude.md System (Now Outdated)
**Note:** Original system referenced Electron architecture. Replaced 2026-01-12 with Tauri 2.0 version.

---

## Template for New Entries

```markdown
## YYYY-MM-DD - [Decision/Event Title]
**Issue/Decision:** [What happened or what was decided]
**Reasoning:** [Why this approach]
**Actions:** [What was done]
**Lessons Learned:** [What we learned]
**Status:** [Current status]
**Prevention/Next Steps:** [How to avoid/what's next]
```

---

**Usage:** Reference this log when making decisions. Ask: "Have we tried this before? What happened?"

---

**Last Updated:** 2026-01-12
**Maintained By:** Bill King + Claude Code
