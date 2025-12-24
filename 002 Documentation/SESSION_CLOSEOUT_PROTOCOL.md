# SESSION CLOSEOUT PROTOCOL
## Mandatory Checklist for Every Session End

**Execute this protocol at the end of EVERY Claude session, regardless of whether it's end of day or just switching chats.**

---

## PHASE 1: DOCUMENT CREATION

### Step 1: Confirm Session Status with User
- [ ] Ask: "Ready to close out this session?"
- [ ] Verify: Any critical work in progress that needs finishing?
- [ ] Confirm: User has time for full closeout (5-10 minutes)

### Step 2: Create All 5 Living Documents
Create these documents in order:

#### A. Session Summary
- [ ] Date and session number
- [ ] Primary objectives accomplished
- [ ] Key decisions made
- [ ] Files created/modified
- [ ] Unresolved issues
- [ ] Next session priorities
- [ ] Format: Markdown (.md)

#### B. Technical Journal Entry
- [ ] Technical work completed
- [ ] Code changes made
- [ ] Bugs fixed/encountered
- [ ] System configurations
- [ ] Technical decisions and rationale
- [ ] Format: Markdown (.md)

#### C. Code Repository Entry
- [ ] Files modified (with line numbers)
- [ ] Current state: Working/Broken/Partial
- [ ] Known issues and bugs
- [ ] Version notes
- [ ] Rollback information if needed
- [ ] Format: Markdown (.md)

#### D. Operational Journal Entry
- [ ] Process improvements
- [ ] Protocol updates
- [ ] Workflow changes
- [ ] Lessons learned
- [ ] Efficiency gains/losses
- [ ] Format: Markdown (.md)

#### E. Personal Diary Entry (Optional)
- [ ] User's perspective on session
- [ ] Challenges faced
- [ ] Wins celebrated
- [ ] Reflections
- [ ] Format: Markdown (.md)

### Step 3: Provide Download Links
- [ ] Generate download link for each document
- [ ] Confirm user has downloaded ALL files
- [ ] Verify files saved to: `G:\My Drive\00 - Trajanus USA\00-Command-Center\`

---

## PHASE 2: AUTOMATION EXECUTION

### Step 4: User Runs Command Center Automation
User executes from Command Center:
- [ ] Open Command Center HTML
- [ ] Click ADVANCED DEVELOPMENT card
- [ ] Click "Complete Session Update" button
- [ ] Save and run the .bat file
- [ ] Verify both scripts complete successfully

**What This Does:**
1. Uploads all 5 session documents to dated archive folder
2. Appends content to all 5 MASTER living documents
3. Updates version tracking

---

## PHASE 3: HANDOFF PREPARATION

### Step 5: Create Next Session Handoff Message
Prepare a concise handoff message containing:
- [ ] Quick context summary (2-3 sentences)
- [ ] Critical items for next session
- [ ] Any blockers or urgent issues
- [ ] Files to upload at startup

### Step 6: Confirm Protocol Completion
- [ ] All 5 documents created ✓
- [ ] User downloaded all files ✓
- [ ] Automation executed successfully ✓
- [ ] Handoff message prepared ✓

---

## PHASE 4: NEW SESSION STARTUP

### For Next Claude Instance - Required Uploads:
1. `credentials.json` (from Credentials folder)
2. `token.json` (from Credentials folder)
3. Most recent Session Summary (from latest dated folder)

### Opening Message Template:
```
Continuing from [date] session. Uploaded credentials and session summary. 
Ready to continue [brief description of work].
```

---

## CRITICAL REMINDERS

**Never Skip Steps:**
- This protocol is mandatory, not optional
- Each step ensures continuity
- Skipping steps breaks the knowledge chain

**Token Management:**
- Start closeout at 15% tokens remaining
- If below 10%, prioritize Session Summary only
- Emergency: Create minimal handoff if <5%

**User Communication:**
- Keep user informed of progress
- Confirm each phase completion
- Ask questions if anything unclear

---

## PROTOCOL VERSION
- Version: 1.0
- Date Created: 2025-11-23
- Last Updated: 2025-11-23
- Status: Active

---

## STORAGE LOCATION
This protocol must be:
1. Saved to Project Knowledge
2. Referenced in OPERATIONAL_PROTOCOL.md
3. Included in every session summary
4. Updated whenever workflow changes

**End of Protocol**
