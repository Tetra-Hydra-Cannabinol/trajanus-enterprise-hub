# Research: Supabase + Agent Orchestration
**Generated:** 2025-12-13
**Researcher:** Knowmad Research Specialist

## Ranked Resources (1 = Most Critical)

---

### 1. Anthropic Python SDK - GitHub Repository
- **Source:** Anthropic (Official)
- **Link:** https://github.com/anthropics/anthropic-sdk-python
- **Type:** Code Repository / Official SDK
- **Description:** The foundational Python SDK for building with Claude. Provides async/sync clients, tool use decorators, streaming helpers, and platform integrations (AWS Bedrock, Google Vertex). Includes 20+ code examples covering messages, streaming, tools, structured outputs, and thinking capabilities. Critical for understanding how to implement agent capabilities.
- **Rank Rationale:** #1 because this is the core technical foundation for all Claude-based agent development in Python. Everything else builds on this.

---

### 2. Building Effective Agents - Anthropic Cookbook Patterns
- **Source:** Anthropic (Official)
- **Link:** https://github.com/anthropics/anthropic-cookbook/tree/main/patterns/agents
- **Type:** Documentation / Jupyter Notebooks
- **Description:** Reference implementation of five core agent patterns: (1) Prompt Chaining, (2) Routing, (3) Parallelization, (4) Orchestrator-Workers, (5) Evaluator-Optimizer. Includes complete Python code with detailed explanations of when to use each pattern, tradeoffs, and real-world examples. Based on Anthropic's research paper on building effective agents.
- **Rank Rationale:** #2 because it provides the architectural blueprints for multi-agent systems. This is the playbook for Claude Prime directing Claude Code directing sub-agents.

---

### 3. Orchestrator-Workers Pattern Implementation
- **Source:** Anthropic Cookbook
- **Link:** https://github.com/anthropics/anthropic-cookbook/blob/main/patterns/agents/orchestrator_workers.ipynb
- **Type:** Jupyter Notebook / Code Example
- **Description:** Complete implementation of the orchestrator-workers pattern where a central LLM analyzes tasks and delegates to specialized worker LLMs. Shows XML-based task parsing, template-based prompts, error handling, and dynamic task breakdown. Demonstrates runtime flexibility where the orchestrator determines optimal subtasks based on context (unlike static parallelization). Perfect model for CP→CC→sub-agent workflows.
- **Rank Rationale:** #3 because this is the exact pattern requested - one agent coordinating multiple specialized agents. Direct application to your architecture.

---

### 4. RAG Implementation with Pinecone (Adaptable to Supabase pgvector)
- **Source:** Anthropic Cookbook
- **Link:** https://github.com/anthropics/anthropic-cookbook/blob/main/third_party/Pinecone/rag_using_pinecone.ipynb
- **Type:** Jupyter Notebook / Code Example
- **Description:** Three-stage RAG architecture: (1) embedding generation with Voyage AI, (2) vector storage/retrieval, (3) LLM answer generation with Claude. Includes batch upload patterns, query optimization with keyword generation, and metadata storage strategies. Provides complete SQL function equivalents for migrating from Pinecone to Supabase pgvector including ivfflat indexing and cosine similarity search.
- **Rank Rationale:** #4 because RAG is critical for agent memory and knowledge retrieval. This shows how to integrate Supabase as the vector database backing Claude agents.

---

### 5. Autonomous Coding Agent (Two-Agent Pattern)
- **Source:** Anthropic Quickstarts
- **Link:** https://github.com/anthropics/anthropic-quickstarts/tree/main/autonomous-coding
- **Type:** Code Repository / Complete Application
- **Description:** Production-ready implementation of a two-agent system: (1) Initializer Agent for project setup and feature planning, (2) Coding Agent for progressive implementation across multiple sessions. Demonstrates session management, git-based progress persistence, security sandboxing, and auto-continuation workflows. Shows how to build long-running autonomous agents that maintain state across sessions.
- **Rank Rationale:** #5 because it's a complete reference architecture for multi-session agent workflows with persistence - critical for understanding how agents coordinate over time.

---

### 6. Anthropic API Fundamentals Course
- **Source:** Anthropic Educational Courses
- **Link:** https://github.com/anthropics/courses/tree/master/anthropic_api_fundamentals
- **Type:** Educational Course / Jupyter Notebooks
- **Description:** Five-course curriculum covering (1) API fundamentals, (2) prompt engineering, (3) real-world prompting, (4) prompt evaluations, (5) tool use. Designed to be completed sequentially, using Claude 3 Haiku for cost-effective learning. Provides foundational knowledge for working with the Claude SDK, writing effective prompts, and implementing tool use patterns.
- **Rank Rationale:** #6 because it provides systematic education on prompt engineering and tool use - essential skills for coordinating agents and optimizing performance.

---

### 7. Prompt Engineering Interactive Tutorial
- **Source:** Anthropic Educational Resources
- **Link:** https://github.com/anthropics/prompt-eng-interactive-tutorial
- **Type:** Interactive Tutorial / Documentation
- **Description:** Comprehensive guide to prompt engineering techniques including role assignment, output formatting, step-by-step thinking (precognition), examples-based learning, and hallucination prevention. Covers basic structure (chapters 1-3), intermediate techniques (4-7), and advanced production patterns (8-9). Includes appendix on chaining prompts, tool use, and search/retrieval patterns for multi-agent coordination.
- **Rank Rationale:** #7 because effective agent orchestration requires mastering prompt engineering. This teaches how to get Claude Prime to provide optimal prompts for Claude Code.

---

### 8. Evaluator-Optimizer Workflow Pattern
- **Source:** Anthropic Cookbook
- **Link:** https://github.com/anthropics/anthropic-cookbook/blob/main/patterns/agents/evaluator_optimizer.ipynb
- **Type:** Jupyter Notebook / Code Example
- **Description:** Iterative improvement loop where one LLM generates solutions while another evaluates against criteria and provides feedback. Demonstrates generate-evaluate cycles, context/memory management, chain-of-thought tracking, and exit conditions. Includes real example of implementing a Stack with O(1) operations, showing refinement from basic implementation to production-quality code with error handling and documentation.
- **Rank Rationale:** #8 because self-improvement patterns are powerful for agent quality control. Useful for ensuring agent outputs meet standards before proceeding.

---

### 9. Basic Multi-LLM Workflow Patterns
- **Source:** Anthropic Cookbook
- **Link:** https://github.com/anthropics/anthropic-cookbook/blob/main/patterns/agents/basic_workflows.ipynb
- **Type:** Jupyter Notebook / Code Example
- **Description:** Three fundamental patterns: (1) Prompt Chaining for sequential refinement, (2) Parallelization for concurrent processing, (3) Routing for specialized handling. Each includes Python implementation with ThreadPoolExecutor for concurrency, XML-based output parsing, and real-world use cases (data pipelines, stakeholder analysis, support ticket routing). Trade-offs analyzed for cost vs latency vs accuracy.
- **Rank Rationale:** #9 because these are the building blocks that combine into more complex orchestration patterns. Start here before implementing orchestrator-workers.

---

### 10. Customer Support Agent with Knowledge Base Integration
- **Source:** Anthropic Quickstarts
- **Link:** https://github.com/anthropics/anthropic-quickstarts/tree/main/customer-support-agent
- **Type:** Code Repository / Complete Application
- **Description:** Full-stack Next.js/TypeScript application integrating Claude with Amazon Bedrock Knowledge Bases for RAG. Shows model switching patterns, environment-based configuration, knowledge base setup, AWS Amplify deployment, and security configurations. Demonstrates real-time thinking display and source visualization. Provides complete architecture for production AI applications with external knowledge retrieval.
- **Rank Rationale:** #10 because it shows production integration patterns between Claude and knowledge bases (similar to Supabase), with deployment and security best practices.

---

### 11. Tool Use Helpers Documentation
- **Source:** Anthropic SDK Documentation
- **Link:** https://github.com/anthropics/anthropic-sdk-python/blob/main/tools.md
- **Type:** Official Documentation
- **Description:** Complete guide to the @beta_tool decorator for defining Python functions Claude can call. Covers automatic JSON schema generation from docstrings, async tool support with @beta_async_tool, and the tool_runner() abstraction for automatic tool execution loops. Shows how tools enable agents to interact with external systems, databases, and APIs - critical for Supabase integration.
- **Rank Rationale:** #11 because tool use is how agents interact with Supabase. This is essential for connecting agents to your database and external services.

---

### 12. Message Streaming Helpers Documentation
- **Source:** Anthropic SDK Documentation
- **Link:** https://github.com/anthropics/anthropic-sdk-python/blob/main/helpers.md
- **Type:** Official Documentation
- **Description:** Streaming response patterns using MessageStream and MessageStreamManager classes. Covers text_stream iterator, event types (text, input_json, message_stop, content_block_stop), async context managers, and methods like get_final_message() and until_done(). Essential for building responsive agent interfaces and handling real-time Claude responses.
- **Rank Rationale:** #12 because streaming is important for user experience in agent applications. Useful for Claude Code showing progress during long operations.

---

### 13. Anthropic SDK Python Examples Directory
- **Source:** Anthropic GitHub
- **Link:** https://github.com/anthropics/anthropic-sdk-python/tree/main/examples
- **Type:** Code Examples Collection
- **Description:** 20+ example scripts covering: basic messages, streaming (sync/async), structured outputs, thinking capabilities, tool use (tools.py, tools_runner.py, tools_runner_search_tool.py), images/vision, web search, batch API, auto-compaction, and platform integrations (Azure, Bedrock, Vertex). Quick reference for implementing specific features.
- **Rank Rationale:** #13 because having working code examples accelerates development. Copy-paste starting points for common patterns.

---

### 14. Anthropic Cookbook Main Repository
- **Source:** Anthropic (Official)
- **Link:** https://github.com/anthropics/anthropic-cookbook
- **Type:** Code Repository / Resource Collection
- **Description:** Comprehensive collection (29.4k stars) covering capabilities (classification, RAG, summarization), tool use, third-party integrations (Pinecone, Voyage AI), multimodal (vision, charts, PDFs), and advanced techniques (sub-agents, JSON mode, prompt caching). 96.9% Jupyter notebooks with Python. Includes specific sections for agents, coding, extended thinking, and finetuning. The go-to resource for advanced Claude patterns.
- **Rank Rationale:** #14 because it's the most comprehensive collection of Claude patterns available. Bookmark and explore by topic as needed.

---

### 15. Supabase Python SDK GitHub
- **Source:** Supabase Community
- **Link:** https://github.com/supabase-community/supabase-py
- **Type:** Code Repository / Official Python Client
- **Description:** Official Python client for Supabase providing database operations, authentication, storage, and realtime subscriptions. Integrates with PostgREST for database queries, GoTrue for auth, and supports async operations. Essential for connecting Claude agents to Supabase backend for data persistence, user management, and vector search with pgvector.
- **Rank Rationale:** #15 because this is the Python interface to Supabase. You'll use this library to connect your Claude agents to Supabase for all database operations.

---

## Additional High-Value Resources

### 16. Supabase AI Documentation
- **Link:** https://supabase.com/docs/guides/ai
- **Type:** Official Documentation
- **Description:** Supabase's official AI integration guides covering vector databases, pgvector extension, embeddings generation, and AI-powered features. Provides setup instructions and integration patterns.

### 17. Supabase pgvector Extension Guide
- **Link:** https://supabase.com/docs/guides/database/extensions/pgvector
- **Type:** Official Documentation
- **Description:** Step-by-step guide for enabling and using pgvector for vector similarity search. Covers index types (ivfflat, hnsw), distance operators, and performance optimization.

### 18. LangChain Supabase Integration
- **Link:** https://python.langchain.com/docs/integrations/vectorstores/supabase
- **Type:** Documentation / Code Examples
- **Description:** LangChain's Supabase vector store integration showing RAG patterns, embedding storage, and similarity search with pgvector. Provides alternative higher-level abstractions if needed.

---

## Summary

### Key Findings

**1. Agent Orchestration Patterns:**
The Anthropic Cookbook provides five proven patterns for multi-agent coordination:
- **Prompt Chaining:** Sequential refinement
- **Routing:** Classification-based delegation
- **Parallelization:** Concurrent processing
- **Orchestrator-Workers:** Dynamic task delegation (CP→CC→sub-agents)
- **Evaluator-Optimizer:** Iterative improvement loops

**2. Supabase + Claude Integration:**
While there's no dedicated "Supabase + Claude Code" guide, the integration is straightforward:
- Use **supabase-py** for database operations
- Use **anthropic SDK** @beta_tool decorator to create Supabase tools
- Implement **pgvector** for RAG following Pinecone patterns from cookbook
- Create SQL functions for semantic search (match_documents)

**3. Multi-Agent Architecture (CP→CC→Sub-agents):**
The **Orchestrator-Workers** pattern directly maps to your vision:
- **Claude Prime** = Orchestrator (analyzes project, breaks into tasks, generates prompts)
- **Claude Code** = Primary Worker (implements tasks, may spawn sub-agents)
- **Sub-agents** = Specialized Workers (specific technical tasks)

**4. Session Management & Persistence:**
The **Autonomous Coding Agent** shows how to maintain state across sessions:
- JSON files for task tracking
- Git for version control
- Progress files for session notes
- Auto-continuation with delays

**5. Tool Use for External Integration:**
The SDK's tool system enables Supabase integration:
```python
@beta_tool
def query_supabase(table: str, filters: dict) -> str:
    """Query Supabase table with filters."""
    result = supabase.table(table).select("*").match(filters).execute()
    return json.dumps(result.data)
```

### Technology Stack Validation

All resources confirm compatibility with your stack:
- **Claude Opus 4.5 / Sonnet 4.5** ✓ (Latest models supported)
- **Python** ✓ (Primary language for all examples)
- **Electron** ✓ (Can host Python backend or use IPC)
- **Google Drive** ✓ (File-based state management patterns shown)
- **Supabase** ✓ (PostgreSQL + pgvector for RAG)

---

## Next Steps

### Recommended Learning Path

**Phase 1: Foundations (Week 1)**
1. Complete Anthropic API Fundamentals course (#6)
2. Read Prompt Engineering Tutorial (#7)
3. Implement basic SDK examples (#13)

**Phase 2: Agent Patterns (Week 2)**
4. Study Basic Workflows notebook (#9)
5. Implement Orchestrator-Workers pattern (#3)
6. Review Evaluator-Optimizer for quality control (#8)

**Phase 3: Integration (Week 3)**
7. Set up Supabase with pgvector (#15, #16, #17)
8. Implement RAG using Pinecone→pgvector migration guide (#4)
9. Create Supabase tools using @beta_tool (#11)

**Phase 4: Production Architecture (Week 4)**
10. Study Autonomous Coding Agent for session management (#5)
11. Review Customer Support Agent for production patterns (#10)
12. Implement CP→CC→sub-agent orchestration using patterns from #2

### Immediate Implementation Order

**Step 1: Quick Win - Basic Tool Integration**
```python
# Create a simple Supabase tool for Claude
from anthropic import beta_tool
from supabase import create_client

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@beta_tool
def store_data(table: str, data: dict) -> str:
    """Store data in Supabase table."""
    result = supabase.table(table).insert(data).execute()
    return f"Stored: {result.data}"

# Use with Claude
runner = client.beta.messages.tool_runner(
    model="claude-sonnet-4-5-20250929",
    tools=[store_data],
    messages=[{"role": "user", "content": "Store project info in projects table"}],
)
```

**Step 2: RAG Setup**
```sql
-- Enable pgvector
CREATE EXTENSION vector;

-- Create documents table
CREATE TABLE documents (
    id BIGSERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(1024),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create similarity search function
CREATE FUNCTION match_documents(
    query_embedding vector(1024),
    match_threshold float,
    match_count int
)
RETURNS TABLE(id bigint, content text, similarity float)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT id, content,
           (1 - (embedding <=> query_embedding)) as similarity
    FROM documents
    WHERE (1 - (embedding <=> query_embedding)) > match_threshold
    ORDER BY embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Create index
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops);
```

**Step 3: Orchestrator Pattern**
```python
# Implement CP→CC workflow
class ProjectOrchestrator:
    def __init__(self):
        self.orchestrator_model = "claude-opus-4-5-20251101"  # Claude Prime
        self.worker_model = "claude-sonnet-4-5-20250929"       # Claude Code

    def plan_project(self, project_spec: str):
        """Orchestrator analyzes and creates task breakdown."""
        response = client.messages.create(
            model=self.orchestrator_model,
            messages=[{
                "role": "user",
                "content": f"Analyze this project and break into tasks:\n{project_spec}"
            }]
        )
        return parse_tasks(response.content)

    def execute_task(self, task: dict):
        """Worker executes specific task."""
        response = client.messages.create(
            model=self.worker_model,
            tools=[store_data, query_supabase],  # Supabase tools
            messages=[{
                "role": "user",
                "content": f"Implement: {task['description']}"
            }]
        )
        return response.content
```

**Step 4: Electron Integration**
```javascript
// Electron main process - Python bridge
const { spawn } = require('child_process');
const python = spawn('python', ['agent_server.py']);

python.stdout.on('data', (data) => {
    // Send to renderer process
    mainWindow.webContents.send('agent-response', data.toString());
});

// IPC handler for agent requests
ipcMain.on('run-agent', (event, task) => {
    python.stdin.write(JSON.stringify(task) + '\n');
});
```

### Critical Success Factors

1. **Start Simple:** Begin with single-agent + Supabase tools before orchestration
2. **Use Haiku for Testing:** Claude 3 Haiku is cost-effective for development
3. **Implement Logging:** Track agent decisions and tool calls for debugging
4. **Version Control:** Use git for agent-generated code (per Autonomous Coding pattern)
5. **Security:** Implement command allowlists if agents execute code
6. **Caching:** Use prompt caching for repeated context (system prompts, project specs)

### Estimated Timeline

- **MVP (Basic agent + Supabase):** 1 week
- **RAG Integration:** 1 week
- **Multi-agent orchestration:** 2 weeks
- **Electron UI + Polish:** 1 week
- **Total:** 5 weeks to production-ready system

---

## Architecture Diagram: CP → CC → Sub-agents

```
┌─────────────────────────────────────────────────────────┐
│ CLAUDE PRIME (Opus 4.5) - Orchestrator                 │
│ - Analyzes project specifications                       │
│ - Breaks down into tasks                                │
│ - Generates optimized prompts for Claude Code           │
│ - Monitors overall progress                             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ├─── Task 1 ───> Claude Code
                     │                (Sonnet 4.5)
                     │                     │
                     │                     ├─── Sub-agent: Database Schema
                     │                     ├─── Sub-agent: API Endpoints
                     │                     └─── Sub-agent: Testing
                     │
                     ├─── Task 2 ───> Claude Code
                     │                     │
                     │                     └─── Sub-agents as needed
                     │
                     └─── Task N ───> Claude Code
                                           │
                                           └─── Sub-agents as needed
┌─────────────────────────────────────────────────────────┐
│ SUPABASE BACKEND                                        │
│ ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │
│ │ PostgreSQL  │  │ pgvector RAG │  │ Auth & Storage │  │
│ │ (Data)      │  │ (Embeddings) │  │ (Files)        │  │
│ └─────────────┘  └──────────────┘  └────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

**Data Flow:**
1. User provides project spec to Claude Prime
2. CP analyzes and creates structured task list (stored in Supabase)
3. CP generates optimized prompts for each task
4. CC receives prompts and executes with access to Supabase tools
5. CC may spawn sub-agents for specialized work
6. Results stored in Supabase, retrieved via RAG for context
7. CP monitors completion, adjusts strategy as needed

---

**Research Complete.** This provides a comprehensive roadmap for building your Supabase + multi-agent Claude system with production-ready patterns and working code examples.