# Research Finding #32

**Date:** 2025-12-17 08:57
**Topic:** MCP protocol SSE server example code
**Score:** 0.99998343

---

## Build a Model Context Protocol (MCP) server in C# - .NET Blog

**URL:** https://devblogs.microsoft.com/dotnet/build-a-model-context-protocol-mcp-server-in-csharp/
**Published:** Unknown date

---

## Content

SSE transport enables server-to-client streaming with HTTP POST requests for client-to-server communication. With the MCP C# SDK, implementing SSE in your MCP server is straightforward. The SDK supports configuring server transports to handle streaming data efficiently to connected clients. You can see an implementation of an SSE MonkeyMCP server on GitHub and on the MCP C# SDK samples. You can go a step further and look at remote MCP servers with the new Azure Functions support. [...] With this minimal code, our MCP server is ready for testing! If you haven’t tried out MCP support in VS Code, check out this video for a guided tour. To run our project locally, we just need to add a new server in our mcp.json file in your .vscode folder or your user settings:

```
{ "inputs": [], "servers": { "MyFirstMCP": { "type": "stdio", "command": "dotnet", "args": [ "run", "--project", "D:\\source\\MyFirstMCP\\MyFirstMCP\\MyFirstMCP.csproj" ] } } }
``` [...] ```
[McpServerToolType] public static class EchoTool { [McpServerTool, Description("Echoes the message back to the client.")] public static string Echo(string message) => $"Hello from C#: {message}"; [McpServerTool, Description("Echoes in reverse the message sent by the client.")] public static string ReverseEcho(string message) => new string(message.Reverse().ToArray()); } 
```

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:13*
