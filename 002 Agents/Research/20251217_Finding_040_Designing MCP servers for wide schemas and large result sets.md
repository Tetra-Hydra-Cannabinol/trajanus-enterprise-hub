# Research Finding #40

**Date:** 2025-12-17 08:57
**Topic:** MCP tools schema best practices
**Score:** 0.9996567

---

## Designing MCP servers for wide schemas and large result sets

**URL:** https://axiom.co/blog/designing-mcp-servers-for-wide-events
**Published:** Unknown date

---

## Content

With any MCP best practice guide there is a lot of focus on not just wrapping REST APIs and instead thinking deeper about the use-cases and tuning the tool list for those use cases.

While that’s very relevant advice, usually somewhere behind the tool call is an API and there isn’t as much discussion on how to format responses from the tool calls to the client. We knew this was going to be an issue for us due to the reasons discussed earlier. [...] Prioritize the essentials -  We start with a priority list of common, high-value field names. Columns like `timestamp`, `service.name`, `status`, and `trace_id` get an immediate head start because they are fundamental to observability.

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:14*
