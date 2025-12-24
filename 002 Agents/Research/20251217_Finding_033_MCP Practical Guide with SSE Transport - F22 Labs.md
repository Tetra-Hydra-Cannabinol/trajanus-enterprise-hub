# Research Finding #33

**Date:** 2025-12-17 08:57
**Topic:** MCP protocol SSE server example code
**Score:** 0.99998164

---

## MCP Practical Guide with SSE Transport - F22 Labs

**URL:** https://www.f22labs.com/blogs/mcp-practical-guide-with-sse-transport/
**Published:** Unknown date

---

## Content

```
from mcp.server.fastmcp import FastMCP import requests import os from dotenv import load_dotenv load_dotenv() mcp = FastMCP() 
```

 FastMCP: Initialises the MCP server.
 dotenv: Loads API keys from the .env file.

Implementing MCP with SSE Transport

Learn how SSE transport enables real-time streaming between tools and LLMs under MCP protocol.

Murtuza Kutub

Co-Founder, F22 Labs

Walk away with actionable insights on AI adoption.

Limited seats available!

Saturday, 6 Dec 2025 [...] Takes user queries and fetches search results from the Serper API.
 Handles API errors gracefully and returns structured results.

### 3. Basic Arithmetic Tool

```
@mcp.tool() def add(a: int, b: int) -> int: """Add two numbers""" print(f"Adding {a} and {b}") return a + b 
```

 Simple function to demonstrate adding tools to MCP.

### 4. Running the MCP Server with sse transport

 SSE transport enables server-to-client streaming with HTTP POST requests for client-to-server communication. [...] ```
async def connect_to_server(self, url: str): """Connect to an MCP SSE server""" streams = await self.exit_stack.enter_async_context(sse_client(url=url)) self.session = await self.exit_stack.enter_async_context(ClientSession(streams)) await self.session.initialize() response = await self.session.list_tools() tools = response.tools print("\nConnected to server with tools:", [tool.name for tool in tools] 
```

 Establishes connection and retrieves available tools.

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:13*
