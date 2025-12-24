# Research Finding #46

**Date:** 2025-12-17 08:57
**Topic:** MCP Python implementation guide
**Score:** 0.99996173

---

## How to Build an MCP Server in Python: A Complete Guide - Scrapfly

**URL:** https://scrapfly.io/blog/posts/how-to-build-an-mcp-server-in-python-a-complete-guide
**Published:** Unknown date

---

## Content

This guide covered how to build an MCP server in Python using a calculator app as a clear, hands-on example. We explored the core components of the Model Context Protocol: tools, resources, and prompts, and how each one allows large language models to interact dynamically with your code. You learned how to implement basic and advanced tools including asynchronous functions, handle user input with custom prompts, and expose data through both static and dynamic resources. [...] ```
 @mcp. resource("usage://guide") def  get_usage() -> str: with open("docs/usage.txt") as f: return f. read()
```

This returns the content of the file when requested by the model.

## Creating Prompts

In MCP, prompts can also be defined using functions decorated with `@mcp.prompt()`. This allows for dynamic, conditional, and reusable prompt generation.

Here’s an example that combines all four operations into a single prompt function: [...] ```
 from  mcp.server.fastmcp  import FastMCP# Import FastMCP, the quickstart server base mcp = FastMCP("Calculator Server") # Initialize an MCP server instance with a descriptive name @mcp. tool() # Register a function as a callable tool for the model def  add(a: int, b: int) -> int:  """Add two numbers and return the result.""" return a + b # Simple arithmetic logic if __name__ == "__main__": mcp. run(transport = "stdio")# Run the server, using standard input/output for communication
```

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:14*
