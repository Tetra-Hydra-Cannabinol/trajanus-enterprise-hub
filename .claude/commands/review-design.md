---
description: Review UI design against Trajanus style guide using Playwright screenshots
allowed-tools: Task, mcp__plugin_playwright_playwright__*, Read
---

# Design Review Command

## Purpose
Invoke the design-reviewer agent to validate UI against Trajanus style specifications.

## Usage
```
/review-design [target]
```

**Examples:**
- `/review-design` - Review current visible page
- `/review-design qcm` - Review QCM workspace
- `/review-design developer` - Review Developer toolkit

## Validation Checklist

### Colors (STRICT)
- Silver: #C0C0C0
- Black: #1a1a1a
- Blue: #0066CC / #00AAFF
- NO GOLD unless explicitly approved

### Layout Standard
- 3-column layout where applicable
- "TRAJANUS USA" header
- "← Hub" navigation button
- 2px blue borders

## Execution

Spawn the design-reviewer agent:
```
@agent design-reviewer Review the [target] workspace
```
