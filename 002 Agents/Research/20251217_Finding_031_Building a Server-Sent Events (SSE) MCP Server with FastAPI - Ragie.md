# Research Finding #31

**Date:** 2025-12-17 08:57
**Topic:** MCP protocol SSE server example code
**Score:** 0.99998987

---

## Building a Server-Sent Events (SSE) MCP Server with FastAPI - Ragie

**URL:** https://www.ragie.ai/blog/building-a-server-sent-events-sse-mcp-server-with-fastapi
**Published:** Unknown date

---

## Content

from  fastapi import  FastAPI  from app.sse import  create_sse_server  from mcp.server.fastmcp import  FastMCP mcp = FastMCP("Echo")  # Mount the Starlette SSE server onto the FastAPI app  app.mount("/", create_sse_server(mcp)) @app.get("/")   def  read_root():   return {"Hello": "World"}  # Add MCP functionality with decorators  @mcp.resource("echo://{message}")   def  echo_resource(message: str) -> str:   """Echo a message as a resource"""   return  f"Resource echo: {message} "  @mcp.tool() [...] from mcp.server.fastmcp import  FastMCP  from mcp.server.sse import  SseServerTransport  from starlette.applications import  Starlette  from starlette.routing import Mount, Route  def  create_sse_server(mcp: FastMCP):   """Create a Starlette app that handles SSE connections and message handling"""   transport = SseServerTransport("/messages/")  # Define handler functions   async  def  handle_sse(request):   async  with transport.connect_sse(  ) as streams:  await mcp._mcp_server.run(  streams, [...] Here's an example of what interacting with the MCP server might look like in Cursor after we've added our echo tool:

## Handling Authentication

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:13*
