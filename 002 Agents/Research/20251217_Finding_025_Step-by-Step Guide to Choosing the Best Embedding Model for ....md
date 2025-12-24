# Research Finding #25

**Date:** 2025-12-17 08:57
**Topic:** text-embedding-3-small optimal parameters
**Score:** 0.9983386

---

## Step-by-Step Guide to Choosing the Best Embedding Model for ...

**URL:** https://weaviate.io/blog/how-to-choose-an-embedding-model
**Published:** Unknown date

---

## Content

Then, you will configure a data collection called `"Pastries"` and configure the properties and vectorizer. This example uses OpenAI’s `text-embedding-3-small` embedding model to vectorize the data at import and query time automatically. Note, that we will repeat this step later with `text-embedding-3-large` to compare the two models. For this, you might want to have a look at how to delete a collection. [...] Across the three example queries, both `text-embedding-3-small` and `text-embedding-3-large` result in an average precision of 0.5 and an average recall of 0.58, although they return different results for the queries. As you can see, you would need to increase both the number of data objects in the dataset and the number of queries to evaluate the embedding models. However, this small example should give you a good starting point for building your own evaluation pipeline.

## Step 4: Iterate​ [...] This section compares two OpenAI embedding models, `text-embedding-3-small` and `text-embedding-3-large`, for three sample queries. Note that the desired outputs for each query are highly subjective. But this is exactly the point: You must decide what result you want for your use case.

Various evaluation metrics are available, such as precision, recall, MRR, MAP, and NDCG. In this section, we will use precision and recall as evaluation metrics.

Query 1: “Sweet pastry”

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:13*
