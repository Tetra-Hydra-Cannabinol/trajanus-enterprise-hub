# Research Finding #139

**Date:** 2025-12-17 08:57
**Topic:** reranking models RAG accuracy
**Score:** 0.7587435

---

## Improving RAG accuracy: 10 techniques that actually work

**URL:** https://redis.io/blog/10-techniques-to-improve-rag-accuracy/
**Published:** Unknown date

---

## Content

When top-k retrieval brings back a mixed bag of useful and irrelevant documents, re-ranking helps reorder the results to prioritize helpful context. This is critical in noisy corpora or where embedding distances alone are insufficient. You can re-rank via shallow ML models or even with a secondary LLM pass. Fusion techniques—combining results from different retrievers—boost robustness and recall. Redis’ support for hybrid search and secondary scoring enables efficient implementation of these [...] Use re-ranking when retrieval precision is low due to noise or when you have multiple complementary retrieval sources. These techniques improve result quality by refining and merging ranked outputs. [...] ## 10. Re-ranking

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:16*
