# Research Finding #71

**Date:** 2025-12-17 08:57
**Topic:** Claude Agent SDK initializer agent example
**Score:** 0.9999685

---

## Effective harnesses for long-running agents - Anthropic

**URL:** https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
**Published:** Unknown date

---

## Content

We developed a two-fold solution to enable the Claude Agent SDK to work effectively across many context windows: an initializer agent that sets up the environment on the first run, and a coding agent that is tasked with making incremental progress in every session, while leaving clear artifacts for the next session. You can find code examples in the accompanying quickstart.

## The long-running agent problem [...] To address the problem of the agent one-shotting an app or prematurely considering the project complete, we prompted the initializer agent to write a comprehensive file of feature requirements expanding on the user’s initial prompt. In the claude.ai clone example, this meant over 200 features, such as “a user can open a new chat, type in a query, press enter, and see an AI response.” These features were all initially marked as “failing” so that later coding agents would have a clear outline of [...] | Problem | Initializer Agent Behavior | Coding Agent Behavior |
 --- 
| Claude declares victory on the entire project too early. | Set up a feature list file: based on the input spec, set up a structured JSON file with a list of end-to-end feature descriptions. | Read the feature list file at the beginning of a session. Choose a single feature to start working on. |

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:14*
