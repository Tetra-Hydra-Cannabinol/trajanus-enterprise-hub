# CLAUDE.md - Trajanus Enterprise Hub

## Project Overview
Tauri 2.0 desktop app for construction project management. Single-file architecture.
**Owner:** Bill King, Principal/CEO Trajanus USA
**Stack:** Tauri 2.0 (Rust backend), HTML/CSS/JavaScript frontend

## Critical Files
- `src/index.html` - Main application (~7000 lines). ALL UI lives here.
- `src-tauri/tauri.conf.json` - Tauri configuration
- `src-tauri/src/lib.rs` - Rust backend, IPC handlers
- `src/toolkits/*.html` - Reference implementations (CORRECT - use as templates)

## MANDATORY RULES (NEVER VIOLATE)

### Rule 1: Surgical Edits Only
- **NEVER** overwrite entire files or large sections
- **ALWAYS** use `str_replace` / `Edit` tool for targeted changes
- One change at a time, verify before next change
- Create backup before ANY risky edit

### Rule 2: Visual Verification Required
- **NEVER** say "file is correct" without visual proof
- **ALWAYS** verify with Playwright screenshot before claiming success
- Test the actual UI behavior, not just code syntax
- No console errors on action = minimum bar

### Rule 3: Follow CP Instructions Exactly
- Execute tasks as specified - no interpretation
- Don't add features not explicitly requested
- Don't "improve" working code
- Don't ask permission - execute and report results

### Rule 4: Tauri API Only
- IPC via `window.__TAURI__.core.invoke()`
- NO `window.electronAPI` - this is Tauri, not Electron
- Reference `src/toolkits/*.html` for correct patterns

### Rule 5: Protected Files
- **NEVER** rename or delete: `index.html`, `lib.rs`, `tauri.conf.json`, `package.json`
- **NEVER** modify `src/toolkits/*.html` unless explicitly requested (they are correct)

## Working Directory
**ALWAYS:** `C:\Dev\trajanus-command-center\` (Windows) or repo root (Linux)
**NEVER:** `C:\Users\`, `C:\Dev\` root, or any other location

## Build & Test Commands
```bash
npm run tauri dev     # Development mode
npm run tauri build   # Production build
npm run lint          # Check code
```

## Architecture Constraints
- NO external browser windows - everything embedded or Tauri-managed
- Script tools use popup modal (see openToolModal pattern ~line 3200)
- Tauri WebView for external URLs (claude.ai embedding)
- WebView2 on Windows - be aware of cache/session persistence

## Code Patterns (from src/toolkits/ reference)
- Workspace switching: `showWorkspace('workspace-id')`
- Tab management: `addToolTab(name, contentHTML)`, `switchTab(tabId)`
- Modal popups: `openToolModal(title, scriptPath)`
- File browser: `openFileBrowser(folderKey)` with `folderPaths` mapping
- Tauri invoke: `await window.__TAURI__.core.invoke('command_name', { args })`

## Security Rules
- NO secrets in code (API keys, tokens)
- NO `eval()` or `Function()` constructors
- NO `innerHTML` with unsanitized user input
- Sanitize all file paths before use

## Git Workflow
```bash
git add src/index.html
git commit -m "Feature: [description]"
git push origin main
```
Commit after EVERY verified feature change.

## Success Criteria Pattern
Every feature must have:
1. Testable completion state (click X, see Y)
2. No console errors on action
3. Visual verification (screenshot or user confirmation)
4. Git commit after approval

## What NOT To Do
- Don't add features not explicitly requested
- Don't "improve" working code
- Don't create new files unless specified
- Don't ask permission - execute the task
- Don't explain what you're going to do - just do it and report results
- Don't claim success without verification
- Don't overwrite files - surgical edits only
