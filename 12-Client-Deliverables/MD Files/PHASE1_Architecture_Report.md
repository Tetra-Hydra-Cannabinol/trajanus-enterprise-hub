# PHASE 1: ARCHITECTURE EXTRACTION REPORT

**Date:** 2025-12-14
**File Analyzed:** index.html
**Total Lines:** 7,381

---

## FILE STRUCTURE OVERVIEW

| Section | Lines | Range | Size |
|---------|-------|-------|------|
| CSS Styles | 2,074 | 8-2082 | ~28% |
| HTML Structure | 1,053 | 2082-3135 | ~14% |
| JavaScript | 4,244 | 3135-7379 | ~58% |

---

## 1. NAVIGATION SECTION (Sidebar)

**Location:** Lines 2085-2220+

### Structure
```
<div class="sidebar">
    ├── <div class="sidebar-header">
    │   ├── <h1>TRAJANUS USA</h1>
    │   ├── <div class="tagline">
    │   ├── <div class="ei-logo"> (SVG)
    │   └── <div class="version">
    │
    ├── <div class="project-section"> (Projects in Development)
    │   ├── enterprise-hub
    │   ├── website
    │   ├── pm-toolkit
    │   ├── qcm-toolkit
    │   ├── ssho-toolkit
    │   ├── route-optimizer
    │   ├── traffic-studies
    │   ├── pe-services
    │   ├── memory
    │   └── developer-toolkit
    │
    ├── <div class="project-section"> (Deployed Projects)
    │   ├── pm-working
    │   ├── qcm-working
    │   ├── ssho-working
    │   ├── traffic-studies
    │   └── pe-services
    │
    └── <div class="quick-access-section"> (Living Documents)
        └── Living docs menu items
```

### Project Button Pattern
```html
<button class="project-btn" data-project="[ID]">
    <span>[Name]</span>
    <span class="sidebar-badge [dev|deployed]">[Status]</span>
</button>
```

---

## 2. WORKSPACE CONTAINERS

**Location:** Lines 2723-2900+

### Terminal Tab System
```
<div class="terminal">
    ├── <div class="terminal-header">
    │   ├── Permanent tabs (devtools, codes, external)
    │   ├── <div id="terminalTabs"> (dynamic tabs)
    │   └── Tab controls (+, Clear)
    │
    └── <div id="terminalBodies">
        ├── terminal-main (hidden)
        ├── terminal-devtools (active)
        ├── terminal-msoffice
        ├── terminal-codes
        ├── terminal-external
        ├── terminal-review-history
        ├── terminal-reference
        └── terminal-qcm-submittal
```

### Container IDs Found

| ID | Type | Lines |
|----|------|-------|
| terminal-main | Hidden terminal | 2749 |
| terminal-devtools | Developer tools | 2754 |
| terminal-msoffice | MS Office tools | 2786 |
| terminal-codes | Codes/Standards | 2805 |
| terminal-external | External links | 2824 |
| terminal-review-history | QCM history | 2849 |
| terminal-reference | Reference library | 2860 |
| terminal-qcm-submittal | QCM workspace | 2879 |

---

## 3. NAVIGATION JAVASCRIPT

**Location:** Lines 3220-3470+

### Core Functions

| Function | Line | Purpose |
|----------|------|---------|
| `switchTab(tabId)` | 3231 | Switches active terminal tab |
| `addTab(name)` | 3247 | Creates new terminal tab |
| `closeTab(event, tabId)` | 3274 | Closes a terminal tab |
| `createWorkspaceTab(name, html)` | 3303 | Creates workspace with content |
| `switchToProject(btn)` | 3448 | Handles project button click |
| `getActiveTerminal()` | 3227 | Returns current terminal |

### Project Navigation (Lines 3372-3470+)
- `currentProject` - tracks active project
- `switchToProject()` - updates header, shows/hides project tools
- Drag/drop reordering with localStorage persistence
- Project order saved: `projectOrder_dev`, `projectOrder_deployed`

### Tab System Variables
```javascript
let activeTab = 'devtools';      // Current tab
let tabCounter = 1;              // Tab numbering
let toolTabCounter = 0;          // Tool tab numbering
const MAX_TOOL_TABS = 4;         // Limit on dynamic tabs
```

---

## 4. PROJECT TOOL SECTIONS

**Location:** Lines 2400-2721

Each project has a corresponding tool section:
```html
<div class="tool-section project-tools" data-project="[ID]">
    <div class="section-intro">...</div>
    <div class="tool-section-header">...</div>
    <div class="button-grid">
        <!-- Tool buttons -->
    </div>
</div>
```

### Projects with Tool Sections

| data-project | Name |
|--------------|------|
| enterprise-hub | Enterprise Hub |
| website | Website Builder |
| pm-toolkit | PM Toolkit |
| qcm-toolkit | QCM Toolkit |
| ssho-toolkit | SSHO Toolkit |
| route-optimizer | Route Optimizer |
| traffic-studies | Traffic Studies |
| pe-services | P.E. Services |
| memory | Memory/Recall |
| developer-toolkit | Developer Toolkit |

---

## 5. CSS ORGANIZATION

**Location:** Lines 8-2082

### Key Style Sections

| Section | Purpose |
|---------|---------|
| Lines 42-90 | Sidebar styles |
| Lines 91-148 | Project buttons |
| Lines 149-167 | Sidebar badges |
| Lines 168-200 | Sidebar footer |
| Lines 200-400 | Main content area |
| Lines 400-600 | Terminal styles |
| Lines 600-800 | Tool sections |
| Lines 800-1200 | QCM workspace |
| Lines 1200-2082 | Various components |

---

## EXTRACTION CANDIDATES

### For Separate Files

1. **styles.css** (~2,074 lines)
   - All CSS from lines 8-2082
   - Clean separation

2. **sidebar.html** (~135 lines)
   - Lines 2085-2220
   - Sidebar structure only

3. **workspaces.html** (~400 lines)
   - Lines 2723-3130
   - Terminal/workspace containers

4. **navigation.js** (~300 lines)
   - Lines 3220-3520
   - Tab switching, project navigation

5. **app.js** (~3,900 lines)
   - Lines 3520-7379
   - All other JavaScript

---

## DEPENDENCIES

### JavaScript Dependencies
- `window.electronAPI` - Electron IPC bridge
- `window.kb` - Knowledge base API (new)
- `localStorage` - Project order persistence
- `sessionStorage` - Session state

### HTML Dependencies
- Project buttons require `data-project` attribute
- Terminals require `id="terminal-{tabId}"`
- Project tools require `data-project` matching sidebar

---

## PHASE 1 COMPLETE

### Summary
- Navigation: Lines 2085-2220 (sidebar with project buttons)
- Containers: Lines 2723-2900 (terminal tab system)
- JavaScript: Lines 3220-3470 (navigation functions)

### Ready for Phase 2
- [ ] Create extraction plan
- [ ] Decide on file splitting strategy
- [ ] Implement modular structure

---

**Status:** PHASE 1 COMPLETE - AWAITING APPROVAL

*Report generated: 2025-12-14*
