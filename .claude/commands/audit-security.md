---
description: Audit code for security vulnerabilities and best practices
allowed-tools: Task, Read, Grep
---

# Security Audit Command

## Purpose
Invoke the security-auditor agent to review code for vulnerabilities.

## Usage
```
/audit-security [target]
```

**Examples:**
- `/audit-security` - Audit current context
- `/audit-security src/toolkits/qcm.html` - Audit specific file
- `/audit-security authentication` - Audit auth code

## Severity Ratings
- CRITICAL - Immediate risk
- HIGH - Significant flaw
- MEDIUM - Should fix
- LOW - Best practice

## Execution

Spawn the security-auditor agent:
```
@agent security-auditor Audit [target] for vulnerabilities
```
