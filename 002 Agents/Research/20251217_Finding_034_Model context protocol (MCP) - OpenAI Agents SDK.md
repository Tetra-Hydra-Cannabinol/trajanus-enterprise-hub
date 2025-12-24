# Research Finding #34

**Date:** 2025-12-17 08:57
**Topic:** MCP protocol SSE server example code
**Score:** 0.99995935

---

## Model context protocol (MCP) - OpenAI Agents SDK

**URL:** https://openai.github.io/openai-agents-python/mcp/
**Published:** Unknown date

---

## Content

If the MCP server implements the HTTP with SSE transport, instantiate `MCPServerSse`. Apart from the transport, the API is identical to the Streamable HTTP server. [...] from agents import Agent, Runner from  agents  import Agent, Runnerfrom agents.model_settings import ModelSettings from  agents.model_settings  import ModelSettingsfrom agents.mcp import MCPServerSse from  agents.mcp  import MCPServerSse  workspace_id = "demo-workspace" workspace_id ="demo-workspace"  async with MCPServerSse( async with MCPServerSse( name="SSE Python Server", name = "SSE Python Server", params={ params ={ "url": " "url":" "headers": {"X-Workspace": workspace_id}, [...] 1. Calls to the MCP server to list tools.
2. MCP-related information on tool calls.

## Further reading

 Model Context Protocol – the specification and design guides.
 examples/mcp – runnable stdio, SSE, and Streamable HTTP samples.
 examples/hosted\_mcp – complete hosted MCP demonstrations including approvals and connectors.

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:13*
