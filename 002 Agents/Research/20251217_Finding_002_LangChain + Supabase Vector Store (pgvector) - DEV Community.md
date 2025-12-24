# Research Finding #2

**Date:** 2025-12-17 08:57
**Topic:** Supabase pgvector setup tutorial step by step
**Score:** 0.81097376

---

## LangChain + Supabase Vector Store (pgvector) - DEV Community

**URL:** https://dev.to/gautam_kumar_d3daad738680/langchain-supabase-vector-store-pgvector-a-beginner-friendly-guide-5h33
**Published:** Unknown date

---

## Content

`.env`
`# OpenAI
OPENAI_API_KEY=sk-your-openai-key
# Supabase
SUPABASE_URL=
# Service role key must be kept server-side only (NEVER expose in frontend code)
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key`

## 4) Prepare your database (Supabase)

Open your Supabase dashboard -> SQL Editor. Run the SQL below to enable pgvector, create a table, index it, and add an RPC function for searching. [...] ## 2) Install dependencies

`npm i @langchain/community @langchain/openai @supabase/supabase-js dotenv`
`@langchain/community`
`@langchain/openai`
`@supabase/supabase-js`
`dotenv`
`.env`

## 3) Create your `.env` (do not commit this)

`.env`

Create a file named `.env` in the project root:

`.env`
`touch .env`

Put the following into `.env` (replace with your values): [...] If you prefer UUID ids, use the first block and don’t pass custom `ids` when inserting. If you want to pass string ids like `"1"`, use the Text ID variant.

`ids`
`"1"`

### 4.1 Enable `pgvector`

`pgvector`
`-- The extension name is "vector"
create extension if not exists vector;`

### 4.2 Create the `documents` table (UUID id)

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:13*
