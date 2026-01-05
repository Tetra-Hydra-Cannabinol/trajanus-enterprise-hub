# CLAUDE.md - Trajanus Enterprise Hub

## Project Overview
Tauri 2.0 desktop app for construction project management. Single-file architecture.
**Owner:** Bill King, Principal/CEO Trajanus USA
**Stack:** Tauri 2.0 (Rust backend), HTML/CSS/JavaScript frontend

## Critical Files
- `src/index.html` - Main application (305KB, ~7000 lines). ALL UI lives here.
- `src-tauri/tauri.conf.json` - Tauri configuration
- `src-tauri/src/main.rs` - Rust backend, IPC handlers

## Working Directory
**ALWAYS:** `C:\Dev\trajanus-command-center\`
**NEVER:** `C:\Users\`, `C:\Dev\` root, or any other location

## File Edit Rules
1. Use `str_replace` for surgical edits - NEVER rewrite sections
2. Create backup before ANY edit: `copy src/index.html src/index.html.backup-YYYYMMDD-HHMM`
3. One change at a time, verify before next change
4. NEVER rename or delete: `index.html`, `main.rs`, `tauri.conf.json`, `package.json`

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
- IPC via `window.__TAURI__.invoke()` or `window.electronAPI` wrapper

## Code Patterns
- Workspace switching: `showWorkspace('workspace-id')`
- Tab management: `addToolTab(name, contentHTML)`, `switchTab(tabId)`
- Modal popups: `openToolModal(title, scriptPath)`
- File browser: `openFileBrowser(folderKey)` with `folderPaths` mapping

## Security Rules
- NO secrets in code (API keys, tokens)
- NO `eval()` or `Function()` constructors
- NO `innerHTML` with user input
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
3. Visual verification by user
4. Git commit after approval

## What NOT To Do
- Don't add features not explicitly requested
- Don't "improve" working code
- Don't create new files unless specified
- Don't ask permission - execute the task
- Don't explain what you're going to do - just do it and report results
