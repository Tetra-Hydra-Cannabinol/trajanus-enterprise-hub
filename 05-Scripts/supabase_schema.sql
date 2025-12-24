--
-- Trajanus RAG System - Supabase Schema
-- Production-ready knowledge base with pgvector for agentic RAG
-- Based on Agentic RAG training transcript architecture

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
    embedding vector(1536),  -- OpenAI text-embedding-3-small dimensions
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Composite unique constraint
    UNIQUE(url, chunk_number)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_knowledge_base_url ON knowledge_base(url);
CREATE INDEX IF NOT EXISTS idx_knowledge_base_metadata ON knowledge_base USING GIN(metadata);
CREATE INDEX IF NOT EXISTS idx_knowledge_base_source ON knowledge_base((metadata->>'source'));
CREATE INDEX IF NOT EXISTS idx_knowledge_base_created_at ON knowledge_base(created_at DESC);

-- Vector similarity index (IVFFlat for speed with acceptable accuracy)
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
        1 - (kb.embedding <=> query_embedding) AS similarity
    FROM knowledge_base kb
    WHERE 
        1 - (kb.embedding <=> query_embedding) > match_threshold
        AND (filter_source IS NULL OR kb.metadata->>'source' = filter_source)
    ORDER BY kb.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Function to get all unique URLs (for agentic RAG tool)
CREATE OR REPLACE FUNCTION list_knowledge_sources(
    filter_source text DEFAULT NULL
)
RETURNS TABLE (
    url text,
    chunk_count bigint,
    source text,
    latest_update timestamp with time zone
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        kb.url,
        COUNT(*) AS chunk_count,
        kb.metadata->>'source' AS source,
        MAX(kb.updated_at) AS latest_update
    FROM knowledge_base kb
    WHERE (filter_source IS NULL OR kb.metadata->>'source' = filter_source)
    GROUP BY kb.url, kb.metadata->>'source'
    ORDER BY kb.url;
END;
$$;

-- Function to get content from specific URL (for agentic RAG tool)
CREATE OR REPLACE FUNCTION get_url_content(
    target_url text,
    filter_source text DEFAULT NULL
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
    WHERE 
        kb.url = target_url
        AND (filter_source IS NULL OR kb.metadata->>'source' = filter_source)
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
        ) AS rank
    FROM knowledge_base kb
    WHERE 
        to_tsvector('english', kb.title || ' ' || kb.summary || ' ' || kb.content) @@ 
        plainto_tsquery('english', search_query)
        AND (filter_source IS NULL OR kb.metadata->>'source' = filter_source)
    ORDER BY rank DESC
    LIMIT match_count;
END;
$$;

-- Row Level Security (RLS) Policies
ALTER TABLE knowledge_base ENABLE ROW LEVEL SECURITY;

-- Policy: Allow service role full access
CREATE POLICY "Service role has full access"
ON knowledge_base
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

-- Policy: Allow authenticated users read access
CREATE POLICY "Authenticated users can read"
ON knowledge_base
FOR SELECT
TO authenticated
USING (true);

-- Policy: Allow anon users read access (for public knowledge)
CREATE POLICY "Anon users can read public knowledge"
ON knowledge_base
FOR SELECT
TO anon
USING (metadata->>'public' = 'true');

-- Trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_knowledge_base_updated_at
BEFORE UPDATE ON knowledge_base
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Analytics view for monitoring
CREATE OR REPLACE VIEW knowledge_base_stats AS
SELECT
    metadata->>'source' AS source,
    COUNT(*) AS total_chunks,
    COUNT(DISTINCT url) AS total_urls,
    MIN(created_at) AS first_crawled,
    MAX(updated_at) AS last_updated,
    AVG(LENGTH(content)) AS avg_chunk_size
FROM knowledge_base
GROUP BY metadata->>'source';

-- Grant permissions
GRANT SELECT ON knowledge_base_stats TO authenticated, anon;

-- Comments for documentation
COMMENT ON TABLE knowledge_base IS 'Main knowledge base for Trajanus RAG system';
COMMENT ON COLUMN knowledge_base.url IS 'Source URL where content was crawled from';
COMMENT ON COLUMN knowledge_base.chunk_number IS 'Sequential position within source document';
COMMENT ON COLUMN knowledge_base.title IS 'AI-generated title describing chunk content';
COMMENT ON COLUMN knowledge_base.summary IS 'AI-generated summary for agentic reasoning';
COMMENT ON COLUMN knowledge_base.content IS 'Actual text content of chunk';
COMMENT ON COLUMN knowledge_base.metadata IS 'Flexible JSON for source, category, filters';
COMMENT ON COLUMN knowledge_base.embedding IS 'Vector embedding for semantic search (1536 dims)';

COMMENT ON FUNCTION match_knowledge_base IS 'Vector similarity search for basic RAG';
COMMENT ON FUNCTION list_knowledge_sources IS 'List all URLs for agentic RAG tool';
COMMENT ON FUNCTION get_url_content IS 'Get full content from specific URL for agentic RAG';
COMMENT ON FUNCTION search_by_text IS 'Full-text search for agentic RAG alternative to vector search';
