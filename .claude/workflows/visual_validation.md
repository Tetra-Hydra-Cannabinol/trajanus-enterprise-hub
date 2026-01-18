# Visual Validation Workflow

## Overview
Playwright MCP-powered iterative loop for UI development. Make change → screenshot → validate → iterate until correct.

---

## Prerequisites

### Playwright MCP Installation
```bash
# Already installed at: C:\Dev\trajanus-command-center\.playwright-mcp\
# 100+ screenshots captured
```

### Available Tools
- `mcp__plugin_playwright_playwright__browser_navigate` - Go to URL
- `mcp__plugin_playwright_playwright__browser_snapshot` - Capture accessibility tree
- `mcp__plugin_playwright_playwright__browser_take_screenshot` - Visual capture
- `mcp__plugin_playwright_playwright__browser_click` - Interact with elements
- `mcp__plugin_playwright_playwright__browser_evaluate` - Run JavaScript

---

## The Iteration Loop

### Core Pattern
```
REPEAT:
    1. Make UI change
    2. Launch/refresh app
    3. Navigate to affected page
    4. Take screenshot
    5. Analyze against style guide
    6. IF matches → DONE
    7. IF issues found → FIX and REPEAT
UNTIL: Visual matches specification
```

### Maximum Iterations
- **Simple changes**: 3 iterations max
- **Complex changes**: 5 iterations max
- **Full page redesign**: 10 iterations max

If max reached without success → STOP and escalate to user.

---

## Screenshot Capture Protocol

### Standard Viewports
```javascript
// Desktop (primary)
{ width: 1920, height: 1080 }

// Tablet
{ width: 768, height: 1024 }

// Mobile (optional for this app)
{ width: 375, height: 667 }
```

### Screenshot Naming
```
[component]_[viewport]_[iteration]_[timestamp].png

Examples:
- qcm_workspace_desktop_01_20260117.png
- header_tablet_03_20260117.png
- buttons_desktop_final_20260117.png
```

### Screenshot Location
```
C:\Dev\trajanus-command-center\.playwright-mcp\screenshots\
```

---

## Validation Checklist

### Color Validation
```
[ ] Primary Silver: #C0C0C0
[ ] Primary Black: #1a1a1a
[ ] Primary Blue: #00AAFF (bright blue)
[ ] NO gold unless explicitly requested
[ ] NO unexpected colors
```

### Layout Validation
```
[ ] 3-column layout maintained (where applicable)
[ ] Header text centered: "TRAJANUS USA"
[ ] Return button top-left: "← Hub"
[ ] Mode tabs horizontal below header
[ ] Proper spacing/padding
[ ] No overflow/clipping
```

### Button Validation
```
[ ] ext-btn: 120×44px with 3D gradient
[ ] script-btn: 160×50px with icon
[ ] nav-btn: 140×44px
[ ] Proper hover effects (translateY, brightness)
[ ] V2 Synapse glow on hover
[ ] Active state (translateY down)
```

### Typography Validation
```
[ ] Roboto font family
[ ] Proper weight hierarchy
[ ] Readable contrast
[ ] No text overflow
```

### Animation Validation
```
[ ] Transitions smooth (0.3s ease)
[ ] No jarring movements
[ ] Hover states animate
[ ] No animation on page load (unless intended)
```

---

## Workflow Steps

### Step 1: Pre-Change Baseline
```
1. Launch app: npm start (in C:\Dev\trajanus-command-center)
2. Navigate to target page
3. Take "BEFORE" screenshot
4. Document current state
```

### Step 2: Make Change
```
1. Edit CSS/HTML/JS
2. Save file
3. Use surgical edit (specific lines only)
4. Document what changed
```

### Step 3: Capture Result
```javascript
// Navigate to page
await browser_navigate({ url: 'http://localhost:1420' });

// Wait for load
await browser_wait_for({ time: 2 });

// Click to navigate if needed
await browser_click({ element: 'QCM Platform card', ref: '[ref]' });

// Take screenshot
await browser_take_screenshot({
    filename: 'component_desktop_01.png',
    fullPage: false
});
```

### Step 4: Analyze
Compare screenshot against:
1. Style guide specifications
2. BEFORE screenshot (regression check)
3. User requirements
4. Brand standards

### Step 5: Document Findings
```markdown
## Iteration 1 Analysis

### Changes Made
- Modified `file.css:line` - [description]

### Screenshot
- File: `component_desktop_01.png`

### Validation Results
- [x] Colors correct
- [x] Layout maintained
- [ ] Button size incorrect - 100px instead of 120px
- [x] Typography correct

### Issues Found
1. Button width too narrow

### Next Action
- Fix button width in line XX
```

### Step 6: Iterate or Complete
```
IF all checks pass:
    - Take FINAL screenshot
    - Document success
    - Commit changes

ELSE:
    - Fix identified issues
    - Return to Step 2
```

---

## Automated Triggers

### When to Auto-Validate
- After ANY CSS change
- After HTML structure change
- After JavaScript affecting DOM
- Before committing UI changes

### Trigger Phrases
When user says:
- "check the UI"
- "validate visually"
- "screenshot please"
- "does it look right?"

→ Execute full validation workflow

---

## Common Issues & Fixes

### Issue: Colors Look Wrong
```
Cause: CSS variable not applied, wrong hex value
Fix: Check computed styles, verify hex codes
```

### Issue: Layout Broken
```
Cause: Flex/grid change, overflow, z-index
Fix: Inspect element, check parent containers
```

### Issue: Buttons Wrong Size
```
Cause: Missing width/height, conflicting CSS
Fix: Add explicit dimensions, check specificity
```

### Issue: Animation Missing
```
Cause: Transition not defined, wrong property
Fix: Add transition, verify property name
```

### Issue: Screenshot Blank/Wrong
```
Cause: Page not loaded, wrong URL, element not rendered
Fix: Add wait time, verify URL, check visibility
```

---

## Integration with Other Workflows

### With GSD Framework
Visual Validation is part of VALIDATE phase:
```
EXPLORE → PLAN → EXECUTE → VALIDATE (includes Visual Validation)
```

### With Planner/Developer
CC executes Visual Validation, reports to CP:
```markdown
## TASK_REPORT

### Visual Validation
- Screenshots: [list]
- Iterations: 2
- Final status: PASSED
- Style guide compliance: YES
```

### With Context Management
Long validation sessions may consume context:
```
- Each screenshot + analysis = ~500 tokens
- 5 iterations = ~2500 tokens
- Monitor gauge, checkpoint if needed
```

---

## Quality Standards

### Minimum Requirements
- At least 1 screenshot per UI change
- Desktop viewport always captured
- BEFORE/AFTER for significant changes
- Style guide check documented

### Best Practice
- 3 viewports for responsive changes
- Compare against reference designs
- Document any deviations with justification
- Keep screenshot archive for reference

---

## Example Session

```markdown
## Visual Validation: QCM Workspace Header

### Iteration 1
- Changed: main.css:245 - header background to #1a1a1a
- Screenshot: qcm_header_01.png
- Issue: Text not visible (white on black needed)
- Fix: Change color to #C0C0C0

### Iteration 2
- Changed: main.css:248 - text color to #C0C0C0
- Screenshot: qcm_header_02.png
- Issue: None found
- Status: PASSED

### Final
- Screenshot: qcm_header_final.png
- Validation: All checks passed
- Commit: "Fix QCM header colors to match style guide"
```

---

**Last Updated:** 2026-01-17
**Version:** 1.0
