# GSD Framework (Get Stuff Done)

## Overview
Four-phase methodology for complex task execution. Use for tasks involving >500 lines of code, multiple files, or architectural changes.

---

## When to Use GSD

### Use GSD Framework When:
- Task involves >500 lines of code
- Multiple files need modification
- Architectural decisions required
- Risk of breaking existing functionality
- Unclear requirements need exploration
- Previous attempts have failed

### Skip GSD When:
- Single function edit
- Bug fix with clear solution
- Documentation updates
- Simple UI text changes
- Routine maintenance

---

## Phase 1: EXPLORE

### Purpose
Build comprehensive understanding before any changes.

### Duration
10-20% of total task time

### Activities
```
1. Read all relevant files completely
2. Understand existing architecture
3. Identify dependencies
4. Map data flow
5. Document current state
6. Note potential risks
```

### Exploration Checklist
- [ ] Read main file(s) being modified
- [ ] Read files that import/reference target
- [ ] Read files that target imports
- [ ] Check for tests related to target
- [ ] Review recent git history for target
- [ ] Search codebase for similar patterns
- [ ] Document findings

### Output
```markdown
## Exploration Summary

### Files Reviewed
- `file1.ext` - [purpose, key functions]
- `file2.ext` - [purpose, key functions]

### Architecture Understanding
[Describe how components interact]

### Dependencies Identified
- [Dependency 1]
- [Dependency 2]

### Potential Risks
- [Risk 1]
- [Risk 2]

### Questions Resolved
- [Question] → [Answer found at file:line]
```

---

## Phase 2: PLAN

### Purpose
Design implementation strategy with clear steps.

### Duration
15-25% of total task time

### Activities
```
1. Break task into atomic steps
2. Identify order of operations
3. Define acceptance criteria per step
4. Plan rollback strategy
5. Estimate complexity per step
6. Document the plan
```

### Planning Template
```markdown
## Implementation Plan

### Approach
[High-level strategy]

### Steps
1. **Step Name**
   - Files: `file.ext:lines`
   - Action: [specific change]
   - Test: [how to verify]
   - Risk: [LOW/MEDIUM/HIGH]

2. **Step Name**
   - Files: `file.ext:lines`
   - Action: [specific change]
   - Test: [how to verify]
   - Risk: [LOW/MEDIUM/HIGH]

### Order of Operations
1. [First] - Because [reason]
2. [Second] - Depends on [first]
3. [Third] - Can be parallelized with [second]

### Rollback Strategy
- Backup: [what to backup]
- Restore: [how to restore]
- Git: [commit strategy]

### Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
```

### Risk Assessment Matrix
| Risk Level | Characteristics | Approach |
|------------|-----------------|----------|
| LOW | Single file, isolated change | Execute directly |
| MEDIUM | Multiple files, some dependencies | Test after each step |
| HIGH | Core architecture, many dependencies | Backup, incremental, extensive testing |
| CRITICAL | Sacred files, build system | Full GSD + pair review |

---

## Phase 3: EXECUTE

### Purpose
Implement changes following the plan exactly.

### Duration
40-50% of total task time

### Principles
```
1. Follow plan step-by-step
2. No improvisation without re-planning
3. Surgical edits only
4. Test after each step
5. Document deviations
6. Commit frequently
```

### Execution Protocol
```
FOR EACH step in plan:
    1. Read current state of target file(s)
    2. Make specific edit (surgical)
    3. Save file
    4. Run immediate test
    5. IF test passes:
        - Document success
        - Move to next step
    6. IF test fails:
        - Document failure
        - Assess: minor fix or re-plan?
        - IF minor: fix and retry
        - IF major: STOP, return to PLAN
    7. Commit if milestone reached
```

### Commit Strategy
```bash
# After each major step
git add [specific files]
git commit -m "[TASK-XXX] Step N: [description]"

# Commit message format
[CATEGORY] Brief description
- What was changed
- Why it was changed
- What was tested
```

### Deviation Handling
If plan doesn't match reality:
1. STOP execution
2. Document discrepancy
3. Return to EXPLORE if understanding wrong
4. Return to PLAN if approach wrong
5. Resume EXECUTE only with updated plan

---

## Phase 4: VALIDATE

### Purpose
Verify changes meet all requirements.

### Duration
20-30% of total task time

### Validation Layers

#### Layer 1: Functional Testing
```
- [ ] App launches without errors
- [ ] Modified functionality works
- [ ] No console errors
- [ ] Edge cases handled
```

#### Layer 2: Regression Testing
```
- [ ] Related features still work
- [ ] Navigation unaffected
- [ ] No new warnings
- [ ] Performance acceptable
```

#### Layer 3: Visual Validation (UI changes)
```
- [ ] Playwright screenshot captured
- [ ] Matches style guide
- [ ] Responsive behavior correct
- [ ] Animations smooth
```

#### Layer 4: Code Quality
```
- [ ] No hardcoded values
- [ ] Error handling present
- [ ] Comments where needed
- [ ] Consistent with codebase style
```

### Validation Report
```markdown
## Validation Report

### Task: [TASK-XXX]
### Date: [DATE]

### Functional Tests
- [x] Test 1 - PASSED
- [x] Test 2 - PASSED
- [ ] Test 3 - FAILED: [reason]

### Regression Tests
- [x] All existing features work
- [x] No new console errors

### Visual Validation
- Screenshot: [path]
- Style guide compliance: YES/NO

### Code Quality
- [x] Follows patterns
- [x] Error handling
- [x] No hardcoded values

### Issues Found
- [Issue 1] - [Resolution]

### Final Status
[PASSED/FAILED/PASSED WITH NOTES]
```

---

## GSD Decision Tree

```
START
  │
  ├─ Is task >500 lines or multi-file?
  │     │
  │     ├─ YES → Use full GSD
  │     │
  │     └─ NO → Is task risky?
  │              │
  │              ├─ YES → Use PLAN + EXECUTE + VALIDATE
  │              │
  │              └─ NO → Direct execution OK
  │
  ├─ Previous attempt failed?
  │     │
  │     └─ YES → Use full GSD with extra EXPLORE
  │
  └─ Touching Sacred File?
        │
        └─ YES → Full GSD + Versioned Copy Protocol
```

---

## Common Pitfalls

### ❌ Skipping EXPLORE
```
WRONG: "I'll just start coding, I know this codebase"
RIGHT: Read files first, even if familiar
```

### ❌ Vague Plans
```
WRONG: "Step 1: Fix the bug"
RIGHT: "Step 1: In file.js:45, change condition from X to Y"
```

### ❌ Plan Deviation
```
WRONG: "While I'm here, I'll also refactor this..."
RIGHT: Complete current plan, then create new task for refactor
```

### ❌ Skipping Validation
```
WRONG: "It should work now"
RIGHT: "Tests passed: [list]. Screenshot: [path]"
```

---

## Integration with Other Workflows

- **Planner/Developer**: CP creates task, CC uses GSD to execute
- **Visual Validation**: Part of VALIDATE phase for UI changes
- **Context Management**: Long GSD may require checkpoint/resume
- **Sacred File Protocol**: Add versioned copy step before EXECUTE

---

**Last Updated:** 2026-01-17
**Version:** 1.0
