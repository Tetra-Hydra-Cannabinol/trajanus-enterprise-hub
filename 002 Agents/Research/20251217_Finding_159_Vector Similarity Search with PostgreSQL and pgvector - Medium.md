# Research Finding #159

**Date:** 2025-12-17 08:57
**Topic:** PostgreSQL vector similarity search SQL
**Score:** 0.8446273

---

## Vector Similarity Search with PostgreSQL and pgvector - Medium

**URL:** https://medium.com/@alexandremnarciso/vector-similarity-search-with-postgresql-and-pgvector-d75a44041689
**Published:** Unknown date

---

## Content

My goal here is not to delve deeply into the benefits of the PostgreSQL plugin but rather to demonstrate how vector searches work in vector databases. To achieve this, I will use PostgreSQL as the foundation and PGAdmin for visualizing the results. The first step involves creating a simple database:

```
CREATE TABLE items ( id SERIAL PRIMARY KEY, name TEXT NOT NULL, embedding VECTOR(3) );
``` [...] Sitemap

Open in app

Sign in

Search

Sign in

# Vector Similarity Search with PostgreSQL and pgvector

Alexandre Martin Narciso

4 min read

·

Nov 26, 2024

--

PostgreSQL is a widely used and well-recognized open-source database within the development community, offering robust support for various ORMs. Additionally, it supports vector storage and manipulation through the open-source plugin pgvector, available at: . [...] Now, let’s perform a cosine similarity search between the vectors stored in the `embedding` column and the query vector `[0.2, 0.2, 0.2]`.

The query will use the `<=>` operator, which calculates the distance between vectors. To adjust the calculation for cosine similarity, we apply the formula `1 - (embedding <=> '[0.2, 0.2, 0.2]')`.

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:17*
