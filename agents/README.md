# Trajanus Sub-Agent Library

## Overview

This library contains specialized sub-agents that can be invoked for specific tasks without polluting the main Claude Code context. Each agent has a defined scope, structured input/output, and success criteria.

## Why Sub-Agents?

- **Context Isolation:** Keeps main conversation focused
- **Expertise Packaging:** Each agent is a domain expert
- **Structured Output:** Returns parseable reports, not free-form text
- **Reusability:** Same agent works across sessions
- **Reduced Token Overhead:** Only load agent context when needed

## Available Agents

| Agent | Purpose | File |
|-------|---------|------|
| QCM Review | Submittal and QC document review | `qcm-review-agent.md` |
| Security Audit | Code security vulnerability scanning | `security-audit-agent.md` |
| UI Validator | UI/UX validation via Playwright | `ui-validator-agent.md` |
| Docs Generator | Documentation generation | `docs-generator-agent.md` |
| GitHub Search | Codebase and GitHub search | `github-search-agent.md` |

## How to Invoke an Agent

### Method 1: Direct Task Tool (Recommended)

```
Use the Task tool with subagent_type and include the agent prompt:

Task(
  subagent_type: "general-purpose",
  prompt: "[Read agents/qcm-review-agent.md and execute against: {target}]"
)
```

### Method 2: Manual Invocation

1. Read the agent file: `Read agents/{agent-name}.md`
2. Follow the input format specified
3. Execute the agent's instructions
4. Return output in the specified format

## Agent Output Format

All agents return structured reports with:

```markdown
# [AGENT NAME] Report

## Summary
[One-line summary]

## Findings
| ID | Severity | Finding | Location | Recommendation |
|----|----------|---------|----------|----------------|
| 1  | HIGH/MED/LOW | Description | file:line | Fix suggestion |

## Metrics
- Items Reviewed: X
- Issues Found: X
- Pass Rate: X%

## Status
[PASS/FAIL/WARNING]
```

## Creating New Agents

Use this template:

```markdown
# [Agent Name]

## Purpose
[What this agent does]

## Scope
**IN SCOPE:**
- [What it handles]

**OUT OF SCOPE:**
- [What it doesn't handle]

## Input Format
[Expected input structure]

## Output Format
[Report template]

## Example Invocation
[How to call it]

## Success Criteria
[How to know it worked]
```

## Best Practices

1. **One agent per task** - Don't chain multiple agents in one call
2. **Clear scope** - If task is out of scope, return immediately
3. **Structured output** - Always use the report template
4. **Severity ratings** - Use HIGH/MEDIUM/LOW consistently
5. **Actionable findings** - Include specific fix recommendations

---

**Last Updated:** 2026-01-12
**Maintained By:** Trajanus Development Team
