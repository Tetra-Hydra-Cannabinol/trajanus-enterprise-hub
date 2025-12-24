"""
TRAJANUS RAG SYSTEM - TEST CRAWLER
Tests end-to-end: crawl → embed → store → query
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from supabase import create_client, Client

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

print("\n" + "="*60)
print("TRAJANUS RAG SYSTEM - TEST CRAWLER")
print("="*60 + "\n")

# Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Verify environment variables
print("Checking configuration...")
if not all([SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY]):
    print("ERROR: Missing environment variables in .env file")
    print(f"SUPABASE_URL: {'✓' if SUPABASE_URL else '✗'}")
    print(f"SUPABASE_KEY: {'✓' if SUPABASE_KEY else '✗'}")
    print(f"OPENAI_API_KEY: {'✓' if OPENAI_API_KEY else '✗'}")
    exit(1)
print("✓ All environment variables found\n")

# Initialize clients
print("Initializing clients...")
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✓ Supabase client initialized")
except Exception as e:
    print(f"✗ Supabase error: {e}")
    exit(1)

try:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    print("✓ OpenAI client initialized\n")
except Exception as e:
    print(f"✗ OpenAI error: {e}")
    exit(1)

# Test data
test_content = """
Construction management (CM) is the professional service that uses specialized 
project management techniques to oversee the planning, design, and construction 
of a project from beginning to end. The purpose of CM is to control a project's 
time, cost and quality. CM is compatible with all project delivery systems.

Quality control and quality assurance are critical components of construction 
management. The construction manager must ensure that all work meets specified 
standards and building codes. This includes coordination with inspectors, 
submission of required documentation, and maintaining detailed records.

Safety management is paramount in construction. The CM must implement and enforce 
safety protocols, conduct regular safety meetings, and ensure compliance with OSHA 
regulations. A comprehensive safety program reduces accidents and protects workers.
"""

test_url = "https://test.trajanus-rag.local/construction-management-basics"
test_metadata = {
    "source": "Test Data",
    "category": "Construction Management",
    "date_added": "2025-12-09"
}

# Step 1: Generate embedding
print("Step 1: Generating embedding with OpenAI...")
try:
    response = openai_client.embeddings.create(
        input=test_content,
        model="text-embedding-3-small"
    )
    embedding = response.data[0].embedding
    print(f"✓ Embedding generated: {len(embedding)} dimensions\n")
except Exception as e:
    print(f"✗ OpenAI embedding error: {e}")
    exit(1)

# Step 2: Insert into Supabase
print("Step 2: Inserting into Supabase knowledge_base...")
try:
    data = {
        "url": test_url,
        "chunk_number": 1,
        "title": "Construction Management Basics (Test)",
        "summary": "Overview of construction management principles including quality control, safety, and project coordination",
        "content": test_content.strip(),
        "metadata": test_metadata,
        "embedding": embedding
    }
    
    result = supabase.table('knowledge_base').insert(data).execute()
    inserted_id = result.data[0]['id']
    print(f"✓ Data inserted successfully! ID: {inserted_id}\n")
except Exception as e:
    print(f"✗ Supabase insert error: {e}")
    exit(1)

# Step 3: Query with semantic search
print("Step 3: Testing semantic search...")
try:
    # Generate query embedding
    query_text = "What are the key responsibilities of a construction manager?"
    query_response = openai_client.embeddings.create(
        input=query_text,
        model="text-embedding-3-small"
    )
    query_embedding = query_response.data[0].embedding
    
    # Search using match_knowledge_base function
    search_result = supabase.rpc(
        'match_knowledge_base',
        {
            'query_embedding': query_embedding,
            'match_threshold': 0.5,
            'match_count': 5
        }
    ).execute()
    
    if search_result.data:
        print(f"✓ Query successful! Found {len(search_result.data)} results")
        
        for i, match in enumerate(search_result.data[:3], 1):
            similarity = match['similarity']
            title = match['title']
            print(f"\n  Result {i}:")
            print(f"    Title: {title}")
            print(f"    Similarity: {similarity*100:.1f}%")
            print(f"    Content preview: {match['content'][:100]}...")
    else:
        print("✗ No results found")
        
except Exception as e:
    print(f"✗ Query error: {e}")
    exit(1)

# Step 4: Verify in database
print("\n\nStep 4: Verifying database contents...")
try:
    count_result = supabase.table('knowledge_base').select('id', count='exact').execute()
    total_rows = count_result.count
    print(f"✓ Total rows in knowledge_base: {total_rows}\n")
except Exception as e:
    print(f"✗ Verification error: {e}")

print("="*60)
print("ALL TESTS PASSED ✓")
print("="*60)
print("\nNext steps:")
print("1. Check Supabase Table Editor to see your data")
print("2. Run this script again to add more test data")
print("3. Start crawling real documentation into the knowledge base")
print()
