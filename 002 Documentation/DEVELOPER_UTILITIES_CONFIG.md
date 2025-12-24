# DEVELOPER UTILITIES CONFIGURATION GUIDE
**Complete Setup Instructions**

---

## WHAT WAS ADDED

### ✅ File Conversion Tools
- **MD → DOCX** - Convert Markdown to Word documents
- **DOCX → Google Docs** - Upload Word docs to Google Drive
- **Google Docs → DOCX** - Export Google Docs as Word files
- **Batch Convert MD** - Convert multiple Markdown files at once

### ✅ User Guides Modal
- **Searchable dropdown** with all your protocol documents
- **Opens in Google Docs** (once configured)
- **Fallback to local files** if Google Docs URLs not set

### ✅ Building Codes & Standards
- **UFGS** - DoD Unified Facilities Guide Specifications
- **IBC** - International Building Code
- **UBC** - Uniform Building Code
- **NFPA** - National Fire Protection Association (all codes)
- **NFPA 70** - National Electrical Code (NEC)
- **USGS** - U.S. Geological Survey
- **UpCodes** - All building codes in one place
- **ASCE** - American Society of Civil Engineers standards
- **ACI 318** - Concrete code
- **ASTM** - Material testing standards

### ✅ Folder Navigation
- **📁 Living Documents** - Opens local folder in Explorer
- **📁 Core Protocols** - Opens local folder in Explorer
- **📁 Templates** - Opens local folder in Explorer
- **📁 Session Files** - Opens local folder in Explorer
- **📁 Command Center** - Opens local folder in Explorer
- **☁️ Google Drive Root** - Opens main Trajanus folder in browser

---

## SETUP INSTRUCTIONS

### Step 1: Configure User Guides to Open in Google Docs

**Option A: Use the Helper Script (RECOMMENDED)**

1. Save `get_user_guide_urls.py` to your Command Center folder:
   ```
   G:\My Drive\00 - Trajanus USA\00-Command-Center\
   ```

2. Run the script:
   ```powershell
   python get_user_guide_urls.py
   ```

3. The script will:
   - Search your Google Drive for all user guide files
   - Display their Google Docs URLs
   - Generate the JavaScript code for you

4. Copy the JavaScript code it outputs

5. Open `index.html` and find this section (around line 800-850):
   ```javascript
   const userGuides = [
       { name: '6-Category System Guide', url: 'https://docs.google.com/document/d/YOUR_DOC_ID_1/edit', file: '6_Category_System_Guide.docx' },
       // ... more entries
   ];
   ```

6. Replace it with the code from the script

7. Save and restart the app

**Option B: Manual Configuration**

1. Open each document in Google Docs

2. Click "Share" → "Copy link"

3. Open `index.html` in VS Code

4. Find the `userGuides` array

5. Replace `YOUR_DOC_ID_X` with the actual document ID from the URL

   **Example:**
   ```
   URL: https://docs.google.com/document/d/1ABC123xyz/edit
   Document ID: 1ABC123xyz
   ```

6. Your entry should look like:
   ```javascript
   { name: '6-Category System Guide', url: 'https://docs.google.com/document/d/1ABC123xyz/edit', file: '6_Category_System_Guide.docx' }
   ```

---

### Step 2: Configure Folder Paths (Already Done!)

The local folder paths are already configured:
- Living Documents: `G:\My Drive\00 - Trajanus USA\02-Living-Documents`
- Core Protocols: `G:\My Drive\00 - Trajanus USA\00-Command-Center\01-Core-Protocols`
- Templates: `G:\My Drive\00 - Trajanus USA\00-Command-Center\02-Templates`
- Session Files: `G:\My Drive\00 - Trajanus USA\00-Command-Center\03-Session-Files`
- Command Center: `G:\My Drive\00 - Trajanus USA\00-Command-Center`

**If your paths are different, update them in the `openLocalFolder` function.**

---

### Step 3: Set Up File Conversion Scripts

The conversion buttons call these Python scripts:
- `convert_md_to_docx.py` - MD → DOCX conversion
- `convert_to_google_docs.py` - DOCX → Google Docs upload
- `export_gdocs_to_docx.py` - Google Docs → DOCX download
- `batch_convert_to_gdocs.py` - Batch MD conversion

**Make sure these scripts exist in:**
```
G:\My Drive\00 - Trajanus USA\00-Command-Center\
```

**If they don't exist yet, you can create them or disable the buttons.**

---

## HOW TO USE

### File Conversion

1. **Single File Conversion:**
   - Click "MD → DOCX" or "DOCX → Google Docs"
   - File picker opens
   - Select your file
   - Conversion runs automatically
   - Check terminal for status

2. **Batch Conversion:**
   - Click "Batch Convert MD"
   - Script processes all MD files in a folder
   - Watch terminal for progress

### User Guides

1. Click "📚 User Guides" button

2. Modal opens with searchable list

3. **Search:**
   - Type in search box
   - List filters in real-time
   - Search by keywords: "session", "protocol", "commandments", etc.

4. **Open a Guide:**
   - Click "Open in Docs" button
   - Opens in Google Docs (if configured)
   - Falls back to local file (if not configured)

5. **Close Modal:**
   - Click the × button
   - Click outside the modal
   - Press ESC (if you add the handler)

### Building Codes

- Click any building code button
- Opens reference site in default browser
- Most useful: **UpCodes** (has all codes in one searchable interface)

### Folder Navigation

1. **Local Folders (📁):**
   - Opens Windows Explorer
   - Navigate to exact folder location
   - Fast access to files

2. **Google Drive (☁️):**
   - Opens folder in browser
   - View/edit cloud files
   - Share with team

---

## FILE LOCATIONS REFERENCE

### Current Files Delivered

```
/mnt/user-data/outputs/
├── index.html                          # Updated with all new features
├── package.json                        # Unchanged
├── main.js                            # Unchanged  
├── preload.js                         # Unchanged
├── DEVELOPMENT_WORKFLOW.md            # From previous session
├── ADDING_UTILITY_BUTTONS.md          # From previous session
├── get_user_guide_urls.py             # NEW - Helper script
└── DEVELOPER_UTILITIES_CONFIG.md      # NEW - This file
```

### Where to Deploy

```
G:\My Drive\00 - Trajanus USA\00-Command-Center\
├── index.html                          # Replace this
├── package.json                        # (no changes needed)
├── main.js                            # (no changes needed)
├── preload.js                         # (no changes needed)
├── get_user_guide_urls.py             # Copy this
└── DEVELOPER_UTILITIES_CONFIG.md      # Copy this (for reference)
```

---

## TESTING CHECKLIST

After deploying the updated files:

### File Conversion
- [ ] MD → DOCX button opens file picker
- [ ] DOCX → Google Docs button works
- [ ] Google Docs → DOCX button works
- [ ] Batch Convert runs script
- [ ] Terminal shows conversion progress
- [ ] Converted files appear in correct location

### User Guides
- [ ] 📚 User Guides button opens modal
- [ ] Search box filters guides
- [ ] "Open in Docs" buttons work
- [ ] Guides open in Google Docs (if configured)
- [ ] Guides open locally (if not configured)
- [ ] Modal closes when clicking outside
- [ ] Modal closes with × button

### Building Codes
- [ ] Each button opens correct website
- [ ] Sites load in default browser
- [ ] All links are valid (not 404)

### Folder Navigation
- [ ] Local folder buttons open Explorer
- [ ] Folders open to correct location
- [ ] Google Drive button opens browser
- [ ] Correct folder displays in Drive

### Developer Mode
- [ ] All utility sections visible when ON
- [ ] All sections hidden when OFF (for Tom)
- [ ] Toggle saves preference
- [ ] Preference persists after restart

---

## CUSTOMIZATION OPTIONS

### Add More User Guides

Edit the `userGuides` array in index.html:

```javascript
const userGuides = [
    // Existing guides...
    { name: 'New Guide Name', url: 'https://docs.google.com/document/d/DOC_ID/edit', file: 'filename.docx' }
];
```

### Add More Building Codes

Add buttons to the Building Codes section:

```html
<button class="session-btn" onclick="openExternal('https://example.com')">
    Code Name
</button>
```

### Add More Folders

Edit the `openLocalFolder` function:

```javascript
const folders = {
    'living-docs': 'G:\\My Drive\\...',
    'new-folder': 'G:\\My Drive\\Your\\New\\Path'  // Add this
};
```

Then add a button:

```html
<button class="session-btn" onclick="openLocalFolder('new-folder')">
    📁 New Folder Name
</button>
```

### Change Search Behavior

The search is currently case-insensitive and matches anywhere in the name.

To make it match only from the start:

```javascript
function filterGuides() {
    const search = document.getElementById('guideSearch').value.toLowerCase();
    const items = document.querySelectorAll('.guide-item');
    
    items.forEach(item => {
        const name = item.dataset.name;
        if (name.startsWith(search)) {  // Changed from includes()
            item.classList.remove('hidden');
        } else {
            item.classList.add('hidden');
        }
    });
}
```

---

## TROUBLESHOOTING

### User Guides Not Opening in Google Docs

**Problem:** Clicking "Open in Docs" does nothing or opens local file

**Solution:**
1. Run `get_user_guide_urls.py` to get correct URLs
2. Make sure URLs don't contain `YOUR_DOC_ID`
3. Check that files exist in Google Drive
4. Verify files are converted to Google Docs format (not just uploaded .docx)

### File Conversion Buttons Don't Work

**Problem:** Clicking conversion buttons shows errors

**Solution:**
1. Check that Python scripts exist in Command Center folder
2. Verify script filenames match exactly
3. Make sure Python is installed and in PATH
4. Check terminal for specific error messages
5. Test scripts manually first: `python convert_md_to_docx.py`

### Folders Don't Open

**Problem:** Clicking folder buttons does nothing

**Solution:**
1. Verify folder paths in `openLocalFolder` function
2. Check that folders actually exist at those paths
3. Try running command manually: `explorer "G:\My Drive\..."`
4. Check for typos in path (backslashes, spaces, etc.)

### Search Doesn't Filter

**Problem:** Typing in search box doesn't filter guides

**Solution:**
1. Open browser console (F12)
2. Check for JavaScript errors
3. Verify `data-name` attributes exist on guide items
4. Test `filterGuides()` function manually in console

### Modal Won't Close

**Problem:** Can't close User Guides modal

**Solution:**
1. Click the × button in top-right
2. Click outside the modal (on dark overlay)
3. Refresh the page (Ctrl+R)
4. Check browser console for errors

---

## ADVANCED FEATURES

### Add Keyboard Shortcuts

Add to the `<script>` section:

```javascript
document.addEventListener('keydown', (e) => {
    // Open User Guides with Ctrl+G
    if (e.ctrlKey && e.key === 'g') {
        e.preventDefault();
        showUserGuides();
    }
    
    // Close modal with ESC
    if (e.key === 'Escape') {
        hideUserGuides();
    }
});
```

### Add Recent Guides

Track recently opened guides:

```javascript
function openGuide(url, filename) {
    // Existing code...
    
    // Save to recent
    let recent = JSON.parse(localStorage.getItem('recentGuides') || '[]');
    recent.unshift({ url, filename, timestamp: Date.now() });
    recent = recent.slice(0, 5); // Keep only 5
    localStorage.setItem('recentGuides', JSON.stringify(recent));
}
```

### Add Favorites

Let users star favorite guides:

```javascript
function toggleFavorite(filename) {
    let favorites = JSON.parse(localStorage.getItem('favoriteGuides') || '[]');
    const index = favorites.indexOf(filename);
    
    if (index > -1) {
        favorites.splice(index, 1); // Remove
    } else {
        favorites.push(filename); // Add
    }
    
    localStorage.setItem('favoriteGuides', JSON.stringify(favorites));
    showUserGuides(); // Refresh display
}
```

---

## NEXT STEPS

1. **Deploy updated index.html**
   ```powershell
   cp /mnt/user-data/outputs/index.html "G:\My Drive\00 - Trajanus USA\00-Command-Center\"
   ```

2. **Run URL helper script**
   ```powershell
   python get_user_guide_urls.py
   ```

3. **Update user guides URLs** in index.html

4. **Test all features** using checklist above

5. **Create conversion scripts** if they don't exist

6. **Add more building codes** as you discover useful sites

7. **Customize folder paths** if your structure is different

---

## FUTURE ENHANCEMENTS

- [ ] Add more building code references (ITE Manual, etc.)
- [ ] Create dropdown categories for building codes
- [ ] Add PDF viewer for local code files
- [ ] Integrate with Procore for spec lookup
- [ ] Add voice search for user guides
- [ ] Create "frequently accessed" section
- [ ] Add guide preview pane
- [ ] Sync recent guides across sessions

---

**END OF CONFIGURATION GUIDE**
**Last Updated:** November 30, 2025
