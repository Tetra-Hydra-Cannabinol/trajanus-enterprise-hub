# Research Finding #74

**Date:** 2025-12-17 08:57
**Topic:** Claude Agent SDK initializer agent example
**Score:** 0.9998795

---

## Agent SDK overview - Claude Docs

**URL:** https://platform.claude.com/docs/en/agent-sdk/overview
**Published:** Unknown date

---

## Content

async def main():
    async for message in query(
        prompt="What files are in this directory?",
        options=ClaudeAgentOptions(allowed_tools=["Bash", "Glob"])
    ):
        print(message)

asyncio.run(main())
```    

Ready to build? Follow the Quickstart to create an agent that finds and fixes bugs in minutes.

Compare the Agent SDK to other Claude tools

The Claude platform offers multiple ways to build with Claude. Here's how the Agent SDK fits in:

Agent SDK vs Client SDK [...] Unless previously approved, we do not allow third party developers to offer Claude.ai login or rate limits for their products, including agents built on the Claude Agent SDK. Please use the API key authentication methods described in this document instead.

4.   4 
Run your first agent  This example creates an agent that lists files in your current directory using built-in tools.

Python      ```
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions [...] async def main():
    async for message in query(
        prompt="Find and fix the bug in auth.py",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Edit", "Bash"])
    ):
        print(message)  # Claude reads the file, finds the bug, edits it

asyncio.run(main())
```

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:14*
