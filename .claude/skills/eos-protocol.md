# Skill: End of Session (EOS) Protocol

## Name
eos-protocol

## Description
Execute the standardized End of Session protocol for Trajanus. Creates session documentation, handoff files, and packages deliverables for continuity.

## When to Use
- User says "end of session", "EOS", "wrap up", "end of shift"
- Before context limit is reached
- When switching to a new conversation
- After completing major milestones

## EOS File Structure

### Living Documents (Append/Revise)
| Document | Purpose | Update Method |
|----------|---------|---------------|
| `DEV_SPEC_LIVING_DOC.md` | All dev/architecture/spec work | Append new sections |
| `BILLS_DIARY.md` | Personal journal entries | Append dated entries |

### Session Files (Timestamped: YYYY-MM-DD-HHMM)
| File | Purpose | Content |
|------|---------|---------|
| `SESSION_SUMMARY.md` | Complete session content | Full details, NO summaries |
| `HANDOFF.md` | Next session context | Current state, priorities |
| `ACCOMPLISHMENTS.md` | What was done | Checklist format |

## Procedure

### Step 1: Gather Session Information
```
- What was accomplished this session?
- What files were created/modified?
- What decisions were made?
- What's pending for next session?
- Any user feedback/quotes to preserve?
```

### Step 2: Create Session Summary
**Location:** `Session_Archive/YYYY-MM-DD-HHMM_SESSION_SUMMARY.md`

```markdown
# SESSION SUMMARY
## YYYY-MM-DD-HHMM
### [Session Title]

---

## SESSION CONTEXT
[What preceded this session]

---

## WORK COMPLETED

### 1. [Category]
[Full details - NO paraphrasing]

---

## FILES CREATED THIS SESSION
| File | Type | Purpose |
|------|------|---------|

---

## DECISIONS MADE
1. [Decision]: [Rationale]

---

## USER FEEDBACK (DIRECT QUOTES)
- "[Exact quote from user]"

---

## TECHNICAL DETAILS CAPTURED
[Code snippets, configurations, paths]

---

## NEXT SESSION PRIORITIES
1. [Priority item]
```

### Step 3: Create Handoff
**Location:** `Session_Archive/YYYY-MM-DD-HHMM_HANDOFF.md`

```markdown
# HANDOFF
## YYYY-MM-DD-HHMM
### For Next Session

---

## CURRENT STATE
[Brief status of each workstream]

---

## FILES READY FOR ACTION
1. [File] - [Action needed]

---

## IMMEDIATE NEXT STEPS
1. [Step]

---

## CONTEXT FOR NEW INSTANCE
[1-2 paragraph summary for cold start]

---

## DON'T FORGET
- [Critical reminders]
```

### Step 4: Create Accomplishments
**Location:** `Session_Archive/ACCOMPLISHMENTS_YYYY-MM-DD.md`

```markdown
# SESSION ACCOMPLISHMENTS
## YYYY-MM-DD

---

## CREATED THIS SESSION
1. [x] [Item with checkmark]

---

## PENDING (NEXT SESSION)
- [ ] [Uncompleted item]

---

## STATS
| Metric | Count |
|--------|-------|
| Files created | X |
```

### Step 5: Update Living Docs
- Append to DEV_SPEC if architecture/spec work done
- Append to BILLS_DIARY if personal notes shared

### Step 6: Package Deliverables
1. List all files for EOS package
2. Note which need Google Docs conversion
3. Identify KB ingestion candidates

### Step 7: Capture Session Learnings (Optional)
Prompt user:
```
Run /reflect to capture session learnings? (y/n)
```

If yes:
1. Execute `/reflect` skill
2. Analyze session for corrections, patterns, preferences
3. Present HIGH confidence findings for approval
4. Append approved learnings to CLAUDE.md LEARNED PATTERNS section
5. Report what was added

If no:
- Skip to finalizing session

**Why this matters:** Corrections made in this session become permanent knowledge, preventing repeated mistakes in future sessions.

## Output Locations
```
G:\My Drive\00 - Trajanus USA\00-Command-Center\Session_Archive\
├── Living_Docs\
│   ├── DEV_SPEC_LIVING_DOC.md
│   └── BILLS_DIARY.md
├── YYYY-MM-DD-HHMM_SESSION_SUMMARY.md
├── YYYY-MM-DD-HHMM_HANDOFF.md
└── ACCOMPLISHMENTS_YYYY-MM-DD.md
```

## Timestamp Format
- Session files: `YYYY-MM-DD-HHMM` (24-hour)
- Example: `2025-12-30-0930`

## Quality Checklist
- [ ] No summaries - full content preserved
- [ ] All user quotes captured exactly
- [ ] All file paths documented
- [ ] Technical details included
- [ ] Next steps clear and actionable
- [ ] Handoff readable by fresh instance
- [ ] Session learnings captured (/reflect offered)
