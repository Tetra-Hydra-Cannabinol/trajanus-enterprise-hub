# Research Finding #37

**Date:** 2025-12-17 08:57
**Topic:** MCP tools schema best practices
**Score:** 0.9999461

---

## 15 Best Practices for Building MCP Servers in Production

**URL:** https://thenewstack.io/15-best-practices-for-building-mcp-servers-in-production/
**Published:** Unknown date

---

## Content

Model your MCP server around a single microservice domain and expose only the capabilities that belong to that domain. Keep tools cohesive and uniquely named, with clear, JSON-schema’d inputs and outputs, so the client/LLM can disambiguate actions.

MCP’s tools design expects clearly typed, discoverable operations with accurate write schemas that include enums when possible, and thoroughly documented failure modes.

2. Prefer stateless, idempotent tool design [...] Use elicitation to fill in missing parameters or confirm risky actions, but never to harvest sensitive data. Keep prompts concise, validate responses against your tool’s schema, and fall back gracefully if the host doesn’t support elicitation yet.

This is new in the June 2025 revision of MCP and not universally supported by mainstream MCP clients, so gate it with capability checks.

5. Build for security first (OAuth 2.1, sessions, scopes) [...] 6. Adopt a “for the agent and the human” UX with structured content

Your responses must be LLM-parsable and human-readable. Use structured content with JSON schemas for the model alongside traditional content blocks for users. The June 2025 MCP specification introduced the `outputSchema` and `structuredContent` fields, which enable precise, typed outputs. Keep error messages actionable by incorporating machine-readable codes along with brief explanations.

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:13*
