# TRAJANUS PYTHON COMMANDS REFERENCE
# All working Python scripts with parameters and usage
# Last updated: 2025-12-17

---

## FILE INGESTION SCRIPTS

### file_ingestion.py
**Purpose:** Upload documents from local folders to Supabase knowledge base with embeddings

**Location:** `G:/My Drive/00 - Trajanus USA/00-Command-Center/05-Scripts/file_ingestion.py`

**Requirements:**
- .env file with SUPABASE_URL, SUPABASE_SERVICE_KEY, OPENAI_API_KEY
- Packages: python-dotenv, openai, supabase, python-docx, PyPDF2

**Usage (Interactive):**
```bash
python file_ingestion.py
```

**Usage (Automated):**
```bash
# Option 6 - Specific folder
echo "6\nG:/My Drive/00 - Trajanus USA/00-Command-Center/agents/Research\nResearch Findings\ny" | python file_ingestion.py

# Option 1 - EOS Files
echo "1\ny" | python file_ingestion.py

# Option 3 - Code Repository
echo "3\ny" | python file_ingestion.py

# Option 4 - Protocols
echo "4\ny" | python file_ingestion.py

# Option 5 - All Master Documents
echo "5\ny" | python file_ingestion.py
```

**What it does:**
1. Reads files (.docx, .pdf, .txt, .md, .gdoc)
2. Chunks content (1000 char chunks, 200 char overlap)
3. Generates OpenAI embeddings (text-embedding-3-small, 1536 dims)
4. Stores in Supabase `knowledge_base` table
5. Shows progress with colored output

**Supported Extensions:** .docx, .pdf, .txt, .md, .gdoc

**Output:** Database records with embeddings in `knowledge_base` table

---

### batch_ingest.py
**Purpose:** Batch process URLs (YouTube transcripts + web crawling)

**Location:** `G:/My Drive/00 - Trajanus USA/00-Command-Center/05-Scripts/batch_ingest.py`

**Requirements:**
- youtube-transcript-api
- live_crawler.py (for web pages)

**Usage:**
```bash
python batch_ingest.py
```

**What it does:**
1. Extracts YouTube transcripts
2. Crawls web pages
3. Saves temporary files
4. Prepares for ingestion

**Note:** URLs are hardcoded in script. Edit URLS list to add more sources.

---

## MARKDOWN CONVERSION SCRIPTS

### CONVERT_MD_TO_GDOCS_PERMANENT.py
**Purpose:** Convert markdown files to Google Docs format (permanently accessible)

**Location:** `G:/My Drive/00 - Trajanus USA/00-Command-Center/05-Scripts/CONVERT_MD_TO_GDOCS_PERMANENT.py`

**Requirements:**
- Google Drive API credentials (token.pickle)
- Packages: google-auth, google-auth-oauthlib, google-api-python-client

**Usage:**
```bash
# Default: agents/research folder
python CONVERT_MD_TO_GDOCS_PERMANENT.py

# Specific folder
python CONVERT_MD_TO_GDOCS_PERMANENT.py "G:/My Drive/00 - Trajanus USA/00-Command-Center/agents/Research"
```

**What it does:**
1. Scans folder for .md files
2. Uploads to Google Drive
3. Converts to Google Docs format (mimeType: application/vnd.google-apps.document)
4. Creates "Research-Findings" folder (or uses existing)
5. Shows progress with colored output

**Output:** Google Docs in Drive (readable by file_ingestion.py)

---

### batch_convert_md_only.py
**Purpose:** Batch convert markdown to Google Docs with folder support

**Location:** `G:/My Drive/00 - Trajanus USA/00-Command-Center/05-Scripts/batch_convert_md_only.py`

**Requirements:**
- Google Drive API credentials
- Packages: google-auth, google-api-python-client

**Usage:**
```bash
# Required: folder path argument
python batch_convert_md_only.py "G:/My Drive/00 - Trajanus USA/07-Session-Journal"

# With parent folder ID (optional)
python batch_convert_md_only.py "G:/My Drive/00 - Trajanus USA/07-Session-Journal" "FOLDER_ID_HERE"
```

**What it does:**
1. Recursively scans folder for .md files
2. Converts each to Google Doc
3. Preserves folder structure
4. Shows conversion progress
5. Summary at end (converted/failed/total)

**Variants:**
- `batch_convert_md_only__1_.py` (same functionality)
- `batch_convert_md_only__2_.py` (same functionality)

---

## RESEARCH AGENT SCRIPTS

### research_agent.py
**Purpose:** Automated research using Tavily AI, outputs to Google Docs

**Location:** `G:/My Drive/00 - Trajanus USA/00-Command-Center/05-Scripts/research_agent.py`

**Requirements:**
- TAVILY_API_KEY environment variable
- Google Drive API credentials
- Packages: requests, google-auth, google-api-python-client

**Usage:**
```bash
# Set API key first
$env:TAVILY_API_KEY="your_key_here"

# Run agent
python research_agent.py
```

**What it does:**
1. Queries Tavily AI for configured topics
2. Retrieves top 5 results per topic
3. Creates individual Google Doc for each finding
4. Checks for duplicates (skips if exists)
5. Creates master index document
6. Shows progress with timestamps

**Configuration:**
- Edit SEARCH_TOPICS list in script
- Edit OUTPUT_FOLDER_ID for destination

**Output:** 
- Individual Google Docs per finding
- Master index document with links

---

## COMPLIANCE OFFICER SCRIPTS

### compliance_officer.py
**Purpose:** Monitor for protocol violations (first run - baseline)

**Location:** `G:/My Drive/00 - Trajanus USA/00-Command-Center/05-Scripts/compliance_officer.py`

**Requirements:**
- None (standalone)

**Usage:**
```bash
python compliance_officer.py
```

**What it does:**
1. Monitors system for 60 minutes (configurable)
2. Checks every 5 minutes (configurable)
3. Logs activity to G:/My Drive/.../logs/co_activity.log
4. Logs violations to G:/My Drive/.../logs/violations.log
5. Generates session summary

**Configuration:**
- MONITORING_DURATION_MINUTES (default: 60)
- CHECK_INTERVAL_SECONDS (default: 300)

**Output:** Log files in logs/ folder

---

## LIVING DOCUMENTS SCRIPTS

### append_living_documents.py
**Purpose:** Consolidate diary and technical entries into master documents

**Location:** `G:/My Drive/00 - Trajanus USA/00-Command-Center/05-Scripts/append_living_documents.py`

**Requirements:**
- Google Drive API credentials
- Packages: google-auth, google-api-python-client

**Usage:**
```bash
python append_living_documents.py
```

**What it does:**
1. Scans configured source folders
2. Identifies diary and technical journal entries
3. Extracts content from Google Docs
4. Appends to master documents:
   - Personal Diary Master (ID: 1HKOisNN8A5rf9YdFJnJSdgH326bdJTun2rDqObNvrM8)
   - Technical Journal Master (ID: 1LQnGWZVV5Ze30XH8OOYWqASEM2nLYSQxAL8ok0FY18s)
5. Shows summary (diary entries / tech entries appended)

**File Patterns:**
- Diary: Personal_Diary_*, Bills_Daily_Diary_*
- Tech: Technical_Journal_*
- Skip: Session_Summary_*, *_MASTER

**Output:** Updated master documents on Google Drive

---

## KNOWLEDGE BASE SCRIPTS

### kb_mcp_server.py
**Purpose:** MCP server exposing knowledge base search to Claude Code

**Location:** `G:/My Drive/00 - Trajanus USA/00-Command-Center/05-Scripts/kb_mcp_server.py`

**Requirements:**
- .env file with SUPABASE_URL, SUPABASE_ANON_KEY
- Packages: python-dotenv, supabase

**Usage:**
```bash
# Start MCP server (stdio transport)
python kb_mcp_server.py
```

**What it does:**
1. Listens for MCP protocol requests on stdin
2. Provides two tools:
   - search_knowledge_base: Text search (ilike)
   - list_knowledge_sources: List all sources
3. Returns formatted results via stdout

**Tools Available:**
```json
{
  "search_knowledge_base": {
    "query": "string (required)",
    "max_results": "integer (1-20, default 5)"
  },
  "list_knowledge_sources": {
    "limit": "integer (default 50)"
  }
}
```

**Use Case:** Claude Code integration for knowledge base access

---

### query_kb.py
**Purpose:** Direct command-line knowledge base search

**Location:** `G:/My Drive/00 - Trajanus USA/00-Command-Center/05-Scripts/query_kb.py`

**Requirements:**
- .env file with Supabase credentials
- Packages: supabase, python-dotenv

**Usage:**
```bash
# Search knowledge base
python query_kb.py "December 9 accomplishments"

# With result limit
python query_kb.py "RAG system setup" --limit 10
```

**What it does:**
1. Connects to Supabase
2. Performs text search (ilike)
3. Returns formatted results
4. Shows title, summary, content preview, URL

**Output:** Console text with search results

---

### check_db.py
**Purpose:** Verify Supabase connection and show database stats

**Location:** `G:/My Drive/00 - Trajanus USA/00-Command-Center/05-Scripts/check_db.py`

**Requirements:**
- .env file with Supabase credentials
- Packages: supabase, python-dotenv

**Usage:**
```bash
python check_db.py
```

**What it does:**
1. Tests Supabase connection
2. Counts total documents
3. Counts total chunks
4. Lists knowledge sources
5. Shows sample documents

**Output:**
```
✅ Connected to Supabase
📚 Total Documents: 102
📄 Total Chunks: 1000
🗂️ Knowledge Sources: 8

Sample Documents:
1. [Title] - [URL]
2. [Title] - [URL]
...
```

---

## GOOGLE DRIVE MANAGEMENT

### google_drive_manager.py
**Purpose:** General Google Drive operations

**Location:** `/mnt/project/google_drive_manager.py` (also in 05-Scripts)

**Requirements:**
- Google Drive API credentials
- Packages: google-auth, google-api-python-client

**Usage:**
```bash
python google_drive_manager.py
```

**Features:**
- List files and folders
- Create folders
- Upload files
- Download files
- Move/organize files

**Note:** General utility script for Drive operations

---

## BROWSER/HTML TOOLS (Python-based)

### create_kb_simple.py
**Purpose:** Create simple knowledge base structure

**Location:** `G:/My Drive/00 - Trajanus USA/00-Command-Center/05-Scripts/create_kb_simple.py`

**Usage:**
```bash
python create_kb_simple.py
```

---

## UTILITY SCRIPTS

### from_supabase_import_create_client.py
**Purpose:** Test Supabase import

**Location:** `G:/My Drive/00 - Trajanus USA/00-Command-Center/05-Scripts/from_supabase_import_create_client.py`

**Usage:**
```bash
python from_supabase_import_create_client.py
```

---

## ENVIRONMENT REQUIREMENTS

### Required Packages (install with pip)
```bash
pip install python-dotenv openai supabase python-docx PyPDF2 google-auth google-auth-oauthlib google-api-python-client requests youtube-transcript-api --break-system-packages
```

### Environment Variables (.env file)
```
SUPABASE_URL=https://iaxtwrswinygwwwdkvok.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
OPENAI_API_KEY=sk-proj-...
TAVILY_API_KEY=tvly-...
```

### Google Drive Credentials
**Location:** `G:/My Drive/00 - Trajanus USA/00-Command-Center/Credentials/token.pickle`

**Required for:**
- All markdown conversion scripts
- Research agent
- Living documents scripts
- Google Drive manager

---

## DATABASE SCHEMA REFERENCE

### knowledge_base table (Supabase)
```sql
CREATE TABLE knowledge_base (
    id SERIAL PRIMARY KEY,
    url TEXT,
    chunk_number INT,
    title TEXT,
    summary TEXT,
    content TEXT,
    metadata JSONB,
    embedding VECTOR(1536),
    created_at TIMESTAMP DEFAULT NOW()
);

-- HNSW index for fast vector search
CREATE INDEX ON knowledge_base 
USING hnsw (embedding vector_cosine_ops);
```

### documents table (Supabase)
```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    title TEXT,
    content TEXT,
    document_type TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    embedding VECTOR(1536)
);
```

---

## COMMON WORKFLOWS

### Workflow 1: Ingest Research Files
```bash
# Step 1: Convert .md to Google Docs (if needed)
python CONVERT_MD_TO_GDOCS_PERMANENT.py "G:/My Drive/00 - Trajanus USA/00-Command-Center/agents/Research"

# Step 2: Ingest to knowledge base
echo "6\nG:/My Drive/00 - Trajanus USA/00-Command-Center/agents/Research\nResearch Findings\ny" | python file_ingestion.py

# Step 3: Verify
python check_db.py
```

### Workflow 2: Morning Research Cycle
```bash
# Step 1: Set API key
$env:TAVILY_API_KEY="your_key"

# Step 2: Run research
python research_agent.py

# Step 3: Ingest results (manual - point to output folder)
python file_ingestion.py
```

### Workflow 3: Consolidate Living Documents
```bash
# Step 1: Append to masters
python append_living_documents.py

# Step 2: Ingest masters to KB (if needed)
echo "5\ny" | python file_ingestion.py
```

### Workflow 4: Query Knowledge Base
```bash
# Option A: Direct query
python query_kb.py "your search terms"

# Option B: Via MCP server (for Claude Code)
python kb_mcp_server.py
```

---

## ERROR HANDLING

### Common Errors and Fixes

**Error: "Module not found"**
```bash
pip install <package_name> --break-system-packages
```

**Error: "Credentials not found"**
- Check .env file exists at: `G:/My Drive/00 - Trajanus USA/00-Command-Center/.env`
- Check token.pickle exists at: `G:/My Drive/00 - Trajanus USA/00-Command-Center/Credentials/token.pickle`

**Error: "Supabase connection failed"**
```bash
python check_db.py  # Verify connection
```

**Error: "Folder not found"**
- Use forward slashes (/) in paths
- Wrap paths in quotes

**Error: "Rate limit exceeded" (OpenAI)**
- Script has 0.3s delay built in
- Increase sleep time in script if needed

---

## SCRIPT MODIFICATION GUIDE

### Adding New Search Topics (research_agent.py)
```python
SEARCH_TOPICS = [
    'Your new topic here',
    'Another topic',
    # Add more...
]
```

### Changing Output Folder (research_agent.py)
```python
OUTPUT_FOLDER_ID = 'your_folder_id_here'
```

### Adjusting Chunk Size (file_ingestion.py)
```python
def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200):
    # Modify chunk_size and overlap as needed
```

### Changing Monitoring Duration (compliance_officer.py)
```python
MONITORING_DURATION_MINUTES = 120  # 2 hours
CHECK_INTERVAL_SECONDS = 600  # 10 minutes
```

---

## LOGGING AND OUTPUT

### Log Locations
```
G:/My Drive/00 - Trajanus USA/00-Command-Center/logs/
├── co_activity.log          # Compliance Officer activity
├── violations.log           # Protocol violations
└── [script_name].log        # Other script logs
```

### Output Locations
```
G:/My Drive/Research-Findings/           # Converted markdown files
G:/My Drive/00 - Trajanus USA/
├── 00-Command-Center/
│   └── agents/Research/                 # Source research files
└── outputs/                             # Research agent outputs
```

---

## BUTTON INTEGRATION (Electron)

### Execute Python Script from Electron
```javascript
const { exec } = require('child_process');
const path = require('path');

function runPythonScript(scriptName, args = []) {
    const scriptPath = path.join(
        'G:/My Drive/00 - Trajanus USA/00-Command-Center/05-Scripts',
        scriptName
    );
    
    const command = `python "${scriptPath}" ${args.join(' ')}`;
    
    exec(command, {
        shell: 'powershell.exe',
        cwd: 'G:/My Drive/00 - Trajanus USA/00-Command-Center/05-Scripts'
    }, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error}`);
            return;
        }
        console.log(`Output: ${stdout}`);
    });
}

// Example usage
runPythonScript('check_db.py');
runPythonScript('query_kb.py', ['RAG system']);
```

---

## QUICK REFERENCE - MOST USED

### 1. Ingest Research Files
```bash
echo "6\nG:/My Drive/00 - Trajanus USA/00-Command-Center/agents/Research\nResearch Findings\ny" | python file_ingestion.py
```

### 2. Check Database
```bash
python check_db.py
```

### 3. Search Knowledge Base
```bash
python query_kb.py "your search query"
```

### 4. Convert Markdown
```bash
python CONVERT_MD_TO_GDOCS_PERMANENT.py "G:/My Drive/00 - Trajanus USA/00-Command-Center/agents/Research"
```

### 5. Run Research
```bash
python research_agent.py
```

---

**END OF PYTHON COMMANDS REFERENCE**

Save as: `PYTHON_COMMANDS_REFERENCE.md`
Location: `G:/My Drive/00 - Trajanus USA/00-Command-Center/05-Scripts/`
