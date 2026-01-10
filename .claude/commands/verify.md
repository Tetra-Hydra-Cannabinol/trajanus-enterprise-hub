---
description: Run Playwright verification on current Tauri app state
allowed-tools: mcp__playwright__*, mcp__plugin_playwright_playwright__*, Bash(*), Read
---

# Playwright Verification Protocol

## Purpose
Verify the current state of the Trajanus Enterprise Hub by running automated UI checks.

## Prerequisites
- Tauri dev server running at localhost:1420
- OR Static server at localhost:8080

## Verification Steps

### Step 1: Check Server Status
First verify a dev server is running:
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:1420 || curl -s -o /dev/null -w "%{http_code}" http://localhost:8080
```

### Step 2: Navigate to App
Use Playwright to navigate to the running app:
- Primary: http://localhost:1420 (Tauri dev)
- Fallback: http://localhost:8080 (static server)

### Step 3: Capture Initial State
Take a browser snapshot to assess current UI state.

### Step 4: Run Verification Checklist

Check the following elements exist and are functional:

**Landing Page:**
- [ ] Page loads without errors
- [ ] Logo/branding visible
- [ ] Navigation buttons present (Enterprise Hub, PM Toolkit, QCM, etc.)
- [ ] No console errors

**Platform Navigation:**
- [ ] Enterprise Hub button clickable
- [ ] QCM/Submittal Review button clickable
- [ ] Developer Project button clickable

**QCM Workspace (if accessible):**
- [ ] 3-panel layout renders
- [ ] "Trajanus EI" branding present
- [ ] "Send to Trajanus for Review" text present

### Step 5: Document Results

Output verification report:
```
## Verification Report - [DATE]

### Summary
- Total Checks: X
- Passed: X
- Failed: X

### Details
[List each check with PASS/FAIL status]

### Screenshots
[Reference any screenshots taken]

### Issues Found
[List any problems discovered]
```

## Quick Commands

To manually start a verification:
1. Ensure server running: `npm run tauri dev` or `python -m http.server 8080`
2. Run Playwright snapshot
3. Check for expected elements

## Troubleshooting

- If Playwright MCP fails, check settings.json has playwright plugin enabled
- If server not responding, start with appropriate command
- If elements missing, document for debugging
