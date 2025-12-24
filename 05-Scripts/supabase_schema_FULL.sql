-- ============================================================================
-- TRAJANUS RAG SYSTEM - SUPABASE SCHEMA
-- ============================================================================
-- Production-ready knowledge base with pgvector for agentic RAG
-- Based on Agentic RAG training transcript architecture
-- Date: December 9, 2025
-- Purpose: Permanent AI memory for Trajanus USA construction management
-- ============================================================================

-- ============================================================================
-- STEP 1: ENABLE PGVECTOR EXTENSION
-- ============================================================================
-- pgvector provides vector similarity search capabilities
-- Required for semantic search with embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================================================
-- STEP 2: CREATE MAIN KNOWLEDGE BASE TABLE
-- ============================================================================
-- This table stores all knowledge chunks with their embeddings
-- Each row represents one chunk of content from a source document
CREATE TABLE IF NOT EXISTS knowledge_base (
    -- Primary key
    id BIGSERIAL PRIMARY KEY,
    
    -- Source tracking
    url TEXT NOT NULL,                    -- Source URL or identifier
    chunk_number INTEGER NOT NULL,        -- Sequential position within source
    
    -- AI-generated metadata for agentic reasoning
    title TEXT NOT NULL,                  -- AI-generated title describing chunk content
    summary TEXT NOT NULL,                -- AI-generated summary for agentic tool selection
    
    -- Content
    content TEXT NOT NULL,                -- Actual text content of chunk
    
    -- Flexible metadata (JSON)
    metadata JSONB NOT NULL DEFAULT '{}', -- source, category, date, etc.
    
    -- Vector embedding for semantic search
    embedding vector(1536),               -- OpenAI text-embedding-3-small dimensions
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Prevent duplicate chunks from same source
    UNIQUE(url, chunk_number)
);

-- ============================================================================
-- STEP 3: CREATE PERFORMANCE INDEXES
-- ============================================================================
-- These indexes speed up common query patterns

-- Index for querying by URL (get all chunks from a source)
CREATE INDEX IF NOT EXISTS idx_knowledge_base_url 
ON knowledge_base(url);

-- GIN index for JSONB metadata queries
CREATE INDEX IF NOT EXISTS idx_knowledge_base_metadata 
ON knowledge_base USING GIN(metadata);

-- Index for filtering by source (metadata->>'source')
CREATE INDEX IF NOT EXISTS idx_knowledge_base_source 
ON knowledge_base((metadata->>'source'));

-- Index for time-based queries (most recent first)
CREATE INDEX IF NOT EXISTS idx_knowledge_base_created_at 
ON knowledge_base(created_at DESC);

-- ============================================================================
-- STEP 4: CREATE VECTOR SIMILARITY INDEX
-- ============================================================================
-- IVFFlat index for fast approximate nearest neighbor search
-- Lists = 100 is good for up to 1M vectors
-- Uses cosine distance (best for normalized embeddings)
CREATE INDEX IF NOT EXISTS idx_knowledge_base_embedding 
ON knowledge_base 
USING ivfflat (embedding vector_cosine_ops) 
WITH (lists = 100);

-- ============================================================================
-- STEP 5: DROP OLD FUNCTIONS (IF THEY EXIST)
-- ============================================================================
-- This ensures clean installation even if schema was partially loaded before
DROP FUNCTION IF EXISTS match_knowledge_base(vector, float, int, text);
DROP FUNCTION IF EXISTS list_knowledge_sources(text);
DROP FUNCTION IF EXISTS get_url_content(text);
DROP FUNCTION IF EXISTS search_by_text(text, text, int);

-- ============================================================================
-- STEP 6: CREATE AGENTIC RAG FUNCTIONS
-- ============================================================================
-- These functions enable multi-tool agentic RAG workflows
-- Agent can decide which tool to use based on the query

-- ----------------------------------------------------------------------------
-- TOOL 1: match_knowledge_base - Vector similarity search
-- ----------------------------------------------------------------------------
-- Primary retrieval tool for semantic search
-- Returns chunks most similar to the query embedding
--
-- Usage: Agent asks "What are NFPA 70 grounding requirements?"
--        Converts to embedding, searches for similar chunks
--
-- Parameters:
--   query_embedding: 1536-dim vector from OpenAI text-embedding-3-small
--   match_threshold: Minimum similarity (0-1), default 0.7
--   match_count: Number of results to return, default 10
--   filter_source: Optional - only search specific source (e.g., "NFPA 70")
CREATE OR REPLACE FUNCTION match_knowledge_base(
    query_embedding vector(1536),
    match_threshold float DEFAULT 0.7,
    match_count int DEFAULT 10,
    filter_source text DEFAULT NULL
)
RETURNS TABLE (
    id bigint,
    url text,
    chunk_number int,
    title text,
    summary text,
    content text,
    metadata jsonb,
    similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        kb.id,
        kb.url,
        kb.chunk_number,
        kb.title,
        kb.summary,
        kb.content,
        kb.metadata,
        1 - (kb.embedding <=> query_embedding) as similarity
    FROM knowledge_base kb
    WHERE 
        (filter_source IS NULL OR kb.metadata->>'source' = filter_source)
        AND kb.embedding IS NOT NULL
        AND 1 - (kb.embedding <=> query_embedding) > match_threshold
    ORDER BY kb.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Example usage:
-- SELECT * FROM match_knowledge_base(
--     query_embedding := (SELECT embedding FROM some_query),
--     match_threshold := 0.8,
--     match_count := 5,
--     filter_source := 'NFPA 70'
-- );

-- ----------------------------------------------------------------------------
-- TOOL 2: list_knowledge_sources - Browse available sources
-- ----------------------------------------------------------------------------
-- Agent can use this to see what knowledge is available
-- Useful when agent needs to decide which source to search
--
-- Usage: Agent asks "What building codes do we have?"
--        Calls this function to see: NFPA 70, IBC 2021, UFC, etc.
--
-- Parameters:
--   filter_source: Optional - get stats for specific source only
CREATE OR REPLACE FUNCTION list_knowledge_sources(
    filter_source text DEFAULT NULL
)
RETURNS TABLE (
    source text,
    url_count bigint,
    chunk_count bigint,
    latest_update timestamp with time zone
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        kb.metadata->>'source' as source,
        COUNT(DISTINCT kb.url) as url_count,
        COUNT(*) as chunk_count,
        MAX(kb.updated_at) as latest_update
    FROM knowledge_base kb
    WHERE filter_source IS NULL OR kb.metadata->>'source' = filter_source
    GROUP BY kb.metadata->>'source'
    ORDER BY chunk_count DESC;
END;
$$;

-- Example usage:
-- SELECT * FROM list_knowledge_sources();
-- Returns: NFPA 70 (500 chunks), IBC 2021 (800 chunks), etc.

-- ----------------------------------------------------------------------------
-- TOOL 3: get_url_content - Read specific document
-- ----------------------------------------------------------------------------
-- Agent can use this to get full content from a specific URL
-- Useful when agent found a relevant source and wants complete content
--
-- Usage: Vector search returns "NFPA 70 Article 250"
--        Agent calls this to get ALL chunks from that article
--
-- Parameters:
--   target_url: The URL to retrieve (could be article, chapter, page)
CREATE OR REPLACE FUNCTION get_url_content(
    target_url text
)
RETURNS TABLE (
    chunk_number int,
    title text,
    summary text,
    content text,
    metadata jsonb
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        kb.chunk_number,
        kb.title,
        kb.summary,
        kb.content,
        kb.metadata
    FROM knowledge_base kb
    WHERE kb.url = target_url
    ORDER BY kb.chunk_number;
END;
$$;

-- Example usage:
-- SELECT * FROM get_url_content('https://nfpa.org/codes/nfpa-70/article-250');
-- Returns: All chunks from that article in order

-- ----------------------------------------------------------------------------
-- TOOL 4: search_by_text - Full-text keyword search
-- ----------------------------------------------------------------------------
-- Alternative to vector search when agent needs exact keyword matching
-- Uses PostgreSQL full-text search (faster than vector for keywords)
--
-- Usage: Agent asks "Find all references to 'conduit size'"
--        Uses this instead of vector search for exact phrase matching
--
-- Parameters:
--   search_query: Keywords or phrase to search for
--   filter_source: Optional - only search specific source
--   match_count: Number of results to return, default 10
CREATE OR REPLACE FUNCTION search_by_text(
    search_query text,
    filter_source text DEFAULT NULL,
    match_count int DEFAULT 10
)
RETURNS TABLE (
    id bigint,
    url text,
    chunk_number int,
    title text,
    summary text,
    content text,
    metadata jsonb,
    rank real
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        kb.id,
        kb.url,
        kb.chunk_number,
        kb.title,
        kb.summary,
        kb.content,
        kb.metadata,
        ts_rank(
            to_tsvector('english', kb.title || ' ' || kb.summary || ' ' || kb.content),
            plainto_tsquery('english', search_query)
        ) as rank
    FROM knowledge_base kb
    WHERE 
        (filter_source IS NULL OR kb.metadata->>'source' = filter_source)
        AND to_tsvector('english', kb.title || ' ' || kb.summary || ' ' || kb.content) @@ plainto_tsquery('english', search_query)
    ORDER BY rank DESC
    LIMIT match_count;
END;
$$;

-- Example usage:
-- SELECT * FROM search_by_text(
--     search_query := 'conduit sizing requirements',
--     filter_source := 'NFPA 70',
--     match_count := 10
-- );

-- ============================================================================
-- STEP 7: ENABLE ROW LEVEL SECURITY
-- ============================================================================
-- Protect data with Supabase auth
ALTER TABLE knowledge_base ENABLE ROW LEVEL SECURITY;

-- Create permissive policy (adjust based on your auth requirements)
CREATE POLICY "Allow all for authenticated users" ON knowledge_base
    FOR ALL USING (true);

-- ============================================================================
-- SCHEMA COMPLETE
-- ============================================================================
-- You now have:
-- ✅ knowledge_base table with vector storage
-- ✅ Performance indexes for fast queries
-- ✅ 4 agentic RAG tools for multi-tool retrieval
-- ✅ Row-level security enabled
--
-- Next steps:
-- 1. Get API keys from Supabase project settings
-- 2. Run crawler to populate knowledge base
-- 3. Test queries with sample data
-- 4. Deploy QCM agent with these tools
-- ============================================================================
