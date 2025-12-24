# DUPLICATE FILE CLEANUP GUIDE
## Trajanus USA - Document Control

**PURPOSE:** Remove or rename empty duplicate MASTER files to prevent future confusion.

---

## THE PROBLEM

When searching by name, Google Drive returns multiple files with the same name.
The script was finding the WRONG file (empty duplicate) instead of the original with content.

**Result:** Weeks of session data was appended to empty files instead of the real MASTERs.

---

## CLEANUP ACTIONS

### Option A: DELETE Duplicates (Recommended)
Permanently remove empty files. Clean and simple.

### Option B: RENAME Duplicates  
Rename to `[name]_DEPRECATED_DO_NOT_USE`
Keeps history but prevents script from finding them.

---

## FILES TO CLEAN UP

### EMPTY DUPLICATES (Delete or Rename These)

**Technical_Journal_November_2025_MASTER** (EMPTY)
- ID: `1LQnGWZVV5Ze30XH8OOYWqASEM2nLYSQxAL8ok0FY18s`
- URL: https://docs.google.com/document/d/1LQnGWZVV5Ze30XH8OOYWqASEM2nLYSQxAL8ok0FY18s/edit
- Created: Nov 22, 17:43 (NEWER - wrong one)
- ACTION: DELETE or rename to `Technical_Journal_DEPRECATED`

**Personal_Diary_November_2025_MASTER** (EMPTY)
- ID: `174kCDc4AU7LqvN2goFefjHAPFsMoG4la5q2CzvZ_TBY`
- URL: https://docs.google.com/document/d/174kCDc4AU7LqvN2goFefjHAPFsMoG4la5q2CzvZ_TBY/edit
- Created: Nov 22, 17:44 (NEWER - wrong one)
- ACTION: DELETE or rename to `Personal_Diary_DEPRECATED`

**Operational_Journal_November_2025_MASTER** (EMPTY - maybe)
- ID: `1W--Zf8mX57M9cYonAnoXJtgEFgXsrALxK-bjqMxxONI`
- URL: https://docs.google.com/document/d/1W--Zf8mX57M9cYonAnoXJtgEFgXsrALxK-bjqMxxONI/edit
- ACTION: Bill to verify if empty, then DELETE or rename

**Session_Summaries_November_2025_MASTER** (EMPTY - maybe)
- ID: `1ug6hyU9kE-n369M0lr1ZAElaphfpP3IfNL3duCtnXu0`
- URL: https://docs.google.com/document/d/1ug6hyU9kE-n369M0lr1ZAElaphfpP3IfNL3duCtnXu0/edit
- ACTION: Bill to verify if empty, then DELETE or rename

---

## KEEP THESE (Correct MASTERs with Content)

**Technical_Journal_November_2025_MASTER** (HAS CONTENT)
- ID: `1iPZAmi2bYBRmDnsgwZK3UZFCsB_YHj9RvRtKWJqDb2Q`
- URL: https://docs.google.com/document/d/1iPZAmi2bYBRmDnsgwZK3UZFCsB_YHj9RvRtKWJqDb2Q/edit
- Content: Entry #001 through #022+
- ACTION: KEEP - This is the correct file

**Personal_Diary_November_2025_MASTER** (HAS CONTENT)
- ID: `1HKOisNN8A5rf9YdFJnJSdgH326bdJTun2rDqObNvrM8`
- URL: https://docs.google.com/document/d/1HKOisNN8A5rf9YdFJnJSdgH326bdJTun2rDqObNvrM8/edit
- Content: Oct 19 - Nov entries
- ACTION: KEEP - This is the correct file

**Operational_Journal** - PENDING
- Bill searching for correct file with content

**Session_Summary** - PENDING
- Bill searching for correct file with content

---

## HOW TO DELETE IN GOOGLE DRIVE

1. Open the URL for the empty file
2. Click File menu → "Move to trash"
3. Or right-click in Drive and select "Remove"

**To permanently delete:**
1. Go to Drive → Trash
2. Right-click → "Delete forever"

---

## HOW TO RENAME IN GOOGLE DRIVE

1. Open the URL for the empty file
2. Click on the title at top of document
3. Change to: `[OriginalName]_DEPRECATED_DO_NOT_USE`
4. Press Enter to save

---

## AFTER CLEANUP

1. Verify only ONE file exists for each MASTER name
2. Update `MASTER_DOC_IDS` in script with correct IDs
3. Run test to confirm script uses correct files
4. Update MASTER_INDEX with verified IDs

---

## PREVENTION

**Why This Happened:**
- Script searched by name, found newest file (empty)
- Original files with content were older, sorted lower
- Name-based search is unreliable when duplicates exist

**How We're Fixing It:**
- Hardcode correct document IDs in script
- Script NEVER searches by name
- INDEX document tracks all IDs
- Cleanup duplicates so only one exists

---

## VERIFICATION CHECKLIST

After cleanup, confirm:
- [ ] Only ONE Technical_Journal_November_2025_MASTER exists
- [ ] Only ONE Personal_Diary_November_2025_MASTER exists
- [ ] Only ONE Operational_Journal_November_2025_MASTER exists
- [ ] Only ONE Session_Summaries_November_2025_MASTER exists
- [ ] All remaining MASTERs contain actual content
- [ ] Script MASTER_DOC_IDS updated with correct IDs
- [ ] MASTER_INDEX updated with correct IDs
- [ ] Test append confirms content goes to right file
