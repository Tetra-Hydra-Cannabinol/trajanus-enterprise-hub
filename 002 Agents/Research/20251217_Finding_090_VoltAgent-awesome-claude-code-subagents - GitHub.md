# Research Finding #90

**Date:** 2025-12-17 08:57
**Topic:** subagent communication patterns production
**Score:** 0.9953904

---

## VoltAgent/awesome-claude-code-subagents - GitHub

**URL:** https://github.com/VoltAgent/awesome-claude-code-subagents
**Published:** Unknown date

---

## Content

```
namesubagent-name description When this agent should be invoked toolsRead, Write, Edit, Bash, Glob, GrepYou are a [role description and expertise areas]...[Agent-specific checklists, patterns, and guidelines]... ## Communication Protocol #Inter-agent communication specifications... ## Development Workflow #Structured implementation phases...
```

### Tool Assignment Philosophy

Each subagent's `tools` field specifies Claude Code built-in tools, optimized for their role: [...] Note: When naming conflicts occur, project-specific subagents override global ones.

## 🛠️ How to Use Subagents

### Setting Up in Claude Code

1. Place subagent files in `.claude/agents/` within your project
2. Claude Code automatically detects and loads the subagents
3. Invoke them naturally in conversation or let Claude decide when to use them

### Creating New Subagents - Step by Step

Step 1: Launch the Agent Interface

```
/agents
```

Step 2: Choose "Create New Agent" [...] Production-ready: Tested in real-world scenarios
 Best practices compliant: Following industry standards and patterns
 Optimized tool access: Each agent has role-specific tool permissions
 Continuously maintained: Regular updates with new capabilities
 Community-driven: Open to contributions and improvements

## Quick Start

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:15*
