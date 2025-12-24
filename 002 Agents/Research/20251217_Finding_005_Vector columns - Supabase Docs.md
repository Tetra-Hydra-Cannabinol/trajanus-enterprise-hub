# Research Finding #5

**Date:** 2025-12-17 08:57
**Topic:** Supabase pgvector setup tutorial step by step
**Score:** 0.7587435

---

## Vector columns | Supabase Docs

**URL:** https://supabase.com/docs/guides/ai/vector-columns
**Published:** Unknown date

---

## Content

1. Go to the Database page in the Dashboard.
2. Click on Extensions in the sidebar.
3. Search for "vector" and enable the extension.

### Create a table to store vectors#

After enabling the `vector` extension, you will get access to a new data type called `vector`. The size of the vector (indicated in parenthesis) represents the number of dimensions stored in that vector.

```

1

create table documents (

2

id serial primary key,

3

title text not null,

4

body text not null,

5

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:13*
