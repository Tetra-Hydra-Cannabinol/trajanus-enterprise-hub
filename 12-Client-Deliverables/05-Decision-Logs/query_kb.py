"""
TRAJANUS KNOWLEDGE BASE QUERY TOOL
Any Claude instance can run this to query the knowledge base
"""

import os
import sys
import io
import argparse
from pathlib import Path

# Force UTF-8 encoding for Windows compatibility (MUST be before any print statements)
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from dotenv import load_dotenv
from openai import OpenAI
from supabase import create_client, Client
import json

# Load environment - try multiple locations
script_dir = Path(__file__).parent
env_paths = [
    script_dir / '.env',                    # Same directory as script
    script_dir.parent / '.env',             # Parent directory
    Path(r'G:\My Drive\00 - Trajanus USA\00-Command-Center\.env'),  # Explicit fallback
]

env_loaded = False
for env_path in env_paths:
    if env_path.exists():
        load_dotenv(env_path, override=True)
        env_loaded = True
        break

if not env_loaded:
    print("[ERROR] No .env file found in expected locations")
    sys.exit(1)

# Validate required environment variables
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY') or os.getenv('SUPABASE_KEY')
OPENAI_KEY = os.getenv('OPENAI_API_KEY')

if not all([SUPABASE_URL, SUPABASE_KEY, OPENAI_KEY]):
    print("[ERROR] Missing required environment variables:")
    print(f"  SUPABASE_URL: {'SET' if SUPABASE_URL else 'MISSING'}")
    print(f"  SUPABASE_KEY: {'SET' if SUPABASE_KEY else 'MISSING'}")
    print(f"  OPENAI_API_KEY: {'SET' if OPENAI_KEY else 'MISSING'}")
    sys.exit(1)

# Initialize clients
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
openai_client = OpenAI(api_key=OPENAI_KEY)

def search_knowledge(query: str, limit: int = 5, threshold: float = 0.3):
    """
    Search knowledge base with semantic similarity
    
    Args:
        query: Natural language search query
        limit: Maximum results to return
        threshold: Minimum similarity score (0-1)
    
    Returns:
        List of relevant documents with similarity scores
    """
    
    print(f"\n[SEARCH] Searching knowledge base for: '{query}'")
    print(f"{'='*70}\n")
    
    # Generate embedding for query
    try:
        response = openai_client.embeddings.create(
            input=query,
            model="text-embedding-3-small"
        )
        query_embedding = response.data[0].embedding
    except Exception as e:
        print(f"[ERROR] Error generating embedding: {e}")
        return []
    
    # Search database using vector similarity
    try:
        # Call the match_knowledge_base function
        result = supabase.rpc(
            'match_knowledge_base',
            {
                'query_embedding': query_embedding,
                'match_threshold': threshold,
                'match_count': limit
            }
        ).execute()
        
        docs = result.data
        
        if not docs:
            print("[INFO] No results found")
            return []
        
        print(f"[OK] Found {len(docs)} results:\n")
        
        for i, doc in enumerate(docs, 1):
            similarity = doc.get('similarity', 0) * 100
            print(f"Result {i}:")
            print(f"  Title: {doc['title']}")
            print(f"  Similarity: {similarity:.1f}%")
            print(f"  Source: {doc['metadata'].get('source', 'Unknown')}")
            print(f"  Content Preview: {doc['content'][:150]}...")
            print()
        
        return docs
        
    except Exception as e:
        print(f"[ERROR] Search error: {e}")
        return []

def get_recent_sessions(limit: int = 5):
    """Get most recent session documents"""
    
    print(f"\n[RECENT] Retrieving {limit} most recent sessions")
    print(f"{'='*70}\n")
    
    try:
        result = supabase.table('knowledge_base')\
            .select('*')\
            .eq('metadata->>source', 'Session History')\
            .order('created_at', desc=True)\
            .limit(limit)\
            .execute()
        
        docs = result.data
        
        if not docs:
            print("[INFO] No sessions found")
            return []

        print(f"[OK] Found {len(docs)} sessions:\n")
        
        for i, doc in enumerate(docs, 1):
            print(f"Session {i}:")
            print(f"  Title: {doc['title']}")
            print(f"  Date: {doc['created_at'][:10]}")
            print(f"  Preview: {doc['content'][:150]}...")
            print()
        
        return docs
        
    except Exception as e:
        print(f"[ERROR] {e}")
        return []

def get_by_source(source: str, limit: int = 10):
    """Get documents from specific source"""

    print(f"\n[SOURCE] Retrieving documents from: {source}")
    print(f"{'='*70}\n")
    
    try:
        result = supabase.table('knowledge_base')\
            .select('*')\
            .eq('metadata->>source', source)\
            .order('created_at', desc=True)\
            .limit(limit)\
            .execute()
        
        docs = result.data
        
        if not docs:
            print(f"[INFO] No documents found for source: {source}")
            return []

        print(f"[OK] Found {len(docs)} documents:\n")
        
        for i, doc in enumerate(docs, 1):
            print(f"Document {i}:")
            print(f"  Title: {doc['title']}")
            print(f"  Preview: {doc['content'][:100]}...")
            print()
        
        return docs
        
    except Exception as e:
        print(f"[ERROR] {e}")
        return []

def list_sources():
    """List all available knowledge sources"""

    print(f"\n[SOURCES] Available Knowledge Sources")
    print(f"{'='*70}\n")
    
    try:
        result = supabase.table('knowledge_base')\
            .select('metadata')\
            .execute()
        
        sources = {}
        for doc in result.data:
            source = doc.get('metadata', {}).get('source', 'Unknown')
            sources[source] = sources.get(source, 0) + 1
        
        for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
            print(f"  {source}: {count} chunks")
        
        print()
        
    except Exception as e:
        print(f"[ERROR] {e}")

def main():
    """Interactive query interface"""

    # Check for command line arguments
    if len(sys.argv) > 1:
        # Parse arguments
        parser = argparse.ArgumentParser(description='Query Trajanus Knowledge Base')
        parser.add_argument('--query', '-q', type=str, help='Search query')
        parser.add_argument('--limit', '-l', type=int, default=5, help='Max results (default: 5)')
        parser.add_argument('--threshold', '-t', type=float, default=0.3, help='Similarity threshold (default: 0.3)')
        parser.add_argument('query_text', nargs='*', help='Query text (alternative to --query)')

        args = parser.parse_args()

        # Determine the query
        if args.query:
            query = args.query
        elif args.query_text:
            query = ' '.join(args.query_text)
            # Remove 'search' if it's the first word
            if query.lower().startswith('search '):
                query = query[7:]
        else:
            print("[ERROR] No query provided. Use --query or provide query text.")
            sys.exit(1)

        search_knowledge(query, limit=args.limit, threshold=args.threshold)
    else:
        # Interactive mode
        print("\n" + "="*70)
        print("TRAJANUS KNOWLEDGE BASE - QUERY TOOL")
        print("="*70)
        
        print("\nCommands:")
        print("  search <query>  - Semantic search")
        print("  recent          - Show recent sessions")
        print("  sources         - List all sources")
        print("  source <name>   - Get docs from source")
        print("  exit            - Quit")
        print()
        
        while True:
            try:
                cmd = input("\nQuery> ").strip()
                
                if not cmd:
                    continue
                
                if cmd.lower() == 'exit':
                    print("\nGoodbye!\n")
                    break
                
                parts = cmd.split(maxsplit=1)
                command = parts[0].lower()
                
                if command == 'search' and len(parts) > 1:
                    search_knowledge(parts[1])
                
                elif command == 'recent':
                    get_recent_sessions()
                
                elif command == 'sources':
                    list_sources()
                
                elif command == 'source' and len(parts) > 1:
                    get_by_source(parts[1])
                
                else:
                    # Default to search
                    search_knowledge(cmd)
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!\n")
                break
            except Exception as e:
                print(f"\n[ERROR] {e}\n")

if __name__ == "__main__":
    main()
