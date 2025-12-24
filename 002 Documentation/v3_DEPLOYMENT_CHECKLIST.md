# v3.0.0 DEPLOYMENT CHECKLIST

## Pre-Deployment

- [ ] Download updated index.html
- [ ] Backup current index.html (just in case)
- [ ] Close any running Command Center instances

---

## Deploy

```powershell
# Copy new version
copy index.html "G:\My Drive\00 - Trajanus USA\00-Command-Center\index.html"

# Start app
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center"
npm start
```

---

## Visual Verification

**Look for these in sidebar:**

1. ✅ **EI Logo**
   - Large orange "E I" letters
   - Between tagline and version
   - Bold, wide spacing

2. ✅ **Version v3.0.0**
   - Below EI logo
   - Gray text

3. ✅ **Living Documents Section**
   - Between "Deployed Projects" and footer
   - "Quick Access ▼" button
   - Expandable menu

---

## Functional Testing

**Test Living Documents Menu:**

1. **Click "Quick Access ▼"**
   - [ ] Menu expands
   - [ ] Arrow changes to ▲
   - [ ] 6 items visible

2. **Test Each Item:**
   - [ ] Daily Diary opens Bills_Daily_Journal.html
   - [ ] Project Journal opens Trajanus_Project_Journal.md
   - [ ] Core Protocols opens 01-Core-Protocols folder
   - [ ] Bill's POV opens Bills_POV.md
   - [ ] Session Summaries opens 03-Session-Files folder
   - [ ] All Living Documents opens 02-Living-Documents folder

3. **Click "Quick Access ▲"**
   - [ ] Menu collapses
   - [ ] Arrow changes back to ▼

---

## Path Verification

If any menu item doesn't work, check these paths exist:

```
G:\My Drive\00 - Trajanus USA\02-Living-Documents\Bills_Daily_Journal.html
G:\My Drive\00 - Trajanus USA\02-Living-Documents\Trajanus_Project_Journal.md
G:\My Drive\00 - Trajanus USA\00-Command-Center\01-Core-Protocols\
G:\My Drive\00 - Trajanus USA\02-Living-Documents\Bills_POV.md
G:\My Drive\00 - Trajanus USA\00-Command-Center\03-Session-Files\
G:\My Drive\00 - Trajanus USA\02-Living-Documents\
```

**To fix paths:** Edit `openLivingDoc()` function in index.html

---

## What You Should See

**Sidebar top to bottom:**
1. TRAJANUS USA
2. Engineered Intelligence™
3. **E I** ← Big orange letters
4. v3.0.0
5. Projects in Development (10 projects)
6. Deployed Projects (3 projects)
7. **Living Documents** ← New section
8. Quick Access ▼
9. Footer (Anthropic Console, Google Drive)

---

## Demo to Tom

**Show him:**
1. Click Living Documents → Quick Access
2. Menu expands with 6 options
3. Click "Daily Diary" → Opens your journal
4. Click "All Living Documents" → Opens main folder
5. Professional, organized, fast access

**He'll love:**
- Clean interface
- Quick access to key documents
- No hunting through folders
- Everything in one place

---

## If Something's Wrong

**Menu doesn't appear:**
- Check you're using the NEW index.html
- Try Ctrl+Shift+R to hard refresh
- Restart app (`npm start`)

**Menu items don't open files:**
- Verify file paths in openLivingDoc()
- Check files exist at those locations
- Terminal will show error message

**EI logo doesn't show:**
- Hard refresh browser
- Check CSS loaded properly
- Inspect element to verify .ei-logo class

---

## Next Steps After Deployment

1. **Test all 6 menu items** to ensure paths are correct
2. **Update file paths** if yours differ
3. **Test Developer Toolkit** password protection
4. **Show Tom** the new features
5. **Document any issues** in terminal logs

---

## Files Created This Session

1. **index.html** - Updated app with v3.0.0 features
2. **ENTERPRISE_HUB_v3_UPDATES.md** - Feature documentation
3. **SIDEBAR_LAYOUT_v3.md** - Visual reference
4. **This checklist** - Deployment guide

All in: `/mnt/user-data/outputs/`

---

**READY TO DEPLOY!**

**Estimated time:** 2 minutes  
**Difficulty:** Easy  
**Risk:** Low (you have backup)

🚀 **GO!**
