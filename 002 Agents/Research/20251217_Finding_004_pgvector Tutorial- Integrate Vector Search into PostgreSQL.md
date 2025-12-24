# Research Finding #4

**Date:** 2025-12-17 08:57
**Topic:** Supabase pgvector setup tutorial step by step
**Score:** 0.77096564

---

## pgvector Tutorial: Integrate Vector Search into PostgreSQL

**URL:** https://www.datacamp.com/tutorial/pgvector-tutorial
**Published:** Unknown date

---

## Content

In this tutorial, we'll walk through setting up pgvector, using its basic features, and building a simple application by integrating it with OpenAI.

We'll cover installation, basic operations, indexing, and integration with Python and LangChain.

### 1. Prerequisites

To follow this tutorial, you should have basic knowledge of SQL and PostgreSQL and be familiar with Python programming.

Before we begin, make sure you have the following: [...] ```
git clone 
```

3. Build and install the `pgvector` extension:

```
cd pgvector make sudo make install
```

If you are a Windows user, ensure you have C++ support in Visual Studio Code installed. The official installation documentation provides a step-by-step process.

4. Connect to your PostgreSQL database: [...] 1. To set up our first vector database in PostgreSQL using pgvector extension, let's create a table to store our vector data:

```
CREATE TABLE items ( id SERIAL PRIMARY KEY, embedding vector(3) );
```

This creates a table named `items` with an `id` column and an `embedding` column of type `vector(3)`, which will store 3-dimensional vectors.

2. Now, let's insert some data into our table:

```
INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]'), ('[1,1,1]');
```

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:13*
