# DEPLOYMENT INSTRUCTIONS
**Get everything ready for Tom in 5 minutes**

---

## STEP 1: DOWNLOAD ALL FILES

Download these files from Claude:
- index.html
- setup_documentation.py
- SETUP_DOCUMENTATION.bat
- All .md files (7 files)
- get_user_guide_urls.py

They're all in your Downloads or at:
`G:\My Drive\00 - Trajanus USA\00-Command-Center`

---

## STEP 2: RUN SETUP SCRIPT

**Double-click:** `SETUP_DOCUMENTATION.bat`

This will:
- Create folder structure (01-06)
- Move all .md files to 04-Documentation
- Move setup scripts to 05-Scripts
- Create README files
- Verify everything

**Takes 5 seconds.**

---

## STEP 3: DEPLOY APP FILES

Copy these 3 files to Command Center root:
- index.html (REPLACE existing)
- package.json (if not already there)
- main.js (if not already there)
- preload.js (if not already there)

---

## STEP 4: TEST

```powershell
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center"
npm start
```

Check:
- App opens
- All buttons work
- Developer mode toggles
- Folder buttons open correct folders
- User Guides modal works

---

## STEP 5: DEMO PREP

**For Tom (clean view):**
- Developer Mode: OFF
- Shows: App launchers, project tools only

**For you (full view):**
- Developer Mode: ON
- Shows: Everything

---

## FOLDER STRUCTURE RESULT

```
G:\My Drive\00 - Trajanus USA\00-Command-Center\
├── index.html                      (main app)
├── main.js                         (Electron main)
├── preload.js                      (security bridge)
├── package.json                    (config)
├── node_modules\                   (dependencies)
├── 01-Core-Protocols\              (operational protocols)
├── 02-Templates\                   (templates)
├── 03-Session-Files\               (session summaries)
├── 04-Documentation\               (NEW - reference docs)
│   ├── README.md
│   ├── DEVELOPMENT_WORKFLOW.md
│   ├── ADDING_UTILITY_BUTTONS.md
│   ├── DEVELOPER_UTILITIES_CONFIG.md
│   ├── DEVELOPER_UTILITIES_QUICK_REF.md
│   ├── CODING_EDUCATION_GUIDE.md
│   ├── CODING_CHEAT_SHEET.md
│   └── LEARNING_TRAINING_SUMMARY.md
├── 05-Scripts\                     (NEW - automation scripts)
│   ├── setup_documentation.py
│   └── get_user_guide_urls.py
└── 06-Archive\                     (NEW - old versions)
```

---

## DONE

**Time to complete: 5 minutes**

**Everything automated. Everything organized. Ready for Tom.**
