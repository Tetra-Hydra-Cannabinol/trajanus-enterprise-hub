# Workflow Reference Card

Quick reference for all development workflows.

---

## GSD Framework

**When to Use:** Tasks >500 lines, multi-file, or high risk

```
┌─────────────┐
│   EXPLORE   │  Read files, understand context
├─────────────┤  10-20% of time
│             │
├─────────────┤
│    PLAN     │  Design approach, break into steps
├─────────────┤  15-25% of time
│             │
├─────────────┤
│   EXECUTE   │  Follow plan, surgical edits
├─────────────┤  40-50% of time
│             │
├─────────────┤
│  VALIDATE   │  Test, screenshot, verify
└─────────────┘  20-30% of time
```

**Exit Criteria Per Phase:**
- EXPLORE: Documented understanding of codebase
- PLAN: Step-by-step implementation list
- EXECUTE: All steps completed, tested
- VALIDATE: All tests pass, screenshots captured

---

## Planner/Developer (CP/CC)

**CP (Planner) Role:**
- Creates task specifications
- Reviews output quality
- Makes architectural decisions
- Maintains session continuity

**CC (Developer) Role:**
- Executes code changes
- Runs tests
- Reports results
- Follows specs exactly

**Communication:**
```
CP → CURRENT_TASK.md → CC
CC → TASK_REPORT.md → CP
```

**Commands:**
- Execute → Begin task
- Status → Report progress
- Redo → Restart
- Abort → Stop

---

## Visual Validation (Playwright)

**Loop:**
```
REPEAT:
  1. Make change
  2. npm run dev
  3. Navigate to page
  4. Take screenshot
  5. Compare to style guide
  6. IF match → DONE
  7. ELSE → Fix and repeat
UNTIL: Visual correct OR max iterations
```

**Max Iterations:**
- Simple: 3
- Complex: 5
- Full page: 10

**Screenshot Tools:**
```javascript
browser_navigate({ url: '...' })
browser_take_screenshot({ filename: '...' })
browser_snapshot({}) // A11y tree
```

---

## Context Management

**Token Gauge:**
```
🟢 20-100%  → Normal ops
🟡 5-20%    → Wrap up task
🔴 <5%      → STOP & rewind
```

**At 5% - Rewind Protocol:**
1. STOP current task
2. Create checkpoint file
3. Document exact state
4. Save to EOS output
5. Inform user

**Conservation Strategies:**
- Summarize, don't quote
- Read specific lines, not whole files
- Use sub-agents for exploration
- Reference docs, don't repeat

---

## Sacred File Protocol

**Files:**
- `src/index.html`
- `src-tauri/src/lib.rs`

**Edit Workflow:**
```
1. Copy to versioned file
   index_v2.1_FEATURE.html

2. Edit the COPY only

3. Test thoroughly
   npm run dev
   Manual test
   Screenshot

4. Replace original
   ONLY after validation
```

---

## Sub-Agent Usage

**When to Spawn:**
- Large codebase exploration
- Specialized review (security, design)
- Research tasks
- Parallel independent work

**Available Agents:**
| Agent | Purpose |
|-------|---------|
| design-reviewer | UI validation |
| qcm-reviewer | Submittal compliance |
| security-auditor | Code security |
| doc-generator | Documentation |
| github-searcher | Solution finding |
| knowledge-retriever | KB search |

**Invocation:**
```
Task tool → subagent_type: "agent-name"
OR
/spawn-agent command
```

---

## End of Session (EOS)

**Trigger:** `/eos` command

**Creates 5 Documents:**
1. Session_Summary_{date}.md
2. Technical_Journal_{date}.md
3. Bills_Daily_Diary_{date}.md
4. Code_Repository_{date}.md
5. Handoff_{date}.md

**Output Location:**
```
G:\My Drive\00 - Trajanus USA\
  00-Command-Center\
    08-EOS-Files\
      001 Claude EOS Output\
```

---

## Quick Decision Tree

```
Is it a Sacred File?
├─ YES → Versioned copy workflow
└─ NO ↓

Is task >500 lines?
├─ YES → GSD Framework
└─ NO ↓

Is it UI change?
├─ YES → Visual Validation loop
└─ NO ↓

Is it exploration/research?
├─ YES → Spawn sub-agent
└─ NO → Direct execution OK
```

---

## Checklist Templates

### Before Any Edit
- [ ] Read target file
- [ ] Understand context
- [ ] Check for Sacred File status
- [ ] Backup if major change

### After Any Edit
- [ ] Test immediately
- [ ] Check console for errors
- [ ] Screenshot if UI change
- [ ] Document if significant

### Before Commit
- [ ] All tests pass
- [ ] No console errors
- [ ] Changes match requirements
- [ ] CHANGELOG updated

---

**Last Updated:** 2026-01-17
