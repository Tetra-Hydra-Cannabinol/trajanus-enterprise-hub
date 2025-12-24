-- Trajanus RAG System - Supabase Schema
-- Production-ready knowledge base with pgvector for agentic RAG

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Main knowledge base table
CREATE TABLE IF NOT EXISTS knowledge_base (
    id BIGSERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    chunk_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}',
    embedding vector(1536),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(url, chunk_number)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_knowledge_base_url ON knowledge_base(url);
CREATE INDEX IF NOT EXISTS idx_knowledge_base_metadata ON knowledge_base USING GIN(metadata);
CREATE INDEX IF NOT EXISTS idx_knowledge_base_source ON knowledge_base((metadata->>'source'));
CREATE INDEX IF NOT EXISTS idx_knowledge_base_created_at ON knowledge_base(created_at DESC);

-- Vector similarity index
CREATE INDEX IF NOT EXISTS idx_knowledge_base_embedding ON knowledge_base 
USING ivfflat (embedding vector_cosine_ops) 
WITH (lists = 100);

-- Function for vector similarity search
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

-- Function to list all available sources
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

-- Function to get full content from a specific URL
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

-- Function to search by title/summary (text search for agentic RAG)
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

-- Enable Row Level Security
ALTER TABLE knowledge_base ENABLE ROW LEVEL SECURITY;

-- Create policies (adjust based on your auth setup)
CREATE POLICY "Allow all for authenticated users" ON knowledge_base
    FOR ALL USING (true);
