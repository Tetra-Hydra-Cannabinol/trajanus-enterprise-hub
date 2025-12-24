#!/usr/bin/env python3
"""
Trajanus Knowledge Base MCP Server - HTTP/SSE Transport
Exposes semantic search to web chat via HTTP MCP protocol
"""

from flask import Flask, request, Response, stream_with_context
from flask_cors import CORS
import json
import os
from typing import List, Dict
from openai import OpenAI
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for web chat access

# Initialize clients
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_SERVICE_KEY')
)

EMBEDDING_MODEL = "text-embedding-3-small"
SIMILARITY_THRESHOLD = 0.3


def generate_embedding(text: str) -> List[float]:
    """Generate OpenAI embedding for query"""
    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding


def search_knowledge_base(query: str, max_results: int = 5) -> Dict:
    """Search knowledge base using vector similarity"""
    try:
        # Generate embedding
        query_embedding = generate_embedding(query)
        
        # Call Supabase function
        result = supabase.rpc(
            'match_knowledge_base',
            {
                'query_embedding': query_embedding,
                'match_threshold': SIMILARITY_THRESHOLD,
                'match_count': max_results
            }
        ).execute()
        
        # Format results
        formatted_results = []
        for doc in result.data:
            formatted_results.append({
                'title': doc['title'],
                'similarity': f"{doc['similarity'] * 100:.1f}%",
                'content': doc['content'],
                'source': doc.get('metadata', {}).get('source', 'Unknown'),
                'url': doc.get('url', '')
            })
        
        return {
            'success': True,
            'query': query,
            'found': len(formatted_results),
            'results': formatted_results
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'query': query,
            'found': 0,
            'results': []
        }


@app.route('/sse', methods=['GET'])
def sse_endpoint():
    """SSE endpoint for MCP protocol"""
    
    def generate():
        # Send initialization
        init_msg = {
            'jsonrpc': '2.0',
            'id': 0,
            'result': {
                'protocolVersion': '2024-11-05',
                'capabilities': {
                    'tools': {}
                },
                'serverInfo': {
                    'name': 'trajanus-kb-http',
                    'version': '1.0.0'
                }
            }
        }
        yield f"data: {json.dumps(init_msg)}\n\n"
        
        # Keep connection alive
        while True:
            yield f": keepalive\n\n"
            import time
            time.sleep(30)
    
    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )


@app.route('/message', methods=['POST'])
def message_endpoint():
    """Handle MCP requests via POST"""
    try:
        data = request.json
        method = data.get('method')
        params = data.get('params', {})
        request_id = data.get('id')
        
        if method == 'tools/list':
            response = {
                'jsonrpc': '2.0',
                'id': request_id,
                'result': {
                    'tools': [
                        {
                            'name': 'search_knowledge_base',
                            'description': 'Search Trajanus knowledge base using semantic similarity. Returns relevant documentation, session history, protocols, and code examples based on natural language queries.',
                            'inputSchema': {
                                'type': 'object',
                                'properties': {
                                    'query': {
                                        'type': 'string',
                                        'description': 'Natural language search query (e.g., "December 9 accomplishments", "RAG system setup", "QCM workflow")'
                                    },
                                    'max_results': {
                                        'type': 'integer',
                                        'description': 'Maximum number of results to return (1-20)',
                                        'default': 5
                                    }
                                },
                                'required': ['query']
                            }
                        }
                    ]
                }
            }
            return json.dumps(response)
        
        elif method == 'tools/call':
            tool_name = params.get('name')
            args = params.get('arguments', {})
            
            if tool_name == 'search_knowledge_base':
                query = args.get('query')
                max_results = args.get('max_results', 5)
                
                result = search_knowledge_base(query, max_results)
                
                # Format for MCP response
                if result['success']:
                    content = f"Found {result['found']} relevant documents:\n\n"
                    for idx, doc in enumerate(result['results'], 1):
                        content += f"{idx}. {doc['title']} (Similarity: {doc['similarity']})\n"
                        content += f"   Source: {doc['source']}\n"
                        content += f"   Content: {doc['content'][:200]}...\n\n"
                else:
                    content = f"Search failed: {result.get('error', 'Unknown error')}"
                
                response = {
                    'jsonrpc': '2.0',
                    'id': request_id,
                    'result': {
                        'content': [
                            {
                                'type': 'text',
                                'text': content
                            }
                        ]
                    }
                }
                return json.dumps(response)
        
        return json.dumps({
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {
                'code': -32601,
                'message': 'Method not found'
            }
        })
        
    except Exception as e:
        return json.dumps({
            'jsonrpc': '2.0',
            'id': request.json.get('id') if request.json else None,
            'error': {
                'code': -32603,
                'message': str(e)
            }
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return json.dumps({'status': 'healthy', 'server': 'trajanus-kb-http'})


if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    print(f"Starting Trajanus KB MCP Server on port {port}")
    print(f"SSE endpoint: http://localhost:{port}/sse")
    print(f"Message endpoint: http://localhost:{port}/message")
    app.run(host='0.0.0.0', port=port, threaded=True)
