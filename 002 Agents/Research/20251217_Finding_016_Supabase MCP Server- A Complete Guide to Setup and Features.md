# Research Finding #16

**Date:** 2025-12-17 08:57
**Topic:** Supabase connection pooling production
**Score:** 0.999959

---

## Supabase MCP Server: A Complete Guide to Setup and Features

**URL:** https://chat2db.ai/resources/blog/supabase-mcp-server-guide
**Published:** Unknown date

---

## Content

// Example: Configuring MCP connection pooling in Supabase// Example: Configuring MCP connection pooling in Supabaseconst { createPool } = require('@supabase/pg-mcp'); const { createPool } =  require('@supabase/pg-mcp');  const pool = createPool({const  pool  =  createPool({ maxClients: 200,  maxClients:  200, idleTimeoutMillis: 30000,  idleTimeoutMillis:  30000, connectionString: process.env.DATABASE_URL,  connectionString:  process. env. DATABASE_URL, authStrategy: 'jwt' // Supports OpenID [...] ```
   # supabase-mcp.yaml# supabase-mcp.yamlconnectionPools: connectionPools: default:  default: minSize: 20  minSize:  20 maxSize: 200  maxSize:  200 maxLifetime: 1800 # seconds  maxLifetime:  1800  # seconds
   ```
2. Security Hardening:

    Enable mTLS between MCP nodes
    Rotate JWT signing keys weekly
    Restrict MCP API access via network policies

Chat2DB simplifies these tasks through its configuration advisor, which: [...] 1. Connection Pooler: Dynamically allocates database connections with configurable timeouts (default: 30s idle timeout)
2. Auth Proxy: Integrates with JWT-based authentication via PostgreSQL's Row-Level Security (opens in a new tab)
3. Query Router: Distributes read queries across replicas using weighted load balancing

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:13*
