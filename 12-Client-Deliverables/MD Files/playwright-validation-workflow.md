# Playwright Validation Workflow

## Purpose
Use Playwright to validate UI changes against design specs in the Trajanus Command Center Electron app.

---

## Quick Reference

### Run Screenshot Test
```powershell
cd "C:\temp\electron-fix"
node test-playwright-electron.js
```

### Screenshots Location
```
G:\My Drive\00 - Trajanus USA\00-Command-Center\screenshots\
```

---

## Workflow Steps

### 1. Before Making UI Changes
Capture baseline screenshots:
```powershell
cd "C:\temp\electron-fix"
node test-playwright-electron.js
```

Rename screenshots folder:
```powershell
Rename-Item "screenshots" "screenshots-before"
```

### 2. Make Code Changes
Edit index.html, CSS, or JavaScript as needed.

### 3. Capture After Screenshots
```powershell
node test-playwright-electron.js
```

### 4. Compare Before/After
Open both screenshot folders and visually compare:
- Layout changes
- Color differences
- Element positioning
- Responsive behavior

### 5. Iterate Until Correct
Repeat steps 2-4 until UI matches design spec.

---

## Test Script Usage

### Basic Test (All Viewports)
```powershell
node test-playwright-electron.js
```

Output:
- main-window.png (initial app state)
- qcm-workspace.png (QCM workspace view)
- viewport-desktop.png (1920x1080)
- viewport-laptop.png (1366x768)
- viewport-tablet-landscape.png (1024x768)

### Custom Test Script Template
```javascript
const { _electron: electron } = require('playwright');
const path = require('path');

const APP_PATH = 'G:\\My Drive\\00 - Trajanus USA\\00-Command-Center';

async function customTest() {
  const electronApp = await electron.launch({
    args: [APP_PATH],
    executablePath: path.join(APP_PATH, 'node_modules', 'electron', 'dist', 'electron.exe')
  });

  const window = await electronApp.firstWindow();
  await window.waitForLoadState('domcontentloaded');
  await new Promise(r => setTimeout(r, 2000));

  // Your custom test code here

  await electronApp.close();
}

customTest().catch(console.error);
```

---

## Common Selectors

### Navigation Elements
| Element | Selector | Notes |
|---------|----------|-------|
| QCM Button | `text=QCM` | Sidebar navigation |
| PM Toolkit | `text=PM Toolkit` | Sidebar navigation |
| Developer | `text=Developer` | Sidebar navigation |

### QCM Workspace Elements
| Element | Selector | Notes |
|---------|----------|-------|
| File Browser | `.file-browser` | Document selection area |
| Template Panel | `.template-panel` | Template selection |
| Selected Queue | `.selected-files` | Files selected for review |

### Generic Selectors
```javascript
// By text content
await window.locator('text=Submit').click();

// By CSS class
await window.locator('.qcm-panel').screenshot({ path: 'panel.png' });

// By ID
await window.locator('#workspace-container').isVisible();

// Combined
await window.locator('button:has-text("Save")').click();
```

---

## Viewport Testing

### Standard Viewports
```javascript
const viewports = [
  { width: 1920, height: 1080, name: 'desktop' },
  { width: 1366, height: 768, name: 'laptop' },
  { width: 1024, height: 768, name: 'tablet-landscape' },
  { width: 768, height: 1024, name: 'tablet-portrait' }
];

for (const vp of viewports) {
  await window.setViewportSize({ width: vp.width, height: vp.height });
  await new Promise(r => setTimeout(r, 500)); // Wait for resize
  await window.screenshot({ path: `${vp.name}.png` });
}
```

---

## Element Screenshots

### Capture Specific Element
```javascript
// Find element
const panel = await window.locator('.qcm-panel');

// Take element screenshot
await panel.screenshot({ path: 'qcm-panel-only.png' });
```

### Full Page vs Viewport
```javascript
// Viewport only (default)
await window.screenshot({ path: 'viewport.png' });

// Full page (scrollable content)
await window.screenshot({ path: 'fullpage.png', fullPage: true });
```

---

## Video Recording

### Record Session
```javascript
const electronApp = await electron.launch({
  args: [APP_PATH],
  executablePath: path.join(APP_PATH, 'node_modules', 'electron', 'dist', 'electron.exe'),
  recordVideo: { dir: './videos/' }
});

// ... test actions ...

await electronApp.close(); // Video saved on close
```

---

## Troubleshooting

### App Won't Launch
```powershell
# Verify electron binary exists
Test-Path "G:\My Drive\00 - Trajanus USA\00-Command-Center\node_modules\electron\dist\electron.exe"
```

### Screenshots Are Blank
Add extra wait time:
```javascript
await window.waitForLoadState('networkidle');
await new Promise(r => setTimeout(r, 3000));
```

### Element Not Found
Use DevTools to inspect:
1. Launch app normally: `npm start`
2. Press F12 for DevTools
3. Use inspector to find correct selector

### Timeout Errors
Increase timeout:
```javascript
await window.waitForSelector('.element', { timeout: 60000 });
```

---

## Integration with Claude Code

### Request Screenshot During Development
Tell Claude Code:
> "Run the Playwright test script and show me the QCM workspace screenshot"

### Request Viewport Testing
> "Test the app at mobile viewport and capture screenshots"

### Compare Changes
> "Take before/after screenshots of the sidebar changes"

---

## Files Reference

| File | Location | Purpose |
|------|----------|---------|
| test-playwright-electron.js | Project root | Main test script |
| test-playwright-electron.js | C:\temp\electron-fix\ | Working copy with Playwright |
| screenshots/ | Project root | Screenshot output |
| playwright-research.md | Project root | Research findings |

---

## Maintenance Notes

### Playwright Location
Playwright is installed at `C:\temp\electron-fix\` because:
- Cannot npm install on Google Drive (file locking issues)
- Temp location allows full package installation
- Scripts reference project on Google Drive but run from temp

### Updating Playwright
```powershell
cd "C:\temp\electron-fix"
npm update playwright
npx playwright install chromium
```

---

**Last Updated:** 2025-12-14
**Status:** Active
