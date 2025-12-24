# ADDING DEVELOPER UTILITY BUTTONS
**Quick Reference Guide**

---

## CURRENT DEVELOPER UTILITIES

### EOS & Session Management
- **Mission Brief** - Generate handoff prompt for new session
- **Sync Memory** - Refresh Claude's memory with key protocol files
- **Perform EOS Protocols** - End-of-session routine

### Reference Tools
- **Thesaurus** - Opens thesaurus.com
- **Style Guide** - Opens writing style reference
- **Regex Tester** - Opens regex testing tool
- **Color Picker** - Opens color selection tool

---

## HOW TO ADD NEW BUTTONS

### Pattern 1: Open External Website
```html
<button class="session-btn" onclick="openExternal('https://example.com')">
    Button Name
</button>
```

**Examples:**
- `openExternal('https://www.thesaurus.com')` - Thesaurus
- `openExternal('https://regex101.com')` - Regex Tester
- `openExternal('https://colorhunt.co')` - Color Palette
- `openExternal('https://caniuse.com')` - Browser Compatibility

### Pattern 2: Open Local File
```html
<button class="session-btn" onclick="openLocalFile('path/to/file.pdf')">
    Button Name
</button>
```

**Add this JavaScript function:**
```javascript
async function openLocalFile(filePath) {
    if (!window.electronAPI) return;
    try {
        await window.electronAPI.runCommand(`start "" "${filePath}"`);
        log(`Opened: ${filePath}`, 'success');
    } catch (err) {
        log(`Error: ${err.message}`, 'error');
    }
}
```

**Examples:**
```html
<!-- IBC Building Code -->
<button class="session-btn" onclick="openLocalFile('G:\\My Drive\\References\\IBC-2021.pdf')">
    IBC 2021
</button>

<!-- ACI Concrete Manual -->
<button class="session-btn" onclick="openLocalFile('G:\\My Drive\\References\\ACI-318.pdf')">
    ACI 318
</button>

<!-- Company Style Guide -->
<button class="session-btn" onclick="openLocalFile('G:\\My Drive\\00 - Trajanus USA\\Brand\\Style_Guide.docx')">
    Brand Guide
</button>
```

### Pattern 3: Run Python Script
```html
<button class="session-btn" onclick="runScript('script_name.py')">
    Button Name
</button>
```

**Add this JavaScript function:**
```javascript
async function runScript(scriptName) {
    if (!window.electronAPI) return;
    try {
        const scriptPath = `G:\\My Drive\\00 - Trajanus USA\\00-Command-Center\\${scriptName}`;
        await window.electronAPI.runCommand(`python "${scriptPath}"`);
        log(`Running: ${scriptName}`, 'info');
    } catch (err) {
        log(`Error: ${err.message}`, 'error');
    }
}
```

**Examples:**
```html
<!-- Update Living Documents -->
<button class="session-btn" onclick="runScript('update_living_documents_v3.py')">
    Update Living Docs
</button>

<!-- Batch Convert to Google Docs -->
<button class="session-btn" onclick="runScript('batch_convert_to_gdocs.py')">
    Batch Convert
</button>

<!-- Parse EOS Files -->
<button class="session-btn" onclick="runScript('parse_eos_automation.py')">
    Parse EOS
</button>
```

### Pattern 4: Open Google Drive Folder
```html
<button class="session-btn" onclick="openDriveFolder('folder-name')">
    Button Name
</button>
```

**Add this JavaScript function:**
```javascript
function openDriveFolder(folderName) {
    const folders = {
        'protocols': 'https://drive.google.com/drive/folders/YOUR_FOLDER_ID',
        'templates': 'https://drive.google.com/drive/folders/YOUR_FOLDER_ID',
        'sessions': 'https://drive.google.com/drive/folders/YOUR_FOLDER_ID'
    };
    
    if (folders[folderName]) {
        openExternal(folders[folderName]);
        log(`Opening ${folderName} folder`, 'info');
    }
}
```

**Examples:**
```html
<!-- Core Protocols Folder -->
<button class="session-btn" onclick="openDriveFolder('protocols')">
    Core Protocols
</button>

<!-- Template Library -->
<button class="session-btn" onclick="openDriveFolder('templates')">
    Templates
</button>

<!-- Session Files -->
<button class="session-btn" onclick="openDriveFolder('sessions')">
    Session Files
</button>
```

---

## RECOMMENDED UTILITIES TO ADD

### Reference Documents
- **IBC Building Code** - Building code reference
- **UFGS Specs** - Unified Facilities Guide Specifications
- **ACI Standards** - Concrete/structural standards
- **OSHA Standards** - Safety regulations
- **ITE Manual** - Traffic engineering reference

### Development Tools
- **JSON Formatter** - Format/validate JSON
- **Markdown Preview** - Preview markdown files
- **Image Compressor** - Reduce image file sizes
- **PDF Merger** - Combine multiple PDFs
- **Code Snippet Manager** - Quick access to code templates

### Writing Tools
- **Grammar Check** - Grammarly or similar
- **Readability Score** - Hemingway app
- **Citation Generator** - APA/MLA citations
- **Acronym Finder** - Construction acronyms

### Calculation Tools
- **Unit Converter** - Imperial/metric conversions
- **Concrete Calculator** - Volume/quantity calcs
- **Load Calculator** - Structural loads
- **Cost Estimator** - Quick cost estimates

### Communication
- **Email Template Generator** - Pre-written templates
- **Meeting Notes Template** - Standardized notes
- **Status Update Generator** - Quick status updates

---

## WHERE TO ADD BUTTONS

**Location in HTML:**
Find the "Developer Utilities" section (around line 450-500):

```html
<!-- Developer Utilities - DEVELOPER MODE ONLY -->
<div class="tool-section dev-mode-only">
    <div class="tool-section-header">Developer Utilities</div>
    <div class="button-grid">
        <!-- ADD NEW BUTTONS HERE -->
        <button class="session-btn" onclick="...">New Button</button>
    </div>
</div>
```

**Button Styling:**
- Standard utility: `class="session-btn"`
- Important action (like EOS): `class="session-btn end-session"` (green gradient)

---

## BUTTON ORGANIZATION

### Group by Function

**Session Management:**
- Mission Brief
- Sync Memory
- Perform EOS Protocols

**Reference Docs:**
- Thesaurus
- Style Guide
- Building Codes
- Standards

**Development Tools:**
- Regex Tester
- Color Picker
- JSON Formatter

**Automation Scripts:**
- Update Living Docs
- Batch Convert
- Parse EOS

---

## TESTING NEW BUTTONS

**After adding a button:**

1. Save index.html
2. Restart app: `npm start`
3. Enable Developer Mode (toggle in sidebar)
4. Click new button
5. Check terminal for output/errors
6. Verify expected action occurs

**Common Issues:**
- **Button doesn't appear** → Check it's inside `.dev-mode-only` section
- **Click does nothing** → Check JavaScript function exists
- **Error in terminal** → Check file path is correct
- **Wrong file opens** → Verify path uses correct slashes (\\)

---

## EXAMPLE: ADDING IBC CODE BUTTON

**Step 1:** Add button to HTML
```html
<button class="session-btn" onclick="openLocalFile('G:\\My Drive\\References\\IBC-2021.pdf')">
    IBC 2021
</button>
```

**Step 2:** Test
- Restart app
- Enable Developer Mode
- Click "IBC 2021" button
- PDF should open in default viewer

**Step 3:** Refine (if needed)
- Wrong file? → Fix path
- Doesn't open? → Check file exists
- Want different viewer? → Change default app in Windows

---

## FUTURE ENHANCEMENTS

### Dropdown Menus
For categories with many options:
```html
<button class="session-btn" onclick="showCodeMenu()">
    Building Codes ▼
</button>
```

### Custom Modals
For tools that need input:
```html
<button class="session-btn" onclick="showUnitConverter()">
    Unit Converter
</button>
```

### Keyboard Shortcuts
Quick access to frequent tools:
```javascript
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 't') {
        openExternal('https://www.thesaurus.com');
    }
});
```

---

## QUICK ADD CHECKLIST

- [ ] Decide button action (external URL, local file, script, folder)
- [ ] Choose appropriate pattern from above
- [ ] Add button HTML to Developer Utilities section
- [ ] Add any required JavaScript functions
- [ ] Test button functionality
- [ ] Add to this documentation
- [ ] Commit change to reference folder

---

**END OF GUIDE**
**Last Updated:** November 30, 2025
