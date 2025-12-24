# Research Finding #75

**Date:** 2025-12-17 08:57
**Topic:** Claude Agent SDK initializer agent example
**Score:** 0.99983394

---

## Agent SDK reference - Python - Claude Docs

**URL:** https://platform.claude.com/docs/en/agent-sdk/python
**Published:** Unknown date

---

## Content

| Method | Description |
 --- |
| `__init__(options)` | Initialize the client with optional configuration |
| `connect(prompt)` | Connect to Claude with an optional initial prompt or message stream |
| `query(prompt, session_id)` | Send a new request in streaming mode |
| `receive_messages()` | Receive all messages from Claude as an async iterator |
| `receive_response()` | Receive messages until and including a ResultMessage | [...] ```
from claude_agent_sdk import tool from  claude_agent_sdk import  tool from typing import Any from  typing import  Any @tool("greet", "Greet a user", {"name": str}) @tool("greet", "Greet a user", {"name": str})async def greet(args: dict[str, Any]) -> dict[str, Any]: async  def  greet(args: dict[str, Any]) -> dict[str, Any]: return { return { "content": [{ "content": [{ "type": "text",  "type": "text", "text": f"Hello, {args['name']}!"  "text": f"Hello, {args['name']}!" }] }] } }
``` [...] import asyncio import  asynciofrom claude_agent_sdk import ClaudeSDKClient, AssistantMessage, TextBlock, ResultMessage from  claude_agent_sdk import ClaudeSDKClient, AssistantMessage, TextBlock, ResultMessage async def main(): async  def  main(): async with ClaudeSDKClient() as client:  async  with ClaudeSDKClient() as client:  # First question  # First question await client.query("What's the capital of France?")  await client.query("What's the capital of France?")  # Process response  #

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:14*
