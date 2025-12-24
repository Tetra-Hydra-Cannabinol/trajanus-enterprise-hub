# PHASE 3: RESEARCH AGENT

**EXECUTE IMMEDIATELY AFTER PHASE 2 COMPLETION**

---

## MISSION: AUTONOMOUS WEEKLY RESEARCH SYSTEM

**Agent Name:** Research Agent (RA)
**Model:** Claude Sonnet 4.5
**Role:** Continuous learning and knowledge acquisition

---

## RESEARCH SCOPE:

### Primary Sources:

1. **Anthropic Official**
   - https://www.anthropic.com/news
   - https://docs.anthropic.com
   - Claude release notes
   - API updates

2. **Claude Code**
   - GitHub releases
   - Feature updates
   - Community discussions
   - Best practices

3. **Supabase**
   - https://supabase.com/blog
   - New features
   - pgvector updates
   - MCP integrations

4. **MCP Ecosystem**
   - MCP server directory
   - New connectors
   - Integration examples
   - Community MCPs

5. **Developer Community**
   - Reddit r/ClaudeAI
   - Discord communities
   - Blog posts
   - YouTube tutorials
   - GitHub repositories

---

## RESEARCH AGENT SPECIFICATION:

### Weekly Automated Tasks:

**Every Monday 6:00 AM:**

1. **Web Search Queries:**
   ```
   - "Claude AI updates last week"
   - "Claude Code new features"
   - "Supabase MCP integration"
   - "Model Context Protocol new servers"
   - "Claude API best practices"
   - "Anthropic Claude release notes"
   ```

2. **Process Findings:**
   - Fetch articles/pages
   - Summarize key points
   - Identify relevant applications for Trajanus
   - Extract code examples
   - Tag by category

3. **Output Format:**
   ```markdown
   # Research Findings - [DATE]
   
   ## Claude Updates
   - [Summary of changes]
   - [Relevant to us: YES/NO]
   - [Action items if any]
   
   ## MCP Ecosystem
   - [New servers/connectors]
   - [Potential integrations]
   - [Examples]
   
   ## Best Practices Discovered
   - [What we learned]
   - [How to apply]
   - [Priority level]
   
   ## Community Insights
   - [Interesting use cases]
   - [Problems solved by others]
   - [Ideas to explore]
   ```

4. **Upload to TKB:**
   - Convert to Google Docs
   - Store in TKB-Trajanus-Knowledge-Base/01-Research-Findings/
   - Add to Supabase with embeddings
   - Tag with date and categories

---

## IMPLEMENTATION:

### STEP 1: Create Research Agent Script

**File:** `scripts/research_agent.py`

```python
import anthropic
from datetime import datetime
import os

class ResearchAgent:
    def __init__(self):
        self.client = anthropic.Client()
        self.search_queries = [
            "Claude AI updates last week",
            "Claude Code new features",
            "Supabase MCP integration",
            "Model Context Protocol new servers"
        ]
    
    def weekly_research(self):
        """Execute weekly research tasks"""
        findings = []
        
        for query in self.search_queries:
            results = self.search_web(query)
            summary = self.summarize_findings(results)
            findings.append(summary)
        
        report = self.create_report(findings)
        self.upload_to_tkb(report)
        
        return report
    
    def search_web(self, query):
        """Use Claude with web_search tool"""
        # Search and retrieve articles
        pass
    
    def summarize_findings(self, results):
        """Extract key points"""
        # Claude summarizes articles
        pass
    
    def create_report(self, findings):
        """Format weekly report"""
        # Compile into markdown
        pass
    
    def upload_to_tkb(self, report):
        """Store in TKB with embeddings"""
        # Convert to Google Docs
        # Upload to Supabase
        pass
```

### STEP 2: Schedule Weekly Execution

**Using Windows Task Scheduler:**
```powershell
# Create scheduled task
$action = New-ScheduledTaskAction -Execute 'python' -Argument 'scripts/research_agent.py'
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 6am
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "TrajanuResearchAgent"
```

### STEP 3: Test Manual Run

```bash
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center"
python scripts/research_agent.py
```

**Expected output:**
- Research report generated
- Uploaded to TKB folder
- Added to Supabase with embeddings
- Confirmation message

---

## RESEARCH CATEGORIES:

**Tag all findings with:**
- Category: CLAUDE / MCP / SUPABASE / BEST_PRACTICE / COMMUNITY
- Priority: HIGH / MEDIUM / LOW
- Actionable: YES / NO
- Date: YYYY-MM-DD

---

## SUCCESS CRITERIA:

- Weekly reports generated automatically
- Findings uploaded to TKB
- Searchable via MCP
- Actionable insights identified
- Knowledge base grows continuously

---

## DELIVERABLES:

1. ✓ Research Agent script created
2. ✓ Web search integration working
3. ✓ Report generation tested
4. ✓ TKB upload working
5. ✓ Scheduled task configured
6. ✓ First research report generated

---

**BEGIN PHASE 3 WHEN PHASE 2 COMPLETE.**
