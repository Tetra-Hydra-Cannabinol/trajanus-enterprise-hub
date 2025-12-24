# Research Finding #45

**Date:** 2025-12-17 08:57
**Topic:** debugging MCP server connections
**Score:** 0.99968255

---

## Use MCP servers in VS Code

**URL:** https://code.visualstudio.com/docs/copilot/customization/mcp-servers
**Published:** Unknown date

---

## Content

When VS Code encounters an issue with an MCP server, it shows an error indicator in the Chat view.

Select the error notification in the Chat view, and then select the Show Output option to view the server logs. Alternatively, run MCP: List Servers from the Command Palette, select the server, and then choose Show Output.

### Debug an MCP server

You can enable development mode for MCP servers by adding a `dev` key to the MCP server configuration. This is an object with two properties: [...] `watch`: A file glob pattern to watch for files change that will restart the MCP server.
 `debug`: Enables you to set up a debugger with the MCP server. Currently, VS Code supports debugging Node.js and Python MCP servers.

Learn more about MCP development mode in the MCP Dev Guide.

## Centrally control MCP access

Organizations can centrally manage access to MCP servers via GitHub policies. Learn more about enterprise management of MCP servers.

## Frequently asked questions [...] In addition to servers available over the network, VS Code can connect to MCP servers listening for HTTP traffic on Unix sockets or Windows named pipes by specifying the socket or pipe path in the form `unix:///path/to/server.sock` or `pipe:///pipe/named-pipe` on Windows. You can specify subpaths by using a URL fragment, such as `unix:///tmp/server.sock#/mcp/subpath`.

 Example remote server configuration

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:14*
