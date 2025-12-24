# Research Finding #48

**Date:** 2025-12-17 08:57
**Topic:** MCP Python implementation guide
**Score:** 0.9998859

---

## MCP server: A step-by-step guide to building from scratch - Composio

**URL:** https://composio.dev/blog/mcp-server-step-by-step-guide-to-building-from-scrtch
**Published:** Unknown date

---

## Content

We start by creating a project directory.

Navigate to your working folder and create a folder named MCP, or u can use the terminal command:

```
mkdir mcp cd mcp
```

Next, create a virtual environment using:

```
python m venv devenv
```

Now activate the environment with:

```
activates env: devenv Linux Mac: source devenv bin activate
```

Ensure you see (dotenv) in Front of the terminal cwd path.

Finally, install two libraries - MCP SDK, MCP CLI: [...] We start by creating a project directory.

Navigate to your working folder and create a folder named MCP, or u can use the terminal command:

```
mkdir mcp cd mcp
```

Next, create a virtual environment using:

```
python m venv devenv
```

Now activate the environment with:

```
activates env: devenv Linux Mac: source devenv bin activate
```

Ensure you see (dotenv) in Front of the terminal cwd path.

Finally, install two libraries - MCP SDK, MCP CLI: [...] In the MCP setup, each tool is defined using decorators (for example, `@mcp.tool()` in Python). These functions handle specific actions like calculations, lookups, or API calls. To test them, you can use a CLI or inspector client that connects to your server, lists the available tools, and allows you to run each one with test inputs. This helps confirm that your server and tool definitions are wired correctly before you move on to full IDE integration.

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:14*
