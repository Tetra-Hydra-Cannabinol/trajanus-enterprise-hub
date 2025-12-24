# Research Finding #19

**Date:** 2025-12-17 08:57
**Topic:** Supabase connection pooling production
**Score:** 0.99954176

---

## Connect to your database | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/connecting-to-postgres
**Published:** Unknown date

---

## Content

## More about connection pooling#

Connection pooling improves database performance by reusing existing connections between queries. This reduces the overhead of establishing connections and improves scalability.

You can use an application-side pooler or a server-side pooler (Supabase automatically provides one called Supavisor), depending on whether your backend is persistent or serverless.

### Application-side poolers# [...] Postgres connections are like a WebSocket. Once established, they are preserved until the client (application server) disconnects. A server might only make a single 10 ms query, but needlessly reserve its database connection for seconds or longer.

Serverside-poolers, such as Supabase's Supavisor in transaction mode, sit between clients and the database and can be thought of as load balancers for Postgres connections. [...] + For temporary clients (for example, serverless or edge functions) use pooler transaction mode

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:13*
