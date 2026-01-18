---
description: Search GitHub for code examples and solutions
allowed-tools: Task, WebSearch, WebFetch
---

# GitHub Search Command

## Purpose
Invoke the github-searcher agent to find relevant code examples and solutions.

## Usage
```
/search-github [query]
```

**Examples:**
- `/search-github Tauri IPC examples`
- `/search-github Supabase vector search`
- `/search-github fix: Cannot read property undefined`

## Quality Filters
- Stars > 100 for libraries
- Recent activity (within 1 year)
- Good documentation

## Execution

Spawn the github-searcher agent:
```
@agent github-searcher Find [query]
```
