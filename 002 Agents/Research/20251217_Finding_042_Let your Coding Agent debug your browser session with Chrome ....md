# Research Finding #42

**Date:** 2025-12-17 08:57
**Topic:** debugging MCP server connections
**Score:** 0.9997981

---

## Let your Coding Agent debug your browser session with Chrome ...

**URL:** https://developer.chrome.com/blog/chrome-devtools-mcp-debug-your-browser-session
**Published:** Unknown date

---

## Content

We've added a new feature to Chrome M145 (currently in Canary) that allows the Chrome DevTools MCP server to request a remote debugging connection. This new flow builds on top of the existing remote debugging capabilities of Chrome. By default, remote debugging connections are disabled in Chrome. Developers have to explicitly enable the feature first by going to `chrome://inspect#remote-debugging`. [...] ### Step 2: Configure Chrome DevTools MCP server to automatically connect to a running Chrome Instance

To connect the `chrome-devtools-mcp` server to the running Chrome instance, use `--autoConnect` command line argument for the MCP server set.

The following code snippet is an example configuration for gemini-cli:

```
{ "mcpServers":  { "chrome-devtools":  { "command":  "npx",  "args":  [ "chrome-devtools-mcp@latest",  "--autoConnect",  "--channel=canary"  ]  }  }}
``` [...] ## Get started

To use the new remote debugging capabilities. You have to first enable remote debugging in Chrome and then configure the Chrome DevTools MCP server to use the new auto connection feature.

### Step 1: Set up remote debugging in Chrome

In Chrome, do the following to set up remote debugging:

1. Navigate to `chrome://inspect/#remote-debugging` to enable remote debugging.
2. Follow the dialog UI to allow or disallow incoming debugging connections.

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:14*
