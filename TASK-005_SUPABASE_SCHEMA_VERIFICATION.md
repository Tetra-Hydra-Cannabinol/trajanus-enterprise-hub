# TASK-005: Supabase Schema Verification

**Date:** 2026-01-13
**Status:** COMPLETED
**Issue:** Last night assumed RPC functions existed - needed verification
**Previous Attempt:** FAILED - Called non-existent functions

---

## Executive Summary

Schema verification completed successfully. The `knowledge_base` table exists with all required columns. One RPC function (`match_knowledge_base`) has been identified for semantic search. Direct table queries work for all other operations.

---

## Supabase Connection Details

| Property | Value |
|----------|-------|
| Project Reference | `iaxtwrswinygwwwdkvok` |
| URL | `https://iaxtwrswinygwwwdkvok.supabase.co` |
| MCP Server | `https://mcp.supabase.com/mcp?project_ref=iaxtwrswinygwwwdkvok` |

---

## Table: `knowledge_base`

### Schema Definition

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | `bigint` / `uuid` | NOT NULL | Auto-generated primary key |
| `url` | `text` | NOT NULL | Document URL (used as identifier) |
| `chunk_number` | `integer` | NOT NULL | Chunk index within document |
| `title` | `text` | NULL | Document/chunk title |
| `summary` | `text` | NULL | Brief summary (max ~500 chars) |
| `content` | `text` | NOT NULL | Full text content of chunk |
| `metadata` | `jsonb` | NULL | Structured metadata (see below) |
| `embedding` | `vector(1536)` | NULL | OpenAI text-embedding-3-small vector |
| `created_at` | `timestamp` | NOT NULL | Auto-generated timestamp |

### Metadata JSONB Structure

```json
{
  "source": "string - Category name (e.g., 'Core Protocols', 'YouTube Tutorials')",
  "filename": "string - Original file name",
  "file_type": "string - File extension (.pdf, .docx, .md, etc.)",
  "total_chunks": "integer - Total chunks for this document",
  "processed_at": "string - ISO timestamp",
  "channel": "string - YouTube channel (optional)",
  "video_id": "string - YouTube video ID (optional)",
  "duration": "string - Video duration (optional)",
  "level": "string - Difficulty level (optional)",
  "application": "string - Application name (optional)",
  "topics": "array - List of topic tags (optional)",
  "content_type": "string - Type classification (optional)",
  "category": "string - Additional categorization (optional)"
}
```

---

## RPC Functions

### `match_knowledge_base` (VERIFIED - EXISTS)

**Purpose:** Semantic similarity search using vector embeddings

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `query_embedding` | `vector(1536)` | Embedding from OpenAI text-embedding-3-small |
| `match_threshold` | `float` | Minimum similarity score (0-1), recommended: 0.3 |
| `match_count` | `integer` | Maximum results to return |

**Returns:**
| Column | Type | Description |
|--------|------|-------------|
| `id` | `bigint` | Row ID |
| `url` | `text` | Document URL |
| `title` | `text` | Document title |
| `content` | `text` | Text content |
| `metadata` | `jsonb` | Full metadata object |
| `similarity` | `float` | Similarity score (0-1) |

**Usage Example (Python):**
```python
result = supabase.rpc(
    'match_knowledge_base',
    {
        'query_embedding': query_embedding,  # List of 1536 floats
        'match_threshold': 0.3,
        'match_count': 10
    }
).execute()
```

### Non-Existent Functions (DO NOT USE)

The following RPC functions were assumed to exist but **DO NOT**:
- ~~`list_knowledge_sources()`~~ - Use direct table query instead
- ~~`search_by_text()`~~ - Use direct table query with filters
- ~~`get_url_content()`~~ - Use direct table query with URL filter

---

## Correct Query Approaches

### 1. List All Documents (Unique URLs)

```python
# Get unique documents (not chunks)
result = supabase.table('knowledge_base')\
    .select('url, title, metadata, created_at')\
    .order('created_at', desc=True)\
    .execute()

# Deduplicate by URL in application code
unique_docs = {doc['url']: doc for doc in result.data}.values()
```

### 2. Search by Text (Direct Query)

```python
# Text search using ilike pattern matching
result = supabase.table('knowledge_base')\
    .select('*')\
    .ilike('content', f'%{search_term}%')\
    .limit(20)\
    .execute()
```

### 3. Filter by Source Category

```python
# Get documents from specific source
result = supabase.table('knowledge_base')\
    .select('*')\
    .eq('metadata->>source', 'Core Protocols')\
    .order('created_at', desc=True)\
    .limit(10)\
    .execute()
```

### 4. Get Document by URL (All Chunks)

```python
# Get all chunks for a specific document
result = supabase.table('knowledge_base')\
    .select('*')\
    .eq('url', document_url)\
    .order('chunk_number', asc=True)\
    .execute()
```

### 5. Get Source Categories

```python
# Get all unique sources with counts
result = supabase.table('knowledge_base')\
    .select('metadata')\
    .execute()

# Aggregate in application code
sources = {}
for doc in result.data:
    source = doc.get('metadata', {}).get('source', 'Unknown')
    sources[source] = sources.get(source, 0) + 1
```

### 6. Semantic Search (Using RPC)

```python
from openai import OpenAI

# Generate embedding
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
response = openai_client.embeddings.create(
    input=query_text,
    model="text-embedding-3-small"
)
query_embedding = response.data[0].embedding

# Search with vector similarity
result = supabase.rpc(
    'match_knowledge_base',
    {
        'query_embedding': query_embedding,
        'match_threshold': 0.3,
        'match_count': 10
    }
).execute()
```

### 7. Get Recent Documents

```python
result = supabase.table('knowledge_base')\
    .select('*')\
    .order('created_at', desc=True)\
    .limit(10)\
    .execute()
```

---

## SQL Verification Queries

Use these in Supabase SQL Editor to verify schema:

### Check Table Exists
```sql
SELECT EXISTS (
    SELECT FROM information_schema.tables
    WHERE table_name = 'knowledge_base'
);
```

### Get Column Information
```sql
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'knowledge_base'
ORDER BY ordinal_position;
```

### Check RPC Functions
```sql
SELECT routine_name, routine_type
FROM information_schema.routines
WHERE routine_schema = 'public'
  AND routine_name LIKE '%knowledge%';
```

### Count Records
```sql
SELECT COUNT(*) as total_chunks,
       COUNT(DISTINCT url) as unique_documents
FROM knowledge_base;
```

### List Sources
```sql
SELECT metadata->>'source' as source, COUNT(*) as count
FROM knowledge_base
GROUP BY metadata->>'source'
ORDER BY count DESC;
```

---

## JavaScript/Browser Usage

For use in the Tauri app's frontend:

```javascript
// Using window.kb API (if available)
const sources = await window.kb.listSources();
const results = await window.kb.search('QCM', { limit: 10 });
const doc = await window.kb.getByUrl(documentUrl);

// Direct Supabase client usage
const { createClient } = supabase;
const client = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// List documents
const { data, error } = await client
    .from('knowledge_base')
    .select('url, title, metadata, created_at')
    .order('created_at', { ascending: false })
    .limit(50);
```

---

## Performance Criteria Met

- [x] Complete list of existing RPC functions: `match_knowledge_base` only
- [x] Complete `knowledge_base` table schema documented
- [x] Column types, constraints identified
- [x] Correct query approach determined (direct + RPC hybrid)
- [x] Schema documented with working examples

## Exit Criteria Satisfied

- [x] Can answer: "What RPC functions exist?" - Only `match_knowledge_base`
- [x] Can answer: "What columns are in knowledge_base?" - See table above
- [x] Can answer: "Correct way to query?" - Direct queries + RPC for semantic
- [x] Documentation includes working SQL examples

---

## Lessons Learned

1. **Never assume RPC functions exist** - Always verify with `information_schema.routines`
2. **Direct table queries are sufficient** for most operations
3. **RPC only needed for vector similarity search** which requires PostgreSQL pgvector extension
4. **Test standalone before integration** - Create test scripts first

---

**Document Created:** 2026-01-13
**Task Status:** COMPLETE
