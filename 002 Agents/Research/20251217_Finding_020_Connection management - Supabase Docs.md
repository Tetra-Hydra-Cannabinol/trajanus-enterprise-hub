# Research Finding #20

**Date:** 2025-12-17 08:57
**Topic:** Supabase connection pooling production
**Score:** 0.99949265

---

## Connection management | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/connection-management
**Published:** Unknown date

---

## Content

You can change how many database connections Supavisor can manage by altering the pool size in the "Connection pooling configuration" section of the Database Settings:

The general rule is that if you are heavily using the PostgREST database API, you should be conscientious about raising your pool size past 40%. Otherwise, you can commit 80% to the pool. This leaves adequate room for the Authentication server and other utilities. [...] Postgres: Direct connections from your application
 PostgREST: Connections from the PostgREST API layer
 Reserved: Administrative connections for Supabase services
 Auth: Connections from Supabase Auth service
 Storage: Connections from Supabase Storage service
 Other roles: Miscellaneous database connections

This chart helps you monitor connection pool usage, identify connection leaks, and plan capacity. It also shows a reference line for your compute size's maximum connection limit. [...] These numbers are generalizations and depends on other Supabase products that you use and the extent of their usage. The actual values depend on your concurrent peak connection usage. For instance, if you were only using 80 connections in a week period and your database max connections is set to 500, then realistically you could allocate the difference of 420 (minus a reasonable buffer) to service more demand.

## Monitoring connections#

### Capturing historical usage#

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:13*
