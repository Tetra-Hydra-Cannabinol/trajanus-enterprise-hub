# Research Finding #140

**Date:** 2025-12-17 08:57
**Topic:** reranking models RAG accuracy
**Score:** 0.7568076

---

## Improving RAG Performance: WTF are Re-Ranking ...

**URL:** https://www.fuzzylabs.ai/blog-post/improving-rag-performance-re-ranking
**Published:** Unknown date

---

## Content

Re-ranking is a two step process, the idea behind is to first retrieve a large number of documents from our vector store using computationally cheap queries and then apply more computationally expensive techniques to identify the highest-quality matches.

### Re-ranker model

A re-ranking model is typically a cross-encoder, a type of transformer model designed for evaluating the relevancy of query-document pairs. [...] 1. Reranking: We take the top 20 results from vector search and pass them into a reranker for evaluation. Unlike vector search, rerankers are more computationally expensive models, which allows them to accurately analyse the semantic relevance of the query-document pair. [...] Because reranking is applied to a smaller subset of documents, we can afford to use these more complex and resource-intensive models without significantly impacting performance. This is the step that ensures the documents we feed to the LLM are the most useful and valuable.

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:16*
