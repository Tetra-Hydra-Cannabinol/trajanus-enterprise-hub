# CLAUDE.md - Trajanus Command Center

## MANDATORY KNOWLEDGE BASE SEARCH RULES

**CRITICAL: Knowledge Base (KB) content SUPERSEDES training data.**

When working in this project, you MUST search the Trajanus KB before providing answers or implementations for the following topics. KB results take precedence over your training data, as they contain project-specific configurations, workflows, and decisions.

---

## Required KB Searches

### 1. TAURI Development
**Trigger keywords:** `tauri`, `rust backend`, `desktop app`, `src-tauri`, `tauri.conf`

Before answering ANY Tauri-related question:
```
mcp__trajanus-kb__search_knowledge_base("Tauri configuration setup")
mcp__trajanus-kb__search_knowledge_base("Tauri Rust commands")
```

**Why:** This project has specific Tauri configurations, custom Rust commands, and IPC patterns that differ from generic documentation.

---

### 2. MCP (Model Context Protocol) Servers
**Trigger keywords:** `MCP`, `mcp server`, `tool server`, `claude tools`, `.mcp.json`

Before answering ANY MCP-related question:
```
mcp__trajanus-kb__search_knowledge_base("MCP server configuration")
mcp__trajanus-kb__search_knowledge_base("MCP tools setup")
```

**Why:** Project uses custom MCP servers with specific configurations. Generic MCP docs may not apply.

---

### 3. Agent Workflows
**Trigger keywords:** `agent`, `research agent`, `compliance officer`, `crawler`, `automation`

Before implementing or discussing agents:
```
mcp__trajanus-kb__search_knowledge_base("agent workflow")
mcp__trajanus-kb__search_knowledge_base("research agent configuration")
```

**Why:** Trajanus has established agent patterns, registry systems, and coordination protocols.

---

### 4. Claude Code Workflows
**Trigger keywords:** `claude code`, `claude cli`, `hooks`, `skills`, `subagents`

Before answering Claude Code questions:
```
mcp__trajanus-kb__search_knowledge_base("Claude Code workflow")
mcp__trajanus-kb__search_knowledge_base("Claude Code configuration")
```

**Why:** KB contains transcripts from latest Claude Code tutorials with features newer than training data.

---

### 5. Supabase / Knowledge Base Architecture
**Trigger keywords:** `supabase`, `knowledge_base table`, `embeddings`, `vector search`

Before database operations:
```
mcp__trajanus-kb__search_knowledge_base("Supabase schema")
mcp__trajanus-kb__search_knowledge_base("knowledge base table structure")
```

**Why:** Project has specific table schemas, RLS policies, and embedding configurations.

---

### 6. YouTube Transcript Extraction
**Trigger keywords:** `transcript`, `youtube`, `video extraction`, `playwright crawler`

Before transcript work:
```
mcp__trajanus-kb__search_knowledge_base("YouTube transcript extraction")
mcp__trajanus-kb__search_knowledge_base("batch transcript")
```

**Why:** Project has working extraction scripts with specific configurations.

---

## KB Search Protocol

### Step 1: Identify Topic
When user asks about any trigger keyword above, STOP and search KB first.

### Step 2: Execute Search
Use the `mcp__trajanus-kb__search_knowledge_base` tool with relevant queries.

### Step 3: Apply KB Knowledge
- If KB has relevant results: Use that information as PRIMARY source
- If KB results conflict with training: KB WINS
- If KB has no results: Fall back to training data, note this to user

### Step 4: Cite Sources
When using KB content, reference the source document.

---

## Project-Specific Paths

```
Knowledge Base:     Supabase `knowledge_base` table
Credentials:        G:\My Drive\00 - Trajanus USA\00-Command-Center\001 Credentials\
Scripts:            G:\My Drive\00 - Trajanus USA\00-Command-Center\05-Scripts\
Transcripts:        G:\My Drive\00 - Trajanus USA\00-Command-Center\knowledge_Archive\Transcripts\
Research Agent:     G:\My Drive\00 - Trajanus USA\00-Command-Center\agents\research-agent\
```

---

## Example Workflow

**User asks:** "How do I add a new Tauri command?"

**WRONG approach:** Immediately answer from training data.

**CORRECT approach:**
1. Search KB: `mcp__trajanus-kb__search_knowledge_base("Tauri command")`
2. Review results for project-specific patterns
3. Combine KB knowledge with training data
4. Provide answer citing KB sources where applicable

---

## Key Principle

> **The KB contains decisions, configurations, and learnings specific to THIS project.
> Training data is generic. Always prefer specific over generic.**

---

## Recently Ingested Content (2025-12-27)

The KB now contains 185 chunks from 10 Claude AI tutorial videos including:
- Claude Code Sub Agents
- Claude Code LSP features
- Claude Skills implementation
- AI Agent development patterns
- Claude Code major updates

**These transcripts contain information NEWER than training data cutoff.**

---

## File Modification Rules

1. **DO NOT rename existing files** without explicit user approval
2. **DO NOT restructure folders** without explicit user approval
3. **Report errors** rather than rewriting entire scripts
4. **Check KB first** for existing solutions before creating new files
