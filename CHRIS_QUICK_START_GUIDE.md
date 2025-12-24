# Chris Bochman - First Week Quick Start

**Welcome to Trajanus USA, Chris!**

This is your accelerated onboarding guide to get you productive in the first 48 hours.

---

## DAY 1: SETUP & ORIENTATION (4-6 hours)

### Morning: Environment Setup

**Step 1: Get Repository Access (15 min)**
```bash
# Bill will add you as collaborator to private repo
# You'll receive email invite
# Accept invite, then:

git clone git@github.com:trajanus-usa/trajanus-enterprise-hub.git
cd trajanus-enterprise-hub
```

**Step 2: Install Dependencies (30 min)**
```bash
# Python backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt --break-system-packages

# Node/Electron frontend
npm install

# PostgreSQL client (for Supabase)
# Mac: brew install postgresql
# Windows: Download from postgresql.org
# Linux: sudo apt install postgresql-client
```

**Step 3: Configure Environment (15 min)**
```bash
# Copy example env file
cp .env.example .env

# Bill will share credentials securely (1Password, LastPass, or email)
# Add to .env file:
SUPABASE_URL=https://[project].supabase.co
SUPABASE_ANON_KEY=[key]
SUPABASE_SERVICE_KEY=[key]
OPENAI_API_KEY=[key]
GOOGLE_DRIVE_CLIENT_ID=[id]
GOOGLE_DRIVE_CLIENT_SECRET=[secret]
```

**Step 4: Test Database Connection (15 min)**
```python
# test_connection.py
from src.backend.database.supabase_client import SupabaseClient

db = SupabaseClient()
print("Testing connection...")

# Get document count
response = db.client.table('documents').select('count').execute()
print(f"Documents in database: {len(response.data)}")

# Test vector search
embedding = [0.1] * 1536  # Dummy embedding
results = db.search_similar(embedding, match_count=5)
print(f"Search returned {len(results)} results")

print("✅ Connection successful!")
```

**Step 5: Run Application (15 min)**
```bash
# Start Electron app
npm run dev

# App should open showing Trajanus Enterprise Hub
# You'll see multiple workspace buttons
# Click around to see what Bill has built
```

### Afternoon: Code Review

**Step 6: Review Current Codebase (2 hours)**

**Read these files in order:**
1. `README.md` - Project overview
2. `ARCHITECTURE.md` - System architecture
3. `docs/04-Domain-Knowledge/BILLS_POV.md` - Understand Bill's methodology
4. `src/backend/database/supabase_client.py` - Current DB layer
5. `database/schema/supabase_schema.sql` - Database structure

**Make notes on:**
- What looks good
- What could be optimized
- What's missing
- Questions for Bill

**Step 7: First Commit (30 min)**

```bash
# Create branch for your first improvement
git checkout -b improvement/database-connection-pooling

# Make a small improvement (example: add connection pooling)
# Edit src/backend/database/supabase_client.py

# Commit
git add .
git commit -m "feat(database): add connection pooling for performance

- Implement PostgreSQL connection pool
- Max 10 connections, min 2
- Reduces connection overhead by ~40%"

# Push
git push origin improvement/database-connection-pooling

# Create PR on GitHub
# Add Bill as reviewer
```

---

## DAY 2: FIRST CONTRIBUTIONS (4-6 hours)

### Morning: Database Optimization

**Priority 1: Add Indexes (2 hours)**

Current schema needs these performance improvements:

```sql
-- database/migrations/004_performance_indexes.sql

-- Improve vector similarity search
CREATE INDEX CONCURRENTLY idx_documents_embedding_ivfflat
ON documents USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Composite indexes for filtered searches
CREATE INDEX idx_documents_category_type ON documents (category, doc_type);
CREATE INDEX idx_documents_created_category ON documents (created_at DESC, category);

-- Full-text search optimization
CREATE INDEX idx_documents_content_gin ON documents USING gin(to_tsvector('english', content));
```

**Test performance improvement:**
```python
import time

# Before index
start = time.time()
results = db.search_similar(embedding, match_count=10)
end = time.time()
print(f"Search time before index: {(end-start)*1000:.2f}ms")

# Apply index
# Run migration

# After index
start = time.time()
results = db.search_similar(embedding, match_count=10)
end = time.time()
print(f"Search time after index: {(end-start)*1000:.2f}ms")
```

**Priority 2: Query Optimization (1 hour)**

Refactor the main search function to use prepared statements:

```python
# src/backend/database/supabase_client.py

def search_similar_optimized(
    self,
    query_embedding: List[float],
    match_threshold: float = 0.7,
    match_count: int = 10
) -> List[Dict[str, Any]]:
    """Optimized search using prepared statement."""
    
    # Use parameterized query for better performance
    query = """
        SELECT 
            id, title, content, category,
            1 - (embedding <=> $1) AS similarity,
            metadata
        FROM documents
        WHERE 1 - (embedding <=> $1) > $2
        ORDER BY embedding <=> $1
        LIMIT $3
    """
    
    # Execute with parameters
    response = self.client.rpc('execute_query', {
        'query': query,
        'params': [query_embedding, match_threshold, match_count]
    }).execute()
    
    return response.data
```

### Afternoon: Integration Testing

**Priority 3: Create Test Suite (2 hours)**

```python
# tests/integration/test_database.py
import pytest
from src.backend.database.supabase_client import SupabaseClient
from src.backend.services.embedding_service import EmbeddingService

@pytest.fixture
def db_client():
    return SupabaseClient()

@pytest.fixture
def embedding_service(db_client):
    return EmbeddingService(db_client)

def test_connection(db_client):
    """Test database connection."""
    response = db_client.client.table('documents').select('count').limit(1).execute()
    assert response.data is not None

def test_insert_document(db_client, embedding_service):
    """Test document insertion."""
    embedding = embedding_service.get_embedding("Test document content")
    
    doc = db_client.insert_document(
        title="Test Document",
        content="This is test content",
        embedding=embedding,
        metadata={"test": True},
        doc_type="test",
        category="test",
        file_path="/test/doc.md",
        file_id="test123",
        mime_type="text/markdown"
    )
    
    assert doc['id'] is not None
    assert doc['title'] == "Test Document"
    
    # Cleanup
    db_client.delete_document(doc['id'])

def test_vector_search(db_client, embedding_service):
    """Test semantic similarity search."""
    query_embedding = embedding_service.get_embedding("project management")
    
    results = db_client.search_similar(
        query_embedding=query_embedding,
        match_count=5
    )
    
    assert len(results) > 0
    assert all('similarity' in r for r in results)
    assert all(r['similarity'] > 0 for r in results)

def test_embedding_cache(embedding_service):
    """Test embedding cache functionality."""
    text = "This is a test for caching"
    
    # First call - generate embedding
    import time
    start = time.time()
    emb1 = embedding_service.get_embedding(text, use_cache=True)
    time1 = time.time() - start
    
    # Second call - should be cached
    start = time.time()
    emb2 = embedding_service.get_embedding(text, use_cache=True)
    time2 = time.time() - start
    
    assert emb1 == emb2
    assert time2 < time1  # Cached call should be faster
```

**Run tests:**
```bash
pytest tests/integration/test_database.py -v
```

---

## WEEK 1 GOALS

**By End of Week 1, you should have:**

- [ ] Development environment fully setup
- [ ] Ran application locally
- [ ] Reviewed all architecture docs
- [ ] Made 3-5 commits
- [ ] Created 2-3 pull requests
- [ ] Optimized database queries
- [ ] Added performance indexes
- [ ] Written integration tests
- [ ] Had 2+ video calls with Bill

**Typical Output:**
- Database query time reduced by 30-50%
- Test coverage for database layer
- Connection pooling implemented
- First feature contribution merged

---

## KEY CONTACTS

**Bill King**
- Email: bill@trajanus-usa.com
- Best time: Morning (9am-12pm EST)
- Response time: Usually same day

**Questions to Ask Bill:**
1. What are the top 3 database pain points?
2. Which features need backend support next?
3. What's the timeline for first client deployment?
4. How do you want to handle database migrations?

---

## RESOURCES

**Essential Reading:**
- `GITHUB_COLLABORATION_SETUP.md` - Complete workflow guide
- `DATABASE_ARCHITECTURE_FOR_CHRIS.md` - Your technical spec
- `docs/02-Architecture/SYSTEM_OVERVIEW.md` - High-level architecture
- `docs/04-Domain-Knowledge/BILLS_POV.md` - Bill's methodology

**External Documentation:**
- Supabase Docs: https://supabase.com/docs
- pgvector Guide: https://github.com/pgvector/pgvector
- OpenAI Embeddings: https://platform.openai.com/docs/guides/embeddings
- Anthropic API: https://docs.anthropic.com

**Tools:**
- VS Code (recommended IDE)
- Supabase Dashboard (for DB inspection)
- GitHub Desktop (if you prefer GUI)
- DBeaver (for SQL query testing)

---

## QUICK WINS FOR WEEK 1

**Easy improvements you can make immediately:**

1. **Add Query Logging**
   - Log all database queries with execution time
   - Identify slow queries for optimization

2. **Implement Connection Pooling**
   - Reduce connection overhead
   - Improve concurrent query performance

3. **Add Database Health Checks**
   - Monitor connection status
   - Track query performance metrics

4. **Create Admin Utilities**
   - Script to view database stats
   - Tool to regenerate embeddings
   - Batch document deletion

5. **Optimize Indexes**
   - Add missing indexes
   - Drop unused indexes
   - Tune vector index parameters

---

## NOTES FROM BILL

"Chris - You're joining at a critical time. We've got the foundation built, but the database layer needs your expertise to scale. 

The goal is to go from ~300 documents to 10,000+ while keeping query times under 100ms. I've built the PM domain knowledge and frontend, but I need you to make the backend bulletproof.

We're targeting first client deployment in Q2 2026. That gives us ~6 months to get this production-ready. Your focus: make the database fast, reliable, and scalable.

Looking forward to working with you. Let's build something exceptional.

- Bill"

---

## SUCCESS METRICS

**You'll know you're on track when:**
- Database queries are consistently < 100ms
- Test coverage is > 80% for database layer
- You're committing daily
- Bill is merging your PRs
- You understand the PM domain context
- You're contributing to architecture decisions

---

**Welcome aboard, Chris. Let's build the future of construction PM.**

---

**Document Version:** 1.0  
**Created:** December 18, 2025  
**For:** Chris Bochman, Principal Developer
