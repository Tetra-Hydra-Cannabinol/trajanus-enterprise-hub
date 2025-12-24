# Trajanus Command Center - Electron App

## Overview

Native desktop application for Trajanus USA project management and automation.
Built with Electron - runs on Windows, Mac, and Linux.

## Features

- **Sidebar Navigation**: Switch between Developer and Working projects
- **Session Management**: 5 core buttons for living document automation
- **Real-time Terminal**: See script output as it happens
- **Native File Picker**: Select files using Windows dialogs
- **Status Bar**: Connection status and platform info

## Installation

### Prerequisites

1. **Node.js** (v18 or higher)
   - Download from: https://nodejs.org/
   - Install the LTS version
   - Verify: `node --version` and `npm --version`

2. **Python** (already installed)
   - Verify: `python --version`

### Setup Steps

1. **Open PowerShell in the project folder:**
   ```
   cd "G:\My Drive\00 - Trajanus USA\00-Command-Center\trajanus-command-center"
   ```

2. **Install dependencies:**
   ```
   npm install
   ```
   This downloads Electron and other packages (~200MB first time)

3. **Run the app:**
   ```
   npm start
   ```

The Command Center window should open!

## Building Distributable

To create a standalone .exe installer:

```
npm run build
```

This creates:
- `dist/Trajanus Command Center Setup.exe` - Windows installer
- `dist/win-unpacked/` - Portable version (no install needed)

## Project Structure

```
trajanus-command-center/
├── package.json      # Project config and dependencies
├── main.js           # Electron main process (runs Python scripts)
├── preload.js        # Secure bridge between UI and Node
├── index.html        # The user interface
├── assets/           # Icons and images
│   └── icon.png      # App icon (add your own)
└── dist/             # Built executables (after npm run build)
```

## Customization

### Adding New Buttons

In `index.html`, add to the `.button-grid`:

```html
<button class="session-btn" data-tooltip="Your tooltip" onclick="yourFunction()">
    Button Text
</button>
```

Then add the function in the `<script>` section:

```javascript
async function yourFunction() {
    log('Starting...', 'info');
    const result = await window.electronAPI.runPythonScript('your_script.py');
    if (result.success) {
        log('Done!', 'success');
    }
}
```

### Adding New Projects

In the sidebar, add to the appropriate section:

```html
<button class="project-btn" data-project="project-id">
    <span class="icon">🔧</span> Project Name
</button>
```

### Changing Colors

Edit the CSS variables in `:root`:

```css
--teal-dark: #1a365d;
--green-mid: #2d7a4f;
/* etc */
```

## Troubleshooting

### "npm is not recognized"
Node.js not installed or not in PATH. Reinstall Node.js.

### "electron is not recognized"
Run `npm install` first.

### Python scripts not found
Make sure the working directory in `main.js` is correct:
```javascript
const workingDir = 'G:\\My Drive\\00 - Trajanus USA\\00-Command-Center';
```

### Window is blank
Open DevTools: Uncomment this line in `main.js`:
```javascript
mainWindow.webContents.openDevTools();
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-24 | Initial proof-of-concept |

---

Created by Bill King & Claude AI
Trajanus USA - Engineered Intelligence
