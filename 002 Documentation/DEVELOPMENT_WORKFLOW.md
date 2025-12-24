# TRAJANUS ENTERPRISE HUB - DEVELOPMENT WORKFLOW
**The Process That Finally Worked**
**Date:** November 30, 2025

---

## THE BREAKTHROUGH

After struggling with a complex, broken system, we discovered the winning approach: **START CLEAN, BUILD INCREMENTALLY, TEST EACH CHANGE.**

---

## THE GOLDEN RULES

### 1. CLEAN SLATE PRINCIPLE
**Never try to fix a Frankenstein monster. Burn it down and rebuild.**

When we had:
- 3 conflicting chat systems
- External CSS/JS files breaking everything
- Complex modals that didn't work
- Buttons that wouldn't display

**Solution:** 
- Archive everything as reference
- Create 4 clean files from scratch
- Extract ONLY the working concepts
- Build foundation first

### 2. ARCHIVE BEFORE REBUILDING
**Always preserve the old version before starting fresh.**

```powershell
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center"
mkdir Reference-Original-$(Get-Date -Format 'yyyy-MM-dd')
copy *.* "Reference-Original-*\"
```

This gives you:
- Complete reference of design vision
- Safe fallback if needed
- Ability to extract working pieces

### 3. THE 4-FILE FOUNDATION
**Start with minimal, proven code.**

**package.json** - Clean Electron config, no bloat
**main.js** - ONLY proven IPC handlers (app launchers work!)
**preload.js** - Security bridge, expose ONLY what's needed
**index.html** - Single file, all CSS/JS embedded, NO external dependencies

### 4. BUILD IN STAGES
**Test after each addition. NEVER add 10 features at once.**

**Stage 1:** Window opens, shows something ✓
**Stage 2:** Sidebar navigation works ✓
**Stage 3:** App launchers work ✓
**Stage 4:** Terminal + tabs ✓
**Stage 5:** File picker ✓
**Stage 6:** Project-specific tools ✓
**Stage 7:** Developer mode ✓

**CRITICAL:** If Stage N breaks, you KNOW what broke it. Fix it before Stage N+1.

### 5. SURGICAL EDITS, NOT REWRITES
**Make the smallest possible change to achieve the goal.**

**BAD:**
- "Rewrite the entire file management system"
- "Add 50 new features at once"
- "Let's completely redesign the UI"

**GOOD:**
- "Add developer mode toggle to sidebar footer"
- "Add preview pane with 3 buttons"
- "Wrap session controls in .dev-mode-only class"

### 6. SINGLE RESPONSIBILITY
**Each file does ONE thing well.**

**main.js** - Electron lifecycle + IPC handlers
**preload.js** - Security bridge (context isolation)
**index.html** - UI + behavior (self-contained)

NO:
- Complex build systems
- Webpack/bundlers (overkill for this)
- Split CSS/JS into 20 files
- Framework bloat

### 7. LOCALHOST TESTING
**Everything lives in Google Drive. Electron runs from G:\**

```
G:\My Drive\00 - Trajanus USA\00-Command-Center\
├── package.json
├── main.js
├── preload.js
├── index.html
└── node_modules\ (from npm install)
```

**NO C:\ copies. NO local duplicates. Single source of truth.**

---

## THE PROVEN PROCESS

### Step 1: Archive Current State
```powershell
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center"
mkdir Reference-Original-$(Get-Date -Format 'yyyy-MM-dd-HHmm')
copy index.html "Reference-Original-*\index-REFERENCE.html"
copy main.js "Reference-Original-*\main-REFERENCE.js"
copy preload.js "Reference-Original-*\preload-REFERENCE.js"
copy package.json "Reference-Original-*\package-REFERENCE.json"
```

### Step 2: Extract What Works
**Review reference files and identify:**
- ✅ Color scheme (CSS variables)
- ✅ Layout structure (sidebar + main + panels)
- ✅ Working features (app launchers, navigation)
- ❌ Broken features (conflicting systems)
- ❌ Unnecessary complexity

### Step 3: Build Clean Foundation
**Create 4 minimal files:**

1. **package.json** - Electron config
2. **main.js** - Proven IPC (app launchers)
3. **preload.js** - Security bridge
4. **index.html** - Minimal UI with working features

### Step 4: Test Base Functionality
```powershell
npm start
```

**Verify:**
- Window opens ✓
- UI displays correctly ✓
- App launchers work ✓
- No console errors ✓

**If anything fails:** Stop. Fix it. Don't proceed.

### Step 5: Add Features ONE AT A TIME
**Example: Adding Terminal Tabs**

1. Add CSS for tabs
2. Add HTML structure
3. Add JavaScript functions
4. Test: Does it work? ✓
5. Commit the change (copy to Reference folder)
6. Move to next feature

**Example: Adding File Picker**

1. Add IPC handler in main.js
2. Expose in preload.js
3. Add UI button in index.html
4. Add JavaScript handler
5. Test: Can I pick files? ✓
6. Add file display
7. Test: Do files show? ✓
8. Add preview pane
9. Test: Does preview work? ✓

### Step 6: Deploy Updates
```powershell
# Replace files in Command Center
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center"
# Copy updated files from /mnt/user-data/outputs/

# Restart app
npm start
```

---

## WHAT WE LEARNED

### ❌ WHAT DIDN'T WORK
- Trying to fix broken code with more code
- Adding features without testing
- External CSS/JS files (caused conflicts)
- Multiple chat systems competing
- Complex file structures
- Assuming "it should work"

### ✅ WHAT WORKED
- Starting from scratch with clean code
- Testing after EACH change
- Single HTML file (all CSS/JS embedded)
- Incremental feature additions
- Preserving reference before rebuilding
- Surgical edits, not rewrites
- Developer mode for different user types

---

## DEVELOPER MODE SYSTEM

### Why We Needed It
Bill = Developer (needs all tools)
Tom = User (needs project tools only)

### How It Works
**Developer Mode Toggle** in sidebar footer
- Saves preference to localStorage
- Shows/hides session controls
- Session controls wrapped in `.dev-mode-only` class

**Developer Tools (Hidden from Users):**
- Mission Brief
- Sync Memory
- End Session
- Update Living Docs (if developer-specific)

**User Tools (Always Visible):**
- Project-specific tools
- App launchers
- File management
- Working files

---

## FILE MANAGEMENT SYSTEM

### The File Picker That Works
**Feature:** Multi-select, preview, View/Open Folder buttons

**Flow:**
1. User clicks "+ Add Files"
2. Electron file picker opens
3. User selects files (multi-select enabled)
4. Files added to "Working Files" list
5. Click file → Preview shows with icon, name, size, date
6. Preview buttons: View (opens file), Open Folder, Complete (moves to Completed)

**Storage:** Per-project in localStorage
- `projectFiles_enterprise-hub`
- `projectFiles_pm-toolkit`
- etc.

**Persistence:** Files persist when switching projects

---

## PROJECT-SPECIFIC TOOLS

### The Concept
Different projects need different tools. Don't show PM tools in QCM project.

### Implementation
**HTML Structure:**
```html
<div class="tool-section project-tools" data-project="pm-toolkit">
    <!-- PM-specific tools here -->
</div>

<div class="tool-section project-tools" data-project="qcm-toolkit">
    <!-- QCM-specific tools here -->
</div>
```

**JavaScript:**
```javascript
// When project clicked
document.querySelectorAll('.project-tools').forEach(section => {
    section.classList.remove('active');
});
const activeTools = document.querySelector(`.project-tools[data-project="${project}"]`);
if (activeTools) {
    activeTools.classList.add('active');
}
```

**CSS:**
```css
.project-tools {
    display: none;
}

.project-tools.active {
    display: block;
}
```

---

## CURRENT PROJECT LIST

### Projects in Development (9)
1. Enterprise Hub - Session management, automation
2. Website Builder - trajanus-usa.com development
3. PM Toolkit - Project management tools
4. QCM Toolkit - Quality control tools
5. SSHO Toolkit - Safety tools
6. Route Optimizer - TSP algorithm, delivery routes
7. Traffic Studies - Traffic analysis, ITE trip gen
8. P.E. Services - Professional engineering services
9. Memory/Recall - Living documents, protocols

### Deployed Projects (3)
1. PM Working - Active PM contracts (BILLABLE)
2. QCM Working - Active QC contracts (BILLABLE)
3. SSHO Working - Active safety contracts (BILLABLE)

---

## TROUBLESHOOTING

### Problem: Buttons Don't Display
**Cause:** External CSS/JS files conflicting or missing
**Solution:** Embed all CSS/JS in single HTML file

### Problem: App Launcher Doesn't Work
**Cause:** IPC handler missing or preload not exposing
**Solution:** Check main.js has handler, preload.js exposes it

### Problem: Files Don't Persist
**Cause:** localStorage not saving or wrong project key
**Solution:** Check `saveProjectFiles()` is called, verify key

### Problem: Changes Don't Show Up
**Cause:** Browser cache or old file loaded
**Solution:** Hard refresh (Ctrl+Shift+R) or restart app

### Problem: Developer Mode Not Saving
**Cause:** localStorage not accessible or blocked
**Solution:** Check browser/Electron storage permissions

---

## MAINTENANCE

### Weekly
- Review active projects
- Test all app launchers
- Verify file picker works
- Check developer mode toggle

### Monthly
- Archive old reference folders
- Update project list
- Review and clean localStorage
- Test all project-specific tools

### Before Major Changes
- **ALWAYS archive current working version**
- Test new features in isolation
- Document what you're changing
- Have rollback plan

---

## SUCCESS METRICS

### ✅ App is Working When:
- Window opens without errors
- All buttons visible and clickable
- App launchers start applications
- File picker adds files to list
- Preview shows file details
- Developer mode toggles correctly
- Project switching shows correct tools
- Terminal tabs can be added/closed
- Clock shows correct time
- Session timer counts up

### ❌ App is Broken When:
- Blank window
- Missing buttons
- Console errors
- App launchers don't fire
- Files don't add
- Mode toggle doesn't work

---

## THE COLLABORATION BREAKTHROUGH

### What Changed
**BEFORE:** Random edits, no testing, broken builds
**AFTER:** Systematic process, test each change, working app

### The Process
1. Bill identifies what's needed
2. Claude makes surgical edit to specific file
3. Bill downloads updated file
4. Bill replaces in Command Center folder
5. Bill tests immediately
6. If works: Next feature
7. If breaks: Roll back, diagnose, fix

### Why It Works
- **Single source of truth** (Google Drive)
- **Immediate feedback** (test after each edit)
- **Small changes** (easy to debug)
- **Clear ownership** (Bill = IT, Tom = User)
- **Reference available** (archived versions)

---

## NEXT STEPS

### Features to Add (In Order)
1. ✅ Developer mode (DONE)
2. ✅ File preview with buttons (DONE)
3. ✅ Project-specific tools (DONE)
4. Mission Brief modal
5. EOS (End of Session) routine
6. Session Library
7. Template picker
8. Google Drive browser integration

### Do NOT Add Yet
- Chat integration (save for last)
- Complex modals (add one at a time)
- External dependencies
- Build systems

---

## FINAL THOUGHTS

**This workflow WORKS because:**
- It's simple
- It's testable
- It's maintainable
- It's documented
- It's repeatable

**Keep doing:**
- Archive before major changes
- Test after each edit
- Make surgical changes
- Document what works

**Stop doing:**
- Trying to fix broken code
- Adding 10 features at once
- Skipping tests
- Assuming it works

---

**END OF WORKFLOW DOCUMENTATION**
**Last Updated:** November 30, 2025
**Status:** WORKING PERFECTLY
