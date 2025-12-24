# Research Finding #87

**Date:** 2025-12-17 08:57
**Topic:** subagent communication patterns production
**Score:** 0.99832565

---

## Best Practices for Building Agentic AI Systems: What Actually Works ...

**URL:** https://userjot.com/blog/best-practices-building-agentic-ai-systems
**Published:** Unknown date

---

## Content

Your agents need structured communication. Not “please analyze this when you get a chance.” Actual structured protocols.

Every task from primary to subagent needs:

 Clear objective (“Find all feedback mentioning ‘slow loading’”)
 Bounded context (“From the last 30 days”)
 Output specification (“Return as JSON with id, text, user fields”)
 Constraints (“Max 100 results, timeout after 5 seconds”)

Every response from subagent to primary needs: [...] Parallel execution: Run 10 subagents at once without them stepping on each other
 Predictable behavior: Same prompt always produces similar results
 Easy testing: Test each agent in isolation
 Simple caching: Cache results by prompt hash

Here’s how I structure subagent communication: [...] Each subagent runs in complete isolation while the primary agent handles all the orchestration.

## Stateless Subagents: The Most Important Rule

Every subagent call should be like calling a pure function with the same input producing the same output, no shared memory, no conversation history, no state.

This sounds limiting until you realize what it gives you:

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:15*
