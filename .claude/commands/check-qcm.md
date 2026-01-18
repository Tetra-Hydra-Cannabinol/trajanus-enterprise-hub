---
description: Review construction submittal for USACE/federal compliance
allowed-tools: Task, Read, mcp__trajanus-kb__*
---

# QCM Review Command

## Purpose
Invoke the qcm-reviewer agent to validate submittals against USACE/federal requirements.

## Usage
```
/check-qcm [submittal-identifier]
```

**Examples:**
- `/check-qcm 00650-001` - Review specific submittal
- `/check-qcm concrete mix` - Review by description

## Review Actions
- APPROVED
- APPROVED AS NOTED
- REVISE AND RESUBMIT
- REJECTED
- FOR INFORMATION ONLY

## Execution

Spawn the qcm-reviewer agent:
```
@agent qcm-reviewer Review submittal [identifier]
```
