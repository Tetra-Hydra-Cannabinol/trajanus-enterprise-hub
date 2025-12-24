# Research Finding #15

**Date:** 2025-12-17 08:57
**Topic:** Supabase RLS policies for multi-user apps
**Score:** 0.7206637

---

## Row Level Security | Supabase Docs

**URL:** https://supabase.com/docs/guides/database/postgres/row-level-security
**Published:** Unknown date

---

## Content

Supabase provides some helpers that simplify RLS if you're using Supabase Auth. We'll use these helpers to illustrate some basic policies:

### SELECT policies#

You can specify select policies with the `using` clause.

Let's say you have a table called `profiles` in the public schema and you want to enable read access to everyone.

```

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15 [...] RLS is incredibly powerful and flexible, allowing you to write complex SQL rules that fit your unique business needs. RLS can be combined with Supabase Auth for end-to-end user security from the browser to the database.

RLS is a Postgres primitive and can provide "defense in depth)" to protect your data from malicious actors even when accessed through third-party tooling.

## Policies# [...] -- 1. Create tablecreate table profiles ( id uuid primary key, user_id uuid references auth.users, avatar_url text);-- 2. Enable RLSalter table profiles enable row level security;-- 3. Create Policycreate policy "Users can update their own profile."on profiles for updateto authenticated -- the Postgres Role (recommended)using ( (select auth.uid()) = user_id ) -- checks if the existing row complies with the policy expressionwith check ( (select auth.uid()) = user_id ); -- checks if the new row

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:13*
