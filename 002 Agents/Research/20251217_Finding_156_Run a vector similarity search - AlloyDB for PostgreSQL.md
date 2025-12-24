# Research Finding #156

**Date:** 2025-12-17 08:57
**Topic:** PostgreSQL vector similarity search SQL
**Score:** 0.9203972

---

## Run a vector similarity search | AlloyDB for PostgreSQL

**URL:** https://docs.cloud.google.com/alloydb/docs/ai/run-vector-similarity-search
**Published:** Unknown date

---

## Content

This document explains how to perform vector similarity searches in AlloyDB for PostgreSQL using the `pgvector` extension. Vector similarity search, also known as nearest neighbor search, lets you find the data points in your data that are most similar to a given query vector.

You can query your AlloyDB database for semantically similar vectors after storing and indexing embeddings. Use `pgvector` query features to find the nearest neighbors for an embedding vector. [...] For more information about storing vector embeddings and creating an index, see Store vector embeddings and Create indexes respectively.

## Run a similarity search with vector input

To run a similarity search, specify the table, embedding column, distance function, target embedding, and the number of rows to return. You can also use the `embedding()` function to translate text into a vector and then compare the vector to stored embeddings using `pgvector` operators. [...] You can use also use the `embedding()` function to translate the text into a vector, and to find the database rows with the most semantically similar embeddings. The stock `pgvector` PostgreSQL extension is customized for AlloyDB, and referred to as `vector`. You apply the vector to one of the `pgvector` nearest-neighbor operators, for example `<=>` for cosine distance.

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:17*
