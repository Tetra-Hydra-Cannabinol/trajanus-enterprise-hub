# Planner/Developer Workflow

## Overview
Hub-and-spoke architecture separating strategic planning (CP) from tactical execution (CC).

---

## Roles

### Claude Chat (CP) - PLANNER
**Purpose:** Strategic oversight, task specification, quality review

**Responsibilities:**
- Create detailed task specifications
- Review work output for quality
- Coordinate multi-session strategies
- Maintain project continuity
- Make architectural decisions

**Does NOT:**
- Write code directly
- Execute commands
- Modify files

### Claude Code (CC) - DEVELOPER
**Purpose:** Tactical execution, code implementation, testing

**Responsibilities:**
- Execute code changes
- Run tests and builds
- Report results accurately
- Follow specifications exactly
- Implement surgical edits only

**Does NOT:**
- Make architectural decisions
- Deviate from specifications
- Skip testing steps

---

## Communication Protocol

### Task Assignment (CP → CC)
Location: `G:\My Drive\00 - Trajanus USA\00-Command-Center\05-Scripts\CURRENT_TASK.md`

```markdown
# CURRENT_TASK

## Task ID: TASK-XXX
## Priority: [CRITICAL/HIGH/MEDIUM/LOW]
## Assigned: [TIMESTAMP]

## Objective
[Clear, specific goal]

## Specifications
- [Detailed requirement 1]
- [Detailed requirement 2]
- [Detailed requirement 3]

## Files to Modify
- `path/to/file1.ext` - [what to change]
- `path/to/file2.ext` - [what to change]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Constraints
- [Any limitations]
- [Do NOT touch: xyz]

## Testing Required
- [ ] Test step 1
- [ ] Test step 2
```

### Status Reporting (CC → CP)
Location: `G:\My Drive\00 - Trajanus USA\00-Command-Center\05-Scripts\TASK_REPORT.md`

```markdown
# TASK_REPORT

## Task ID: TASK-XXX
## Status: [IN_PROGRESS/BLOCKED/COMPLETE/FAILED]
## Updated: [TIMESTAMP]

## Work Completed
- [Specific change 1] - `file:line`
- [Specific change 2] - `file:line`

## Test Results
- [x] Test 1 - PASSED
- [ ] Test 2 - FAILED: [reason]

## Issues Encountered
- [Issue description]
- [Resolution or blocker status]

## Next Steps
- [What needs to happen next]

## Evidence
- Screenshot: [path]
- Console output: [summary]
```

---

## Voice Commands

### CP to CC
| Command | Meaning |
|---------|---------|
| **Execute** | Begin task execution |
| **Status** | Report current progress |
| **Redo** | Restart task from scratch |
| **Abort** | Stop current task |
| **Verify** | Run validation checks |

### CC Responses
| Response | Meaning |
|----------|---------|
| **Tracking** | Task received, beginning work |
| **Complete** | Task finished, see TASK_REPORT |
| **Blocked** | Cannot proceed, see TASK_REPORT |
| **Failed** | Task unsuccessful, see details |

---

## Workflow Execution

### Standard Task Flow
```
1. CP creates CURRENT_TASK.md with specifications
2. CP says "Execute"
3. CC reads CURRENT_TASK.md
4. CC executes task (surgical edits only)
5. CC tests changes
6. CC updates TASK_REPORT.md
7. CC reports completion
8. CP reviews output
9. CP approves or requests revision
```

### Blocked Task Flow
```
1. CC encounters blocker
2. CC updates TASK_REPORT.md with blocker details
3. CC reports "Blocked"
4. CP reviews and resolves blocker
5. CP updates CURRENT_TASK.md if needed
6. CP says "Execute" to resume
```

### Multi-Task Session
```
1. CP creates task list in PLAN.md
2. CP assigns first task via CURRENT_TASK.md
3. CC completes and reports
4. CP reviews and approves
5. CP assigns next task
6. Repeat until complete
7. CP conducts session review
```

---

## Context Separation

### Why Separation Matters
- **Prevents context pollution** - Planning thoughts don't consume CC's execution context
- **Maintains focus** - Each instance has clear, singular purpose
- **Enables parallel work** - CP can plan next task while CC executes current
- **Preserves history** - CP maintains session continuity across CC resets

### What Stays in CP
- Project strategy and roadmap
- Architectural decisions
- Multi-session task tracking
- Quality review notes
- User preference documentation

### What Stays in CC
- Active code context
- File contents being modified
- Test results
- Execution details
- Technical implementation notes

---

## Anti-Patterns

### ❌ CP Writing Code
```
WRONG: "Here's the code to add: function xyz() { ... }"
RIGHT: "Add function xyz that does [specification]"
```

### ❌ CC Making Decisions
```
WRONG: "I decided to restructure the architecture..."
RIGHT: "Specification unclear on architecture. Blocked. Options: A, B, C"
```

### ❌ Skipping Communication Files
```
WRONG: Direct verbal task assignment without CURRENT_TASK.md
RIGHT: Write CURRENT_TASK.md, then say "Execute"
```

### ❌ Incomplete Reporting
```
WRONG: "Done"
RIGHT: "Complete. Modified file:line. Tests passed. Screenshot: path"
```

---

## Session Handoff

When CP session ends:
1. Create Next_Session_Handoff.md
2. Include current PLAN.md state
3. Document active/blocked tasks
4. Provide trigger phrase for next session

When CC session ends:
1. Complete TASK_REPORT.md
2. Commit all changes with clear message
3. Document any partial work
4. Note what was tested vs. untested

---

## Integration with Other Workflows

- **GSD Framework**: Use for tasks >500 lines or high complexity
- **Visual Validation**: Trigger Playwright after UI changes
- **Context Management**: CC triggers rewind at 5% remaining
- **Sub-Agents**: CC spawns for specialized tasks

---

**Last Updated:** 2026-01-17
**Version:** 1.0
