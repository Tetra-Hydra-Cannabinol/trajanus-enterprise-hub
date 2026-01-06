# Skill: Reflect (Session Learning Capture)

## Name
reflect

## Description
Analyze the current session for corrections, patterns, and preferences. Extract high-confidence learnings and append them to CLAUDE.md for persistent memory.

## When to Use
- User invokes `/reflect` manually
- At end of session (integrated with EOS protocol)
- After significant corrections or decisions

## What to Analyze

### 1. Explicit Corrections (HIGH confidence)
Look for phrases like:
- "No, actually..."
- "Don't do that"
- "Use X instead of Y"
- "That's wrong, it should be..."
- "I already told you..."
- "The correct way is..."
- "Stop doing X"
- "Always use..."
- "Never use..."

### 2. Approval Signals (HIGH confidence)
- "Perfect"
- "That's exactly right"
- "Yes, keep doing that"
- "Good approach"
- Acceptance without correction

### 3. Pattern Observations (MEDIUM confidence)
- Repeated successful workflows
- User preferences for output format
- File organization patterns
- Naming conventions used

### 4. Technical Decisions (MEDIUM-HIGH confidence)
- Stack/tooling choices
- File locations established
- API integrations configured
- Build processes defined

## Confidence Levels

| Level | Criteria | Action |
|-------|----------|--------|
| HIGH | Explicit correction, direct instruction, repeated pattern (3+) | Auto-add to CLAUDE.md |
| MEDIUM | Single successful pattern, implicit preference | Report for user review |
| LOW | Observation, uncertain pattern | Note for later |

## Procedure

### Step 1: Scan Session
Analyze the conversation for:
```
- User corrections (negative feedback)
- User approvals (positive feedback)
- Repeated patterns
- Technical decisions
- Process deviations that were corrected
```

### Step 2: Categorize Findings
Group by type:
- **Workflow Preferences**: How user wants tasks done
- **Technical Decisions**: Stack, tools, file locations
- **Communication Preferences**: Response format, verbosity
- **Process Corrections**: Mistakes to not repeat

### Step 3: Format HIGH Confidence Items
```markdown
### [Category]
- [YYYY-MM-DD] [Learning statement]
```

### Step 4: Present Findings
```
## REFLECT ANALYSIS

### HIGH Confidence (Will add to CLAUDE.md)
1. [Learning] - Source: [Quote or context]

### MEDIUM Confidence (Review these)
1. [Observation] - Source: [Context]

### LOW Confidence (Noted)
1. [Pattern observed]

Proceed with adding HIGH confidence items? (y/n)
```

### Step 5: Update CLAUDE.md
If approved, append to `LEARNED PATTERNS` section:
- Add dated entries under appropriate category
- Keep entries concise and actionable
- No duplicate entries

## Output Location
Learnings append to:
```
G:\My Drive\00 - Trajanus USA\00-Command-Center\CLAUDE.md
```
Under section: `## LEARNED PATTERNS (Auto-Updated by /reflect)`

## Example Session Analysis

**Session Context:** User asked to extract YouTube transcripts, Claude deviated from standard process.

**User Correction:** "there is a standard process for this. we've done it dozens of times... why are you deviating from the process already created?"

**Extracted Learning (HIGH):**
```markdown
### Workflow Preferences
- [2026-01-06] YouTube transcripts: Always use established pipeline (batch_ingest_files.py), don't create custom approaches
```

**Pattern Observation (MEDIUM):**
```markdown
### Process Corrections
- [2026-01-06] Check scripts folder and KB for existing solutions before building new ones
```

## Quality Criteria
- [ ] Each learning is actionable
- [ ] Source/context is traceable
- [ ] No vague or generic statements
- [ ] Dated for tracking
- [ ] Categorized correctly

## Integration with EOS
When running EOS protocol, Step 7 prompts:
```
Run /reflect to capture session learnings? (y/n)
```
If yes, execute this skill before finalizing session.
