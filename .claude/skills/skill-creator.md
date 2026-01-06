# Skill: Skill Creator

## Name
skill-creator

## Description
Meta-skill for creating new Claude Code skills. Guides through research, design, and implementation of production-quality skills following best practices.

## When to Use
- User wants to create a new skill
- User says "create a skill for...", "I need a skill that...", "build me a skill"
- Automating a repetitive workflow
- Standardizing a process across sessions

## Core Principle
**"Make AI think like an expert, not follow steps"**

Skills should encode expertise and judgment, not just procedures.

## 10-Step Skill Creation Process

### Phase 1: Discovery

**Step 1: Understand**
```
- What problem does this skill solve?
- Who uses it? (User persona)
- What's the expected input?
- What's the expected output?
- How often will it be used?
```

**Step 2: Explore**
```
- Test Claude WITHOUT the skill first
- Identify where Claude fails or deviates
- Note what guidance would have helped
- Find edge cases and failure modes
```

**Step 3: Research**
```
- Search KB for related knowledge
- Find industry best practices
- Look for existing patterns in codebase
- Gather reference materials
```

### Phase 2: Design

**Step 4: Synthesize**
```
- Extract principles from research
- Identify decision points
- Define quality criteria
- List required context/data
```

**Step 5: Draft**
```
Write initial skill.md with:
- Clear trigger conditions (When to Use)
- Step-by-step procedure
- Example inputs/outputs
- Quality checklist
```

### Phase 3: Refinement

**Step 6: Self-Critique**
```
Review against:
- Is each section earning its place?
- Does it sound like a practitioner?
- Are constraints ruthless enough?
- Will it produce output, not documents?
```

**Step 7: Iterate**
```
- Fix gaps identified in critique
- Get user feedback on draft
- Simplify where possible
- Remove redundant instructions
```

### Phase 4: Validation

**Step 8: Test**
```
- Run skill on real scenario
- Verify output quality
- Check for edge cases
- Confirm trigger detection works
```

**Step 9: Finalize**
```
- Codify into optimal structure
- Add to skills directory
- Commit to git with description
- Update CLAUDE.md if needed
```

**Step 10: Document**
```
- Add to CUSTOM COMMANDS table if slash command
- Note any MCP dependencies
- Record any data sources needed
```

## Skill File Structure

```
.claude/skills/[skill-name]/
├── skill.md           # Main skill definition (required)
├── examples/          # Example inputs/outputs (optional)
├── data/              # Reference data, templates (optional)
└── scripts/           # Python/bash helpers (optional)
```

Or for simple skills:
```
.claude/skills/[skill-name].md
```

## Skill.md Template

```markdown
# Skill: [Name]

## Name
[kebab-case-name]

## Description
[1-2 sentence description of what this skill does]

## When to Use
- [Trigger condition 1]
- [Trigger condition 2]
- [Key phrases that invoke this skill]

## Prerequisites
- [Required tools, APIs, or access]
- [Required context or data]

## Procedure

### Step 1: [Action]
[Detailed instructions]

### Step 2: [Action]
[Detailed instructions]

## Output Format
[Expected output structure]

## Examples

### Example 1: [Scenario]
**Input:** [Sample input]
**Output:** [Expected output]

## Quality Checklist
- [ ] [Quality criterion 1]
- [ ] [Quality criterion 2]

## Common Errors
- **Error:** [What goes wrong]
  **Fix:** [How to fix it]
```

## Procedure

### When User Requests New Skill

1. **Gather Requirements**
   Ask:
   - What task should this skill automate?
   - What does success look like?
   - What context does it need?
   - Any existing patterns to follow?

2. **Research Phase**
   - Search Trajanus KB for related knowledge
   - Check existing skills for patterns
   - Identify best practices

3. **Present Draft**
   Show user:
   - Proposed skill structure
   - Key decision points
   - Any assumptions made

4. **Implement**
   - Create skill.md file
   - Add supporting files if needed
   - Test with sample input

5. **Version Control**
   ```bash
   git add .claude/skills/[skill-name].md
   git commit -m "Add [skill-name] skill: [description]"
   ```

6. **Update References**
   - Add to CLAUDE.md CUSTOM COMMANDS if slash command
   - Note in session for future reference

## Quality Criteria for Skills

### Must Have
- [ ] Clear trigger conditions
- [ ] Actionable procedure
- [ ] Expected output defined
- [ ] Can be tested

### Should Have
- [ ] Examples with expected output
- [ ] Error handling guidance
- [ ] Quality checklist

### Nice to Have
- [ ] Supporting data/templates
- [ ] Integration with other skills
- [ ] Automated testing

## Anti-Patterns to Avoid

1. **Too Generic** - Skill should be specific enough to be useful
2. **Too Rigid** - Allow for judgment and adaptation
3. **Documentation Heavy** - Produce output, not intermediate docs
4. **Missing Context** - Include what AI needs to know
5. **Untested** - Always validate before finalizing

## Output Location
```
G:\My Drive\00 - Trajanus USA\00-Command-Center\.claude\skills\
```

## After Creation
- Commit to git for version tracking
- Test in real scenario
- Iterate based on results
