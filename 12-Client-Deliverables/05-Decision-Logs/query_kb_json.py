#!/usr/bin/env python3
"""
Trajanus Knowledge Base Query Tool - JSON Output
Enhanced version for Claude cross-session continuity

Returns structured JSON that Claude can parse and use
to provide seamless continuity across sessions.

Usage:
    python query_kb_json.py <search terms>
    
Example:
    python query_kb_json.py "December 9 2025 RAG system"
"""

import sys
import json
import os
from typing import List, Dict, Optional
from openai import OpenAI
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
EMBEDDING_MODEL = "text-embedding-3-small"
SIMILARITY_THRESHOLD = 0.3
MAX_RESULTS = 5


class KnowledgeBaseQuery:
    """Query interface for Trajanus knowledge base"""
    
    def __init__(self):
        """Initialize clients"""
        if not all([SUPABASE_URL, SUPABASE_SERVICE_KEY, OPENAI_API_KEY]):
            raise ValueError("Missing required environment variables. Check .env file.")
        
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
        self.supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate vector embedding for query text
        
        Args:
            text: Query string to embed
            
        Returns:
            List of 1536 floats (embedding vector)
        """
        try:
            response = self.openai_client.embeddings.create(
                model=EMBEDDING_MODEL,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Embedding generation failed: {str(e)}")
    
    def search(
        self, 
        query: str, 
        max_results: int = MAX_RESULTS,
        threshold: float = SIMILARITY_THRESHOLD
    ) -> Dict:
        """
        Search knowledge base using vector similarity
        
        Args:
            query: Search query text
            max_results: Maximum number of results to return
            threshold: Minimum similarity score (0.0-1.0)
            
        Returns:
            Dictionary with query results in structured format
        """
        
        # Strip "search" prefix if present
        if query.lower().startswith("search "):
            query = query[7:]
        
        try:
            # Generate embedding for query
            query_embedding = self.generate_embedding(query)
            
            # Call Supabase function
            result = self.supabase.rpc(
                'match_knowledge_base',
                {
                    'query_embedding': query_embedding,
                    'match_threshold': threshold,
                    'match_count': max_results
                }
            ).execute()
            
            # Format results
            return {
                'success': True,
                'query': query,
                'threshold': threshold,
                'found': len(result.data),
                'results': [
                    {
                        'id': doc['id'],
                        'title': doc['title'],
                        'similarity': f"{doc['similarity'] * 100:.1f}%",
                        'similarity_score': doc['similarity'],
                        'content': doc['content'],
                        'content_preview': doc['content'][:300] + "..." if len(doc['content']) > 300 else doc['content'],
                        'source': doc.get('metadata', {}).get('source', 'Unknown'),
                        'url': doc.get('url', ''),
                        'chunk_number': doc.get('chunk_number', 0)
                    }
                    for doc in result.data
                ]
            }
            
        except Exception as e:
            return {
                'success': False,
                'query': query,
                'error': str(e),
                'found': 0,
                'results': []
            }


def main():
    """Main entry point"""
    
    # Check arguments
    if len(sys.argv) < 2:
        result = {
            'success': False,
            'error': 'No query provided',
            'usage': 'python query_kb_json.py <search terms>',
            'example': 'python query_kb_json.py "December 9 2025"'
        }
        print(json.dumps(result, indent=2))
        sys.exit(1)
    
    # Get query from arguments
    query = ' '.join(sys.argv[1:])
    
    try:
        # Initialize and search
        kb = KnowledgeBaseQuery()
        results = kb.search(query)
        
        # Output JSON
        print(json.dumps(results, indent=2))
        
        # Exit with appropriate code
        sys.exit(0 if results['success'] else 1)
        
    except Exception as e:
        error_result = {
            'success': False,
            'query': query,
            'error': str(e),
            'found': 0,
            'results': []
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
