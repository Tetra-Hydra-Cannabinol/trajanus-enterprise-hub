# Research Finding #35

**Date:** 2025-12-17 08:57
**Topic:** MCP protocol SSE server example code
**Score:** 0.99992573

---

## How to Build and Deploy an SSE MCP Server with OAuth in Rust

**URL:** https://www.shuttle.dev/blog/2025/08/13/sse-mcp-server-with-oauth-in-rust
**Published:** Unknown date

---

## Content

```
#[tool_handler] impl ServerHandler for TodoService{... async fn initialize(& self,: InitializeRequestParam,: RequestContext< RoleServer>,) -> Result< InitializeResult, McpError>{if let Some() =.. get::<axum::http::request:::::::: Parts>(){if let Some() =.. get::< String>(){let mut = self.. lock(). await; = Some(. clone());} else{tracing::::warn!("No client_id found in HTTP request extensions");}} Ok(self. get_info())}}
``` [...] ```
let = SseServerConfig{:,:"/mcp/sse". to_string(),:"/mcp/message". to_string(),: CancellationToken:: new(),: Some(Duration:: from_secs(15)),};
```

Using this configuration, we've specified the MCP server to run on `

### Setting Up the Metadata Endpoint [...] So far, we've defined our `MCP` service `struct`, implemented the `ServerHandler` trait, and used the `#[tool_router]` macro to register our tools. Now, we need to integrate this service into an SSE server so it can be accessed from a URL.

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:13*
