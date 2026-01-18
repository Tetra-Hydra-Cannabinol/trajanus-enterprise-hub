# Context Management Workflow

## Overview
Strategies for managing Claude Code's context window during long sessions. Prevent context exhaustion, enable session continuity, and maintain work quality.

---

## Token Gauge Protocol

### Gauge Display (Every Response)
```
Token Gauge: 🟢 XX% remaining (green: 20-100%)
Token Gauge: 🟡 XX% remaining (yellow: 5-20%)
Token Gauge: 🔴 XX% remaining (red: <5%)
```

### Response Actions by Level

#### 🟢 Green (20-100%)
- Normal operation
- Full exploration permitted
- Can read large files
- Can spawn sub-agents

#### 🟡 Yellow (5-20%)
- Prioritize completion of current task
- Avoid reading new large files
- Summarize instead of quoting
- Consider checkpoint soon

#### 🔴 Red (<5%)
- STOP new work immediately
- Complete only critical in-progress items
- Create session summary
- Execute rewind protocol

---

## Rewind Protocol (At 5%)

### Trigger
When token gauge reaches 5% or lower.

### Immediate Actions
```
1. STOP current task (even mid-execution)
2. Create CHECKPOINT file
3. Summarize session state
4. Save to handoff location
5. Inform user of rewind
```

### Checkpoint File Template
```markdown
# SESSION CHECKPOINT - [TIMESTAMP]

## Active Task
- Task ID: TASK-XXX
- Status: [IN_PROGRESS/BLOCKED]
- Progress: [X/Y steps complete]

## Files Modified This Session
- `file1.ext` - [changes made]
- `file2.ext` - [changes made]

## Current State
[Describe exactly where work stopped]

## To Resume
1. Read this checkpoint
2. Read files: [list]
3. Continue from: [specific step]

## Context Requirements
- Must read: [critical files]
- Nice to read: [helpful files]
- Skip: [already processed]

## Trigger Phrase
"Continue TASK-XXX from checkpoint [timestamp]"
```

### Checkpoint Location
```
G:\My Drive\00 - Trajanus USA\00-Command-Center\08-EOS-Files\001 Claude EOS Output\
```

---

## Context Conservation Strategies

### Strategy 1: Summarize Don't Quote
```
WRONG: Pasting 500 lines of code into response
RIGHT: "File contains 3 main functions: init(), process(), render()"
```

### Strategy 2: Targeted Reading
```
WRONG: Read entire 3000-line file
RIGHT: Read specific sections (lines 100-200)
```

### Strategy 3: Sub-Agent Delegation
```
WRONG: Load entire codebase into main context
RIGHT: Spawn exploration agent, receive summary
```

### Strategy 4: Reference Don't Repeat
```
WRONG: Repeating specifications each response
RIGHT: "Per style_guide.md section 3..."
```

### Strategy 5: Progressive Disclosure
```
WRONG: Load all documentation upfront
RIGHT: Load only what's needed for current step
```

---

## Sub-Agent Usage

### When to Use Sub-Agents
- Code exploration (large codebase)
- Research tasks (web search, docs)
- Specialized review (security, design)
- Parallel independent tasks

### Sub-Agent Benefits
- Separate context window
- Returns summary only
- Preserves main context
- Can run in parallel

### Available Agents
```
.claude/agents/
├── design-reviewer.md     - UI validation
├── qcm-reviewer.md        - QCM compliance
├── security-auditor.md    - Code security
├── doc-generator.md       - Documentation
├── github-searcher.md     - Solution finding
├── kb-researcher.md       - Knowledge base
├── code-surgeon.md        - Precise edits
├── research-agent.md      - General research
└── [others as needed]
```

### Agent Invocation Pattern
```
1. Identify task suitable for delegation
2. Select appropriate agent
3. Provide clear, specific prompt
4. Receive summary (not full output)
5. Act on summary in main context
```

---

## Session Planning

### Estimate Before Starting
```
Small task (<100 lines): ~5-10% context
Medium task (100-500 lines): ~10-25% context
Large task (500+ lines): ~25-50% context
Exploration session: ~20-40% context
```

### Plan for Context Budget
```
Available: 100%
- Session startup/context: -10%
- Main task execution: -40%
- Testing/validation: -15%
- Documentation: -10%
- Buffer for issues: -15%
- Remaining: 10%
```

### Session Structure
```
Phase 1 (0-30%): Setup + Exploration
Phase 2 (30-70%): Execution
Phase 3 (70-90%): Validation + Documentation
Phase 4 (90-95%): Wrap-up
Phase 5 (95-100%): Emergency buffer only
```

---

## Multi-Session Work

### Handoff Document (End of Session)
```markdown
# SESSION HANDOFF - [DATE]

## Current State
[Exact state of project]

## Accomplished This Session
- [Specific change 1] - `file:line`
- [Specific change 2] - `file:line`

## Next Immediate Action
[Exact next step, no ambiguity]

## File Locations
- Modified: [list]
- Created: [list]
- Need review: [list]

## Warnings/Blockers
[Any known issues]

## Trigger for Next Session
"[Exact phrase to resume work]"
```

### Resume Protocol (Start of Session)
```
1. Read MAIN_CLAUDE_MD.md (auto-loaded)
2. Search for recent handoffs
3. Read most recent handoff
4. Understand current state
5. Resume from trigger phrase
```

---

## Emergency Procedures

### Context Exhaustion Mid-Task
```
IF context runs out during critical task:
1. DON'T try to finish
2. Save current file state
3. Document exact stopping point
4. Create minimal checkpoint
5. Inform user immediately
```

### Recovery from Bad State
```
IF previous session left broken state:
1. Read git diff to see changes
2. Identify what was incomplete
3. Decide: continue or revert
4. If revert: git checkout [file]
5. If continue: plan completion
```

### Context Poisoning
```
IF context filled with irrelevant info:
1. Don't continue reading more
2. Summarize what's known
3. Create checkpoint
4. Request session restart
5. Next session: targeted loading only
```

---

## Best Practices

### DO
- Check gauge before large operations
- Use sub-agents for exploration
- Summarize findings immediately
- Create checkpoints proactively
- Plan multi-session work upfront

### DON'T
- Read files "just in case"
- Repeat information unnecessarily
- Continue at red gauge
- Skip handoff documentation
- Assume next session has context

---

## Integration with Other Workflows

### With Planner/Developer
- CP maintains long-term context
- CC handles execution context
- Handoffs bridge sessions

### With GSD Framework
- EXPLORE may consume significant context
- Plan context budget per phase
- Checkpoint between phases if large

### With Visual Validation
- Screenshots consume context (as base64)
- Limit iterations to preserve context
- Summarize visual findings

---

## Metrics to Track

### Per Session
- Starting context level
- Tasks completed
- Context consumed per task
- Checkpoint created: Y/N
- Clean handoff: Y/N

### Patterns to Optimize
- Which operations consume most context?
- Which files are re-read unnecessarily?
- Are sub-agents being utilized?
- Are summaries replacing raw data?

---

**Last Updated:** 2026-01-17
**Version:** 1.0
