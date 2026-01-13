# MASTER RECOVERY PLAN
## Lost Commits: Jan 6 - Jan 10, 2026

**Created:** January 11, 2026
**Base Commit:** `bba56a3` (SACRED - Working Tauri API)
**Target:** Restore visual/feature changes while preserving Tauri API

---

## LOST COMMITS INVENTORY (16 total)

### COMMIT 1: `16b67c6`
- **Message:** Major UI overhaul: Blue theme, Research Agent, streamlined tools
- **Date:** 2026-01-06 20:06:37
- **Files Changed:**
  - `.claude.md` (325 lines changed)
  - `src-tauri/Cargo.lock` (767 lines)
  - `src/index.html` (478 lines) ⚠️ SACRED FILE
  - `src/main.css` (510 lines)
- **Risk:** HIGH - touches sacred index.html
- **Recovery Status:** [ ] Not Started

---

### COMMIT 2: `90dd124`
- **Message:** Add backup files before YouTube Agent implementation
- **Date:** 2026-01-08 10:54:21
- **Files Changed:**
  - `src/index.html.backup-jan6` (3629 lines)
  - `src/toolkits/developer.html.backup-jan6` (2574 lines)
  - `src/toolkits/pm.html.backup-jan6` (1792 lines)
  - `src/toolkits/qcm.html.backup-jan6` (1912 lines)
  - `src/toolkits/traffic.html.backup-jan6` (3609 lines)
- **Risk:** LOW - backup files only
- **Recovery Status:** [ ] Not Started

---

### COMMIT 3: `ff37251`
- **Message:** Add YouTube Agent Runner tool UI
- **Date:** 2026-01-08 12:11:37
- **Files Changed:**
  - `src/index.html` (14 lines) ⚠️ SACRED FILE
  - `src/toolkits/youtube-agent.html` (1115 lines) - NEW FILE
- **Risk:** MEDIUM - new toolkit file is safe, index.html touch needs review
- **Recovery Status:** [ ] Not Started

---

### COMMIT 4: `4279ab6`
- **Message:** Update YouTube Agent: branding (blue) + display-only mode
- **Date:** 2026-01-08 14:35:59
- **Files Changed:**
  - `src/toolkits/youtube-agent.html` (92 lines)
- **Risk:** LOW - toolkit file only
- **Recovery Status:** [ ] Not Started

---

### COMMIT 5: `4b4a28b`
- **Message:** YouTube Agent: Complete UI overhaul per feedback
- **Date:** 2026-01-08 15:36:08
- **Files Changed:**
  - `src/toolkits/youtube-agent.html` (270 lines)
- **Risk:** LOW - toolkit file only
- **Recovery Status:** [ ] Not Started

---

### COMMIT 6: `d89dee3`
- **Message:** YouTube Agent: Replace emojis with Lucide icons + UI fixes
- **Date:** 2026-01-08 16:04:35
- **Files Changed:**
  - `src/toolkits/youtube-agent.html` (62 lines)
- **Risk:** LOW - toolkit file only
- **Recovery Status:** [ ] Not Started

---

### COMMIT 7: `db63374`
- **Message:** Add shared Claude Code plugin configuration
- **Date:** 2026-01-09 11:21:16
- **Files Changed:**
  - `.claude/settings.json` (9 lines) - NEW FILE
  - `.gitignore` (3 lines)
- **Risk:** LOW - config files only
- **Recovery Status:** [ ] Not Started

---

### COMMIT 8: `bf0bbe9`
- **Message:** Add /eos slash command for End of Session protocol
- **Date:** 2026-01-09 11:46:01
- **Files Changed:**
  - `.claude/commands/eos.md` (102 lines) - NEW FILE
- **Risk:** LOW - command file only
- **Recovery Status:** [ ] Not Started

---

### COMMIT 9: `34d753e`
- **Message:** BACKUP: before CC Master Build Specification execution
- **Date:** 2026-01-09 18:42:31
- **Files Changed:**
  - `index.html` (145 lines) ⚠️ ROOT SACRED FILE
  - Research files in 002 Agents/Research/ (8 new files, 1148 lines)
- **Risk:** MEDIUM - touches root index.html, research files safe
- **Recovery Status:** [ ] Not Started

---

### COMMIT 10: `3b3ae10`
- **Message:** COMPLETE: CC Master Build Specification - All 6 phases
- **Date:** 2026-01-09 19:58:20
- **Files Changed:**
  - `.claude/agents/` (6 new agent files)
  - `.claude/commands/` (5 new command files)
  - `.claude/hooks/ralph-stop-hook.ps1`
  - `package.json` (5 lines)
  - `playwright.config.js` (77 lines) - NEW FILE
  - `tests/verification.spec.js` (241 lines) - NEW FILE
- **Risk:** LOW - mostly new files, very valuable
- **Recovery Status:** [ ] Not Started

---

### COMMIT 11: `00db97a`
- **Message:** BRANDING: New Trajanus 3D logo lockup - Black/White/Blue theme
- **Date:** 2026-01-10 09:32:32
- **Files Changed:**
  - `index.html` (268 lines) ⚠️ ROOT SACRED FILE - 3D LOGO CSS/HTML
- **Risk:** MEDIUM - visual changes to root index.html
- **Recovery Status:** [ ] Not Started

---

### COMMIT 12: `0ced170`
- **Message:** FIX: Copy logo update to correct src/index.html location
- **Date:** 2026-01-10 11:46:00
- **Files Changed:**
  - `src/index.html` (10913 lines) ⚠️ SACRED FILE - MASSIVE OVERWRITE
- **Risk:** CRITICAL - this overwrote working Tauri API with broken version
- **Recovery Status:** [ ] SKIP - This broke the API

---

### COMMIT 13: `7c53c6a` ⚠️ DANGER
- **Message:** PURGE: Remove all Electron code - Tauri 2.0 only
- **Date:** 2026-01-10 12:10:25
- **Files Changed:**
  - `main.js` (335 lines DELETED)
  - `package.json` (24 lines)
  - `preload.js` (137 lines DELETED)
- **Risk:** LOW - removing Electron files is correct
- **Note:** The PURGE was correct for Rust/Tauri, but the index.html from 0ced170 had Electron API calls
- **Recovery Status:** [ ] Partial - package.json cleanup may be useful

---

### COMMIT 14: `1d50266`
- **Message:** ENHANCE: Add Google Docs conversion to /eos command
- **Date:** 2026-01-10 12:31:26
- **Files Changed:**
  - `.claude/commands/eos.md` (34 lines)
- **Risk:** LOW - command file only
- **Recovery Status:** [ ] Not Started

---

### COMMIT 15: `62ece88`
- **Message:** UPDATE: Clarify Google Docs conversion is GUI-based (optional)
- **Date:** 2026-01-10 12:38:05
- **Files Changed:**
  - `.claude/commands/eos.md` (40 lines)
- **Risk:** LOW - command file only
- **Recovery Status:** [ ] Not Started

---

### COMMIT 16: `b0be32a`
- **Message:** SIMPLIFY: Remove conversion step from /eos command
- **Date:** 2026-01-10 12:47:54
- **Files Changed:**
  - `.claude/commands/eos.md` (26 lines)
- **Risk:** LOW - command file only
- **Recovery Status:** [ ] Not Started

---

## RECOVERY CATEGORIES

### SAFE TO CHERRY-PICK (No index.html changes)
| Commit | Description | Priority |
|--------|-------------|----------|
| `db63374` | Claude Code plugin config | HIGH |
| `bf0bbe9` | /eos slash command | HIGH |
| `3b3ae10` | CC Master Build (agents, commands, tests) | HIGH |
| `90dd124` | Backup files | LOW |
| `4279ab6` | YouTube Agent branding | MEDIUM |
| `4b4a28b` | YouTube Agent UI overhaul | MEDIUM |
| `d89dee3` | YouTube Agent icons | MEDIUM |

### REQUIRES SURGICAL EXTRACTION (Touch index.html)
| Commit | Description | Risk |
|--------|-------------|------|
| `ff37251` | YouTube Agent - 14 lines in index.html | MEDIUM |
| `00db97a` | 3D logo in ROOT index.html | MEDIUM |
| `16b67c6` | Blue theme - 478 lines in src/index.html | HIGH |

### SKIP - CAUSED THE BREAK
| Commit | Description | Reason |
|--------|-------------|--------|
| `0ced170` | Copy logo to src/index.html | Overwrote Tauri API with Electron calls |

---

## RECOVERY SEQUENCE

### Phase 1: Safe Cherry-Picks (No risk)
1. [ ] `db63374` - Claude Code plugin config
2. [ ] `bf0bbe9` - /eos slash command
3. [ ] `3b3ae10` - CC Master Build (agents, commands, playwright)
4. [ ] Playwright verify app still works

### Phase 2: YouTube Agent (New files, minimal index.html)
5. [ ] Extract `youtube-agent.html` from `d89dee3` (final version)
6. [ ] Surgical add YouTube Agent button to index.html (14 lines from ff37251)
7. [ ] Playwright verify

### Phase 3: 3D Logo (Visual only, root index.html)
8. [ ] Extract 3D logo CSS from `00db97a`
9. [ ] Apply to ROOT index.html only (not src/index.html)
10. [ ] Playwright verify

### Phase 4: Blue Theme (Most complex)
11. [ ] Extract main.css changes from `16b67c6`
12. [ ] Apply to src/main.css
13. [ ] DO NOT touch src/index.html
14. [ ] Playwright verify

---

## VERIFICATION CHECKLIST

### After Each Phase:
- [ ] Run `cargo tauri dev`
- [ ] App launches without error
- [ ] Playwright screenshot taken
- [ ] Visual changes confirmed
- [ ] Tauri API still works (test invoke calls)

### Final Verification:
- [ ] All 9 Tauri invoke calls intact in src/index.html
- [ ] App launches and runs
- [ ] YouTube Agent accessible
- [ ] 3D logo visible
- [ ] Blue theme applied
- [ ] All sidebar buttons functional

---

## TAURI API VERIFICATION

**Must preserve these 9 invoke calls in src/index.html:**
```javascript
window.__TAURI__.core.invoke('run_python_script', ...)
window.__TAURI__.core.invoke('embed_url', ...)
window.__TAURI__.core.invoke('close_embedded', ...)
window.__TAURI__.core.invoke('enable_quad_chat', ...)
window.__TAURI__.core.invoke('disable_quad_chat', ...)
window.__TAURI__.core.invoke('is_quad_chat_enabled', ...)
// Plus 3 more
```

**After ANY change, verify with:**
```powershell
grep -c "__TAURI__" src/index.html
# Should return: 9
```

---

## NOTES

- `bba56a3` is now SACRED baseline
- All recovery work on VERSIONED COPIES only
- Bill approves before any integration
- Playwright verification MANDATORY

---

**END OF MASTER RECOVERY PLAN**
