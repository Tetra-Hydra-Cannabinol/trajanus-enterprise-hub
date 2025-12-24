# Research Finding #3

**Date:** 2025-12-17 08:57
**Topic:** Supabase pgvector setup tutorial step by step
**Score:** 0.79099923

---

## Build a RAG App With Descope, Supabase & pgvector: Part 1

**URL:** https://www.descope.com/blog/post/rag-descope-supabase-pgvector-1
**Published:** Unknown date

---

## Content

To complete this tutorial, you need the following:

 A basic understanding of React and Node.js
 A basic understanding of pgvector
 Familiarity with AI concepts, like embeddings and vector similarity search
 A Descope account on the Enterprise plan
 A Supabase account on the Pro plan
 OpenAI developer account with credits
 Node.js installed on your local machine

## Setting up Supabase as your backend [...] In this two-part series, you’ll learn how to combine all these tools to build a secure and intelligent RAG application. In this first part, you will set up the backend using Supabase and utilize pgvector to manage embeddings. In the second part of this series, you will integrate Descope for authentication as a custom Security Assertion Markup Language (SAML) provider and leverage the Supabase Row-Level Security (RLS) to implement granular permissions to make sure that data is accessible only to [...] 1. Preprocess the knowledge base (in this case, Descope developer docs) and generate embeddings for each of these pages.
2. Store the page content, along with the generated embeddings in Supabase.
3. Prompt the user for input.
4. Generate embeddings for the user input and use it to perform a similarity search against the embeddings in the database.
5. Return the most similar pages and pass them to OpenAI API to generate a response for the user’s query.

## Prerequisites

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:13*
