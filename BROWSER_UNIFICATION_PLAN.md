# FIX ALL BROWSERS - USE LIVING DOCS TEMPLATE

**Mission:** Make ALL browser buttons work like Living Documents Browser.

---

## STEP 1: ANALYZE WORKING TEMPLATE

**Extract Living Documents Browser code:**

```bash
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center"

# Find the working openLivingDocsBrowser function
grep -n "function openLivingDocsBrowser" index.html

# Extract complete function (approximately lines 6276-6400)
sed -n '6276,6400p' index.html > living_docs_browser_template.js
```

**Document what makes it work:**
- Modal overlay structure
- Brown/orange styling
- Real Google Drive IPC call: `window.electronAPI.listDirectory()`
- Search/sort/refresh functionality
- File list rendering
- Preview panel

---

## STEP 2: IDENTIFY ALL BROWSER BUTTONS

**Website Tools workspace:**
- ✅ Living Documents Browser (WORKING - this is the template)

**Developer Tools workspace (terminal tabs):**
- ❌ Core Protocols
- ❌ Learning Folder
- ❌ Scripts
- ❌ Documentation
- ❌ Session Files (if exists)
- ❌ Templates (if exists)

**Other workspaces:**
- ❌ TKB button (rename to "Trajanus Knowledge Base (MCP)")

**List all buttons and their current onclick handlers:**

```bash
# Find all browser-related buttons
grep -n "onclick=.*[Bb]rowser\|onclick=.*openLocal" index.html | grep -v "Living"

# Show what each button currently does
```

---

## STEP 3: MAP BUTTONS TO FOLDERS

**Create folder mapping:**

| Button Name | Target Folder | Path |
|-------------|--------------|------|
| Core Protocols | 03-Protocols | G:\\My Drive\\00 - Trajanus USA\\03-Protocols |
| Learning Folder | 07-Learning | G:\\My Drive\\00 - Trajanus USA\\07-Learning |
| Scripts | 08-Scripts | G:\\My Drive\\00 - Trajanus USA\\08-Scripts |
| Documentation | 09-Documentation | G:\\My Drive\\00 - Trajanus USA\\09-Documentation |
| Session Files | 01-Morning-Sessions | G:\\My Drive\\00 - Trajanus USA\\01-Morning-Sessions |
| Templates | 06-Templates | G:\\My Drive\\00 - Trajanus USA\\06-Templates |
| Trajanus Knowledge Base (MCP) | [TBD - ASK USER] | [Path TBD] |

**Verify folders exist:**

```bash
# Check each folder exists
for folder in "03-Protocols" "07-Learning" "08-Scripts" "09-Documentation" "01-Morning-Sessions" "06-Templates"; do
  if [ -d "G:\My Drive\00 - Trajanus USA\$folder" ]; then
    echo "✓ $folder exists"
  else
    echo "✗ $folder NOT FOUND"
  fi
done
```

---

## STEP 4: CREATE BROWSER FUNCTIONS

**For each browser button, create function based on template:**

**Pattern:**
```javascript
function openCoreProtocolsBrowser() {
    // Copy exact structure from openLivingDocsBrowser()
    // Only change:
    // 1. Function name
    // 2. Modal title: "CORE PROTOCOLS BROWSER"
    // 3. Description: "Operational protocols and procedures"
    // 4. Folder path: 'G:\\My Drive\\00 - Trajanus USA\\03-Protocols'
}
```

**Create all functions:**
- openCoreProtocolsBrowser()
- openLearningFolderBrowser()
- openScriptsBrowser()
- openDocumentationBrowser()
- openSessionFilesBrowser()
- openTemplatesBrowser()
- openTKBBrowser() // Rename button text to "Trajanus Knowledge Base (MCP)"

---

## STEP 5: SURGICAL INJECTIONS

**DO NOT rewrite existing code. Use str_replace for each:**

**Example for Core Protocols button:**

```javascript
// Find current button
OLD: onclick="openLocalFolder('G:\\My Drive\\00 - Trajanus USA\\03-Protocols')"
NEW: onclick="openCoreProtocolsBrowser()"

// Add new function after openLivingDocsBrowser()
// Insert at line ~6400 (after Living Docs function)
```

**For each browser:**
1. Find button in HTML
2. Change onclick handler
3. Add browser function (copy/modify template)
4. Update modal title and path
5. Test in app

---

## STEP 6: RENAME TKB BUTTON

**Find TKB button:**
```bash
grep -n "TKB\|tkb\|Knowledge Base" index.html
```

**Change button text:**
```
OLD: >TKB Browser</button>
NEW: >Trajanus Knowledge Base (MCP)</button>
```

**Ask user for correct folder path before implementing.**

---

## STEP 7: TEST EACH BROWSER

**Systematic testing:**

```markdown
## BROWSER TESTING CHECKLIST

- [ ] Living Documents Browser (already working)
- [ ] Core Protocols Browser
  - [ ] Opens modal
  - [ ] Shows files from 03-Protocols
  - [ ] Search works
  - [ ] Refresh works
- [ ] Learning Folder Browser
  - [ ] Opens modal
  - [ ] Shows files from 07-Learning
  - [ ] Search works
- [ ] Scripts Browser
  - [ ] Opens modal
  - [ ] Shows files from 08-Scripts
  - [ ] Search works
- [ ] Documentation Browser
  - [ ] Opens modal
  - [ ] Shows files from 09-Documentation
  - [ ] Search works
- [ ] Session Files Browser
  - [ ] Opens modal
  - [ ] Shows files from 01-Morning-Sessions
  - [ ] Search works
- [ ] Templates Browser
  - [ ] Opens modal
  - [ ] Shows files from 06-Templates
  - [ ] Search works
- [ ] Trajanus Knowledge Base (MCP)
  - [ ] Button renamed
  - [ ] Opens modal
  - [ ] Shows correct files
  - [ ] Search works
```

---

## STEP 8: DOCUMENT CHANGES

**Create:** BROWSER_UNIFICATION_REPORT.md

```markdown
# BROWSER UNIFICATION - IMPLEMENTATION REPORT

**Date:** 2025-12-15
**Template:** Living Documents Browser (Website Tools)

## Functions Created

1. openCoreProtocolsBrowser() - Line XXXX
2. openLearningFolderBrowser() - Line XXXX
3. openScriptsBrowser() - Line XXXX
4. openDocumentationBrowser() - Line XXXX
5. openSessionFilesBrowser() - Line XXXX
6. openTemplatesBrowser() - Line XXXX
7. openTKBBrowser() - Line XXXX (renamed to Trajanus Knowledge Base MCP)

## Buttons Modified

[List each button with before/after onclick handlers]

## Testing Results

[Checklist results from Step 7]

## Issues Found

[Any problems encountered]

## Files Modified

- index.html (main app file)
- Lines changed: [list specific line ranges]
```

---

## EXECUTION ORDER

**DO NOT skip steps. Work sequentially:**

1. ✅ Extract Living Docs Browser template
2. ✅ Identify all browser buttons
3. ✅ Map buttons to folders (verify folders exist)
4. ⚠️ **STOP and ask about TKB folder path**
5. Create all browser functions
6. Surgical injections (one at a time)
7. Test EACH browser after injection
8. Document everything

---

## CRITICAL RULES

**For each browser function:**
- ✅ Copy EXACT structure from Living Docs Browser
- ✅ Only change: title, description, folder path
- ✅ Keep all styling identical
- ✅ Keep all functionality identical

**For button modifications:**
- ✅ Use str_replace for surgical edits
- ✅ Never rewrite large sections
- ✅ Test app launch after EACH change
- ✅ Create backup before starting

---

## BEFORE YOU START

**Answer these questions:**

1. What folder should "Trajanus Knowledge Base (MCP)" point to?
2. Are there any other browser buttons not listed?
3. Should Session Files browser point to 01-Morning-Sessions or somewhere else?

**Then execute Steps 1-3 and report findings before proceeding.**

**BEGIN ANALYSIS.**
