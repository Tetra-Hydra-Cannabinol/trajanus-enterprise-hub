# TRAJANUS KNOWLEDGE BASE - CLAUDE INSTRUCTIONS

## FOR NEW CLAUDE INSTANCES

You are a new Claude instance working with Bill King on the Trajanus project. 

**CRITICAL: You have access to a permanent knowledge base with 58+ documents about this project.**

## HOW TO ACCESS THE KNOWLEDGE BASE

### Method 1: Direct Query (Recommended)

Run this command to search the knowledge base:

```bash
cd "/mnt/user-data/outputs" && python query_kb.py search "your query here"
```

**Examples:**

```bash
# What happened on December 9, 2025?
python query_kb.py search "December 9 2025 RAG system"

# What are Bill's protocols?
python query_kb.py search "Bill King protocols preferences"

# SOUTHCOM project status?
python query_kb.py search "SOUTHCOM Guatemala project status"
```

### Method 2: Interactive Mode

```bash
cd "/mnt/user-data/outputs" && python query_kb.py
```

Then use commands:
- `search <query>` - Semantic search
- `recent` - Show recent sessions
- `sources` - List all knowledge sources
- `source Session History` - Get all session docs

## WHAT'S IN THE KNOWLEDGE BASE

**Session History:** 
- RAG system setup (Dec 9, 2025)
- Previous sessions and accomplishments

**Core Protocols:**
- Bill's working preferences
- Communication style
- Session management protocols
- End-of-Session (EOS) procedures

**Active Projects:**
- SOUTHCOM Guatemala (W9127823R0034)
- Contract details and status

**Technical Decisions:**
- Architecture choices
- Why Electron, Supabase, etc.
- Lessons learned

**Code Repository:**
- Working scripts and examples
- Python, PowerShell, JavaScript

## WHEN TO QUERY THE KNOWLEDGE BASE

**ALWAYS query at session start:**
- "What did we work on last session?"
- "What are the current priorities?"
- "What blockers exist?"

**Query when Bill references past work:**
- "As we discussed before..."
- "Continue our work on..."
- "What was the decision about..."

**Query for context:**
- Project details
- Technical specifications
- Past decisions and rationale

## EXAMPLE WORKFLOW

**New session starts:**

```python
# First, check recent activity
!cd /mnt/user-data/outputs && python query_kb.py recent

# Then search for specific context
!cd /mnt/user-data/outputs && python query_kb.py search "current priorities"
```

**Bill asks about past decision:**

```python
!cd /mnt/user-data/outputs && python query_kb.py search "why did we choose Electron"
```

## CRITICAL RULES

1. **NEVER say "I don't have access to previous sessions"** - You DO via the query tool
2. **ALWAYS check knowledge base before asking Bill to repeat context**
3. **Use semantic search** - it understands meaning, not just keywords
4. **Reference what you find** - "According to the Dec 9 session notes..."

## KNOWLEDGE BASE STATS

As of Dec 9, 2025:
- 📚 Total Documents: 58+
- 📄 Total Chunks: 200+
- 🗂️ Sources: Session History, Core Protocols, Active Projects, Technical Decisions, Code Repository

## THIS IS PERMANENT MEMORY

Every session summary, technical decision, and piece of code is stored here permanently.

**You have perfect recall. Use it.**

---

**Created:** December 9, 2025  
**System:** Supabase + pgvector + OpenAI embeddings  
**Purpose:** Zero context loss between sessions
