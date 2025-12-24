# Research Finding #47

**Date:** 2025-12-17 08:57
**Topic:** MCP Python implementation guide
**Score:** 0.99992454

---

## Python MCP Server: Connect LLMs to Your Data

**URL:** https://realpython.com/python-mcp/
**Published:** Unknown date

---

## Content

To install Python MCP, create a virtual environment and run `python -m pip install "mcp[cli]"`. To confirm the install, you can optionally import `mcp` in a REPL.

You store reusable instructions as prompts, expose read-only data via resource URIs, and implement callable actions as tools. The client exposes these to the LLM so it can select resources and invoke tool functions. [...] To build a simple MCP server in Python, you create a `FastMCP` instance, decorate async tool functions with `@mcp.tool()`, and call `mcp.run(transport="stdio")` to serve them.

You open a `ClientSession` over `stdio` using `StdioServerParameters` and `stdio_client()`, then call `session.initialize()` followed by `session.list_tools()`. [...] ```
 import  asyncio from  mcp.server.fastmcp  import FastMCP from  transactional_db  import CUSTOMERS_TABLE, ORDERS_TABLE, PRODUCTS_TABLE mcp = FastMCP("ecommerce_tools") @mcp. tool() async def  get_customer_info(customer_id: str) -> str:  """Search for a customer using their unique identifier""" customer_info = CUSTOMERS_TABLE. get(customer_id) if not customer_info: return "Customer not found" return str(customer_info)
```

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:14*
