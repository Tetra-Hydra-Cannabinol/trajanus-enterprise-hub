# TASK-003 QUICK START - REVISED CONFIGS

**Version:** 2.1 (NO OPTIONS enforcement)  
**Time:** 10 minutes  

---

## WHAT CHANGED FROM v2.0

**Problem:** Planner asking "Do you want me to create planner-plan.md?" instead of just creating it.

**Fix:** Military-style directives. NO asking, NO options, JUST EXECUTE.

---

## SETUP (3 STEPS)

### STEP 1: OPEN TERMINALS

Terminal 1: Already open (from previous work)
Terminal 2: New PowerShell → `cd "G:\My Drive\00 - Trajanus USA\00-Command-Center"` → `claude-code`

### STEP 2: CONFIGURE PLANNER (Terminal 1)

Copy/paste entire block from: `PLANNER_CONFIG_REVISED.md`

**Key phrase in config:** "NO questions. NO options. EXECUTE."

### STEP 3: CONFIGURE DEVELOPER (Terminal 2)

Copy/paste entire block from: `DEVELOPER_CONFIG_REVISED.md`

**Key phrase in config:** "NO questions. NO options. EXECUTE."

---

## TEST (5 MINUTES)

### To Planner:

```
Create plan for adding startup log message.

Task: Add console.log('Trajanus Hub v1.0 starting...') on app launch

Write to /home/claude/planner-plan.md

Execute now.
```

**Expected response:** "Plan created. File: planner-plan.md"
**NOT:** "Do you want me to..."

---

### To Developer:

```
Read /home/claude/planner-plan.md

Execute step 1 only.

Write report to /home/claude/developer-report-1.md

Execute now.
```

**Expected response:** "Step 1 complete. File: developer-report-1.md"
**NOT:** "Should I proceed with..."

---

### To Planner:

```
Read /home/claude/developer-report-1.md

Write review to /home/claude/planner-review-1.md

Execute now.
```

**Expected response:** "Review written. File: planner-review-1.md"
**NOT:** "I have several thoughts..."

---

## IF THEY VIOLATE PROTOCOL

**Command:**
```
STOP. Protocol violation.

NEVER ask "Do you want me to..."
NEVER offer options.
JUST EXECUTE.

[Repeat original command]
```

---

## SUCCESS CRITERIA

✅ Planner creates files without asking
✅ Developer executes without asking
✅ Both report completion immediately
✅ No options, no explanations, just results
✅ Console.log appears on app startup

---

## FILES

- `PLANNER_CONFIG_REVISED.md` - Paste into Terminal 1
- `DEVELOPER_CONFIG_REVISED.md` - Paste into Terminal 2

---

**READY. Execute setup now.**
