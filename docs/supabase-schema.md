# Supabase Schema Documentation

**Project:** trajanus-rag-production
**Project ID:** iaxtwrswinygwwwdkvok
**Region:** us-east-1
**Database Version:** PostgreSQL 17.6.1
**Status:** ACTIVE_HEALTHY
**Documented:** January 13, 2026

---

## Database Statistics

| Metric | Value |
|--------|-------|
| Total Chunks | 30,781 |
| Unique Sources | 987 |
| Database Host | db.iaxtwrswinygwwwdkvok.supabase.co |

---

## Public Tables

### 1. knowledge_base (Primary RAG Table)

**Row Count:** 30,778
**RLS Enabled:** Yes
**Purpose:** Main vector storage for RAG semantic search

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | bigint | NO | nextval sequence | Primary key |
| url | text | NO | - | Source document URL |
| chunk_number | integer | NO | - | Chunk sequence within document |
| title | text | NO | - | Document/chunk title |
| summary | text | NO | - | Brief summary of content |
| content | text | NO | - | Full text content |
| metadata | jsonb | NO | '{}' | Flexible metadata (source, category, etc.) |
| embedding | vector | YES | NULL | 1536-dimension OpenAI embedding |
| created_at | timestamptz | YES | now() | Creation timestamp |
| updated_at | timestamptz | YES | now() | Last update timestamp |

**Primary Key:** id

---

### 2. documents

**Row Count:** 1
**RLS Enabled:** Yes
**Purpose:** Simple document storage (minimal use)

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| id | integer | NO | nextval sequence |
| title | text | YES | - |
| content | text | YES | - |
| document_type | text | YES | - |
| metadata | jsonb | YES | - |
| created_at | timestamp | YES | now() |

**Primary Key:** id

---

### 3. team_feedback

**Row Count:** 6
**RLS Enabled:** Yes
**Purpose:** Team feedback system with threading support

| Column | Type | Nullable | Default | Constraint |
|--------|------|----------|---------|------------|
| id | integer | NO | nextval sequence | Primary key |
| author | text | NO | - | - |
| category | text | YES | - | CHECK: 'works', 'doesnt', 'suggestion' |
| message | text | NO | - | - |
| parent_id | integer | YES | - | FK to team_feedback.id (threading) |
| resolved | boolean | YES | false | - |
| created_at | timestamptz | YES | now() | - |

**Primary Key:** id
**Foreign Key:** parent_id -> team_feedback.id (self-referential for replies)

---

## RPC Functions

### 1. match_knowledge_base (Semantic Search)

**Purpose:** Vector similarity search using embeddings

**Parameters:**
- `query_embedding` - vector(1536) - The embedding to search for
- `match_threshold` - float - Minimum similarity score (0-1)
- `match_count` - integer - Maximum results to return

**Returns:** Table of matching records with similarity scores

```sql
-- Function Logic
SELECT
    kb.id, kb.url, kb.chunk_number, kb.title,
    kb.summary, kb.content, kb.metadata,
    1 - (kb.embedding <=> query_embedding) AS similarity
FROM knowledge_base kb
WHERE
    kb.embedding IS NOT NULL
    AND 1 - (kb.embedding <=> query_embedding) > match_threshold
ORDER BY kb.embedding <=> query_embedding
LIMIT match_count;
```

---

### 2. search_by_text (Full-Text Search)

**Purpose:** PostgreSQL full-text search with ranking

**Parameters:**
- `search_query` - text - Search terms
- `filter_source` - text (optional) - Filter by metadata source
- `match_count` - integer - Maximum results

**Returns:** Table of matching records with relevance rank

```sql
-- Function Logic
SELECT
    kb.id, kb.url, kb.chunk_number, kb.title,
    kb.summary, kb.content, kb.metadata,
    ts_rank(
        to_tsvector('english', kb.title || ' ' || kb.summary || ' ' || kb.content),
        plainto_tsquery('english', search_query)
    ) as rank
FROM knowledge_base kb
WHERE
    (filter_source IS NULL OR kb.metadata->>'source' = filter_source)
    AND to_tsvector('english', ...) @@ plainto_tsquery('english', search_query)
ORDER BY rank DESC
LIMIT match_count;
```

---

### 3. list_knowledge_sources

**Purpose:** Aggregate statistics by source

**Parameters:**
- `filter_source` - text (optional) - Filter to specific source

**Returns:** Source statistics (url_count, chunk_count, latest_update)

```sql
-- Function Logic
SELECT
    kb.metadata->>'source' as source,
    COUNT(DISTINCT kb.url) as url_count,
    COUNT(*) as chunk_count,
    MAX(kb.updated_at) as latest_update
FROM knowledge_base kb
WHERE filter_source IS NULL OR kb.metadata->>'source' = filter_source
GROUP BY kb.metadata->>'source'
ORDER BY chunk_count DESC;
```

---

### 4. get_url_content

**Purpose:** Retrieve all chunks for a specific URL

**Parameters:**
- `target_url` - text - The URL to retrieve

**Returns:** All chunks ordered by chunk_number

```sql
-- Function Logic
SELECT
    kb.chunk_number, kb.title, kb.summary,
    kb.content, kb.metadata
FROM knowledge_base kb
WHERE kb.url = target_url
ORDER BY kb.chunk_number;
```

---

## Views

**None** - No views exist in the public schema.

---

## Installed Extensions

| Extension | Version | Schema | Purpose |
|-----------|---------|--------|---------|
| vector | 0.8.0 | public | pgvector for embeddings & similarity search |
| pg_graphql | 1.5.11 | graphql | GraphQL API support |
| supabase_vault | 0.3.1 | vault | Secrets management |
| uuid-ossp | 1.1 | extensions | UUID generation |
| pgcrypto | 1.3 | extensions | Cryptographic functions |
| pg_stat_statements | 1.11 | extensions | Query statistics |
| plpgsql | 1.0 | pg_catalog | PL/pgSQL procedural language |

---

## Migrations

| Version | Name | Description |
|---------|------|-------------|
| 20251231185157 | enable_rls_knowledge_base | Enabled Row Level Security on knowledge_base |

---

## Connection Details

```
Host: db.iaxtwrswinygwwwdkvok.supabase.co
API URL: https://iaxtwrswinygwwwdkvok.supabase.co
Region: us-east-1
```

**Credentials Location:** `G:\My Drive\00 - Trajanus USA\00-Command-Center\05-Scripts\.env`

---

*Documentation generated: January 13, 2026*
