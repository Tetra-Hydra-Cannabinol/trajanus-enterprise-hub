# DEVELOPER UTILITIES - QUICK REFERENCE
**Visual Guide to Your New Tools**

---

## 🎯 SECTION OVERVIEW

```
DEVELOPER UTILITIES (4 Sections)
├── Developer Utilities          (3 buttons)
├── File Conversion             (4 buttons)
├── Reference & Documentation   (8 buttons)
└── Building Codes & Standards  (10 buttons)
```

---

## 📋 DEVELOPER UTILITIES SECTION

```
┌─────────────────────────────────────────────┐
│  Developer Utilities                        │
├─────────────────────────────────────────────┤
│  [ Mission Brief ]  [ Sync Memory ]         │
│                                             │
│  [  Perform EOS Protocols  ]  ← GREEN      │
└─────────────────────────────────────────────┘
```

**Buttons:**
- **Mission Brief** - Generate handoff prompt for new session
- **Sync Memory** - Refresh Claude's memory with protocols
- **Perform EOS Protocols** - End-of-session routine (green button)

---

## 🔄 FILE CONVERSION SECTION

```
┌─────────────────────────────────────────────┐
│  File Conversion                            │
├─────────────────────────────────────────────┤
│  [ MD → DOCX ]        [ DOCX → Google Docs ]│
│                                             │
│  [ Google Docs → DOCX ]  [ Batch Convert ]  │
└─────────────────────────────────────────────┘
```

**Buttons:**
- **MD → DOCX** - Convert single Markdown file to Word
- **DOCX → Google Docs** - Upload Word doc to Drive
- **Google Docs → DOCX** - Download Google Doc as Word
- **Batch Convert MD** - Convert multiple MD files at once

**How it works:**
1. Click button
2. File picker opens
3. Select file
4. Conversion runs automatically
5. Check terminal for status

---

## 📚 REFERENCE & DOCUMENTATION SECTION

```
┌─────────────────────────────────────────────┐
│  Reference & Documentation                  │
├─────────────────────────────────────────────┤
│  [ 📚 User Guides ]  [ 📁 Living Documents ]│
│  [ 📁 Core Protocols ]  [ 📁 Templates ]    │
│  [ 📁 Session Files ]  [ 📁 Command Center ]│
│  [ ☁️ Google Drive Root ]  [ Thesaurus ]    │
└─────────────────────────────────────────────┘
```

**Buttons:**

### 📚 User Guides
Opens searchable modal with all your protocol documents:
```
┌──────────────────────────────────────────┐
│  📚 User Guides & Documentation      [×] │
├──────────────────────────────────────────┤
│  [ Search guides...                    ] │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ 6-Category System Guide  [Open]    │ │
│  │ End of Session Closeout  [Open]    │ │
│  │ File Systems User Guide  [Open]    │ │
│  │ Morning Session Startup  [Open]    │ │
│  │ Operational Protocols    [Open]    │ │
│  │ The Commandments of AI   [Open]    │ │
│  │ Bill's Profile           [Open]    │ │
│  │ START HERE Guide         [Open]    │ │
│  │ Development Workflow     [Open]    │ │
│  │ Adding Utility Buttons   [Open]    │ │
│  │ Operational Protocol MD  [Open]    │ │
│  │ Limitless Integration    [Open]    │ │
│  └────────────────────────────────────┘ │
└──────────────────────────────────────────┘
```

**Features:**
- Real-time search filtering
- Opens in Google Docs (when configured)
- Falls back to local files
- Click outside or × to close

### 📁 Folder Buttons
- **Living Documents** → Opens: `G:\...\02-Living-Documents`
- **Core Protocols** → Opens: `G:\...\01-Core-Protocols`
- **Templates** → Opens: `G:\...\02-Templates`
- **Session Files** → Opens: `G:\...\03-Session-Files`
- **Command Center** → Opens: `G:\...\00-Command-Center`

### ☁️ Cloud Access
- **Google Drive Root** → Opens main Trajanus folder in browser

### 📖 Reference
- **Thesaurus** → Opens thesaurus.com

---

## 🏗️ BUILDING CODES & STANDARDS SECTION

```
┌─────────────────────────────────────────────┐
│  Building Codes & Standards                 │
├─────────────────────────────────────────────┤
│  [ UFGS (DoD) ]   [ IBC ]      [ UBC ]      │
│  [ NFPA (All) ]   [ NFPA 70 ]  [ USGS ]     │
│  [ UpCodes ]      [ ASCE ]     [ ACI 318 ]  │
│  [ ASTM ]                                   │
└─────────────────────────────────────────────┘
```

**Quick Reference:**

| Button | Full Name | What It Is |
|--------|-----------|------------|
| **UFGS (DoD)** | Unified Facilities Guide Specs | DoD construction standards |
| **IBC** | International Building Code | General building requirements |
| **UBC** | Uniform Building Code | Legacy building code |
| **NFPA (All)** | NFPA Codes & Standards | All fire protection codes |
| **NFPA 70** | National Electrical Code (NEC) | Electrical requirements |
| **USGS** | U.S. Geological Survey | Seismic, soil, geological data |
| **UpCodes** | All Codes in One | Searchable database of ALL codes |
| **ASCE** | Civil Engineering Standards | Structural, geotechnical standards |
| **ACI 318** | Concrete Code | Concrete design & construction |
| **ASTM** | Material Testing Standards | Testing methods & specs |

**Most Useful for Quick Reference:**
→ **UpCodes** - Has everything in one searchable interface
→ **UFGS** - Your primary spec source for DoD work
→ **NFPA 70** - Electrical work reference

---

## 🎨 VISUAL LAYOUT IN APP

```
┌─────────────────────────────────────────────────────────────────────┐
│                        TRAJANUS COMMAND CENTER                      │
├─────────────┬───────────────────────────────────────────────────────┤
│             │                                                       │
│  SIDEBAR    │                 MAIN CONTENT AREA                    │
│             │                                                       │
│  Projects   │  ┌──────────────────────────────────────────────┐   │
│  ├ Dev      │  │  Developer Utilities                         │   │
│  ├ Deploy   │  │  [ Mission ] [ Sync ] [ EOS Protocols ]      │   │
│             │  └──────────────────────────────────────────────┘   │
│             │                                                       │
│  [Dev Mode] │  ┌──────────────────────────────────────────────┐   │
│             │  │  File Conversion                             │   │
│             │  │  [ MD→DOCX ] [ DOCX→Docs ] [ Docs→DOCX ]    │   │
│             │  └──────────────────────────────────────────────┘   │
│             │                                                       │
│             │  ┌──────────────────────────────────────────────┐   │
│             │  │  Reference & Documentation                   │   │
│             │  │  [ 📚 Guides ] [ 📁 Folders ] [ ☁️ Drive ]   │   │
│             │  └──────────────────────────────────────────────┘   │
│             │                                                       │
│             │  ┌──────────────────────────────────────────────┐   │
│             │  │  Building Codes & Standards                  │   │
│             │  │  [ UFGS ] [ IBC ] [ NFPA ] [ USGS ]         │   │
│             │  └──────────────────────────────────────────────┘   │
│             │                                                       │
└─────────────┴───────────────────────────────────────────────────────┘
```

---

## ⚙️ CONFIGURATION CHECKLIST

Before using all features, complete these setups:

### ✅ File Conversion Scripts
- [ ] `convert_md_to_docx.py` exists
- [ ] `convert_to_google_docs.py` exists
- [ ] `export_gdocs_to_docx.py` exists
- [ ] `batch_convert_to_gdocs.py` exists
- [ ] All scripts are in Command Center folder
- [ ] Scripts have Google API credentials

### ✅ User Guides URLs
- [ ] Run `get_user_guide_urls.py`
- [ ] Copy JavaScript code it generates
- [ ] Update `userGuides` array in index.html
- [ ] Replace all `YOUR_DOC_ID_X` placeholders
- [ ] Test that guides open in Google Docs

### ✅ Folder Paths
- [ ] Verify Living Documents path
- [ ] Verify Core Protocols path
- [ ] Verify Templates path
- [ ] Verify Session Files path
- [ ] Verify Command Center path
- [ ] Test that folders open in Explorer

### ✅ Developer Mode
- [ ] Toggle ON/OFF works
- [ ] Preference saves to localStorage
- [ ] Badge shows correct state (ON/OFF)
- [ ] All utility sections hide when OFF
- [ ] Sections show when ON

---

## 🚀 USAGE PATTERNS

### Daily Workflow
1. **Morning:** Enable Developer Mode
2. **Check Guides:** Open relevant protocols for today's work
3. **Convert Files:** Process any documentation
4. **Reference Codes:** Look up specs as needed
5. **Navigate Folders:** Quick access to files
6. **End of Day:** Run EOS Protocols

### File Management
1. **Create MD files** in VS Code/other editor
2. **Convert to DOCX** when ready for sharing
3. **Upload to Google Docs** for collaboration
4. **Download as DOCX** when final version needed

### Research & Reference
1. **Search User Guides** for internal protocols
2. **Check Building Codes** for compliance
3. **Open Folders** to find specific files
4. **Use Thesaurus** for better writing

---

## 📝 KEYBOARD SHORTCUTS (Future Enhancement)

**Could be added:**
- `Ctrl+G` → Open User Guides
- `Ctrl+F` → Open Folder Navigator
- `Ctrl+C` → Open Code References
- `Esc` → Close any modal
- `Ctrl+E` → Run EOS Protocols

---

## 🎯 QUICK TROUBLESHOOTING

| Problem | Quick Fix |
|---------|-----------|
| Button does nothing | Check browser console (F12) for errors |
| File won't convert | Verify Python script exists and runs |
| Guide won't open | Update URLs using `get_user_guide_urls.py` |
| Folder won't open | Check path in `openLocalFolder()` function |
| Search doesn't work | Clear browser cache, reload app |
| Modal stuck open | Click outside modal or refresh page |

---

## 💡 PRO TIPS

1. **Use UpCodes** instead of individual code sites - it searches everything
2. **Set up Google Docs URLs** ASAP - much faster than local files
3. **Enable Developer Mode** only when you need it (keeps interface clean for Tom)
4. **Batch convert** all your MD files at once instead of one-by-one
5. **Use search** in User Guides - way faster than scrolling
6. **Bookmark folders** you use most - add dedicated buttons

---

## 🔮 COMING SOON

**Features you might want to add:**
- [ ] Recent guides list
- [ ] Favorite guides
- [ ] Code snippets library
- [ ] Quick notes panel
- [ ] Project-specific bookmarks
- [ ] Integration with Procore
- [ ] Voice commands for hands-free operation
- [ ] Mobile companion app

---

## 📊 BUTTON COUNT BY SECTION

```
Developer Utilities:        3 buttons
File Conversion:           4 buttons
Reference & Documentation: 8 buttons
Building Codes:           10 buttons
──────────────────────────────────
TOTAL:                    25 buttons
```

Plus:
- 1 searchable modal (User Guides)
- 12 documents in User Guides
- 6 local folder shortcuts
- 1 cloud folder shortcut

---

## 🎨 COLOR CODING

```
🟢 Green  → Critical actions (EOS Protocols)
🟤 Brown  → Standard utilities
🟠 Orange → Active/hover states
⚪ Cream  → Text and highlights
```

---

**This is your complete developer toolkit. Everything you need for daily PM work, reference lookup, file management, and workflow automation - all in one place.**

**END OF QUICK REFERENCE**
**Last Updated:** November 30, 2025
