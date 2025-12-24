# DRAG & DROP PROJECT REORDERING + DYNAMIC DEFAULT PROJECT
**Date:** December 1, 2025
**Version:** v3.3.0
**Previous Backup:** index_BACKUP_2025-12-01_BeforeDragDrop.html

## FEATURE OVERVIEW

**Two new capabilities:**
1. **Drag & Drop Reordering** - Grab any project button, drag up/down to reorder
2. **Dynamic Default Project** - Top project in list is always the default on startup

## USER EXPERIENCE

### How to Reorder Projects

**Development Projects:**
1. Click and hold any project button in "Projects in Development"
2. Drag up or down to desired position
3. Visual feedback shows where button will be placed
4. Release to drop in new position
5. Order automatically saves to localStorage

**Deployed Projects:**
1. Same process for "Deployed Projects" section
2. Can only reorder within same section (Dev or Deployed)
3. Order persists between app restarts

### Visual Feedback

**While Dragging:**
- Grabbed button becomes semi-transparent (50% opacity)
- Cursor changes to "grabbing" hand
- Target position shows orange line at top

**Cursor States:**
- Default: Grab hand cursor (indicates draggable)
- While dragging: Grabbing hand cursor
- After release: Returns to grab cursor

### Default Project Behavior

**On Startup:**
- App loads with TOP project in Development section active
- If you reorder projects, new top project becomes default
- No need to manually set default - it's always the first one

**Example:**
- Original order: Enterprise Hub, Website Builder, PM Toolkit...
- Default: Enterprise Hub ✓
- After reordering: PM Toolkit, Website Builder, Enterprise Hub...
- New default: PM Toolkit ✓

## TECHNICAL IMPLEMENTATION

### HTML Changes

**All project buttons:**
```html
<button class="project-btn" data-project="project-id" draggable="true">
```

Added `draggable="true"` to all 15 project buttons:
- 10 in "Projects in Development"
- 5 in "Deployed Projects"

### CSS Additions

**Drag states:**
```css
.project-btn.dragging {
    opacity: 0.5;
    cursor: grabbing;
}

.project-btn.drag-over {
    border-top: 3px solid var(--orange-light);
}

.project-btn {
    cursor: grab;
}

.project-btn:active {
    cursor: grabbing;
}
```

### JavaScript Implementation

**Three main functions:**

**1. restoreProjectOrder()**
- Runs on app startup
- Reads saved order from localStorage
- Reorders DOM elements to match saved order
- Separate orders for Dev and Deployed sections

**2. saveProjectOrder(container, key)**
- Saves current button order to localStorage
- Gets all buttons in container
- Maps to array of data-project values
- Stores as JSON

**3. setDefaultProject()**
- Gets first project button in Development section
- Sets as currentProject
- Marks as active (visual highlight)
- Updates header text
- Shows correct tool section
- Loads project files

**Drag Event Handlers:**

**dragstart** - When drag begins:
- Store reference to dragged element
- Add 'dragging' class (opacity effect)
- Set effectAllowed to 'move'

**dragend** - When drag finishes:
- Remove 'dragging' class
- Remove all 'drag-over' classes
- Save new order to localStorage
- Update default project

**dragover** - While dragging over target:
- Prevent default (allows drop)
- Add 'drag-over' class (orange line)
- Only if different from dragged element

**dragleave** - When leaving target:
- Remove 'drag-over' class

**drop** - When dropped on target:
- Check both in same section (Dev or Deployed)
- Calculate draggedIndex and targetIndex
- Insert before or after based on direction
- Order saves automatically in dragend

### LocalStorage Keys

**Two storage keys:**
```javascript
localStorage.setItem('projectOrder_dev', JSON.stringify([...]))
localStorage.setItem('projectOrder_deployed', JSON.stringify([...]))
```

**Stored format:**
```json
{
  "projectOrder_dev": [
    "enterprise-hub",
    "website",
    "pm-toolkit",
    "qcm-toolkit",
    ...
  ],
  "projectOrder_deployed": [
    "pm-working",
    "qcm-working",
    ...
  ]
}
```

### currentProject Initialization

**Changed from:**
```javascript
let currentProject = 'website';
```

**To:**
```javascript
let currentProject = null; // Will be set to first project in list
```

Then dynamically set by `setDefaultProject()` function.

## BEHAVIOR NOTES

### Section Isolation
- Development projects can only be reordered with other Dev projects
- Deployed projects can only be reordered with other Deployed projects
- Cannot drag Dev project into Deployed section (and vice versa)

### Persistence
- Order survives app restart
- Clears with localStorage.clear()
- Each section maintains independent order

### Default Project Logic
**Always follows this rule:**
1. Get all buttons in "Projects in Development"
2. Take the first one
3. That's the default

**Result:**
- Reorder list → default changes automatically
- No separate "set as default" needed
- Top = Default, always

## TESTING CHECKLIST

**Drag and Drop:**
- [ ] Can grab any project button
- [ ] Visual feedback while dragging (opacity + cursor)
- [ ] Orange line shows drop target
- [ ] Drop works correctly (inserts at target)
- [ ] Order persists after app restart
- [ ] Cannot drag between Dev/Deployed sections

**Default Project:**
- [ ] App opens with top Development project active
- [ ] Reordering changes default correctly
- [ ] Header updates to show active project
- [ ] Correct tools display for active project
- [ ] Files load for active project

**Edge Cases:**
- [ ] Works with 1 project in list
- [ ] Works with all 10 projects
- [ ] Dragging to same position (no change)
- [ ] Rapid dragging (no glitches)

## USER BENEFITS

**Flexibility:**
- Organize projects by priority
- Group related projects together
- Change workflow as needs evolve

**No Configuration:**
- No "set default" button needed
- Top = Default is intuitive
- Works automatically

**Visual Control:**
- See order immediately
- Instant feedback
- Physical metaphor (dragging)

**Persistence:**
- Set once, stays that way
- No need to reorder every session
- Order follows you

## FUTURE ENHANCEMENTS

Possible additions:
- Drag projects between sections (Dev ↔ Deployed)
- Keyboard shortcuts for reordering (Alt+Up/Down)
- Reset to default order button
- Import/export project order
- Project groups/folders
- Collapse/expand sections

## FILES MODIFIED

**index_NO_PASSWORD.html:**
- Added draggable="true" to all project buttons
- Added drag state CSS
- Added drag/drop event handlers
- Added localStorage save/restore functions
- Changed currentProject initialization
- Added setDefaultProject() function

**Backup:** index_BACKUP_2025-12-01_BeforeDragDrop.html

## HOW TO USE

**To Reorder:**
1. Click and hold any project button
2. Drag up or down
3. Drop where you want it
4. Done - order saved automatically

**To Change Default:**
1. Drag desired project to top of Development list
2. That's it - it's now the default

**To Reset Order:**
1. Open DevTools (F12)
2. Console: `localStorage.removeItem('projectOrder_dev')`
3. Console: `localStorage.removeItem('projectOrder_deployed')`
4. Reload app
5. Projects return to original HTML order
