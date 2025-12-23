# Database Architecture & Backend Services

**For:** Chris Bochman, Principal Developer  
**Date:** December 18, 2025  
**Purpose:** Technical specification for Trajanus Enterprise Hub backend

---

## SYSTEM OVERVIEW

The Trajanus Enterprise Hub uses a cloud-hosted PostgreSQL database (Supabase) with pgvector extension for AI-augmented document retrieval.

**Database Host:** Supabase (PostgreSQL 15+)  
**Vector Search:** pgvector extension  
**Embeddings:** OpenAI text-embedding-3-small (1536 dimensions)  
**Primary Use Case:** RAG (Retrieval Augmented Generation) for construction PM knowledge base

---

## DATABASE SCHEMA

### Current Tables

**documents**
```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536),  -- OpenAI embeddings
    metadata JSONB DEFAULT '{}'::jsonb,
    doc_type VARCHAR(50),     -- 'protocol', 'template', 'guide', etc.
    category VARCHAR(100),    -- '03-Living-Documents', '05-Scripts', etc.
    file_path TEXT,          -- Original Google Drive path
    file_id TEXT UNIQUE,     -- Google Drive file ID
    mime_type VARCHAR(100),
    word_count INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    ingested_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_documents_embedding ON documents USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_documents_doc_type ON documents (doc_type);
CREATE INDEX idx_documents_category ON documents (category);
CREATE INDEX idx_documents_file_id ON documents (file_id);
CREATE INDEX idx_documents_created_at ON documents (created_at DESC);

-- Full-text search index
CREATE INDEX idx_documents_content_fts ON documents USING gin(to_tsvector('english', content));
CREATE INDEX idx_documents_title_fts ON documents USING gin(to_tsvector('english', title));
```

**chunks** (for large document chunking)
```sql
CREATE TABLE chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536),
    token_count INTEGER,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(document_id, chunk_index)
);

CREATE INDEX idx_chunks_document_id ON chunks (document_id);
CREATE INDEX idx_chunks_embedding ON chunks USING ivfflat (embedding vector_cosine_ops);
```

**queries** (for analytics and optimization)
```sql
CREATE TABLE queries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query_text TEXT NOT NULL,
    query_embedding vector(1536),
    results_count INTEGER,
    execution_time_ms INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    user_id TEXT,
    session_id TEXT
);

CREATE INDEX idx_queries_created_at ON queries (created_at DESC);
CREATE INDEX idx_queries_session_id ON queries (session_id);
```

**embeddings_cache** (to avoid re-embedding identical text)
```sql
CREATE TABLE embeddings_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    text_hash VARCHAR(64) UNIQUE NOT NULL,  -- SHA256 of text
    embedding vector(1536),
    model VARCHAR(100) DEFAULT 'text-embedding-3-small',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_accessed TIMESTAMPTZ DEFAULT NOW(),
    access_count INTEGER DEFAULT 1
);

CREATE INDEX idx_embeddings_cache_text_hash ON embeddings_cache (text_hash);
CREATE INDEX idx_embeddings_cache_last_accessed ON embeddings_cache (last_accessed);
```

---

## VECTOR SIMILARITY SEARCH

### Core Query Function

```sql
-- Function for semantic similarity search
CREATE OR REPLACE FUNCTION search_documents(
    query_embedding vector(1536),
    match_threshold float DEFAULT 0.7,
    match_count int DEFAULT 10,
    filter_category text DEFAULT NULL
)
RETURNS TABLE (
    id uuid,
    title text,
    content text,
    category varchar(100),
    similarity float,
    metadata jsonb
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        d.id,
        d.title,
        d.content,
        d.category,
        1 - (d.embedding <=> query_embedding) AS similarity,
        d.metadata
    FROM documents d
    WHERE 
        (filter_category IS NULL OR d.category = filter_category)
        AND (1 - (d.embedding <=> query_embedding)) > match_threshold
    ORDER BY d.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
```

### Hybrid Search (Vector + Full-Text)

```sql
CREATE OR REPLACE FUNCTION hybrid_search(
    query_text text,
    query_embedding vector(1536),
    vector_weight float DEFAULT 0.7,
    fts_weight float DEFAULT 0.3,
    match_count int DEFAULT 10
)
RETURNS TABLE (
    id uuid,
    title text,
    content text,
    category varchar(100),
    combined_score float,
    vector_score float,
    fts_score float
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    WITH vector_results AS (
        SELECT
            d.id,
            d.title,
            d.content,
            d.category,
            1 - (d.embedding <=> query_embedding) AS score
        FROM documents d
        ORDER BY d.embedding <=> query_embedding
        LIMIT match_count * 2
    ),
    fts_results AS (
        SELECT
            d.id,
            ts_rank(
                to_tsvector('english', d.content),
                plainto_tsquery('english', query_text)
            ) AS score
        FROM documents d
        WHERE to_tsvector('english', d.content) @@ plainto_tsquery('english', query_text)
    )
    SELECT
        vr.id,
        vr.title,
        vr.content,
        vr.category,
        (vr.score * vector_weight + COALESCE(fr.score * fts_weight, 0)) AS combined_score,
        vr.score AS vector_score,
        COALESCE(fr.score, 0) AS fts_score
    FROM vector_results vr
    LEFT JOIN fts_results fr ON vr.id = fr.id
    ORDER BY combined_score DESC
    LIMIT match_count;
END;
$$;
```

---

## PYTHON BACKEND SERVICES

### Database Client (supabase_client.py)

```python
from supabase import create_client, Client
from typing import List, Dict, Any, Optional
import os
from datetime import datetime

class SupabaseClient:
    """Manages connection to Supabase database."""
    
    def __init__(self):
        self.url = os.getenv('SUPABASE_URL')
        self.key = os.getenv('SUPABASE_ANON_KEY')
        self.client: Client = create_client(self.url, self.key)
    
    def insert_document(
        self,
        title: str,
        content: str,
        embedding: List[float],
        metadata: Dict[str, Any],
        doc_type: str,
        category: str,
        file_path: str,
        file_id: str,
        mime_type: str
    ) -> Dict[str, Any]:
        """
        Insert a document with its embedding.
        
        Args:
            title: Document title
            content: Full document text
            embedding: 1536-dimension embedding vector
            metadata: Additional metadata as dict
            doc_type: Type classification
            category: Folder category
            file_path: Original file path
            file_id: Google Drive file ID
            mime_type: File MIME type
            
        Returns:
            Inserted document record
        """
        data = {
            'title': title,
            'content': content,
            'embedding': embedding,
            'metadata': metadata,
            'doc_type': doc_type,
            'category': category,
            'file_path': file_path,
            'file_id': file_id,
            'mime_type': mime_type,
            'word_count': len(content.split()),
            'ingested_at': datetime.utcnow().isoformat()
        }
        
        response = self.client.table('documents').insert(data).execute()
        return response.data[0]
    
    def search_similar(
        self,
        query_embedding: List[float],
        match_threshold: float = 0.7,
        match_count: int = 10,
        filter_category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Semantic similarity search using vector embeddings.
        
        Args:
            query_embedding: Query embedding vector
            match_threshold: Minimum similarity score (0-1)
            match_count: Maximum results to return
            filter_category: Optional category filter
            
        Returns:
            List of matching documents with similarity scores
        """
        # Call RPC function
        response = self.client.rpc(
            'search_documents',
            {
                'query_embedding': query_embedding,
                'match_threshold': match_threshold,
                'match_count': match_count,
                'filter_category': filter_category
            }
        ).execute()
        
        return response.data
    
    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve document by UUID."""
        response = self.client.table('documents').select('*').eq('id', doc_id).execute()
        return response.data[0] if response.data else None
    
    def update_document_embedding(self, doc_id: str, embedding: List[float]) -> Dict[str, Any]:
        """Update document embedding (for re-embedding)."""
        response = self.client.table('documents').update({
            'embedding': embedding,
            'updated_at': datetime.utcnow().isoformat()
        }).eq('id', doc_id).execute()
        return response.data[0]
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete document by UUID."""
        response = self.client.table('documents').delete().eq('id', doc_id).execute()
        return len(response.data) > 0
```

### Embedding Service (embedding_service.py)

```python
from openai import OpenAI
from typing import List, Optional
import hashlib
import os

class EmbeddingService:
    """Generates embeddings using OpenAI API with caching."""
    
    def __init__(self, db_client):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "text-embedding-3-small"
        self.db = db_client
    
    def _text_hash(self, text: str) -> str:
        """Generate SHA256 hash of text for caching."""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()
    
    def get_embedding(self, text: str, use_cache: bool = True) -> List[float]:
        """
        Generate embedding for text with optional caching.
        
        Args:
            text: Input text
            use_cache: Whether to check/store in cache
            
        Returns:
            1536-dimension embedding vector
        """
        if use_cache:
            text_hash = self._text_hash(text)
            
            # Check cache
            cached = self.db.client.table('embeddings_cache')\
                .select('embedding')\
                .eq('text_hash', text_hash)\
                .execute()
            
            if cached.data:
                # Update access count
                self.db.client.table('embeddings_cache')\
                    .update({'access_count': cached.data[0]['access_count'] + 1})\
                    .eq('text_hash', text_hash)\
                    .execute()
                
                return cached.data[0]['embedding']
        
        # Generate new embedding
        response = self.client.embeddings.create(
            input=text,
            model=self.model
        )
        
        embedding = response.data[0].embedding
        
        if use_cache:
            # Store in cache
            self.db.client.table('embeddings_cache').insert({
                'text_hash': text_hash,
                'embedding': embedding,
                'model': self.model
            }).execute()
        
        return embedding
    
    def batch_embed(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts efficiently."""
        response = self.client.embeddings.create(
            input=texts,
            model=self.model
        )
        
        return [item.embedding for item in response.data]
```

### RAG Engine (rag_engine.py)

```python
from typing import List, Dict, Any, Optional
import anthropic
import os

class RAGEngine:
    """Retrieval Augmented Generation engine."""
    
    def __init__(self, db_client, embedding_service):
        self.db = db_client
        self.embeddings = embedding_service
        self.claude = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    def query(
        self,
        question: str,
        num_results: int = 5,
        category_filter: Optional[str] = None,
        include_context: bool = True
    ) -> Dict[str, Any]:
        """
        Execute RAG query: embed question, search similar docs, generate answer.
        
        Args:
            question: User's question
            num_results: Number of documents to retrieve
            category_filter: Optional category filter
            include_context: Whether to return source documents
            
        Returns:
            Dict with answer, sources, and metadata
        """
        # Generate query embedding
        query_embedding = self.embeddings.get_embedding(question)
        
        # Semantic search
        results = self.db.search_similar(
            query_embedding=query_embedding,
            match_count=num_results,
            filter_category=category_filter
        )
        
        if not results:
            return {
                'answer': 'No relevant documents found in knowledge base.',
                'sources': [],
                'confidence': 0.0
            }
        
        # Build context from results
        context_parts = []
        for i, doc in enumerate(results):
            context_parts.append(f"[Document {i+1}]")
            context_parts.append(f"Title: {doc['title']}")
            context_parts.append(f"Content: {doc['content'][:1000]}...")  # Truncate
            context_parts.append(f"Similarity: {doc['similarity']:.3f}")
            context_parts.append("")
        
        context = "\n".join(context_parts)
        
        # Generate answer with Claude
        message = self.claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": f"""Based on the following documents from the Trajanus knowledge base, answer the question.

QUESTION: {question}

DOCUMENTS:
{context}

Provide a clear, concise answer based on the documents. If the documents don't contain enough information to answer fully, say so."""
            }]
        )
        
        answer = message.content[0].text
        
        return {
            'answer': answer,
            'sources': results if include_context else [],
            'confidence': max([doc['similarity'] for doc in results]),
            'num_sources': len(results)
        }
```

---

## PERFORMANCE OPTIMIZATION

### Connection Pooling

```python
from psycopg2 import pool
import os

class DatabasePool:
    """PostgreSQL connection pool for high-performance queries."""
    
    def __init__(self, minconn=1, maxconn=10):
        self.pool = pool.ThreadedConnectionPool(
            minconn,
            maxconn,
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT', 5432)
        )
    
    def get_connection(self):
        """Get connection from pool."""
        return self.pool.getconn()
    
    def return_connection(self, conn):
        """Return connection to pool."""
        self.pool.putconn(conn)
    
    def close_all(self):
        """Close all connections."""
        self.pool.closeall()
```

### Query Optimization Tips

**1. Use appropriate indexes:**
```sql
-- For vector similarity
CREATE INDEX USING ivfflat WITH (lists = 100);

-- For filtering
CREATE INDEX ON documents (category, doc_type);

-- For time-based queries
CREATE INDEX ON documents (created_at DESC);
```

**2. Limit result sets:**
```python
# Don't retrieve entire content if not needed
query = "SELECT id, title, embedding FROM documents"

# Use LIMIT
query += " LIMIT 100"
```

**3. Cache embeddings:**
```python
# Avoid re-embedding identical queries
embedding = cache.get(query) or generate_embedding(query)
```

**4. Batch operations:**
```python
# Insert multiple documents in one transaction
db.insert_many(documents)  # Better than loop of insert_one
```

---

## MIGRATION STRATEGY

### Version Control for Schema

```sql
-- migrations/001_initial_schema.sql
CREATE TABLE documents (...);
CREATE INDEX ...;

-- migrations/002_add_chunks_table.sql
CREATE TABLE chunks (...);

-- migrations/003_add_embeddings_cache.sql
CREATE TABLE embeddings_cache (...);
```

### Migration Script

```python
# scripts/run_migrations.py
import psycopg2
import os
from pathlib import Path

def run_migrations():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    cursor = conn.cursor()
    
    # Track migrations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version INTEGER PRIMARY KEY,
            applied_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    
    # Get applied migrations
    cursor.execute("SELECT version FROM schema_migrations")
    applied = set(row[0] for row in cursor.fetchall())
    
    # Run pending migrations
    migration_dir = Path('database/migrations')
    for migration_file in sorted(migration_dir.glob('*.sql')):
        version = int(migration_file.stem.split('_')[0])
        
        if version not in applied:
            print(f"Applying migration {version}...")
            with open(migration_file) as f:
                cursor.execute(f.read())
            
            cursor.execute(
                "INSERT INTO schema_migrations (version) VALUES (%s)",
                (version,)
            )
            conn.commit()
            print(f"Migration {version} applied.")
    
    cursor.close()
    conn.close()
```

---

## MONITORING & MAINTENANCE

### Query Performance Monitoring

```sql
-- Create query stats table
CREATE TABLE query_stats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query_type VARCHAR(50),
    execution_time_ms INTEGER,
    rows_returned INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Log slow queries
CREATE OR REPLACE FUNCTION log_query_stats(
    query_type text,
    execution_time integer,
    rows_returned integer
)
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO query_stats (query_type, execution_time_ms, rows_returned)
    VALUES (query_type, execution_time, rows_returned);
END;
$$;
```

### Database Health Checks

```python
def check_database_health(db_client):
    """Run health checks on database."""
    results = {
        'connection': False,
        'document_count': 0,
        'avg_query_time': 0,
        'index_usage': {}
    }
    
    try:
        # Test connection
        db_client.client.table('documents').select('count').limit(1).execute()
        results['connection'] = True
        
        # Get document count
        count_response = db_client.client.table('documents').select('count').execute()
        results['document_count'] = len(count_response.data)
        
        # Get average query time
        stats = db_client.client.table('query_stats')\
            .select('execution_time_ms')\
            .limit(100)\
            .execute()
        
        if stats.data:
            avg = sum(s['execution_time_ms'] for s in stats.data) / len(stats.data)
            results['avg_query_time'] = avg
        
    except Exception as e:
        results['error'] = str(e)
    
    return results
```

---

## BACKUP & RECOVERY

### Automated Backups

```bash
#!/bin/bash
# scripts/backup_database.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
DB_NAME="trajanus"

# Create backup
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME -F c -f "$BACKUP_DIR/trajanus_$DATE.dump"

# Keep only last 30 days
find $BACKUP_DIR -name "trajanus_*.dump" -mtime +30 -delete

echo "Backup completed: trajanus_$DATE.dump"
```

### Restore Procedure

```bash
#!/bin/bash
# scripts/restore_database.sh

BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: ./restore_database.sh <backup_file>"
    exit 1
fi

pg_restore -h $DB_HOST -U $DB_USER -d $DB_NAME -c $BACKUP_FILE

echo "Database restored from $BACKUP_FILE"
```

---

## SECURITY CONSIDERATIONS

### Row-Level Security (Future)

```sql
-- Enable RLS
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own documents
CREATE POLICY user_documents ON documents
    FOR SELECT
    USING (metadata->>'owner_id' = current_user);

-- Policy: Admins can see everything
CREATE POLICY admin_documents ON documents
    FOR ALL
    USING (current_user IN (SELECT id FROM admin_users));
```

### API Key Management

```python
# Store API keys securely
from cryptography.fernet import Fernet

class SecureKeyManager:
    def __init__(self, master_key):
        self.cipher = Fernet(master_key)
    
    def encrypt_key(self, key: str) -> bytes:
        return self.cipher.encrypt(key.encode())
    
    def decrypt_key(self, encrypted_key: bytes) -> str:
        return self.cipher.decrypt(encrypted_key).decode()
```

---

## NEXT STEPS FOR CHRIS

**Immediate:**
1. Review current Supabase schema
2. Optimize vector similarity queries
3. Implement connection pooling
4. Add query performance logging

**Short Term:**
5. Build batch ingestion pipeline
6. Implement hybrid search (vector + FTS)
7. Add caching layer for embeddings
8. Create migration system

**Long Term:**
9. Implement RLS for multi-tenant
10. Build admin dashboard for DB monitoring
11. Add advanced analytics
12. Optimize for scale (10K+ documents)

---

**This is your domain, Chris. Make it sing.**

---

**Document Version:** 1.0  
**Author:** Bill King  
**For:** Chris Bochman  
**Last Updated:** December 18, 2025
