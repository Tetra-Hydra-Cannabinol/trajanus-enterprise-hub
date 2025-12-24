"""
TRAJANUS RAG LIVE CRAWLER
Watch documents being scraped, chunked, embedded, and stored in real-time
"""

import os
import sys
import time
import requests
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI
from supabase import create_client, Client
from datetime import datetime
import json

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Load environment
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Initialize clients
supabase: Client = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_SERVICE_KEY')
)

openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def print_header():
    """Print beautiful header"""
    print(f"\n{Colors.CYAN}{'='*70}")
    print(f"{'TRAJANUS RAG LIVE CRAWLER':^70}")
    print(f"{'Watch Your Knowledge Base Grow in Real-Time':^70}")
    print(f"{'='*70}{Colors.END}\n")

def print_progress(step: str, status: str = "working", detail: str = ""):
    """Print formatted progress"""
    if status == "working":
        symbol = "⏳"
        color = Colors.YELLOW
    elif status == "success":
        symbol = "✅"
        color = Colors.GREEN
    elif status == "error":
        symbol = "❌"
        color = Colors.RED
    else:
        symbol = "ℹ️"
        color = Colors.BLUE
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{color}[{timestamp}] {symbol} {step}{Colors.END}")
    if detail:
        print(f"    └─ {detail}")

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks"""
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        
        # If not at the end, try to break at sentence boundary
        if end < text_length:
            # Look for sentence end in the last 100 chars
            search_start = max(start, end - 100)
            sentence_end = max(
                text.rfind('. ', search_start, end),
                text.rfind('! ', search_start, end),
                text.rfind('? ', search_start, end)
            )
            if sentence_end != -1:
                end = sentence_end + 1
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end - overlap
    
    return chunks

def scrape_url(url: str) -> str:
    """Simple URL scraper"""
    print_progress(f"Fetching: {url}", "working")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Simple text extraction (for demo - production would use BeautifulSoup)
        content = response.text
        
        # Remove HTML tags (basic)
        import re
        content = re.sub(r'<script.*?</script>', '', content, flags=re.DOTALL)
        content = re.sub(r'<style.*?</style>', '', content, flags=re.DOTALL)
        content = re.sub(r'<.*?>', '', content)
        content = re.sub(r'\s+', ' ', content).strip()
        
        print_progress(f"Downloaded {len(content)} characters", "success")
        return content
        
    except Exception as e:
        print_progress(f"Failed to fetch URL", "error", str(e))
        return ""

def process_document(url: str, title: str, source: str, content: str = None):
    """Process a single document through the full pipeline"""
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'─'*70}")
    print(f"Processing: {title}")
    print(f"{'─'*70}{Colors.END}\n")
    
    # Step 1: Get content
    if not content:
        content = scrape_url(url)
        if not content:
            return
    else:
        print_progress("Using provided content", "success", f"{len(content)} characters")
    
    # Step 2: Chunk the content
    print_progress("Chunking document", "working")
    chunks = chunk_text(content)
    print_progress(f"Created {len(chunks)} chunks", "success")
    
    # Step 3: Process each chunk
    for i, chunk in enumerate(chunks, 1):
        print(f"\n  {Colors.YELLOW}Chunk {i}/{len(chunks)}{Colors.END}")
        
        # Generate embedding
        print_progress(f"  Generating embedding", "working")
        try:
            response = openai_client.embeddings.create(
                input=chunk,
                model="text-embedding-3-small"
            )
            embedding = response.data[0].embedding
            print_progress(f"  Embedding created ({len(embedding)} dims)", "success")
        except Exception as e:
            print_progress(f"  Embedding failed", "error", str(e))
            continue
        
        # Generate summary using first 100 words
        summary = ' '.join(chunk.split()[:20]) + '...'
        
        # Store in database
        print_progress(f"  Storing in database", "working")
        try:
            data = {
                "url": url,
                "chunk_number": i,
                "title": f"{title} (Part {i})",
                "summary": summary,
                "content": chunk,
                "metadata": {
                    "source": source,
                    "total_chunks": len(chunks),
                    "processed_at": datetime.now().isoformat()
                },
                "embedding": embedding
            }
            
            result = supabase.table('knowledge_base').insert(data).execute()
            doc_id = result.data[0]['id']
            print_progress(f"  Stored successfully (ID: {doc_id})", "success")
            
            # Small delay to show progress
            time.sleep(0.5)
            
        except Exception as e:
            print_progress(f"  Database insert failed", "error", str(e))
            continue
    
    print(f"\n{Colors.GREEN}✅ Document processing complete!{Colors.END}\n")
    print(f"{Colors.CYAN}{'─'*70}{Colors.END}\n")

def show_current_stats():
    """Show current knowledge base statistics"""
    try:
        result = supabase.table('knowledge_base').select('id,url,metadata').execute()
        data = result.data
        
        unique_urls = len(set(d['url'] for d in data))
        total_chunks = len(data)
        sources = set(d['metadata'].get('source', 'Unknown') for d in data if d.get('metadata'))
        
        print(f"\n{Colors.CYAN}{'='*70}")
        print(f"{'CURRENT KNOWLEDGE BASE STATS':^70}")
        print(f"{'='*70}{Colors.END}")
        print(f"  📚 Total Documents: {unique_urls}")
        print(f"  📄 Total Chunks: {total_chunks}")
        print(f"  🗂️  Knowledge Sources: {len(sources)}")
        print(f"{Colors.CYAN}{'='*70}{Colors.END}\n")
        
        return total_chunks
        
    except Exception as e:
        print_progress("Failed to get stats", "error", str(e))
        return 0

def main():
    """Main crawler interface"""
    print_header()
    
    initial_count = show_current_stats()
    
    print(f"{Colors.BOLD}What would you like to add to the knowledge base?{Colors.END}\n")
    print("1. Tonight's RAG Setup Session")
    print("2. Your Protocols & Preferences")
    print("3. SOUTHCOM Project Context")
    print("4. Technical Decision Log")
    print("5. Agentic RAG Training (YouTube transcripts)")
    print("6. Custom URL")
    print("7. Exit\n")
    
    choice = input(f"{Colors.YELLOW}Enter choice (1-7): {Colors.END}")
    
    if choice == "1":
        content = f"""
TRAJANUS RAG SYSTEM SETUP SESSION - December 9, 2025

EXECUTIVE SUMMARY:
Tonight we completed the setup of a permanent AI memory system using RAG (Retrieval-Augmented Generation). 
After an 8-hour marathon session, we successfully deployed a Supabase PostgreSQL database with pgvector 
extension, integrated OpenAI embeddings API, and created a complete pipeline for storing and retrieving 
knowledge across Claude sessions.

KEY ACCOMPLISHMENTS:
- Supabase database created with vector search capabilities
- Complete schema with 4 agentic RAG functions deployed
- Folder structure established (13-Knowledge-Base with 9 categories)
- OpenAI embeddings API integrated and tested
- Python dependencies resolved and verified
- End-to-end pipeline tested and operational

TECHNICAL DETAILS:
The system uses text-embedding-3-small model from OpenAI to generate 1536-dimension vectors for semantic 
search. Content is chunked into 1000-character segments with 200-character overlap to preserve context. 
Supabase stores vectors alongside metadata and enables similarity search using cosine distance.

CHALLENGES OVERCOME:
- Row-Level Security (RLS) blocking initial inserts - solved by temporary disable
- Python module dependency conflicts - resolved with --break-system-packages
- OAuth authentication hanging - switched to console flow
- Google Drive mount point write issues - migrated to Drive API
- OpenAI billing activation delay - added $10 credits

BUSINESS IMPLICATIONS:
This system eliminates the "starting from zero" problem that plagued every session. Future Claude 
instances can query this database and retrieve context instantly. Expected time savings: 15-20 minutes 
per session. ROI achieved after approximately 30 sessions (2 months).

NEXT STEPS:
1. Test continuity with fresh Claude session tomorrow
2. Populate knowledge base with building codes, USACE standards, project docs
3. Integrate with End-of-Session protocol for automated updates
4. Deploy multi-agent "Claude Squad" system for parallel work

TECHNICAL SPECIFICATIONS:
- Database: Supabase PostgreSQL with pgvector
- Embedding Model: text-embedding-3-small (1536 dims)
- Chunk Size: 1000 characters with 200 overlap
- Storage: Vector + metadata + full text
- Search: Cosine similarity with 0.7 threshold
- Cost: ~$1-3/month for typical usage

SESSION PARTICIPANTS:
Bill King (Principal/CEO Trajanus USA) and Claude (AI Assistant)

SESSION DURATION:
Approximately 8 hours (5:00 PM - 1:00 AM EST)

STATUS:
System operational. Database contains test data. Ready for production knowledge ingestion.

KEY INSIGHT:
"This isn't just a database. It's permanent external memory for AI. Every session summary, every 
technical decision, every piece of code - stored permanently and instantly retrievable by any Claude 
instance." - Session reflection, 11:30 PM

QUOTE OF THE SESSION:
Bill: "holy shit how can i test it so you know. I want to show you screenshots agin. this is hard 
collaboration without that ability. i think we fucking did it!"
        """
        
        process_document(
            url="https://trajanus.local/sessions/2025-12-09-rag-setup",
            title="RAG System Setup Session - December 9, 2025",
            source="Session History",
            content=content
        )
    
    elif choice == "2":
        content = """
BILL KING - WORKING PROTOCOLS & PREFERENCES

COMMUNICATION STYLE:
- Direct, military-style communication preferred
- No platitudes or excessive affirmations
- Casual professional interaction ("brothers working outside the wire")
- Foreign language phrases welcome (occasional Spanish, French, German)
- Humor and personal banter about dreams/aspirations encouraged
- Action over affirmation - verify before confirming

SESSION MANAGEMENT:
- Marathon development sessions: 13-16 hours typical
- End-of-Session (EOS) protocol: 5-6 files per session
  * Session Summary
  * Technical Journal
  * Personal Diary
  * Code Repository
  * Handoff document
  * Context Update
- Naming convention: YYYY-MM-DD-HHMM_[CAT]_[Description]
- Categories: DEV, DEBUG, DOC, REVIEW, EXPLORE, QUICK

FILE ARCHITECTURE:
- Google Drive as primary backend: G:\\My Drive\\00 - Trajanus USA\\
- Numbered folders: 00-Command-Center through 12-Credentials
- Source files in C:\\trajanus-command-center\\
- Runtime copies sync to Google Drive on startup
- Electron build process copies source → Drive
- CRITICAL: Edits must target correct location

DOCUMENTATION PHILOSOPHY:
- Documentation = value creation and intellectual property
- Living documents system with 5 master documents
- Automated conversion: CONVERT_AND_APPEND.ps1
- Markdown → Google Docs for Claude accessibility
- Master documents accumulate over time
- Comprehensive session documentation for continuity

CODE PRACTICES:
- "Surgical edits only" protocol
- No token-consuming recreation loops
- Preserve working functionality
- Hub-and-spoke model for multiple Claude instances
- Version control with git when appropriate

TOKEN MANAGEMENT:
- Display color-coded gauge in EVERY response
- Green (>40%), Yellow (20-40%), Red (<20%)
- Format: "🟢 Token Gauge: XX% remaining"
- Critical awareness for long sessions

PROJECT MANAGEMENT:
- Procore: Primary construction management platform
- Primavera P6 & MS Project: Scheduling
- RMS 3.0: USACE projects
- Federal contracting systems integrated

CURRENT FOCUS:
- SOUTHCOM Guatemala contract (W9127823R0034)
- Multiple HAP sites
- January 2026 completion deadline
- Enterprise Hub development (Electron desktop app)
- QCM review automation
- AI-augmented PM methodology development

COLLABORATORS:
- Tom Chlebanowski: Business partner, PE Civil/JD, currently in Kwajalein
- Various federal agency clients: USACE, NAVFAC, VA

VISION:
Create scalable AI-augmented PM methodologies that become intellectual property and training 
materials for the construction industry. The Trajanus Enterprise Hub should serve as both 
personal productivity tool and demonstration platform for the methodology.

TECHNICAL ENVIRONMENT:
- Windows 11
- VS Code for development
- PowerShell for scripts
- Python, Node.js, Electron
- Google Drive integration via API
- Multiple Claude instances for parallel work

CRITICAL DISCOVERY:
Claude cannot read markdown files from Google Drive directly - all documentation must be 
converted to Google Docs format for accessibility across sessions. This breakthrough solved 
months of continuity problems.

EXPECTATIONS:
- Verify claims before making them
- Use tools (past chats, project knowledge) before saying "I don't have access"
- Default to assuming answers are in project knowledge
- Every response must be actionable
- No false confidence - admit uncertainty when appropriate
        """
        
        process_document(
            url="https://trajanus.local/protocols/working-preferences",
            title="Bill King - Working Protocols and Preferences",
            source="Protocols",
            content=content
        )
    
    elif choice == "3":
        content = """
SOUTHCOM GUATEMALA CONTRACT - PROJECT CONTEXT
Contract: W9127823R0034

PROJECT OVERVIEW:
Department of Defense construction project in Guatemala under SOUTHCOM jurisdiction. Multiple HAP 
(Haiti Action Plan) sites requiring infrastructure development, quality control, and comprehensive 
project management services.

CONTRACT DETAILS:
- Client: U.S. Southern Command (SOUTHCOM)
- Contract Number: W9127823R0034
- Project Manager: Bill King, Trajanus USA
- Completion Deadline: January 2026
- Contract Type: Federal construction management

ACTIVE SITES:
- HAP-3: Foundation inspection passed
- HAP-4: Electrical submittal under review
- Additional HAP sites in various phases

PROJECT DELIVERABLES:
- Monthly progress reports
- Schedule updates (Primavera P6 format)
- Quality Control Management (QCM) documentation
- Submittal reviews and approvals
- As-built documentation
- Earned Value reporting

CURRENT STATUS:
- Overall project progressing on schedule
- HAP-3 foundation work completed and inspected
- HAP-4 electrical systems in submittal review phase
- 47 submittals processed this month
- 3 outstanding deficiencies requiring resolution

QUALITY MANAGEMENT:
QCM (Quality Control Management) system implemented using 6-category framework:
1. Submittal review and approval
2. Material testing and verification
3. Construction inspection
4. Deficiency tracking and resolution
5. Documentation and record keeping
6. Final acceptance and closeout

SCHEDULE MANAGEMENT:
- Primary tool: Primavera P6
- Backup: MS Project
- Update frequency: Bi-weekly
- Critical path monitoring active
- Float analysis performed monthly

REPORTING REQUIREMENTS:
- Monthly progress report with earned value analysis
- Schedule narrative explaining variances
- Cost reports (if applicable)
- Safety reports and incident tracking
- Quality reports with deficiency status

CHALLENGES:
- Remote location logistics
- International construction standards compliance
- Coordination with SOUTHCOM requirements
- Documentation in both English and Spanish
- Limited site access periods

SUCCESS FACTORS:
- Comprehensive QCM system
- Proactive submittal management
- Strong communication with SOUTHCOM
- Detailed documentation practices
- Integration with Trajanus Enterprise Hub

INTEGRATION WITH RAG SYSTEM:
Project documents, submittals, specifications, and decisions will be crawled into knowledge base 
for instant retrieval. Expected benefits:
- Faster submittal reviews (30 min → 5 min)
- Instant access to specification requirements
- Historical decision tracking
- Automated compliance checking
- Pattern recognition across similar projects

FILES TO INGEST:
- Contract specifications
- Submittal logs
- Inspection reports
- Meeting minutes
- Correspondence files
- RFI responses
- Change orders
- Monthly progress reports

NEXT ACTIONS:
1. Upload contract specifications to 03-Project-History/2025-Q1/
2. Process submittal templates into knowledge base
3. Add USACE standards specific to this contract
4. Integrate QCM templates for automated review
5. Train system on past project decisions
        """
        
        process_document(
            url="https://trajanus.local/projects/southcom-guatemala",
            title="SOUTHCOM Guatemala Contract - W9127823R0034",
            source="Project History",
            content=content
        )
    
    elif choice == "4":
        content = """
TECHNICAL DECISIONS LOG - TRAJANUS ENTERPRISE HUB

DECISION: Use Electron for Desktop Application Framework
DATE: November 2024
RATIONALE:
- Cross-platform support (Windows, Mac, Linux)
- Familiar web technologies (HTML, CSS, JavaScript)
- Strong ecosystem and community support
- Easy integration with Google Drive API
- Bill already experienced with web development
- Native desktop features accessible via Node.js

ALTERNATIVES CONSIDERED:
- Qt Framework: Rejected due to C++ learning curve
- .NET/WPF: Rejected due to Windows-only limitation
- Native web app: Rejected due to limited offline capabilities

OUTCOME: Successful. Application functional and integrating well with Google Drive.

---

DECISION: Google Drive as Primary Backend
DATE: October 2024
RATIONALE:
- Already using Drive for document management
- Familiar interface for Bill and team
- Excellent API support
- Automatic sync across devices
- Version history built-in
- Shareable with Tom and clients when needed

ALTERNATIVES CONSIDERED:
- Local SQLite database: Rejected due to sync complexity
- AWS S3: Rejected due to cost and complexity
- Dropbox: Rejected due to API limitations

OUTCOME: Successful. Drive API working well despite initial OAuth challenges.

---

DECISION: Convert Markdown to Google Docs for Claude Access
DATE: December 2025
RATIONALE:
- Claude cannot read markdown files from Google Drive
- Context loss between sessions was crippling workflow
- Google Docs format is Claude-accessible
- Automated conversion via CONVERT_AND_APPEND.ps1
- Preserves markdown for source control

ALTERNATIVES CONSIDERED:
- Keep markdown only: Rejected - Claude can't read it
- Manual conversion: Rejected - too time consuming
- Different documentation format: Rejected - markdown is standard

OUTCOME: Breakthrough success. Solved months of continuity problems.

---

DECISION: Supabase for RAG Database
DATE: December 9, 2025
RATIONALE:
- PostgreSQL with pgvector extension
- Excellent free tier for testing
- Managed service - no infrastructure management
- Strong API and Python client
- Built-in authentication and security
- Dashboard for visualization

ALTERNATIVES CONSIDERED:
- Pinecone: Rejected due to cost for small scale
- Weaviate: Rejected due to self-hosting complexity
- Local PostgreSQL: Rejected due to maintenance burden
- ChromaDB: Rejected due to limited production features

OUTCOME: Successful after RLS configuration issues resolved.

---

DECISION: OpenAI Embeddings (text-embedding-3-small)
DATE: December 9, 2025
RATIONALE:
- Industry standard for embeddings
- 1536 dimensions balances quality and performance
- Excellent semantic search capabilities
- Cost-effective ($0.02 per 1M tokens)
- Easy integration with existing OpenAI usage

ALTERNATIVES CONSIDERED:
- Sentence Transformers: Rejected due to hosting requirements
- Cohere embeddings: Rejected due to unfamiliarity
- Custom trained model: Rejected due to time/complexity

OUTCOME: Working perfectly. Semantic search proving very effective.

---

DECISION: 6-Category QCM System
DATE: 2024
RATIONALE:
- Comprehensive coverage of quality management needs
- Aligns with USACE requirements
- Proven effective on past projects
- Trackable and auditable
- Integrates with submittal workflow

CATEGORIES:
1. Submittal Review
2. Material Testing
3. Construction Inspection
4. Deficiency Tracking
5. Documentation
6. Final Acceptance

OUTCOME: Successful. System working well for SOUTHCOM project.

---

DECISION: Surgical Edits Protocol for Code
DATE: November 2025
RATIONALE:
- Token-consuming recreation loops were breaking workflow
- Preserve working functionality
- Faster iteration cycles
- Less risk of introducing bugs
- Better version control

IMPLEMENTATION:
- Edit specific functions/sections only
- Always preserve surrounding code
- Test each edit before proceeding
- Document why changes made

OUTCOME: Dramatically improved development speed and reliability.

---

DECISION: Hub-and-Spoke Multiple Claude Instances
DATE: November 2025
RATIONALE:
- Parallel work on different components
- Isolate complex debugging from main work
- Fresh context for new problems
- Avoid context window exhaustion

APPROACH:
- Main session: Overall coordination
- Specialist sessions: Deep dives on specific issues
- Document handoffs between instances
- Consolidate learnings back to main

OUTCOME: Effective but requires good handoff documentation.

---

DECISION: End-of-Session Protocol
DATE: October 2025
RATIONALE:
- Continuity between sessions was poor
- Information loss was expensive
- Need systematic knowledge capture
- Create reusable documentation
- Build intellectual property

PROTOCOL:
- Session Summary (accomplishments, blockers, next steps)
- Technical Journal (detailed technical decisions)
- Personal Diary (reflections, insights, frustrations)
- Code Repository (working code samples)
- Handoff Document (context for next session)
- Context Update (master document updates)

OUTCOME: Game-changing for continuity and IP development.

---

DECISION FRAMEWORK:
When making technical decisions, consider:
1. Alignment with overall architecture
2. Bill's existing skills and learning curve
3. Integration with current tools (Drive, Procore, etc.)
4. Cost (time and money)
5. Maintenance burden
6. Scalability for future needs
7. Documentation and support available

LESSONS LEARNED:
- Invest time upfront in infrastructure that reduces friction
- Automation is worth the setup time
- Documentation is intellectual property
- Working code beats perfect architecture
- Small, verified steps beat big rewrites
- Context preservation is critical for AI collaboration
        """
        
        process_document(
            url="https://trajanus.local/decisions/technical-log",
            title="Technical Decisions Log - Architecture and Rationale",
            source="Technical Decisions",
            content=content
        )
    
    elif choice == "5":
        print_progress("YouTube transcript processing", "working", "Feature coming soon")
        print(f"\n{Colors.YELLOW}Note: This would process the 3 Agentic RAG training videos{Colors.END}")
        print(f"{Colors.YELLOW}Feature requires YouTube transcript API integration{Colors.END}\n")
        return
    
    elif choice == "6":
        url = input(f"\n{Colors.YELLOW}Enter URL to scrape: {Colors.END}")
        title = input(f"{Colors.YELLOW}Document title: {Colors.END}")
        source = input(f"{Colors.YELLOW}Source category: {Colors.END}")
        
        process_document(url, title, source)
    
    elif choice == "7":
        print(f"\n{Colors.GREEN}Exiting crawler. Knowledge base updated!{Colors.END}\n")
        return
    
    # Show updated stats
    final_count = show_current_stats()
    added = final_count - initial_count
    
    if added > 0:
        print(f"{Colors.GREEN}{Colors.BOLD}📊 Added {added} new chunks to knowledge base!{Colors.END}\n")
        print(f"{Colors.CYAN}Open the dashboard to see your new content:{Colors.END}")
        print(f"  file:///{os.path.abspath('../kb_dashboard.html')}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Crawler interrupted. Exiting...{Colors.END}\n")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.END}\n")
