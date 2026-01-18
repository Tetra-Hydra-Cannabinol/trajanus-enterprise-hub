# Quick Start Guide - Claude Code Developer

## Session Startup

### 1. Read Context Files
```
Auto-loaded: CLAUDE.md (project instructions)
Optional: .claude/context/ files for deeper context
```

### 2. Check Current State
- Read `PLAN.md` for active tasks
- Read `CHANGELOG.md` for recent decisions
- Check workspace `.claude.md` for specific context

### 3. Understand Protocols

**Sacred Files (NEVER edit directly):**
- `src/index.html`
- `src-tauri/src/lib.rs`

**Edit Workflow:**
```
1. Copy to versioned file: index_v2.1_FEATURE.html
2. Edit the copy
3. Test thoroughly
4. Replace original only after validation
```

---

## Common Tasks

### UI Change
1. Read target file
2. Use surgical edit (specific lines)
3. Test: `npm run dev`
4. Screenshot: Use Playwright MCP
5. Validate against style guide

### Add New Feature
1. Use GSD Framework (see workflows/)
2. EXPLORE → PLAN → EXECUTE → VALIDATE
3. Test each step
4. Document in CHANGELOG.md

### Fix Bug
1. Locate issue (search codebase)
2. Understand context (read surrounding code)
3. Make minimal fix
4. Test fix
5. Verify no regression

---

## Tools Available

### Sub-Agents
Spawn with Task tool or `/spawn-agent`:
- `design-reviewer` - UI validation
- `security-auditor` - Code review
- `knowledge-retriever` - KB search

### Commands
- `/eos` - End of Session
- `/checkpoint` - Save progress
- `/verify` - Playwright validation

### Playwright MCP
```javascript
browser_navigate({ url: 'http://localhost:1420' })
browser_take_screenshot({ filename: 'test.png' })
browser_snapshot({}) // Accessibility tree
```

---

## Checklist Before Completing Task

- [ ] Changes made surgically (not full rewrites)
- [ ] Tested with `npm run dev`
- [ ] No console errors
- [ ] Screenshot captured (if UI change)
- [ ] Matches style guide
- [ ] Documented in CHANGELOG.md (if significant)

---

## When Stuck

1. Search `.claude.md` files for guidance
2. Check CHANGELOG.md for similar past issues
3. Use knowledge-retriever agent
4. Ask for clarification (don't assume)

---

## Token Management

### Monitor Gauge
```
🟢 Green (20-100%): Normal operation
🟡 Yellow (5-20%): Wrap up current task
🔴 Red (<5%): STOP - execute rewind protocol
```

### At 5% Remaining
1. Create checkpoint file
2. Document exact state
3. Save to EOS output folder
4. Report to user

---

**Remember:** Surgical edits only. Test everything. Backup before major changes.
