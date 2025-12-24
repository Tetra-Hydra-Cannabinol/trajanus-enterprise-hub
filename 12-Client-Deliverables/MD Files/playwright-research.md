# Playwright MCP Research for Electron Apps

## Research Date: 2025-12-14

---

## Executive Summary

**Can we use Playwright MCP with our Electron app?**

**Answer:** YES, with caveats.

Two approaches available:
1. **Standard Playwright MCP** - For browser-based testing (web views)
2. **Playwright Electron API** - For direct Electron app control (custom scripts)

---

## Option 1: Standard Playwright MCP (@playwright/mcp)

### What It Does
- Automates browsers (Chrome, Firefox, WebKit)
- Uses accessibility tree instead of screenshots (LLM-friendly)
- Works via structured data, not vision models

### Installation for Claude Code
```bash
claude mcp add playwright npx @playwright/mcp@latest
```

Or with user scope (available across all projects):
```bash
claude mcp add playwright -s user npx @playwright/mcp@latest
```

### Configuration Options
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

### Key Arguments
- `--browser` - Browser selection (chromium, firefox, webkit)
- `--headless` - Run without visible window
- `--viewport-size` - Screen dimensions
- `--save-trace` - Save trace files for debugging
- `--save-video` - Record video of session

### Limitations for Electron
- **Does NOT directly control Electron apps**
- Controls browsers only
- Would need Electron app to serve via localhost for this to work

### Use Case for Us
- Testing web components in a browser context
- Validating HTML/CSS in Chrome before Electron integration
- NOT suitable for direct Electron app screenshots

---

## Option 2: Playwright Electron API (Native)

### What It Does
- **EXPERIMENTAL** support for Electron automation
- Launches Electron apps directly via `_electron.launch()`
- Can take screenshots, interact with UI, record video
- Works with Electron v12.2.0+ (we use v28.0.0 - compatible)

### How to Use
Requires custom scripts, not MCP. Example:

```javascript
const { _electron: electron } = require('playwright');

async function testApp() {
  // Launch our Electron app
  const electronApp = await electron.launch({
    args: ['.'],
    executablePath: 'node_modules/electron/dist/electron.exe'
  });

  // Get the first window
  const window = await electronApp.firstWindow();

  // Take screenshot
  await window.screenshot({ path: 'screenshot.png' });

  // Navigate and interact
  await window.click('text=QCM');
  await window.screenshot({ path: 'qcm-workspace.png' });

  // Close
  await electronApp.close();
}
```

### Capabilities
- Launch Electron apps
- Execute code in main process
- Control application windows
- Capture screenshots
- Record videos
- HAR file recording
- UI interaction (click, type, etc.)

### Installation
```bash
# In local temp directory (not Google Drive!)
npm install playwright
npx playwright install chromium
```

### For Our Project
Since we can't npm install on Google Drive, we installed Playwright in the temp fix directory:
```
C:\temp\electron-fix\node_modules\playwright
```

---

## Option 3: electron-playwright-mcp (Specialized)

### What It Does
- Dedicated MCP server for Electron apps (published Nov 2025)
- Enables AI assistants to interact with Electron apps
- Accessibility-first automation

### Status
- Very new (Nov 2025)
- Less documented than standard Playwright MCP
- Worth monitoring but standard approach is more stable

### Installation (if needed later)
```bash
claude mcp add electron-playwright npx electron-playwright-mcp@latest
```

---

## Recommendation for Trajanus Command Center

### Hybrid Approach:

1. **Install Standard Playwright MCP**
   - For general browser testing
   - Stable, well-documented
   - Useful for web component validation

2. **Create Custom Electron Test Script**
   - Uses Playwright's native `_electron` API
   - Direct control of our app
   - Screenshots, navigation, UI testing

3. **Playwright Installation Location**
   - Already installed at: `C:\temp\electron-fix\node_modules\playwright`
   - Copy to project if needed, or reference from temp location

---

## Sources

- [Playwright MCP GitHub](https://github.com/microsoft/playwright-mcp)
- [Playwright Electron Class](https://playwright.dev/docs/api/class-electron)
- [Simon Willison - Playwright MCP with Claude Code](https://til.simonwillison.net/claude-code/playwright-mcp-claude-code)
- [Testing Electron Apps with Playwright](https://dev.to/kubeshop/testing-electron-apps-with-playwright-3f89)

---

## Next Steps

1. Install standard Playwright MCP: `claude mcp add playwright npx @playwright/mcp@latest`
2. Create test-playwright.js script using Electron API
3. Test screenshot capability
4. Document workflow

---

**Conclusion:** Use standard Playwright MCP for browser testing + custom scripts for Electron app control. This gives us the best of both worlds with mature, stable tooling.
