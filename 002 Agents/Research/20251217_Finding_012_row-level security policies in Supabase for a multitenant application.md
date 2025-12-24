# Research Finding #12

**Date:** 2025-12-17 08:57
**Topic:** Supabase RLS policies for multi-user apps
**Score:** 0.7859175

---

## row-level security policies in Supabase for a multitenant application

**URL:** https://github.com/orgs/community/discussions/149922
**Published:** Unknown date

---

## Content

### Select Topic Area

Question

### Body

I’m having a really hard time setting up RLS policies in Supabase. I’m building a multi-tenant app, and I need to restrict access to rows based on the `tenant_id` column. I’ve tried writing a policy, but it’s not working, and I’m not sure what I’m doing wrong. Here’s what I have so far:

`tenant_id` [...] | Select Topic Area Question Body I’m having a really hard time setting up RLS policies in Supabase. I’m building a multi-tenant app, and I need to restrict access to rows based on the `tenant_id` column. I’ve tried writing a policy, but it’s not working, and I’m not sure what I’m doing wrong. Here’s what I have so far:  ``` CREATE POLICY "Tenant can access their own data" ON my_table FOR SELECT USING (tenant_id = auth.uid()); ```  But when I query the table, I’m still seeing all the rows, not [...] | No need to worry, RLS can be a bit tricky at first, but I’ll walk you through it... :D  First, it looks like you’re on the right track with your policy, but there’s a small misunderstanding. The `auth.uid()` function returns the UUID of the currently authenticated user, not the `tenant_id`. If your `tenant_id` is stored in a different way (e.g., in a `profiles` table or as a custom claim in the JWT), you’ll need to adjust your policy accordingly.  Here’s an example of how you can set this up:

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:13*
