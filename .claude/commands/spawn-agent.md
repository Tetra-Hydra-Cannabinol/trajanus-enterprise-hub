---
description: Spawn an isolated subagent for specific task execution
argument-hint: "<agent-type> | <task-description>"
allowed-tools: Task, Read, Write
---

# Spawn Agent Command

Launches an isolated subagent to execute a specific task.

## Arguments

Format: `<agent-type> | <task-description>`

### Available Agent Types

| Agent | Type | Purpose |
|-------|------|---------|
| playwright-verifier | Explore | UI verification, screenshots, navigation testing |
| code-surgeon | general-purpose | Precise, surgical code modifications |
| knowledge-retriever | Explore | Supabase KB queries and research |
| eos-protocol-agent | general-purpose | End of Session documentation |
| ai-memory-research-specialist | general-purpose | AI memory/RAG research |
| electron-fullstack-architect | general-purpose | Complex coding tasks |

## Spawn Protocol

### Step 1: Parse Arguments
- Extract agent type from first segment
- Extract task description from second segment

### Step 2: Validate Agent Type
Confirm agent type matches one of:
- playwright-verifier
- code-surgeon
- knowledge-retriever
- eos-protocol-agent
- ai-memory-research-specialist
- electron-fullstack-architect

### Step 3: Read Agent Definition
Read the agent's .md file from `.claude/agents/` to get:
- Description
- Model preference
- Capabilities

### Step 4: Spawn Agent
Use the Task tool with:
- `subagent_type`: Map to appropriate type
- `prompt`: Include task description and agent instructions
- `model`: Use agent's preferred model (or inherit)

### Step 5: Report Spawn
Output:
```
## Agent Spawned

**Agent:** [name]
**Task:** [description]
**Model:** [model]

Awaiting agent completion...
```

## Agent Type Mapping

| Agent Definition | subagent_type |
|-----------------|---------------|
| playwright-verifier | Explore |
| code-surgeon | general-purpose |
| knowledge-retriever | Explore |
| eos-protocol-agent | general-purpose |
| ai-memory-research-specialist | general-purpose |
| electron-fullstack-architect | general-purpose |

## Hub-and-Spoke Integration

When spawning agents:
1. Write task to CURRENT_TASK.md (if complex)
2. Agent executes task
3. Agent writes results to TASK_REPORT.md
4. Hub reads report and validates

## Example Usage

```
/spawn-agent playwright-verifier | Verify QCM workspace displays correctly with 3 panels
```

```
/spawn-agent code-surgeon | Fix the CSS color from brown to silver on line 45 of main.css
```

```
/spawn-agent knowledge-retriever | Find all YouTube content about CLAUDE.md best practices
```

## Isolation Rules

1. Each agent operates independently
2. Agents only access their defined tools
3. Hub coordinates all inter-agent communication
4. Agents report back via TASK_REPORT.md
5. Hub validates all agent outputs

## Error Handling

If agent fails:
1. Capture error message
2. Report failure to Hub
3. Hub decides: retry, skip, or escalate
