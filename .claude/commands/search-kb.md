---
description: Search Trajanus knowledge base for protocols and documentation
allowed-tools: Task, mcp__trajanus-kb__*, mcp__plugin_supabase_supabase__execute_sql
---

# Knowledge Base Search Command

## Purpose
Search the Supabase knowledge base for protocols, documentation, and YouTube transcript insights.

## Usage
```
/search-kb [query]
```

**Examples:**
- `/search-kb GSD framework`
- `/search-kb Planner Developer workflow`
- `/search-kb Sacred File Protocol`

## KB Contents
- Protocol documents (CLAUDE.md, Bills_POV)
- YouTube transcripts (286+ chunks)
- Session history and decisions

## Execution

Spawn the knowledge-retriever agent:
```
@agent knowledge-retriever Search KB for [query]
```

Or use MCP directly:
```
mcp__trajanus-kb__search_knowledge_base query="[term]"
```
