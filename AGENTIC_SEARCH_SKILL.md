# Agentic Search Skill

Use this skill when querying the Knowledge Base for complex, multi-step information retrieval.

## Agentic vs Simple RAG

Simple RAG: Query → Retrieve → Return
Agentic: Query → Plan → Retrieve → Reason → Retrieve more → Validate → Synthesize

## When to Use Agentic Search

- Multi-source queries (ITE + jurisdiction + site data)
- Report building (Traffic Studies, QCM reviews)
- Cross-referencing requirements against documents
- Any query requiring reasoning over results

## Agentic Search Process

1. **Parse Intent**: What does user actually need?
2. **Plan Retrieval**: Which sources? What order?
3. **Execute Search**: Call match_knowledge_base or search_by_text
4. **Evaluate Results**: Sufficient? Relevant? Conflicting?
5. **Iterate if Needed**: Refine query, search different source
6. **Synthesize**: Combine findings into coherent answer
7. **Validate**: Check against known thresholds/requirements

## Available RPC Functions

- match_knowledge_base(query, threshold 0.3-0.5, count)
- search_by_text(query, filter_source)
- list_knowledge_sources()
- get_url_content(url)

## Trajanus Applications

- Traffic Study Agent: ITE rates → Distribution → Capacity
- QCM Review: Spec requirements → Submittal comparison
- KB Browser: Smart search with reasoning
