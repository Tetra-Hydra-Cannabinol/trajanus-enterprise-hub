---
description: Generate technical documentation from code
allowed-tools: Task, Read, Grep, Write
---

# Documentation Generator Command

## Purpose
Invoke the doc-generator agent to create technical documentation.

## Usage
```
/generate-docs [type] [target]
```

**Types:**
- `readme` - Project README
- `api` - API documentation
- `user-guide` - User guide
- `functions` - Function docs

**Examples:**
- `/generate-docs readme`
- `/generate-docs api kb-endpoints`
- `/generate-docs functions qcm.html`

## Execution

Spawn the doc-generator agent:
```
@agent doc-generator Generate [type] documentation for [target]
```
