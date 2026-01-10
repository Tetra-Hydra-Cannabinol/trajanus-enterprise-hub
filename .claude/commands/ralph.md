---
allowed-tools: Bash(*), Read, Write, Edit, Glob, Grep, Task, WebFetch, WebSearch
argument-hint: "<prompt> | <completion_signal> | [max_iterations]"
description: Loop prompt until completion signal found in output (default 5 iterations)
---

# RALPH - Recursive Auto-Loop Prompt Handler

**Arguments received:** `$ARGUMENTS`

## Step 1: Parse Arguments

Parse the pipe-delimited arguments:
- Format: `<prompt> | <completion_signal> | [max_iterations]`
- Default max_iterations: 5

## Step 2: Initialize State File

IMMEDIATELY run this PowerShell command to create the state file (replace values with parsed arguments):

```powershell
powershell -Command "$state = @{iteration=1; max_iterations=5; signal='COMPLETION_SIGNAL'; prompt='THE_PROMPT'} | ConvertTo-Json; $state | Out-File -FilePath \"$env:TEMP\ralph-state-$env:CLAUDE_SESSION_ID.json\" -Encoding utf8"
```

## Step 3: Execute the Task

Now execute the prompt task. Work on it thoroughly.

## Step 4: Signal Completion

When the task is complete and meets the success criteria:
- Output the exact completion signal text
- Also output: `RALPH_SIGNAL_FOUND`

If you cannot complete the task in this iteration:
- Output: `RALPH_ITERATION_COMPLETE`
- The stop hook will automatically re-trigger you

## Important Notes

1. The stop hook checks your output for the completion signal
2. If found: Session ends successfully
3. If NOT found AND iterations remain: You get re-prompted automatically
4. Max iterations prevents infinite loops

## Begin Task

Parse and execute: $ARGUMENTS
