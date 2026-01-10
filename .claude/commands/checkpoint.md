---
description: Save checkpoint state and validate progress
allowed-tools: Read, Write, Bash(date:*), Bash(dir:*)
---

# Checkpoint Protocol

## Purpose
Save current progress state to CHECKPOINT_STATE.json for session continuity and recovery.

## State File Location
```
G:\My Drive\00 - Trajanus USA\00-Command-Center\05-Scripts\CHECKPOINT_STATE.json
```

## Checkpoint Actions

### 1. Read Current State
First, read the existing checkpoint state file to understand current progress.

### 2. Update State
Update the following fields:
- `last_updated`: Current ISO timestamp
- `session_id`: Current session identifier if available
- `current_phase`: Current phase number (0-10 per CC_MASTER_TASK_LIST.md)
- `active_task`: Current task being worked on

### 3. Log Checkpoint Entry
Add entry to `checkpoint_log` array:
```json
{
  "timestamp": "ISO timestamp",
  "phase": "Phase number",
  "checkpoint_name": "CHECKPOINT N: description",
  "status": "PASSED | PENDING | BLOCKED",
  "notes": "Any relevant notes"
}
```

### 4. Token Estimate
Update `token_estimates`:
- Estimate remaining context percentage based on conversation length
- Color code:
  - GREEN: 20-100%
  - YELLOW: 5-20%
  - RED: under 5%

### 5. Validate Checkpoint Requirements
Per CC_MASTER_TASK_LIST.md, each checkpoint has specific requirements:

- **CHECKPOINT 0**: Baseline status documented
- **CHECKPOINT 1**: Phase 1 findings complete
- **CHECKPOINT 2**: Chat working
- **CHECKPOINT 3**: QCM full-width with branding
- **CHECKPOINT 4**: Buttons work
- **CHECKPOINT 5**: Terminal tabs work
- **CHECKPOINT 6**: Assistant works
- **CHECKPOINT 7**: Main chat with history
- **CHECKPOINT 8**: Visual appearance correct
- **CHECKPOINT 9**: File browsers functional
- **CHECKPOINT 10**: EOS complete

### 6. Report to User
Output checkpoint summary:
```
## Checkpoint Report

**Phase:** [N]
**Checkpoint:** [Name]
**Status:** [PASSED/PENDING/BLOCKED]
**Token Estimate:** [COLOR] XX% remaining

**Completed Checkpoints:**
- [List completed]

**Next Steps:**
- [What comes next]
```

## Emergency Checkpoint
If tokens are low (under 25%):
1. Save immediate checkpoint
2. Trigger EOS Protocol
3. Document handoff information

## Checkpoint File Schema

```json
{
  "version": "1.0",
  "last_updated": "ISO timestamp",
  "session_id": "string or null",
  "current_phase": 0,
  "completed_checkpoints": ["CHECKPOINT 0", "CHECKPOINT 1"],
  "token_estimates": {
    "start_tokens": null,
    "current_tokens": null,
    "estimated_remaining_percent": 100
  },
  "checkpoint_log": [
    {
      "timestamp": "ISO",
      "phase": 0,
      "checkpoint_name": "CHECKPOINT 0",
      "status": "PASSED",
      "notes": ""
    }
  ],
  "active_task": "Task ID or null",
  "notes": "Free form notes"
}
```
