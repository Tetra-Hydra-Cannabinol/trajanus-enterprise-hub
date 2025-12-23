# COMPLETE BROWSER FIX + SIDEBAR CLEANUP

**Mission:** Fix ALL browser buttons across entire app + clean up sidebar.

---

## PART 1: SIDEBAR CLEANUP

### REMOVE THESE ELEMENTS:

1. **"Working Projects" section** - Delete entire section from sidebar
2. **"IN DEVELOPMENT" badges/text** - Remove all instances
3. **Keep:** BETA ACCESS icons (already present)

### ACTUAL PLATFORMS (Keep these 8):

1. Enterprise Hub
2. Website Builder  
3. PM Toolkit
4. QCM Toolkit
5. Route Optimizer
6. Traffic Studies
7. P.E. Services
8. Developer Toolkit

---

## PART 2: BROWSER BUTTON AUDIT

### STEP 1: SURVEY ALL PLATFORMS

**For EACH of the 8 platforms, document:**

```bash
# Search for all browser/folder buttons in index.html
grep -n "onclick.*[Bb]rowser\|onclick.*openLocal\|onclick.*Folder" index.html > browser_buttons_audit.txt

# For each platform workspace, list:
# - Button text
# - Current onclick handler
# - Current folder path (if any)
# - Line number
```

**Create:** `BROWSER_AUDIT_REPORT.md`

**Format:**
```markdown
## Platform: Developer Toolkit

### Browser Buttons Found:
1. Core Protocols
   - Line: 2750
   - Current: onclick="openLocalFolder('protocols')"
   - Status: BROKEN (wrong path)
   
2. Scripts
   - Line: 2785
   - Current: onclick="openLocalFolder('scripts')"
   - Status: BROKEN (wrong path)

[etc for all buttons]

### Duplicates on Same Page:
- [List any duplicate buttons to remove]
```

---

## PART 3: FOLDER PATH MAPPING

**CORRECT FOLDER PATHS:**

```javascript
const correctFolderPaths = {
    // Core folders
    'living-docs': 'G:\\My Drive\\00 - Trajanus USA\\03-Living-Documents',
    'core-protocols': 'G:\\My Drive\\00 - Trajanus USA\\01-Core-Protocols',
    'scripts': 'G:\\My Drive\\00 - Trajanus USA\\04-Scripts',
    'sessions': 'G:\\My Drive\\00 - Trajanus USA\\07-Session-Journal',
    
    // Project-specific folders (to be determined per platform)
    'qcm-templates': '[TBD per platform]',
    'pm-tools': '[TBD per platform]',
    'traffic-data': '[TBD per platform]',
    // etc.
};
```

**Update the existing `folderPaths` object in index.html with correct paths.**

---

## PART 4: WORKING BROWSER TEMPLATE

**Living Documents Browser (line 6276) is the WORKING template.**

**Key features:**
- Modal overlay with brown/orange theme
- Real Google Drive IPC call: `window.electronAPI.listDirectory()`
- Search/sort/refresh functionality
- File list with icons
- Preview panel
- Upload/View/Download buttons

**For generic file browser (line 3814):**
- Already uses IPC
- Just needs correct folder paths in mapping
- Keep this as universal browser function

---

## PART 5: EXECUTION STEPS

### A. SIDEBAR CLEANUP

```javascript
// Find and REMOVE entire "Working Projects" section
// Search for: "PROJECTS IN DEVELOPMENT" or "Working Projects"
// Delete entire div/section

// Find and REMOVE all "IN DEVELOPMENT" badges
// Search for: "IN DEVELOPMENT" or "DEVELOPMENT"
// Delete span/badge elements only (keep BETA ACCESS icons)
```

### B. UPDATE FOLDER PATHS

```javascript
// Find folderPaths object (around line 3790-3800)
// Replace with correct paths:

const folderPaths = {
    'living-docs': 'G:\\My Drive\\00 - Trajanus USA\\03-Living-Documents',
    'core-protocols': 'G:\\My Drive\\00 - Trajanus USA\\01-Core-Protocols',
    'scripts': 'G:\\My Drive\\00 - Trajanus USA\\04-Scripts',
    'sessions': 'G:\\My Drive\\00 - Trajanus USA\\07-Session-Journal',
    'command-center': 'G:\\My Drive\\00 - Trajanus USA\\00-Command-Center'
};
```

### C. FIX BROWSER BUTTONS

**For each broken button:**

1. **Find button** in HTML
2. **Check for duplicates** on same page
3. **Remove duplicates**, keep one
4. **Update onclick** to use correct function:
   ```html
   OLD: onclick="openLocalFolder('wrong-key')"
   NEW: onclick="openFileBrowser('correct-key')"
   ```
5. **Test in app** after each change

### D. REMOVE PAGE DUPLICATES

**Rule:** If same button appears TWICE on same page → remove one

**Example:**
```html
<!-- Developer Tools page has two "Scripts" buttons -->
<button onclick="openFileBrowser('scripts')">Scripts</button>  <!-- Keep -->
<button onclick="openFileBrowser('scripts')">Scripts</button>  <!-- DELETE -->
```

**Important:** Keep duplicate buttons on DIFFERENT platforms.

---

## PART 6: TESTING CHECKLIST

**After all changes, test EACH platform:**

### Enterprise Hub
- [ ] Opens without errors
- [ ] No broken browser buttons

### Website Builder
- [ ] Living Documents Browser works (already working)
- [ ] Other browsers (if any) work

### PM Toolkit
- [ ] All browser buttons work
- [ ] No duplicate buttons on page
- [ ] Correct folders open

### QCM Toolkit
- [ ] All browser buttons work
- [ ] 3-panel system intact
- [ ] File browser in Panel 1 works

### Route Optimizer
- [ ] All browser buttons work
- [ ] No duplicate buttons on page

### Traffic Studies
- [ ] All browser buttons work
- [ ] No duplicate buttons on page

### P.E. Services
- [ ] All browser buttons work
- [ ] No duplicate buttons on page

### Developer Toolkit
- [ ] Core Protocols browser works
- [ ] Scripts browser works
- [ ] Session Files browser works
- [ ] No duplicate buttons on page

---

## PART 7: SPECIAL CASE - TKB BUTTON

**Trajanus Knowledge Base (MCP) button:**

**NOT a file browser** - uses KB integration from yesterday.

**Implementation:**
```javascript
function openTKBBrowser() {
    // Show modal with KB search interface
    // Use window.kb.search(), window.kb.listSources(), etc.
    // Different implementation - NOT using openFileBrowser()
}
```

**Button text:** "Trajanus Knowledge Base (MCP)"

**Defer this** - Focus on file browsers first.

---

## PART 8: DELIVERABLES

**Create these files:**

1. **BROWSER_AUDIT_REPORT.md**
   - All browser buttons found
   - Current status of each
   - Duplicates identified
   - Changes needed

2. **SIDEBAR_CLEANUP_REPORT.md**
   - What was removed
   - Before/after line counts
   - Screenshots if possible

3. **BROWSER_FIX_IMPLEMENTATION.md**
   - What was changed
   - Line numbers modified
   - Testing results
   - Issues encountered

4. **Updated index.html**
   - Backup created first
   - All changes applied
   - Ready for testing

---

## EXECUTION ORDER

**DO NOT skip steps:**

1. ✅ Backup current index.html
2. ✅ Audit all browser buttons (create report)
3. ✅ Clean up sidebar (remove working projects, in development)
4. ✅ Update folderPaths mapping
5. ✅ Fix browser buttons one platform at a time
6. ✅ Remove page duplicates as you go
7. ✅ Test EACH platform after its changes
8. ✅ Document everything
9. ✅ Report back with all deliverables

---

## CRITICAL RULES

**Surgical edits only:**
- Use str_replace for each change
- Never rewrite large sections
- Test after each platform's changes
- Create timestamped backup before starting

**For folder paths:**
- Use EXACT paths provided
- Use double backslashes: `\\`
- Test path exists before updating

**For duplicates:**
- Only remove duplicates on SAME page
- Keep duplicates on different platforms
- Ask if unsure

---

## BEFORE YOU START

**Answer:**
1. Do you see the "Working Projects" section in sidebar?
2. How many browser buttons total did you find?
3. List all platforms with browser buttons
4. Confirm you understand duplicate removal rule

**Then execute all steps systematically and report progress.**

**BEGIN WORK.**
