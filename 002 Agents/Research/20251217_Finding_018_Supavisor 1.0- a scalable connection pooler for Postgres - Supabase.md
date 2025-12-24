# Research Finding #18

**Date:** 2025-12-17 08:57
**Topic:** Supabase connection pooling production
**Score:** 0.9998697

---

## Supavisor 1.0: a scalable connection pooler for Postgres - Supabase

**URL:** https://supabase.com/blog/supavisor-postgres-connection-pooler
**Published:** Unknown date

---

## Content

Blog

# Supavisor 1.0: a scalable connection pooler for Postgres

13 Dec 2023

7 minute read

Stanislav Muzhyk
Engineering

After launching Supavisor in August, we've successfully migrated all projects on the platform. Every new Supabase project launched now gets a Supavisor connection string to use for connection pooling.

Supavisor 1.0 symbolizes production readiness and comes with many bug fixes. It includes three important features: [...] `default_pool_size`: the number of connections from Supavisor to your database (configurable)
 `max_connections`: the max number of direct connections Postgres is configured to allow (configurable)
 `default_max_clients` : the maximum number of clients allowed to connect to Supavisor (upgrade to increase)

### IPv4 Deprecation#

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:13*
