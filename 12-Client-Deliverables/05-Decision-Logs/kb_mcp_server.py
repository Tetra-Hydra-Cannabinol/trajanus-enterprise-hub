#!/usr/bin/env python3
"""
Trajanus Knowledge Base MCP Server
Exposes search capabilities to Claude Code via MCP protocol

Updated 2025-12-14: Simplified to use text search (no OpenAI required)
"""

import sys
import json
import os

# Force UTF-8 encoding for Windows compatibility
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
from typing import Dict
from pathlib import Path

# Load .env from parent directory
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Initialize Supabase client
from supabase import create_client

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')  # Use anon key, not service key

if not SUPABASE_URL or not SUPABASE_KEY:
    print(json.dumps({
        'jsonrpc': '2.0',
        'id': 0,
        'error': {
            'code': -32603,
            'message': f'Missing Supabase credentials. URL: {bool(SUPABASE_URL)}, Key: {bool(SUPABASE_KEY)}'
        }
    }), file=sys.stderr)
    sys.exit(1)

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(json.dumps({
        'jsonrpc': '2.0',
        'id': 0,
        'error': {
            'code': -32603,
            'message': f'Failed to create Supabase client: {str(e)}'
        }
    }), file=sys.stderr)
    sys.exit(1)


def search_knowledge_base(query: str, max_results: int = 5) -> Dict:
    """Search knowledge base using text matching (ilike)"""
    try:
        # Use text search with ilike for pattern matching
        # Search across title, summary, and content
        result = supabase.from_('knowledge_base').select(
            'id, url, title, summary, content, metadata, created_at'
        ).or_(
            f'title.ilike.%{query}%,summary.ilike.%{query}%,content.ilike.%{query}%'
        ).limit(max_results).execute()

        # Format results
        formatted_results = []
        for doc in result.data:
            formatted_results.append({
                'title': doc.get('title', 'Untitled'),
                'summary': doc.get('summary', '')[:200] if doc.get('summary') else '',
                'content': doc.get('content', '')[:500] if doc.get('content') else '',
                'url': doc.get('url', ''),
                'metadata': doc.get('metadata', {}),
                'created_at': doc.get('created_at', '')
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


def list_sources(limit: int = 50) -> Dict:
    """List all unique sources/URLs in knowledge base"""
    try:
        result = supabase.from_('knowledge_base').select(
            'url, title, created_at'
        ).order('created_at', desc=True).limit(limit).execute()

        # Deduplicate by URL
        seen_urls = set()
        unique_sources = []
        for doc in result.data:
            url = doc.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_sources.append({
                    'url': url,
                    'title': doc.get('title', 'Untitled'),
                    'created_at': doc.get('created_at', '')
                })

        return {
            'success': True,
            'found': len(unique_sources),
            'sources': unique_sources
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'found': 0,
            'sources': []
        }


def handle_mcp_request(request: Dict) -> Dict:
    """Handle MCP protocol requests"""
    method = request.get('method')
    params = request.get('params', {})

    if method == 'initialize':
        return {
            'protocolVersion': '2024-11-05',
            'capabilities': {
                'tools': {}
            },
            'serverInfo': {
                'name': 'trajanus-kb',
                'version': '1.1.0'
            }
        }

    elif method == 'tools/list':
        return {
            'tools': [
                {
                    'name': 'search_knowledge_base',
                    'description': 'Search Trajanus knowledge base using text matching. Returns relevant documentation, session history, protocols, and code examples based on natural language queries.',
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
                },
                {
                    'name': 'list_knowledge_sources',
                    'description': 'List all document sources in the knowledge base. Shows URLs, titles, and dates.',
                    'inputSchema': {
                        'type': 'object',
                        'properties': {
                            'limit': {
                                'type': 'integer',
                                'description': 'Maximum number of sources to return',
                                'default': 50
                            }
                        }
                    }
                }
            ]
        }

    elif method == 'tools/call':
        tool_name = params.get('name')
        args = params.get('arguments', {})

        if tool_name == 'search_knowledge_base':
            query = args.get('query', '')
            max_results = args.get('max_results', 5)

            result = search_knowledge_base(query, max_results)

            # Format for MCP response
            if result['success']:
                if result['found'] > 0:
                    content = f"Found {result['found']} relevant documents for '{query}':\n\n"
                    for idx, doc in enumerate(result['results'], 1):
                        content += f"## {idx}. {doc['title']}\n"
                        content += f"**URL:** {doc['url']}\n"
                        if doc['summary']:
                            content += f"**Summary:** {doc['summary']}\n"
                        content += f"**Content Preview:** {doc['content'][:300]}...\n\n"
                else:
                    content = f"No documents found matching '{query}'. Try different search terms."
            else:
                content = f"Search failed: {result.get('error', 'Unknown error')}"

            return {
                'content': [
                    {
                        'type': 'text',
                        'text': content
                    }
                ]
            }

        elif tool_name == 'list_knowledge_sources':
            limit = args.get('limit', 50)

            result = list_sources(limit)

            if result['success']:
                content = f"Knowledge Base Sources ({result['found']} unique URLs):\n\n"
                for idx, source in enumerate(result['sources'], 1):
                    content += f"{idx}. {source['title']}\n"
                    content += f"   URL: {source['url']}\n"
                    content += f"   Added: {source['created_at'][:10] if source['created_at'] else 'Unknown'}\n\n"
            else:
                content = f"Failed to list sources: {result.get('error', 'Unknown error')}"

            return {
                'content': [
                    {
                        'type': 'text',
                        'text': content
                    }
                ]
            }

        return {
            'content': [
                {
                    'type': 'text',
                    'text': f"Unknown tool: {tool_name}"
                }
            ]
        }

    elif method == 'notifications/initialized':
        # Client acknowledging initialization - no response needed
        return None

    return {'error': {'code': -32601, 'message': f'Unknown method: {method}'}}


def main():
    """Main MCP server loop - stdio transport"""
    # Handle incoming requests
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            request = json.loads(line)
            response = handle_mcp_request(request)

            # Some notifications don't need responses
            if response is None:
                continue

            output = {
                'jsonrpc': '2.0',
                'id': request.get('id'),
                'result': response
            }

            print(json.dumps(output))
            sys.stdout.flush()

        except json.JSONDecodeError as e:
            print(json.dumps({
                'jsonrpc': '2.0',
                'id': None,
                'error': {
                    'code': -32700,
                    'message': f'Parse error: {str(e)}'
                }
            }))
            sys.stdout.flush()

        except Exception as e:
            print(json.dumps({
                'jsonrpc': '2.0',
                'id': request.get('id') if 'request' in locals() else None,
                'error': {
                    'code': -32603,
                    'message': f'Internal error: {str(e)}'
                }
            }))
            sys.stdout.flush()


if __name__ == "__main__":
    main()
