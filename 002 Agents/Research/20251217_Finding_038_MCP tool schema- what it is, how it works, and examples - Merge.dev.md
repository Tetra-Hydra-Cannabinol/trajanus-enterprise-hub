# Research Finding #38

**Date:** 2025-12-17 08:57
**Topic:** MCP tools schema best practices
**Score:** 0.9997154

---

## MCP tool schema: what it is, how it works, and examples - Merge.dev

**URL:** https://www.merge.dev/blog/mcp-tool-schema
**Published:** Unknown date

---

## Content

Note: MCP tool descriptions and names are the other core elements of an MCP tool. They can help your AI agents determine the best tool to invoke, so they’re used before the agent leverages a tool’s schema.

## Examples of MCP tool schemas

Here are just a few MCP tool schemas from Merge Agent Handler’s MCP servers.

### GitHub’s tool schema for fetching issues

The project management platform for developers can use the tool schema below for its `get_issue` tool. [...] Greenhouse can help agents move candidates to different stages in the ATS platform by providing the following schema for its `move_applications` tool. [...] Putting this all together, here’s how it can be structured:

```
{ "name": "tool_name_here", "description": "Describe what this tool does and list key parameters.", "input_schema": { "type": "object", "properties": { "param1": { "type": "string", "description": "Required parameter." }, "param2": { "type": "integer", "description": "Optional parameter." } }, "required": ["param1"] } }
```

Related: What is an MCP connector?

## How to use MCP tool schema

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:13*
