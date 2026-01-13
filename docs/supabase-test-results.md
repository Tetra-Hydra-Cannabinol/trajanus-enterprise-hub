# Supabase RPC Function Test Results

**Test Date:** January 13, 2026, 9:30 AM
**Project:** trajanus-rag-production
**Test Script:** `test-supabase.js`

---

## Test Summary

| Test | Function | Status | Records |
|------|----------|--------|---------|
| 1 | list_knowledge_sources | ✅ PASS | 34 |
| 2 | search_by_text | ✅ PASS | 5 |
| 3 | get_url_content | ✅ PASS | 1 |
| 4 | match_knowledge_base | ✅ PASS | 5 |

**Total: 4 Passed, 0 Failed**

---

## Test 1: list_knowledge_sources

**Purpose:** Aggregate statistics by source
**Parameters:** `filter_source: null` (all sources)
**Result:** 34 unique sources found

### Sample Response

```json
{
    "source": "Traffic-Studeis Package I",
    "url_count": 149,
    "chunk_count": 13067,
    "latest_update": "2026-01-04T19:33:39.330027+00:00"
}
```

### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| source | string | Source name from metadata |
| url_count | integer | Number of unique URLs |
| chunk_count | integer | Total chunks |
| latest_update | timestamptz | Most recent update |

### Top 5 Sources

1. **Traffic-Studies Package I** - 13,067 chunks, 149 URLs
2. **YouTube Tutorials** - 8,320 chunks, 120 URLs
3. **LangChain Tutorials** - 1,805 chunks, 6 URLs
4. **ms-office-tutorials** - 1,647 chunks, 7 URLs
5. **Session History** - 1,069 chunks, 101 URLs

---

## Test 2: search_by_text

**Purpose:** Full-text search with PostgreSQL ts_rank
**Parameters:**
- `search_query: 'RAG'`
- `filter_source: 'Session History'`
- `match_count: 5`

**Result:** 5 matching records

### Sample Response

```json
{
    "id": 4,
    "url": "https://trajanus.local/sessions/2025-12-09-rag-setup",
    "chunk_number": 1,
    "title": "RAG System Setup Session - December 9, 2025 (Part 1)",
    "summary": "TRAJANUS RAG SYSTEM SETUP SESSION - December 9, 2025...",
    "content": "Full content text...",
    "metadata": {
        "source": "Session History",
        "processed_at": "2025-12-09T18:32:33.668117",
        "total_chunks": 4
    },
    "rank": 0.0889769
}
```

### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| id | bigint | Record ID |
| url | text | Source URL |
| chunk_number | integer | Position in document |
| title | text | Chunk title |
| summary | text | Brief summary |
| content | text | Full text content |
| metadata | jsonb | Source and processing info |
| rank | float | PostgreSQL ts_rank score |

### Performance Note

⚠️ **Full table scans timeout without source filter.** Always use `filter_source` parameter when possible. Consider adding a GIN index for better performance:

```sql
CREATE INDEX idx_kb_fts ON knowledge_base
USING GIN(to_tsvector('english', title || ' ' || summary || ' ' || content));
```

---

## Test 3: get_url_content

**Purpose:** Retrieve all chunks for a specific URL
**Parameters:** `target_url: 'https://test.local/manual-insert'`
**Result:** 1 chunk returned

### Sample Response

```json
{
    "chunk_number": 1,
    "title": "Manual Test Insert",
    "summary": "Testing direct SQL insert",
    "content": "This is a manual test to verify the database accepts inserts.",
    "metadata": {
        "test": true,
        "source": "SQL"
    }
}
```

### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| chunk_number | integer | Chunk sequence |
| title | text | Chunk title |
| summary | text | Brief summary |
| content | text | Full content |
| metadata | jsonb | Source metadata |

---

## Test 4: match_knowledge_base (Semantic Search)

**Purpose:** Vector similarity search using embeddings
**Parameters:**
- `query_embedding`: 1536-dimension vector from OpenAI
- `match_threshold: 0.3`
- `match_count: 5`

**Query:** "RAG system database setup"
**Result:** 5 semantically similar records

### Sample Response

```json
{
    "id": 1123,
    "url": "file:///08-EOS-Files\\EOS Files 12-10\\2025-12-10_Next_Session_Handoff.md",
    "chunk_number": 5,
    "title": "2025-12-10_Next_Session_Handoff (Part 5)",
    "summary": "Environment Configuration...",
    "content": "Full content about RAG setup...",
    "metadata": {
        "source": "Session History",
        "filename": "2025-12-10_Next_Session_Handoff.md",
        "total_chunks": 15
    },
    "similarity": 0.444359772747799
}
```

### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| id | bigint | Record ID |
| url | text | Source URL |
| chunk_number | integer | Position in document |
| title | text | Chunk title |
| summary | text | Brief summary |
| content | text | Full text content |
| metadata | jsonb | Source metadata |
| similarity | float | Cosine similarity (0-1) |

### Similarity Scores

| Rank | Title | Similarity |
|------|-------|------------|
| 1 | 2025-12-10_Next_Session_Handoff (Part 5) | 0.4444 |
| 2 | Research_Index_20251217 (Part 46) | 0.4067 |
| 3 | 2025-12-10_Next_Session_Handoff (Part 2) | 0.3971 |

### Threshold Recommendations

| Threshold | Use Case |
|-----------|----------|
| 0.7+ | High precision, exact matches |
| 0.5-0.7 | Balanced results |
| 0.3-0.5 | Broader recall, more results |
| < 0.3 | Too noisy, not recommended |

---

## Integration Guide

### JavaScript Usage

```javascript
const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(
    process.env.SUPABASE_URL,
    process.env.SUPABASE_KEY
);

// Semantic search
const { data } = await supabase.rpc('match_knowledge_base', {
    query_embedding: embedding,  // from OpenAI
    match_threshold: 0.5,
    match_count: 10
});

// Full-text search
const { data } = await supabase.rpc('search_by_text', {
    search_query: 'your query',
    filter_source: 'Session History',  // recommended for performance
    match_count: 10
});

// List sources
const { data } = await supabase.rpc('list_knowledge_sources', {
    filter_source: null
});

// Get URL content
const { data } = await supabase.rpc('get_url_content', {
    target_url: 'https://example.com/doc'
});
```

### Embedding Generation

```javascript
async function generateEmbedding(text) {
    const response = await fetch('https://api.openai.com/v1/embeddings', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            model: 'text-embedding-3-small',
            input: text
        })
    });
    const result = await response.json();
    return result.data[0].embedding;
}
```

---

## Ready for Integration

All 4 RPC functions tested and working:

| Function | Ready | Notes |
|----------|-------|-------|
| match_knowledge_base | ✅ Yes | Use threshold 0.3-0.5 |
| search_by_text | ✅ Yes | Use filter_source to avoid timeout |
| list_knowledge_sources | ✅ Yes | No issues |
| get_url_content | ✅ Yes | No issues |

---

*Test results generated: January 13, 2026*
*Test script: C:\Dev\trajanus-command-center\test-supabase.js*
