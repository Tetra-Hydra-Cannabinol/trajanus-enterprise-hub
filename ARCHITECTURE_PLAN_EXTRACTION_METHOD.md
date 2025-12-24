# ARCHITECTURE REDESIGN PLAN - EXTRACTION METHOD

**Mission:** Redesign from flat workspace list to multi-platform hierarchy.

**Method:** Extract → Build → Test → Inject

---

## CURRENT STATE ANALYSIS

**File:** index.html (7,211 lines)

**Current structure:**
```
Main Page
├── QCM Workspace button
├── PM Toolkit button
└── Developer Project button
```

**Target structure:**
```
Platform Selection
├── Construction Management
│   ├── QCM
│   ├── PM Toolkit
│   └── Dashboard
├── PE Services (placeholder)
├── Route Optimization (placeholder)
└── Traffic Studies (placeholder)
```

---

## PHASE 1: EXTRACT CURRENT SECTIONS

**Task:** Identify what sections need extraction

### 1.1 LOCATE NAVIGATION SECTION

```bash
# Find where workspace buttons are defined
grep -n "QCM Workspace\|PM Toolkit\|Developer" index.html | head -20
```

**Extract to:** `nav-section-original.html`

### 1.2 LOCATE WORKSPACE CONTAINERS

```bash
# Find workspace div IDs
grep -n "id=\"qcm-workspace\"\|id=\"pm-toolkit\"\|id=\"developer\"" index.html
```

**Extract to:** `workspaces-original.html`

### 1.3 LOCATE NAVIGATION JAVASCRIPT

```bash
# Find show/hide functions
grep -n "function.*Workspace\|function.*show\|function.*hide" index.html | head -30
```

**Extract to:** `nav-functions-original.js`

---

## PHASE 2: BUILD NEW ARCHITECTURE (ISOLATION)

**DO NOT touch index.html**

### 2.1 CREATE PLATFORM SELECTION PAGE

**File:** `platform-selection-test.html`

**Contents:**
- Standalone HTML file
- 4 platform cards
- Click handlers
- CSS styling
- Test in browser

**Success criteria:**
- Cards display in 2x2 grid
- Hover effects work
- Click handlers fire
- Looks professional

### 2.2 CREATE PLATFORM VIEWS

**File:** `construction-platform-test.html`

**Contents:**
- Platform header with back button
- 3 workspace cards (QCM, PM Toolkit, Dashboard)
- Click handlers
- Test navigation flow

**Success criteria:**
- Cards display correctly
- Click opens "workspace"
- Back button returns to platform selection
- All interactions work

### 2.3 CREATE NAVIGATION SYSTEM

**File:** `platform-navigation.js`

**Contents:**
```javascript
// View management
function showPlatformSelection() {}
function showConstructionPlatform() {}
function showWorkspace(id) {}

// Event handlers
function setupPlatformNavigation() {}
```

**Test in isolation** with test HTML files.

---

## PHASE 3: INTEGRATION STRATEGY

**Once Phases 1 & 2 complete and tested:**

### 3.1 BACKUP CURRENT FILE

```bash
cp index.html "index_backup_$(date +%Y%m%d_%H%M%S).html"
```

### 3.2 CREATE INTEGRATION POINTS

**Identify exact line numbers for:**
- Where to insert platform selection HTML
- Where to insert platform view HTML
- Where to insert navigation JavaScript
- What to hide/comment out (old navigation)

### 3.3 SURGICAL INJECTIONS

**Use str_replace for each section:**
1. Insert platform selection HTML at line X
2. Insert platform views HTML at line Y
3. Insert navigation JS at line Z
4. Comment out old navigation at line A-B
5. Update CSS at line C

**Each injection:**
- Single str_replace operation
- Test after each one
- Verify app still launches
- Rollback if breaks

---

## PHASE 4: VERIFICATION

### 4.1 FUNCTIONALITY TESTS

- [ ] App launches without errors
- [ ] Platform selection displays
- [ ] Click Construction → Shows platform view
- [ ] Click QCM → Opens QCM workspace (existing)
- [ ] Back buttons work
- [ ] All existing features still work

### 4.2 VISUAL TESTS

- [ ] Layout matches design
- [ ] Colors correct
- [ ] Icons display
- [ ] Responsive design works
- [ ] No visual glitches

---

## DELIVERABLES

**From Phase 1:**
- nav-section-original.html
- workspaces-original.html
- nav-functions-original.js

**From Phase 2:**
- platform-selection-test.html (working)
- construction-platform-test.html (working)
- platform-navigation.js (tested)

**From Phase 3:**
- index.html (modified with surgical edits)
- index_backup_TIMESTAMP.html
- Integration checklist (completed)

**From Phase 4:**
- ARCHITECTURE_TEST_RESULTS.md
- Screenshots of working interface

---

## EXECUTION ORDER

**DO NOT proceed to next phase until previous complete:**

1. Run PHASE 1 (extraction)
2. Verify extracted sections are correct
3. Run PHASE 2 (build in isolation)
4. Test standalone components thoroughly
5. Get approval for Phase 3
6. Run PHASE 3 (surgical integration)
7. Test after EACH injection
8. Run PHASE 4 (full verification)

---

## SAFETY PROTOCOLS

**Before ANY edit to index.html:**
- [ ] Timestamped backup created
- [ ] Exact line numbers identified
- [ ] str_replace command prepared
- [ ] Test plan ready
- [ ] Rollback plan ready

**After EACH edit:**
- [ ] File saves to disk (verify with ls -la)
- [ ] App launches (npm start)
- [ ] Console clean (no errors)
- [ ] Feature tested
- [ ] Document change

---

**READY TO BEGIN PHASE 1 EXTRACTION**

Wait for test results from KB integration before proceeding.
