# Research Finding #49

**Date:** 2025-12-17 08:57
**Topic:** MCP Python implementation guide
**Score:** 0.99984026

---

## A Quick Introduction to Model Context Protocol (MCP) in Python

**URL:** https://medium.com/@adev94/a-quick-introduction-to-model-context-protocol-mcp-in-python-bee6d36334ec
**Published:** Unknown date

---

## Content

```
from mcp.server.fastmcp import FastMCPmcp = FastMCP("MCP Server")@mcp.tool()async def count_letters(word: str, letter: str) -> int: """ Count the occurrences of a letter in a word. Args: word: The word in which to count the letter. letter: The letter to count. Returns: The number of occurrences of the letter in the word. """ return word.lower().count(letter.lower())if __name__ == "__main__": mcp.run(transport="stdio")
``` [...] In this article we’ll briefly explore Model Context Protocol (MCP). We’ll define core concepts and terms around MCP. Then we’ll create a Function Call example, followed by a local MCP server. After that we’ll create an Agent, then add our local MCP server to our Agent. All of which will be implemented using Python and Anthropic’s API.

## What is MCP? [...] from mcp import ClientSession, StdioServerParameters, typesfrom mcp.client.stdio import stdio_clientasync def query_mcp_agent(user_prompt): """ Agent able to execute 'count_letters' function using MCP server. """  API_KEY = ... # Create server parameters for stdio connection server_params = StdioServerParameters( command="uv", # Executable args=[ "run", "mcp", "run", "mcp_server.py", ], ) # Client transport for stdio:  # - Spawn a process which it will communicate with over stdin/stdout async

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:14*
