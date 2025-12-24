# Research Finding #129

**Date:** 2025-12-17 08:57
**Topic:** RAG chunk size optimization experiments
**Score:** 0.9998952

---

## The Ultimate Guide to RAG Chunking Strategies - Agenta

**URL:** https://agenta.ai/blog/the-ultimate-guide-for-chunking-strategies
**Published:** Unknown date

---

## Content

Next, testing a chunk size of two works better, grouping sentences 1 and 2 together and 3 and 4 together, both with high similarity.

`Chunk size=2: [S1 S2]` ✓ `[S3 S4]` ✓

Trying a chunk size of four again fails due to topic mismatch.

`Chunk size=4: [S1 S2 S3 S4]` ✗ [...] OpenAI’s default chunker (800 tokens, 400 overlap), which showed below-average results. Notably, reducing chunk overlap improved efficiency (IoU) by minimizing redundancy. Based on these findings, the report recommends either using `RecursiveCharacterTextSplitter` with 200–400 token chunks and no overlap for simplicity and good performance, or `ClusterSemanticChunker` for maximum efficiency if complexity is acceptable. The results are summarized in this table : [...] The Chroma Technical Report (July 3, 2024), titled "Evaluating Chunking Strategies for Retrieval", assess the effectiveness of these different text chunking methods used in Retrieval-Augmented Generation (RAG) systems using metrics such as Recall, Precision, Precision Ω (maximum achievable precision under perfect recall), and IoU (Intersection over Union) which captures both completeness and efficiency by penalizing irrelevant token inclusion and missed relevant tokens.

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:16*
