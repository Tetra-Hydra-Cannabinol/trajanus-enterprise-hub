# Research Finding #23

**Date:** 2025-12-17 08:57
**Topic:** text-embedding-3-small optimal parameters
**Score:** 0.99938333

---

## Vector embeddings | OpenAI API

**URL:** https://platform.openai.com/docs/guides/embeddings
**Published:** Unknown date

---

## Content

By default, the length of the embedding vector is `1536` for `text-embedding-3-small` or `3072` for `text-embedding-3-large`. To reduce the embedding's dimensions without losing its concept-representing properties, pass in the dimensions parameter. Find more detail on embedding dimensions in the embedding use case section.

## Embedding models [...] | Model | ~ Pages per dollar | Performance on MTEB eval | Max input |
 ---  --- |
| text-embedding-3-small | 62,500 | 62.3% | 8192 |
| text-embedding-3-large | 9,615 | 64.6% | 8192 |
| text-embedding-ada-002 | 12,500 | 61.0% | 8192 |

## Use cases

Here we show some representative use cases, using the Amazon fine-food reviews dataset.

### Obtaining the embeddings [...] For third-generation embedding models like `text-embedding-3-small`, use the `cl100k_base` encoding.

More details and example code are in the OpenAI Cookbook guide how to count tokens with tiktoken.

### How can I retrieve K nearest embedding vectors quickly?

For searching over many vectors quickly, we recommend using a vector database. You can find examples of working with vector databases and the OpenAI API in our Cookbook on GitHub.

### Which distance function should I use?

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:13*
