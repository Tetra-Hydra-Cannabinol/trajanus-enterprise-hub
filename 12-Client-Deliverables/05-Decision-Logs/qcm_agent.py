"""
Trajanus QCM Review Agent - Agentic RAG Implementation
Reviews submittals against building codes with intelligent knowledge retrieval

Based on training transcripts:
- Agentic RAG architecture (multiple tools for reasoning)
- Pydantic AI patterns (dependencies, tools, retries)
- Construction domain knowledge
"""

import os
from typing import Optional, List, Dict
from dataclasses import dataclass
import json

# Pydantic AI
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

# External clients
from openai import OpenAI
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Initialize clients
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
supabase_client: Client = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_SERVICE_KEY')
)

# Models
MODEL = os.getenv('LLM_MODEL', 'gpt-4o')
EMBEDDING_MODEL = "text-embedding-3-small"


@dataclass
class AgentDependencies:
    """
    Dependencies available to QCM Review Agent
    
    These are injected into every tool call, providing
    access to external services and clients
    """
    openai_client: OpenAI
    supabase_client: Client
    source_filter: str = "Building Codes"  # Default knowledge source


# System prompt for QCM Review Agent
SYSTEM_PROMPT = """You are a construction quality control expert specializing in submittal reviews for federal and military construction projects.

Your role:
- Review shop drawings, submittals, and product data
- Check compliance against building codes (NFPA, IBC, UFC, etc.)
- Cite specific code sections and requirements
- Provide clear, actionable findings

Your tools:
1. retrieve_relevant_codes() - Vector search for semantically similar code sections
2. list_available_codes() - Browse all available building codes and standards
3. get_code_content() - Read specific code sections or entire documents
4. search_codes_by_text() - Full-text search for keywords or terms

Approach:
1. Start with basic RAG (retrieve_relevant_codes) for quick semantic search
2. If results inadequate, list available codes to find relevant sources
3. Then get_code_content for detailed sections
4. Always cite specific code sections with exact text
5. Provide professional, structured review findings

Format findings as:
✅ COMPLIANT: [finding] - Reference: [Code Section X.Y.Z]
❌ NON-COMPLIANT: [finding] - Reference: [Code Section X.Y.Z] 
⚠️ CLARIFICATION NEEDED: [finding] - Reference: [Code Section X.Y.Z]
"""

# Create the agent
qcm_agent = Agent(
    model=OpenAIModel(MODEL),
    system_prompt=SYSTEM_PROMPT,
    deps_type=AgentDependencies,
    retries=2  # Retry LLM calls on failure
)


def get_query_embedding(query: str, openai_client: OpenAI) -> List[float]:
    """
    Generate embedding vector for search query
    
    Args:
        query: User's question or search term
        openai_client: OpenAI client instance
        
    Returns:
        Embedding vector (1536 dimensions)
    """
    try:
        response = openai_client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=query
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return [0.0] * 1536


@qcm_agent.tool
async def retrieve_relevant_codes(
    ctx: AgentDependencies,
    query: str,
    match_count: int = 5
) -> str:
    """
    Search knowledge base for relevant building code sections (Basic RAG)
    
    Use this tool first for quick semantic search. If results are insufficient,
    use list_available_codes() and get_code_content() for more targeted retrieval.
    
    Args:
        query: Description of what you're looking for
        match_count: Number of results to return (default: 5)
        
    Returns:
        Formatted string with relevant code sections
    """
    try:
        # Get query embedding
        query_embedding = get_query_embedding(query, ctx.openai_client)
        
        # Perform vector search
        result = ctx.supabase_client.rpc(
            'match_knowledge_base',
            {
                'query_embedding': query_embedding,
                'match_count': match_count,
                'filter_source': ctx.source_filter
            }
        ).execute()
        
        if not result.data:
            return "No relevant code sections found. Try list_available_codes() to browse sources."
        
        # Format results
        formatted = []
        for i, item in enumerate(result.data, 1):
            formatted.append(f"""
RESULT {i}:
Source: {item['url']}
Title: {item['title']}
Summary: {item['summary']}
Similarity: {item['similarity']:.2%}

Content:
{item['content']}
---
""")
        
        return "\n".join(formatted)
        
    except Exception as e:
        return f"Error retrieving codes: {str(e)}"


@qcm_agent.tool
async def list_available_codes(
    ctx: AgentDependencies
) -> str:
    """
    List all available building codes and standards in knowledge base
    
    Use this tool to browse what codes are available, then use get_code_content()
    to read specific sections. Useful when basic RAG doesn't find what you need.
    
    Returns:
        List of all available code URLs with metadata
    """
    try:
        result = ctx.supabase_client.rpc(
            'list_knowledge_sources',
            {'filter_source': ctx.source_filter}
        ).execute()
        
        if not result.data:
            return "No codes found in knowledge base."
        
        # Format as browsable list
        formatted = ["AVAILABLE BUILDING CODES AND STANDARDS:\n"]
        for item in result.data:
            formatted.append(f"""
• {item['url']}
  Source: {item['source']}
  Chunks: {item['chunk_count']}
  Last Updated: {item['latest_update']}
""")
        
        return "\n".join(formatted)
        
    except Exception as e:
        return f"Error listing codes: {str(e)}"


@qcm_agent.tool
async def get_code_content(
    ctx: AgentDependencies,
    url: str
) -> str:
    """
    Get full content from specific building code URL
    
    Use this after list_available_codes() to read detailed sections.
    Returns all chunks for the specified URL in order.
    
    Args:
        url: Exact URL from list_available_codes() results
        
    Returns:
        Full content of the code document
    """
    try:
        result = ctx.supabase_client.rpc(
            'get_url_content',
            {
                'target_url': url,
                'filter_source': ctx.source_filter
            }
        ).execute()
        
        if not result.data:
            return f"No content found for URL: {url}"
        
        # Format with section markers
        formatted = [f"CONTENT FROM: {url}\n"]
        for chunk in result.data:
            formatted.append(f"""
--- SECTION {chunk['chunk_number']} ---
Title: {chunk['title']}
Summary: {chunk['summary']}

{chunk['content']}
""")
        
        return "\n".join(formatted)
        
    except Exception as e:
        return f"Error getting code content: {str(e)}"


@qcm_agent.tool
async def search_codes_by_text(
    ctx: AgentDependencies,
    search_terms: str,
    match_count: int = 5
) -> str:
    """
    Full-text search across all building codes (alternative to vector search)
    
    Use when you know specific keywords or phrases but vector search isn't working.
    Searches titles, summaries, and content for exact term matches.
    
    Args:
        search_terms: Keywords or phrases to search for
        match_count: Number of results to return (default: 5)
        
    Returns:
        Matching code sections with relevance ranking
    """
    try:
        result = ctx.supabase_client.rpc(
            'search_by_text',
            {
                'search_query': search_terms,
                'filter_source': ctx.source_filter,
                'match_count': match_count
            }
        ).execute()
        
        if not result.data:
            return f"No results found for: {search_terms}"
        
        # Format results
        formatted = [f"TEXT SEARCH RESULTS FOR: '{search_terms}'\n"]
        for i, item in enumerate(result.data, 1):
            formatted.append(f"""
RESULT {i}:
Source: {item['url']}
Title: {item['title']}
Relevance: {item['rank']:.4f}

Content:
{item['content']}
---
""")
        
        return "\n".join(formatted)
        
    except Exception as e:
        return f"Error searching codes: {str(e)}"


# Convenience functions for different use cases
async def review_submittal(
    submittal_text: str,
    submittal_type: str = "General",
    required_codes: Optional[List[str]] = None
) -> str:
    """
    Review submittal against building codes
    
    Args:
        submittal_text: Extracted text from submittal PDF/document
        submittal_type: Type (e.g., "Electrical", "Structural", "Mechanical")
        required_codes: Optional list of specific codes to check against
        
    Returns:
        Formatted review with findings and code citations
    """
    # Create dependencies
    deps = AgentDependencies(
        openai_client=openai_client,
        supabase_client=supabase_client
    )
    
    # Build prompt
    prompt = f"""Review this {submittal_type} submittal for code compliance:

SUBMITTAL CONTENT:
{submittal_text}
"""
    
    if required_codes:
        prompt += f"\nREQUIRED CODES TO CHECK: {', '.join(required_codes)}"
    
    prompt += """

Provide comprehensive review with:
1. Summary of submittal
2. Applicable codes identified
3. Detailed findings (compliant, non-compliant, clarifications needed)
4. Specific code citations for each finding
5. Recommendations

Use your tools strategically to find relevant code sections.
"""
    
    # Run agent
    result = await qcm_agent.run(prompt, deps=deps)
    return result.data


async def answer_code_question(question: str) -> str:
    """
    Answer general questions about building codes
    
    Args:
        question: User's question about codes or standards
        
    Returns:
        Answer with code references
    """
    deps = AgentDependencies(
        openai_client=openai_client,
        supabase_client=supabase_client
    )
    
    result = await qcm_agent.run(question, deps=deps)
    return result.data


# Example usage
if __name__ == "__main__":
    import asyncio
    
    # Example 1: Answer code question
    async def test_question():
        question = "What are the requirements for electrical conduit sizing per NFPA 70?"
        response = await answer_code_question(question)
        print(response)
    
    # Example 2: Review submittal
    async def test_review():
        submittal = """
        SHOP DRAWING SUBMITTAL
        Project: SOUTHCOM Guatemala
        Item: Electrical Conduit - 2" EMT
        
        Proposed conduit: 2-inch EMT with 4x #10 THHN conductors
        Installation: Surface mounted in mechanical room
        Supports: 8-foot intervals with rigid straps
        """
        
        response = await review_submittal(
            submittal_text=submittal,
            submittal_type="Electrical",
            required_codes=["NFPA 70", "IBC 2021"]
        )
        print(response)
    
    # Run tests
    asyncio.run(test_question())
    # asyncio.run(test_review())
