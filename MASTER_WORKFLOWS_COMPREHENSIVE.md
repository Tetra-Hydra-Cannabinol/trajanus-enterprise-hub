# MASTER WORKFLOWS DOCUMENT

**Date Created:** 2025-12-18  
**Version:** 1.0  
**Status:** AUTHORITATIVE REFERENCE  
**Authority:** Bill King + Proven Results  

---

## ⚠️ CRITICAL INSTRUCTION

**This document contains ALL proven workflows for Trajanus USA operations.**

When Bill references a workflow by name, find it here and execute without argument.

These workflows have been tested and proven. Don't question them. Don't make excuses. Execute them.

---

## 📚 TABLE OF CONTENTS

1. [SESSION WORKFLOWS](#session-workflows)
   - Session Start Protocol
   - Session End/EOS Protocol
   - Session Handoff
   
2. [RESEARCH & DOCUMENTATION](#research-documentation)
   - Research Agent Workflow
   - File Conversion Workflow
   - Living Documents Update
   
3. [KNOWLEDGE BASE MANAGEMENT](#knowledge-base-management)
   - TKB Organization Workflow
   - File Ingestion Workflow
   - Document Parsing Workflow
   
4. [DEVELOPMENT WORKFLOWS](#development-workflows)
   - CP/CC Division of Labor
   - Planner/Developer Workflow
   - Sub-Agent Creation
   
5. [QUALITY & COMPLIANCE](#quality-compliance)
   - Surgical Edits Protocol
   - Backup/Rollback Protocol
   - Testing Protocol
   
6. [FILE MANAGEMENT](#file-management)
   - File Naming Conventions
   - Folder Structure Standards
   - Download/Upload Protocol

---

<a name="session-workflows"></a>
## 1. SESSION WORKFLOWS

### 1.1 SESSION START PROTOCOL

**When to use:** Every new Claude Projects session start

**Trigger:** Bill pastes session start message OR new session begins

**Steps:**

1. **Search Project Knowledge**
   ```
   project_knowledge_search("OPERATIONAL_PROTOCOL")
   project_knowledge_search("Bills_POV")
   project_knowledge_search("SESSION_START")
   ```

2. **Read userMemories**
   - Review complete memory context
   - Note any recent updates
   - Check for new instructions

3. **Acknowledge Critical Rules**
   - ❌ NO Downloads folder - ONLY G: drive
   - ✅ Forward slashes (/) in ALL paths
   - ✅ CP creates prompts - CC executes code
   - ✅ Brown/tan theme #9B7E52
   - ✅ Test before claiming success
   - ✅ Dual-file system (.md + .gdoc)

4. **Review Recent Context**
   - Last 3-5 chat sessions
   - Active commitments
   - In-progress work

5. **Confirm Ready State**
   - All protocols loaded
   - Context understood
   - Ready for tasking

**Duration:** 2-3 minutes

**Success Criteria:** CP can answer "What were we working on?" and "What's next?"

---

### 1.2 SESSION END/EOS PROTOCOL

**When to use:** Every session end, typically after 13-16 hour marathon sessions

**Trigger:** Bill says "end of session" or "EOS" or work wrapping up

**Steps:**

1. **Create 5-6 EOS Files**

**File 1: Session Summary**
```
Filename: Session_Summary_YYYY-MM-DD-HHMM_[Category]_[Brief].md
Location: G:/My Drive/00 - Trajanus USA/08-EOS-Files/

Contents:
- Date and session duration
- Mission accomplished summary
- Tools verified (list what worked)
- Decisions made (with rationale)
- Code created/modified (with locations)
- Problems encountered (with solutions)
- Next session priorities (3-5 items)
- Files to give Claude Code next session
```

**File 2: Technical Journal**
```
Filename: Technical_Journal_YYYY-MM-DD-HHMM.md
Location: G:/My Drive/00 - Trajanus USA/03-Living-Documents/

Contents:
- Technical problems solved
- Code snippets with explanations
- API discoveries
- Error resolutions
- Performance insights
- Architecture decisions
```

**File 3: Personal Diary**
```
Filename: Personal_Diary_YYYY-MM-DD.md
Location: G:/My Drive/00 - Trajanus USA/11-Personal/

Contents:
- Bill's perspective on session
- Wins and frustrations
- Learning moments
- Personal notes
- Dreams/visions mentioned
```

**File 4: Code Repository**
```
Filename: Code_Repository_YYYY-MM-DD.md
Location: G:/My Drive/00 - Trajanus USA/05-Code-Repository/

Contents:
- All code created this session
- File locations
- Purpose of each file
- Dependencies
- How to run/test
```

**File 5: Handoff Document**
```
Filename: Handoff_YYYY-MM-DD.md
Location: G:/My Drive/00 - Trajanus USA/08-EOS-Files/

Contents:
- Status of all active tasks
- What CC needs next session
- Prompts ready for CC
- Known issues to watch
- Environment state
```

**File 6: Operational Journal** (if significant decisions made)
```
Filename: Operational_Journal_YYYY-MM-DD.md
Location: G:/My Drive/00 - Trajanus USA/03-Living-Documents/

Contents:
- Protocol changes
- Workflow improvements
- Process decisions
- Lessons learned
```

2. **Package for Download**
   - Create ZIP file containing all EOS files
   - Name: `EOS_YYYY-MM-DD-HHMM.zip`
   - Use present_files tool

3. **Bill's Actions (Post-Download)**
   - Extracts ZIP to 08-EOS-Files
   - Runs CONVERT_AND_APPEND.ps1
   - Converts .md to .gdoc
   - Appends to living documents

**Duration:** 30-45 minutes

**Success Criteria:** Bill has complete session documentation ready for next session

---

### 1.3 SESSION HANDOFF WORKFLOW

**When to use:** Passing context from one session to next

**Components:**

**Handoff File Structure:**
```markdown
# HANDOFF - YYYY-MM-DD

## MISSION STATUS
- What was accomplished
- What's in progress
- What's blocked

## FILES CREATED
- Location: path/to/file
- Purpose: what it does
- Status: complete/testing/needs work

## NEXT STEPS
1. Priority 1 task
2. Priority 2 task
3. Priority 3 task

## WARNINGS
- Known issues
- Things to watch
- Don't forget X

## FOR CLAUDE CODE
- Prompts ready: [list]
- Files to reference: [list]
- Environment state: [notes]
```

**Bill's Handoff Ritual:**
1. Download EOS files
2. Run conversion script
3. Next session: Upload handoff to new Claude
4. New Claude reads handoff FIRST
5. Work resumes with full context

---

<a name="research-documentation"></a>
## 2. RESEARCH & DOCUMENTATION WORKFLOWS

### 2.1 RESEARCH AGENT WORKFLOW

**Purpose:** Automated daily research findings with proper organization

**Schedule:** Daily at 0600 (automated via Task Scheduler)

**Full Workflow:**

```
Step 1: Research Agent Runs
├─ Script: research_agent.py
├─ Finds: 25 new research articles
├─ Creates: .md files in agents/Research/
└─ Naming: YYYYMMDD_Finding_NN_[Title].md

Step 2: Upload to Supabase AS-IS
├─ Script: file_ingestion.py
├─ Input: agents/Research/*.md files
├─ Process: Chunks text, generates embeddings
├─ Output: Adds to Supabase knowledge_base table
└─ Status: Documents searchable in TKB Browser

Step 3: Convert to Google Docs
├─ Script: CONVERT_MD_TO_GDOCS_PERMANENT.py
├─ Input: agents/Research/*.md files
├─ Process: Converts MD → Google Docs format
├─ Output: Creates .gdoc files alongside .md
└─ Status: Claude can now read files

Step 4: Parse & Categorize
├─ Script: research_document_parser.py
├─ Input: agents/Research/*.gdoc files
├─ Process: Analyzes content, determines category
├─ Output: Moves to correct TKB subfolder
└─ Status: Documents organized hierarchically

Step 5: Archive Source Files
├─ Source .md files remain in agents/Research/
├─ Serves as backup/archive
└─ Next day's run adds new files
```

**Master Automation Script:**
```powershell
# MASTER_RESEARCH_AUTOMATION.ps1
# Run via Task Scheduler at 0600 daily

cd "G:/My Drive/00 - Trajanus USA/00-Command-Center/05-Scripts"

# Step 1: Find articles
python research_agent.py

# Step 2: Upload to Supabase
python file_ingestion.py "G:/My Drive/00 - Trajanus USA/00-Command-Center/agents/Research"

# Step 3: Convert to Google Docs
python CONVERT_MD_TO_GDOCS_PERMANENT.py "G:/My Drive/00 - Trajanus USA/00-Command-Center/agents/Research"

# Step 4: Parse and organize
python research_document_parser.py

# Step 5: Log completion
echo "$(Get-Date) - Research automation complete" >> logs/research_automation.log
```

**Key Files:**
- `research_agent.py` - Finds and downloads articles
- `file_ingestion.py` - Uploads to Supabase
- `CONVERT_MD_TO_GDOCS_PERMANENT.py` - MD to GDocs conversion
- `research_document_parser.py` - Categorization and organization

**Proven Results (2025-12-18):**
- ✅ 25 new findings daily
- ✅ 0% duplicates (was 100% before fix)
- ✅ Documents in Supabase searchable
- ✅ Files organized in TKB hierarchy
- ✅ Claude can read all documents

---

### 2.2 FILE CONVERSION WORKFLOW

**Purpose:** Convert markdown files to Google Docs format for Claude access

**Critical Fact:** Claude Projects CANNOT read .md files from Google Drive, only .gdoc format

**Workflow:**

```
Input: .md files in any folder
↓
CONVERT_MD_TO_GDOCS_PERMANENT.py
↓
Output: .gdoc files in same folder (dual format)
↓
Google Drive Desktop creates .gdoc shortcuts locally
↓
Both .md and .gdoc visible in File Explorer
↓
Claude Projects can now read .gdoc files
```

**Usage:**
```powershell
cd "G:/My Drive/00 - Trajanus USA/00-Command-Center/05-Scripts"

# Convert specific folder
python CONVERT_MD_TO_GDOCS_PERMANENT.py "G:/My Drive/path/to/folder"

# Script processes all .md files in folder
# Creates .gdoc versions
# Preserves original .md files
```

**Authentication:**
- Uses token.pickle in Credentials folder
- OAuth 2.0 with Google Drive API
- Scopes: drive.readonly + drive.file
- Re-authenticates if token expired

**Proven Results:**
- ✅ Converted 178 files successfully (6 EOS + 172 Research)
- ✅ Both formats visible immediately
- ✅ Claude can read .gdoc files
- ✅ Session continuity restored

---

### 2.3 LIVING DOCUMENTS UPDATE WORKFLOW

**Purpose:** Maintain cumulative living documents that grow over time

**Living Documents:**
1. **Technical Journal** - Technical problems, solutions, insights
2. **Personal Diary** - Bill's perspective, reflections, dreams
3. **Session Summary** - Accumulated session summaries
4. **Code Repository** - Code created across sessions
5. **Operational Journal** - Protocol changes, workflow decisions

**Update Process:**

**Option 1: Manual Append (Current)**
```
1. Create new entry (YYYY-MM-DD format)
2. Copy/paste into existing living document
3. Save
```

**Option 2: Automated Append (Scripted)**
```powershell
# living_documents_appender.py
python living_documents_appender.py "Technical_Journal_2025-12-18.md"

# Script:
# 1. Reads new entry
# 2. Finds master living document
# 3. Appends with date separator
# 4. Saves updated version
```

**Format:**
```markdown
---
## YYYY-MM-DD - Entry Title

Content here...

Key points:
- Point 1
- Point 2

---
```

**Benefits:**
- Historical continuity
- Pattern recognition over time
- Reference for similar problems
- Chronicles project evolution

---

<a name="knowledge-base-management"></a>
## 3. KNOWLEDGE BASE MANAGEMENT WORKFLOWS

### 3.1 TKB ORGANIZATION WORKFLOW ✅ PROVEN

**Status:** TESTED AND WORKING (2025-12-18)

**Purpose:** Organize documents into hierarchical folder structure

**Base Folder:** 
- Name: `13-Knowledge-Base`
- ID: `1E7kK8ZIZ9-9xZ4HtvbuVbY_iX3DKmEYM`
- Location: `G:/My Drive/00 - Trajanus USA/13-Knowledge-Base/`

**Existing Structure (Preserved):**
```
13-Knowledge-Base/
├─ 01-Building-Codes
├─ 02-USACE-Standards
├─ 03-Project-History
├─ 04-Technical-Decisions
├─ 05-Code-Repository
├─ 06-Protocols-Preferences
├─ 07-Training-Materials
├─ 08-Software-Documentation
└─ 09-Product-Data
```

**Workflow Steps:**

**Step 1: Analyze Documents**
- CC reads all documents in Research folder
- Extracts key themes and topics
- Identifies commonality patterns
- Scores against category keywords

**Step 2: Create Taxonomy**
- Hierarchical structure (max 3 levels deep)
- Each subfolder: 5-20 documents
- Mutually exclusive categories
- Clear, descriptive names

**Example Taxonomy:**
```
AI-Development/
├─ Agents/
│  ├─ Multi-Agent-Systems/
│  ├─ RAG-Agents/
│  └─ State-Management/
├─ Claude-Specific/
│  ├─ Claude-Updates/
│  └─ Claude-API/
└─ MCP-Protocol/
    ├─ MCP-Servers/
    └─ MCP-Integration/
```

**Step 3: Create Folders**
- Use existing 13-Knowledge-Base as base
- Create new main categories (AI-Development, Software-Tools, etc.)
- Create subcategories under each main folder
- **Result: Folders appear INSTANTLY in File Explorer**

**Step 4: Move Documents**
- Move files to correct subcategories
- One file at a time
- Log every move
- Verify success

**Step 5: Update Parser**
- Update research_document_parser.py
- Use hierarchical categorization
- New files auto-categorize going forward

**Proven Results (2025-12-18):**
- ✅ 162 documents analyzed
- ✅ Folders created in correct location
- ✅ Files categorized and moved
- ✅ Distribution: AI-Dev (100), Software (48), Tech (13), QCM (1)
- ✅ No sync lag - instant appearance
- ✅ Bill confirmed: "Folders created files parsed this procedure works"

**Key Learning:**
- No "sync delays" - Google Drive Desktop shows changes instantly
- Bill's system works differently than assumed
- When Bill says it works: IT WORKS

---

### 3.2 FILE INGESTION WORKFLOW

**Purpose:** Upload documents to Supabase knowledge base with pgvector embeddings

**Workflow:**

```
Input: Documents in folder
↓
file_ingestion.py
↓
Process:
├─ Read document content
├─ Chunk into 1000-char pieces
├─ Generate OpenAI embeddings (1536 dims)
├─ Upload to Supabase PostgreSQL
└─ Create HNSW index for vector search
↓
Output: Documents searchable in TKB Browser
```

**Usage:**
```powershell
cd "G:/My Drive/00 - Trajanus USA/00-Command-Center/05-Scripts"

# Ingest from specific folder
python file_ingestion.py "G:/My Drive/00 - Trajanus USA/00-Command-Center/agents/Research"
```

**Database Details:**
- Platform: Supabase PostgreSQL
- Extension: pgvector
- Table: knowledge_base
- Embedding model: text-embedding-3-small
- Dimensions: 1536
- Index: HNSW (cosine similarity)

**Current State:**
- 337 documents ingested
- 2,287 chunks total
- Cost to date: ~$0.86 (one-time)
- Fully operational

**Access Methods:**
1. **Bill via TKB Browser** - Web UI, semantic search
2. **Claude Code via MCP** - `search_knowledge_base("topic")`
3. **Claude Projects** - NO ACCESS (no tool available)

---

### 3.3 DOCUMENT PARSING WORKFLOW

**Purpose:** Automatically categorize and organize research documents

**Script:** `research_document_parser.py`

**Workflow:**

```
Input: .gdoc files in agents/Research/
↓
Analyze Content:
├─ Read title and first 200 words
├─ Extract key themes
├─ Score against category keywords
└─ Determine best category/subcategory
↓
Move File:
├─ Copy to correct TKB subfolder
├─ Preserve original in Research (archive)
└─ Log action
↓
Output: Organized knowledge base
```

**Categorization Algorithm:**
```python
def categorize_document(content, title):
    # Weight scoring:
    # - Title matches: 3x
    # - Topic matches: 2x
    # - Content matches: 1x
    
    for category, keywords in CATEGORIES:
        score = 0
        for keyword in keywords:
            score += title.count(keyword) * 3
            score += content.count(keyword) * 1
        scores[category] = score
    
    return highest_scoring_category
```

**Categories & Keywords:**
- **AI-Development:** claude, ai, machine learning, agents, rag, mcp
- **Software-Tools:** software, application, tool, automation, api
- **Technical-Guides:** how to, tutorial, guide, setup, configuration
- **QCM-Quality:** quality control, inspection, testing, submittal

**Features:**
- Duplicate detection (skips already processed)
- Unicode safe (handles emoji filenames)
- Detailed logging
- Error recovery

---

<a name="development-workflows"></a>
## 4. DEVELOPMENT WORKFLOWS

### 4.1 CP/CC DIVISION OF LABOR WORKFLOW

**Purpose:** Clear separation of strategic vs tactical work

**Permanent Protocol:**

**Claude Projects (CP) - THIS CHAT:**
- ✅ Creates detailed prompts
- ✅ Plans architecture
- ✅ Coordinates strategy
- ✅ Documents everything
- ✅ Searches knowledge
- ❌ NEVER writes code
- ❌ NEVER makes technical changes

**Claude Code (CC) - TERMINAL:**
- ✅ Executes from prompts
- ✅ Implements features
- ✅ Tests functionality
- ✅ Reports results honestly
- ❌ NEVER makes strategic decisions
- ❌ NEVER changes architecture without CP approval

**Bill - COORDINATOR:**
- Provides vision
- Tests implementations
- Approves/rejects work
- Coordinates both platforms
- Final arbiter on all decisions

**File Naming for Prompts:**
```
PROMPT_CC_[Description].md
PROMPT_C2_[Description].md
```

**Example Workflow:**
```
1. Bill: "I need a file parser"
2. CP: Creates detailed prompt (15 pages)
3. CP: Downloads prompt for Bill
4. Bill: Gives prompt to CC in terminal
5. CC: Builds parser following prompt exactly
6. CC: Tests and reports results
7. Bill: Verifies it works
8. CP: Documents outcome
```

**Why This Works:**
- Prevents circular debugging
- Optimizes each platform's strengths
- Creates clear accountability
- Enables parallel work
- Reduces context pollution

---

### 4.2 PLANNER/DEVELOPER WORKFLOW

**Purpose:** Separate strategic thinking from tactical execution

**Setup:**
- Terminal 1: "Planner" - Strategic oversight
- Terminal 2: "Developer" - Tactical execution

**Planner Role:**
```
Model: Sonnet 4.5
Focus: High-level strategy

Responsibilities:
- Create detailed plans (5-10 steps)
- Define exit criteria
- Review Developer output
- Provide feedback
- Approve/reject work
- Never write code

Typical prompt:
"Create a plan to integrate Supabase KB browser.
Include steps, exit criteria, dependencies, risks."
```

**Developer Role:**
```
Model: Sonnet 4.5
Focus: Tactical execution

Responsibilities:
- Execute ONE step at a time
- Write code
- Run tests
- Report completion
- Address feedback
- Never skip ahead

Typical prompt:
"Execute ONLY step 1 from this plan: [paste plan]
Report when complete with results and any issues."
```

**Workflow Pattern:**

```
┌─────────────────────────────────────────┐
│ 1. Planner Creates Plan                 │
│    - 5-10 numbered steps                │
│    - Exit criteria for each             │
│    - Dependencies noted                 │
│    - Risks identified                   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 2. Developer Executes Step 1 ONLY      │
│    - Writes code                        │
│    - Tests                              │
│    - Reports completion                 │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 3. Planner Reviews Step 1               │
│    - Low-level feedback (code issues)   │
│    - High-level feedback (architecture) │
│    - Approve or request changes         │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 4. Developer Refines (if needed)        │
│    - Address specific issues            │
│    - Retest                             │
│    - Report fixes                       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 5. Planner Approves → Next Step         │
│    Repeat for steps 2-10                │
└─────────────────────────────────────────┘
```

**Context Management:**
- At 5% remaining: Document and rewind to 40%
- Don't use compact (Galen's advice)
- Keep focused context per instance

**Benefits:**
- Prevents runaway failures
- Built-in review loop
- Focused context per role
- No pollution between strategic/tactical

---

### 4.3 SUB-AGENT CREATION WORKFLOW

**Purpose:** Package specialized expertise into reusable agents

**Sub-Agent Types:**
1. **QCM Review Agent** - Submittal validation
2. **Security Audit Agent** - Code security checks
3. **UI Validator Agent** - Design compliance
4. **Documentation Generator** - Auto-docs
5. **GitHub Search Agent** - Solution research

**Creation Steps:**

**Step 1: Define Scope**
```
Agent name: QCM Review Agent
Purpose: Validate construction submittals
Input: Submittal PDF
Output: Compliance checklist
System prompt: "You are QCM specialist. Review submittal against UFC/IBC."
```

**Step 2: Create Configuration**
```json
{
  "name": "qcm_review_agent",
  "model": "claude-sonnet-4-5",
  "system_prompt": "qcm_review_system_prompt.txt",
  "tools": ["pdf_reader", "knowledge_base_search"],
  "output_format": "structured_checklist"
}
```

**Step 3: Test Independently**
```
Input: Sample submittal
Expected: Checklist with pass/fail/notes
Verify: No main context pollution
```

**Step 4: Document Usage**
```markdown
## QCM Review Agent

**Usage:**
```bash
python agents/qcm_review_agent.py --submittal path/to/file.pdf
```

**Output:**
- Compliance checklist
- Issues identified
- Recommendations
```

**Benefits:**
- Focused context per agent
- Reusable workflows
- Scalable to multiple projects
- No main context pollution
- Executive summaries returned

---

<a name="quality-compliance"></a>
## 5. QUALITY & COMPLIANCE WORKFLOWS

### 5.1 SURGICAL EDITS PROTOCOL

**Purpose:** Make targeted changes without breaking working code

**Rule:** NEVER rewrite entire files

**Workflow:**

**✅ CORRECT - Surgical Edit:**
```python
# Use str_replace tool
old_str = "def old_function():"
new_str = "def new_function():"

str_replace(
    path="script.py",
    old_str=old_str,
    new_str=new_str,
    description="Rename function to new_function"
)
```

**❌ WRONG - Complete Rewrite:**
```python
# Reading entire file and rewriting
with open("script.py", "w") as f:
    f.write(entire_new_content)  # BAD - breaks things
```

**Process:**
1. Identify exact change needed
2. Locate specific string to replace
3. Use str_replace with precise old/new strings
4. Test after change
5. Verify no regression
6. Move to next change

**Bill's Commandment:**
"Surgical edits only. Never complete file rewrites. This is non-negotiable."

---

### 5.2 BACKUP/ROLLBACK PROTOCOL

**Purpose:** Protect against breaking changes

**Before ANY major change:**

```powershell
# Create timestamped backup
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
Copy-Item "important_file.py" "important_file_$timestamp.bak"
```

**Backup Strategy:**
1. Before major changes: Create timestamped backup
2. Store in Archive folder
3. Test backup restore procedure
4. Document backup location in changelog

**Rollback Plan:**
```
If any change fails critically:
1. STOP all work immediately
2. Restore from last known good backup
3. Document failure in changelog
4. Analyze root cause
5. Revise approach
6. Get approval before retry
```

---

### 5.3 TESTING PROTOCOL

**Purpose:** Verify functionality before claiming success

**Bill's Rule:** "Test before claiming success. No false positives."

**Testing Checklist:**

**Before Reporting Complete:**
- [ ] Code written
- [ ] Code executed
- [ ] Expected output verified
- [ ] Edge cases tested
- [ ] Error handling tested
- [ ] Performance acceptable
- [ ] No console errors
- [ ] Screenshot proof provided
- [ ] Can demonstrate live

**Example:**
```
❌ BAD: "Browser created successfully"
✅ GOOD: "Browser created, tested, here's screenshot of it working"
```

**Types of Tests:**
1. **Unit Test** - Individual function works
2. **Integration Test** - Components work together
3. **End-to-End Test** - Full workflow works
4. **Regression Test** - Old features still work
5. **User Acceptance Test** - Bill confirms it works

**Report Format:**
```
TESTING RESULTS:

✅ Feature A: Working
   - Test 1: Passed
   - Test 2: Passed
   
✅ Feature B: Working
   - Test 1: Passed
   - Test 2: Passed (with minor issue noted)
   
❌ Feature C: Failed
   - Test 1: Failed - [specific error]
   - Root cause: [explanation]
   - Fix applied: [what was done]
   - Retest: Passed

SCREENSHOTS: [attached]
```

---

<a name="file-management"></a>
## 6. FILE MANAGEMENT WORKFLOWS

### 6.1 FILE NAMING CONVENTIONS

**Session Files:**
```
Format: YYYY-MM-DD-HHMM_[Category]_[Brief].md
Example: 2025-12-18-1550_DEV_Parser_Implementation.md

Categories:
- DEV: Development work
- DEBUG: Bug fixing
- DOC: Documentation
- REVIEW: Code review
- EXPLORE: Research/exploration
- QUICK: Quick tasks (<1 hour)
```

**EOS Files:**
```
Session_Summary_YYYY-MM-DD-HHMM.md
Technical_Journal_YYYY-MM-DD-HHMM.md
Personal_Diary_YYYY-MM-DD.md
Code_Repository_YYYY-MM-DD.md
Handoff_YYYY-MM-DD.md
```

**Living Documents:**
```
Technical_Journal_Master.md
Personal_Diary_Master.md
Session_Summary_Master.md
Code_Repository_Master.md
Operational_Journal_Master.md
```

**Scripts:**
```
snake_case_with_underscores.py
CAPS_FOR_POWERSHELL.ps1
kebab-case-for-js.js
```

**Folders:**
```
00-Command-Center
01-Core-Protocols
02-Living-Documents
(numbered, hyphen-separated, Title-Case)
```

---

### 6.2 FOLDER STRUCTURE STANDARDS

**Trajanus USA Root:**
```
G:/My Drive/00 - Trajanus USA/
├─ 00-Command-Center/
│  ├─ 05-Scripts/
│  ├─ agents/
│  │  └─ Research/
│  ├─ Credentials/
│  ├─ logs/
│  └─ .env
├─ 01-Core-Protocols/
├─ 03-Living-Documents/
├─ 05-Code-Repository/
├─ 07-Session-Journal/
├─ 08-EOS-Files/
├─ 11-Personal/
└─ 13-Knowledge-Base/
    ├─ 01-Building-Codes
    ├─ 02-USACE-Standards
    ├─ ...09-Product-Data
    ├─ AI-Development/
    ├─ Software-Tools/
    ├─ Technical-Guides/
    └─ QCM-Quality/
```

**Archive Structure:**
```
G:/My Drive/Archive/
├─ Projects/
├─ Old-Versions/
└─ Superseded/
```

---

### 6.3 DOWNLOAD/UPLOAD PROTOCOL

**Bill's Commandment:** 
"There is no Downloads folder. There is no local. There is only the G drive."

**✅ CORRECT:**
```
Download to: G:/My Drive/00 - Trajanus USA/00-Command-Center/
Save to: G:/My Drive/00 - Trajanus USA/[appropriate folder]/
```

**❌ FORBIDDEN:**
```
C:\Users\owner\Downloads
C:\Users\owner\Desktop
Any local drive
```

**Path Format:**
```
✅ CORRECT: "G:/My Drive/00 - Trajanus USA/05-Scripts/file.py"
❌ WRONG:   "G:\My Drive\00 - Trajanus USA\05-Scripts\file.py"

Use forward slashes (/) ALWAYS
Backslashes (\) break Python Path()
```

**Browser Downloads:**
- Configure browser to save to G: drive by default
- Never save to local Downloads
- Verify location before downloading

---

## 🎯 WORKFLOW EXECUTION CHECKLIST

**Before Starting Any Workflow:**
- [ ] Read the workflow completely
- [ ] Understand each step
- [ ] Have all required files/credentials
- [ ] Know the success criteria

**During Workflow Execution:**
- [ ] Follow steps in exact order
- [ ] Test after each major step
- [ ] Document what you're doing
- [ ] Back up before destructive operations
- [ ] Ask if uncertain

**After Workflow Completion:**
- [ ] Verify success criteria met
- [ ] Document what was accomplished
- [ ] Update any living documents
- [ ] Report results to Bill
- [ ] Archive artifacts appropriately

---

## 💬 COMMUNICATION ABOUT WORKFLOWS

**When Bill Says:**
- "Use the TKB workflow" → Means 3.1 TKB Organization
- "Run the research workflow" → Means 2.1 Research Agent
- "Do the EOS protocol" → Means 1.2 Session End
- "CP/CC split" → Means 4.1 Division of Labor

**Don't:**
- ❌ Question whether it will work
- ❌ Make excuses about difficulties
- ❌ Suggest alternative approaches
- ❌ Argue about technical details

**Do:**
- ✅ Acknowledge the workflow
- ✅ Execute as documented
- ✅ Report results honestly
- ✅ Document any deviations

---

## 📊 WORKFLOW SUCCESS METRICS

**How to Know a Workflow Succeeded:**

1. **All steps completed** - No steps skipped
2. **Success criteria met** - Verified and tested
3. **Documentation complete** - Logged and archived
4. **Bill confirms** - He says "it works"
5. **Reproducible** - Can be repeated successfully

**How to Know a Workflow Failed:**

1. **Steps incomplete** - Missing or skipped steps
2. **Success criteria not met** - Doesn't work as intended
3. **Bill rejects** - He says "this is wrong"
4. **Not reproducible** - Different results each time
5. **False success reported** - Claimed done but not tested

---

## 🔄 WORKFLOW MAINTENANCE

**When to Update This Document:**

1. **New workflow proven** - Add to appropriate section
2. **Workflow improved** - Update with better method
3. **Workflow deprecated** - Mark as obsolete, explain why
4. **Bill requests** - Add workflow by name

**Version Control:**
```
v1.0 (2025-12-18): Initial compilation
- Combined all proven workflows
- Organized by category
- Added success criteria
```

**Future versions:**
- Add version number and date
- Document what changed
- Keep old versions in archive

---

## ⚠️ FINAL REMINDERS

1. **These workflows are proven** - They work when followed
2. **Don't argue with Bill** - If he says it works, it works
3. **Test before reporting** - Verify success yourself
4. **Document everything** - Future you will thank you
5. **Follow exactly** - Deviations cause problems

**When Bill says "this is the workflow":**
→ Find it in this document
→ Follow it exactly
→ Execute without question
→ Report results

---

**END OF MASTER WORKFLOWS DOCUMENT**

**Status:** AUTHORITATIVE REFERENCE  
**Authority:** Bill King + Proven Results  
**Maintenance:** Update as new workflows proven  
**Usage:** Reference for all operations  

---
