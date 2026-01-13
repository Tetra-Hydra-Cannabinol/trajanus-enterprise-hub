# Supabase Working Queries

**Project:** trajanus-rag-production
**Tested:** January 13, 2026

---

## Connection Information

```
API URL: https://iaxtwrswinygwwwdkvok.supabase.co
Database Host: db.iaxtwrswinygwwwdkvok.supabase.co
Region: us-east-1
```

**Credentials File:** `G:\My Drive\00 - Trajanus USA\00-Command-Center\05-Scripts\.env`

```env
SUPABASE_URL=https://iaxtwrswinygwwwdkvok.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## Knowledge Base Queries

### Basic Statistics

```sql
-- Total chunks and unique sources
SELECT
    COUNT(*) as total_chunks,
    COUNT(DISTINCT url) as unique_sources
FROM knowledge_base;
-- Result: 30,781 chunks from 987 sources
```

### List All Sources (Top 10)

```sql
SELECT * FROM list_knowledge_sources(NULL) LIMIT 10;
```

**Current Results:**

| Source | URLs | Chunks | Latest Update |
|--------|------|--------|---------------|
| Traffic-Studies Package I | 149 | 13,067 | 2026-01-04 |
| YouTube Tutorials | 120 | 8,320 | 2025-12-23 |
| LangChain Tutorials | 6 | 1,805 | 2025-12-22 |
| ms-office-tutorials | 7 | 1,647 | 2025-12-20 |
| Session History | 101 | 1,069 | 2025-12-10 |
| supabase-youtube-tutorials | 13 | 935 | 2025-12-19 |
| claude_code | 38 | 753 | 2026-01-02 |
| Research | 173 | 496 | 2025-12-29 |
| Living Documents | 41 | 351 | 2025-12-10 |
| Core Protocols | 18 | 334 | 2025-12-23 |

### Filter by Specific Source

```sql
SELECT * FROM list_knowledge_sources('claude_code');
```

---

## Full-Text Search (search_by_text)

### Basic Text Search

```sql
-- Search for "RAG system" across all sources
SELECT id, url, title, LEFT(summary, 100) as summary_preview
FROM search_by_text('RAG system', NULL, 5);
```

### Search Within Specific Source

```sql
-- Search only in Session History
SELECT id, title, content
FROM search_by_text('database setup', 'Session History', 10);
```

### Search with Full Results

```sql
SELECT * FROM search_by_text('construction management', NULL, 20);
```

---

## Semantic Search (match_knowledge_base)

**Note:** Requires pre-computed embedding vector (1536 dimensions from OpenAI text-embedding-3-small)

### Usage Pattern

```sql
-- First, generate embedding via OpenAI API, then:
SELECT * FROM match_knowledge_base(
    '[0.123, -0.456, ...]'::vector,  -- 1536-dimension embedding
    0.7,                              -- match_threshold (0-1)
    10                                -- match_count
);
```

### Python Example

```python
import openai
from supabase import create_client

# Generate embedding
response = openai.embeddings.create(
    model="text-embedding-3-small",
    input="your search query"
)
query_embedding = response.data[0].embedding

# Search Supabase
result = supabase.rpc('match_knowledge_base', {
    'query_embedding': query_embedding,
    'match_threshold': 0.7,
    'match_count': 10
}).execute()
```

---

## Get Document by URL

```sql
-- Retrieve all chunks for a specific URL
SELECT * FROM get_url_content('https://example.com/document');
```

---

## Direct Table Queries

### Sample Records

```sql
-- Get sample records with metadata
SELECT
    id, url, chunk_number, title,
    LEFT(summary, 100) as summary_preview,
    metadata->>'source' as source
FROM knowledge_base
LIMIT 5;
```

### Records Without Embeddings

```sql
-- Find records missing embeddings
SELECT COUNT(*) FROM knowledge_base WHERE embedding IS NULL;
```

### Recent Additions

```sql
-- Records added in last 7 days
SELECT id, url, title, created_at
FROM knowledge_base
WHERE created_at > NOW() - INTERVAL '7 days'
ORDER BY created_at DESC
LIMIT 20;
```

### Query by Metadata

```sql
-- Filter by metadata field
SELECT id, url, title
FROM knowledge_base
WHERE metadata->>'source' = 'claude_code'
LIMIT 10;
```

---

## Team Feedback Queries

### All Feedback

```sql
SELECT * FROM team_feedback ORDER BY created_at DESC;
```

### Unresolved Items

```sql
SELECT * FROM team_feedback
WHERE resolved = false
ORDER BY created_at DESC;
```

### Feedback by Category

```sql
SELECT category, COUNT(*) as count
FROM team_feedback
GROUP BY category;
```

---

## Insert Examples

### Add to Knowledge Base

```sql
INSERT INTO knowledge_base (url, chunk_number, title, summary, content, metadata)
VALUES (
    'https://example.com/doc',
    1,
    'Document Title',
    'Brief summary of the content',
    'Full content text goes here...',
    '{"source": "Manual Entry", "category": "Documentation"}'::jsonb
);
```

### Add with Embedding

```sql
INSERT INTO knowledge_base (url, chunk_number, title, summary, content, metadata, embedding)
VALUES (
    'https://example.com/doc',
    1,
    'Document Title',
    'Summary',
    'Content',
    '{"source": "API"}'::jsonb,
    '[0.1, 0.2, ...]'::vector  -- 1536 dimensions
);
```

### Add Team Feedback

```sql
INSERT INTO team_feedback (author, category, message)
VALUES ('Bill', 'suggestion', 'Add dark mode to the interface');
```

---

## Useful Aggregations

### Content by Source and Month

```sql
SELECT
    metadata->>'source' as source,
    DATE_TRUNC('month', created_at) as month,
    COUNT(*) as chunks
FROM knowledge_base
GROUP BY metadata->>'source', DATE_TRUNC('month', created_at)
ORDER BY month DESC, chunks DESC;
```

### Average Chunk Size by Source

```sql
SELECT
    metadata->>'source' as source,
    AVG(LENGTH(content)) as avg_content_length,
    COUNT(*) as chunk_count
FROM knowledge_base
GROUP BY metadata->>'source'
ORDER BY chunk_count DESC
LIMIT 10;
```

---

## Supabase JavaScript Client

```javascript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
    'https://iaxtwrswinygwwwdkvok.supabase.co',
    'your-anon-key'
)

// Full-text search
const { data, error } = await supabase
    .rpc('search_by_text', {
        search_query: 'construction management',
        filter_source: null,
        match_count: 10
    })

// List sources
const { data: sources } = await supabase
    .rpc('list_knowledge_sources', { filter_source: null })
```

---

## Python Client

```python
from supabase import create_client
import os

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

# Full-text search
result = supabase.rpc('search_by_text', {
    'search_query': 'RAG setup',
    'filter_source': None,
    'match_count': 10
}).execute()

# Direct table query
result = supabase.table('knowledge_base') \
    .select('id, url, title') \
    .eq('metadata->>source', 'claude_code') \
    .limit(10) \
    .execute()
```

---

*Documentation generated: January 13, 2026*
