# CODE REPOSITORY ENTRY
## Date: December 7, 2025 21:00 EST
## Version: index_v2.1.0_UniversalFileBrowser.html
## Change Type: Major Architecture Restructuring + Universal File Browser

---

## CHANGES COMPLETED

### 1. Removed Projects from Sidebar

**Removed from "Projects in Development":**
- Developer Toolkit
- SSHO Toolkit
- Memory/Recall

**Removed from "Deployed Projects":**
- SSHO Toolkit (was showing as v1 ACTIVE)

**Rationale:** Developer Toolkit functionality moved to universal terminal tabs. SSHO and Memory/Recall not needed for the 4 core toolkits.

### 2. Created Universal File Browser Modal

**New modal:** `fileBrowserModal`
- User Guides style: clean list, no date grouping
- Shows ALL files from selected folder
- 3 buttons per file:
  - **Preview** (blue) - View file
  - **Download DOCX** (orange) - Save as Word doc
  - **Download G-Docs** (green) - Upload to Google Docs

**Modal HTML:**
```html
<div class="modal-overlay" id="fileBrowserModal" onclick="closeFileBrowser(event)">
    <div class="modal" onclick="event.stopPropagation()" style="max-width: 900px;">
        <div class="modal-header">
            <h2 id="fileBrowserTitle">📁 Files</h2>
            <button class="modal-close" onclick="hideFileBrowser()">×</button>
        </div>
        <div class="modal-body">
            <input type="text" class="search-box" id="fileBrowserSearch" placeholder="Search files..." onkeyup="filterBrowserFiles()">
            <div class="guide-list" id="fileBrowserList"></div>
        </div>
    </div>
</div>
```

### 3. Replaced openFileBrowser() Function

**OLD:** Created complex overlay with date grouping, search, filters
**NEW:** Simple modal like User Guides with file list and 3 buttons

**Key features:**
- Uses Electron API: `window.electronAPI.listDirectory(path)`
- Folder-specific titles with emojis
- Error handling for missing Electron environment
- Search/filter capability

**Folder mappings:**
```javascript
const folderPaths = {
    'living-docs': 'G:\\My Drive\\00 - Trajanus USA\\03-Living-Documents',
    'sessions': 'G:\\My Drive\\00 - Trajanus USA\\07-Session-Journal',
    'templates': 'G:\\My Drive\\00 - Trajanus USA\\02-Templates',
    'command-center': 'G:\\My Drive\\00 - Trajanus USA\\00-Command-Center',
    'protocols': 'G:\\My Drive\\00 - Trajanus USA\\01-Core-Protocols',
    'learning': 'G:\\My Drive\\00 - Trajanus USA\\00-Command-Center\\02-Learning',
    'scripts': 'G:\\My Drive\\00 - Trajanus USA\\00-Command-Center\\05-Scripts',
    'documentation': 'G:\\My Drive\\00 - Trajanus USA\\00-Command-Center\\04-Documentation'
};
```

### 4. Added Helper Functions

**New functions:**
```javascript
renderFileBrowserList()      // Renders files with 3 buttons
filterBrowserFiles()         // Search filter
closeFileBrowser(event)      // Click outside to close
hideFileBrowser()            // Close modal
previewFile(path, name)      // TODO: Implement
downloadAsDOCX(path, name)   // TODO: Implement
downloadAsGoogleDocs(path, name) // TODO: Implement
```

### 5. Added CSS for File Browser Items

**New classes:**
```css
.file-browser-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 15px;
    background: rgba(0,0,0,0.2);
    border-radius: 6px;
    margin-bottom: 8px;
    border-left: 3px solid var(--orange-dark);
}

.file-browser-buttons {
    display: flex;
    gap: 8px;
}

.file-browser-buttons .guide-btn {
    padding: 6px 10px;
    font-size: 0.7rem;
}
```

---

## REMAINING WORK (NOT COMPLETED YET)

### 1. Remove Old Project Workspace Sections

Still need to remove HTML sections for:
- Developer Toolkit workspace (line ~2241)
- SSHO Toolkit workspace (line ~2550)
- Memory/Recall workspace (line ~2659)

### 2. Implement Button Functionality

Placeholder functions created, need implementation:
- `previewFile()` - Show file content in modal
- `downloadAsDOCX()` - Convert and download as Word
- `downloadAsGoogleDocs()` - Upload to Google Drive

### 3. Universal Terminal Tabs

Terminal tabs (Developer Tools, Codes and Standards, External Programs) already exist and are universal. Need to verify they show in all 6 remaining projects:
- Enterprise Hub
- Website Builder
- PM Toolkit
- QCM Toolkit
- Route Optimizer
- Traffic Studies

---

## FILES MODIFIED

**Lines changed:** ~200 lines
- Removed: 3 project buttons from sidebar
- Added: File browser modal HTML
- Replaced: openFileBrowser() function (~100 lines)
- Added: CSS for file-browser-item
- Added: 6 new helper functions

---

## TESTING REQUIRED

1. **Click any file browser button** (Living Documents, Session Library, etc.)
2. **Modal should appear** with User Guides styling
3. **Files should list** with filename and 3 buttons
4. **Search should filter** files
5. **Buttons should show** proper colors:
   - Preview = Blue (#3498db)
   - Download DOCX = Orange (#e67e22)
   - Download G-Docs = Green (default)

---

## KNOWN ISSUES

1. **Button functions not implemented** - Preview/Download buttons log to console only
2. **Old project workspaces still in HTML** - Need removal
3. **Path escaping** - Backslashes need proper escaping for onclick attributes

---

## NEXT SESSION PRIORITIES

1. Implement Preview, Download DOCX, Download Google Docs functions
2. Remove old project workspace HTML sections
3. Test file browser in all 6 projects
4. Verify terminal tabs appear universally

---

**Status:** 60% complete
**Risk:** Medium - Old code still present, button functions TODO
**Rollback:** Previous version available
