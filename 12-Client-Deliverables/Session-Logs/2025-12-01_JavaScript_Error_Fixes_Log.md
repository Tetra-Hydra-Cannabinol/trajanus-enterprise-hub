# JAVASCRIPT ERROR FIXES - PROJECT PICKER & CLOCK
**Date:** December 1, 2025
**Issue:** Project picker not working, buttons returning errors, file picker non-functional
**Root Cause:** Variable hoisting and temporal dead zone errors, plus removed DOM elements

## ERRORS IDENTIFIED

From DevTools console:
1. `Uncaught ReferenceError: Cannot access 'selectedFilesForUpload' before initialization`
2. `Uncaught TypeError: Cannot set properties of null (setting 'textContent')` at updateClock
3. Multiple similar errors cascading through the code

## ROOT CAUSES

### 1. Variable Declaration Order (Temporal Dead Zone)
**Problem:**
- `addFiles()` function defined at line ~2826
- Uses `selectedFilesForUpload` variable
- But `let selectedFilesForUpload = []` declared at line ~2833
- With `let`/`const`, you cannot reference variables before declaration

**Fix:**
- Moved `let selectedFilesForUpload = []` and `let previewingFile = null` 
- From AFTER addFiles() function
- To BEFORE addFiles() function
- Variables now declared before first use

### 2. Clock Initialization Timing
**Problem:**
- `setInterval(updateClock, 1000)` and `updateClock()` called in global scope
- Executed immediately when script loads
- But DOM elements don't exist yet
- Trying to set textContent on null elements → TypeError

**Fix:**
- Removed `setInterval(updateClock, 1000)` and `updateClock()` from global scope
- Added to `DOMContentLoaded` event listener
- Clock now initializes AFTER DOM is ready
- Elements exist when code tries to access them

### 3. Session Timer References
**Problem:**
- `updateClock()` function tried to set `sessionTimer` element textContent
- But we removed `<div class="clock-session">` with session timer from HTML
- Trying to access removed element → TypeError

**Fix:**
- Removed session timer code from `updateClock()` function
- Removed unused `const sessionStart = new Date()` variable
- Function now only updates date and time (which still exist)

## CODE CHANGES

### Change 1: Move Variable Declarations
**Before:**
```javascript
// Add files via file picker
async function addFiles() {
    document.getElementById('filePickerModal').style.display = 'flex';
    selectedFilesForUpload = []; // ERROR: not declared yet!
    renderSelectedFiles();
}

let selectedFilesForUpload = []; // Declared too late
let previewingFile = null;
```

**After:**
```javascript
let selectedFilesForUpload = []; // Declared first
let previewingFile = null;

// Add files via file picker
async function addFiles() {
    document.getElementById('filePickerModal').style.display = 'flex';
    selectedFilesForUpload = []; // Now works!
    renderSelectedFiles();
}
```

### Change 2: Clock Initialization
**Before:**
```javascript
function updateClock() {
    // ...update date and time...
    // Session duration (REMOVED ELEMENT)
    document.getElementById('sessionTimer').textContent = `${sessionHours}h ${sessionMinutes}m`;
}

setInterval(updateClock, 1000); // Called immediately, DOM not ready
updateClock();
```

**After:**
```javascript
function updateClock() {
    // ...update date and time only...
    // Session timer code removed
}

// Inside DOMContentLoaded:
window.addEventListener('DOMContentLoaded', () => {
    // Initialize clock after DOM ready
    setInterval(updateClock, 1000);
    updateClock();
    
    // ... rest of initialization
});
```

### Change 3: Remove Session Timer Code
**Removed:**
```javascript
const sessionStart = new Date(); // No longer needed

// Inside updateClock():
// Session duration
const elapsed = Math.floor((now - sessionStart) / 1000);
const sessionHours = Math.floor(elapsed / 3600);
const sessionMinutes = Math.floor((elapsed % 3600) / 60);
document.getElementById('sessionTimer').textContent = `${sessionHours}h ${sessionMinutes}m`;
```

## TESTING CHECKLIST

After fixes applied:
- [ ] No console errors on page load
- [ ] Project buttons clickable in sidebar
- [ ] Projects switch correctly when clicked
- [ ] Clock displays and updates every second
- [ ] Add Files button opens file picker modal
- [ ] Terminal tabs switch correctly
- [ ] All buttons log to terminal as expected

## TECHNICAL NOTES

**JavaScript Variable Hoisting:**
- `var` declarations are hoisted (moved to top of scope)
- `let` and `const` are NOT hoisted
- Using a `let`/`const` variable before declaration = Temporal Dead Zone error
- Always declare `let`/`const` variables BEFORE functions that use them

**DOM Timing:**
- Scripts in `<head>` execute before DOM loads
- Must wait for `DOMContentLoaded` event before accessing DOM elements
- Or put scripts at end of `<body>` (after DOM elements)
- Our scripts are in `<head>`, so we must use `DOMContentLoaded`

**Null Safety:**
- `document.getElementById()` returns `null` if element doesn't exist
- Trying to set properties on `null` → TypeError
- Always ensure elements exist before accessing them
- Or check for null: `if (element) { element.textContent = '...' }`

## FILES
**Active:** index_NO_PASSWORD.html
**Last Backup:** index_BACKUP_2025-12-01_BeforeClockAndDescriptions.html

## NEXT SESSION NOTES
If session timer needs to be added back:
1. Add back `<div class="clock-session">` with `<span id="sessionTimer"></span>` to HTML
2. Add back `const sessionStart = new Date()` before updateClock function
3. Add back session timer calculation code to updateClock function
4. Update CSS to show session timer section
