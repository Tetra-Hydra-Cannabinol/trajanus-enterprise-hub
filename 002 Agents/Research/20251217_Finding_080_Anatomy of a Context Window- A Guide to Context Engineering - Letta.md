# Research Finding #80

**Date:** 2025-12-17 08:57
**Topic:** multi-context window agent state management
**Score:** 0.512376

---

## Anatomy of a Context Window: A Guide to Context Engineering - Letta

**URL:** https://www.letta.com/blog/guide-to-context-engineering
**Published:** Unknown date

---

## Content

Traditional LLMs operate in a stateless paradigm—each interaction exists in isolation, with no knowledge carried forward from previous conversations. Agent memory solves this problem.

May 14, 2025

Memory Blocks: The Key to Agentic Context Management

Memory blocks offer an elegant abstraction for context window management. By structuring the context into discrete, functional units, we can give LLM agents more consistent, usable memory.

Feb 13, 2025

RAG is not Agent Memory [...] Combining these tools allows for management of agent context windows via the LLM. These tools can be used both by the agent itself to manage its own memory and context, or by other specialized agents (e.g. sleep-time agents which process information in the background).

### Memory Blocks

Introduced by MemGPT, memory blocks are reserved portions of the context window designed for persistent memory. Each memory block has several key properties: [...] Context management refers to both how this context window is designed (through configuration of files, blocks, tools, and prompts), as well as how this context window evolves over time. The context window can be controlled directly by the underlying system (the “LLM OS” or “AI OS”) or with agentic tool calling (which is executed by the OS).

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:15*
