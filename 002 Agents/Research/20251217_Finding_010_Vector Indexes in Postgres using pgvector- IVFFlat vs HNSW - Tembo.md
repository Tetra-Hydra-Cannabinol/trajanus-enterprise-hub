# Research Finding #10

**Date:** 2025-12-17 08:57
**Topic:** pgvector indexing strategies HNSW vs IVFFlat
**Score:** 0.8995547

---

## Vector Indexes in Postgres using pgvector: IVFFlat vs HNSW | Tembo

**URL:** https://legacy.tembo.io/blog/vector-indexes-in-pgvector/
**Published:** Unknown date

---

## Content

| Index type | Parameters |
 --- |
| IVFFlat | Lists = 200, Probes = 100 |
| HNSW | m = 24, ef\_construction = 200, ef\_search = 800 |

### Build Time

For the chosen parameters, IVFFlat indexes can be created quicker (128 seconds) compared to HNSW (4065 seconds). HNSW creation is almost 32X slower.

### Size

In terms of index size, IVFFlat is again the winner. For a recall of 0.998, IVFFlat requires around 257MB, whereas HNSW requires about 729MB. HNSW requires 2.8X more space.

### Speed [...] The benchmark uses one thread to execute the vector queries.

It is in speed where HNSW shines. With a recall of 0.998, HNSW can achieve a throughput of 40.5 QPS, whereas IVFFlat can only execute 2.6 QPS. HNSW is 15.5X better in this aspect.

### Recall vs Index Updates [...] Let’s take another example. Imagine a system of Facial Recognition. You’d likely want a fast response time (guideline #2) with good accuracy. You may also be OK with the size of the index (inverse of guideline #1). So, HNSW would be the best choice.

The case of an IoT Sensor Data Database where read values keep changing (e.g., temperature, position, etc.) would also be a good candidate for HNSW (guideline #4). IVFFlat could not handle the index changes properly.

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:13*
