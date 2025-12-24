# Research Finding #29

**Date:** 2025-12-17 08:57
**Topic:** build MCP server from scratch tutorial
**Score:** 0.84215075

---

## MCP server: A step-by-step guide to building from scratch

**URL:** https://composio.dev/blog/mcp-server-step-by-step-guide-to-building-from-scrtch
**Published:** Unknown date

---

## Content

1. First, we imported the `FastMCP` server from the MCP package and the `math` module. The FastMCP Server manages connections, follows the MCP protocol, and routes messages.
2. Next, we created an MCP server client and named it "Hello World".
3. Then, we added tools `@mcp.tool()` and resources using `@mcp.resource()`. These tools help the server perform operations, and the resource provides personalized greetings. (talk about exposing your data to LLM) [...] 1. First, we imported the `FastMCP` server from the MCP package and the `math` module. The FastMCP Server manages connections, follows the MCP protocol, and routes messages.
2. Next, we created an MCP server client and named it "Hello World".
3. Then, we added tools `@mcp.tool()` and resources using `@mcp.resource()`. These tools help the server perform operations, and the resource provides personalized greetings. (talk about exposing your data to LLM) [...] This process happens seamlessly, allowing Cursor to integrate with multiple services through a standardized interface.

But understanding fundamentals is no use if one can’t build, so let’s get building!

## How to Build an MCP Server

There are two ways to build an MCP Server: using the Python SDK or the JavaScript SDK. For simplicity, I will focus on the Python SDK.

So, like any other good dev, let’s create a separate work environment to isolate things.

### 1. Work Environment Setup

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:13*
