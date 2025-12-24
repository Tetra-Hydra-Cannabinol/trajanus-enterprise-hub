# Research Finding #6

**Date:** 2025-12-17 08:57
**Topic:** pgvector indexing strategies HNSW vs IVFFlat
**Score:** 0.9227683

---

## pgvector v0.5.0: Faster semantic search with HNSW indexes

**URL:** https://supabase.com/blog/increase-performance-pgvector-hnsw
**Published:** Unknown date

---

## Content

In most cases today, HNSW offers a more performant and robust index over IVFFlat. It's worth noting though that HNSW indexes will almost always be slower to build and use more memory than IVFFlat, so if your system is memory-constrained and you don't foresee the need to rebuild your index often, you may find IVFFlat to be more suitable. It's also worth noting that product quantization (compressing index entries for vectors) is expected for IVF in the next versions of pgvector which should

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:13*
