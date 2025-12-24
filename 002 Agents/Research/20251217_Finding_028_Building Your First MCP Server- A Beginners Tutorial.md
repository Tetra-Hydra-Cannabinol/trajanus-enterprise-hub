# Research Finding #28

**Date:** 2025-12-17 08:57
**Topic:** build MCP server from scratch tutorial
**Score:** 0.84277284

---

## Building Your First MCP Server: A Beginners Tutorial

**URL:** https://dev.to/debs_obrien/building-your-first-mcp-server-a-beginners-tutorial-5fag
**Published:** Unknown date

---

## Content

## Conclusion

🎉 Congratulations! You've successfully built your first MCP weather server!

What You've Accomplished:

 ✅ Created a functional MCP server from scratch
 ✅ Integrated real-time weather data from an external API
 ✅ Connected it to VS Code and GitHub Copilot
 ✅ Learned the fundamentals of the Model Context Protocol

Key Takeaways: [...] ## Step 3: Building the Basic Server

Now let's create our MCP server. Open `main.ts` and let's build it step by step.

### 1. Add the Required Imports

```
import{McpServer} from "@modelcontextprotocol/sdk/server/mcp.js "; import{StdioServerTransport} from '@modelcontextprotocol/sdk/server/stdio.js '; import{z} from " zod ";
```

### 2. Create the Server Instance

```
const server = new McpServer({name: " Weather Server ", version: "1.0.0 "});
``` [...] 1. Open Command Palette: `Cmd/Ctrl + Shift + P`
2. Type: `MCP: Add Server`
3. Choose: "Local server using stdio"
4. Enter Command: `npx -y tsx main.ts`
5. Name: `my-weather-server`
6. Setup Type: Local setup

This creates a `.vscode/mcp.json` file in your project:

```
{ "inputs":  [],  "servers":  { "my-weather-server":  { "type":  "stdio",  "command":  "npx",  "args":  [ "-y",  "tsx",  "/Users/your-username/path/to/main.ts"  ]  }  }  }  
```

### Start and Test

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:13*
