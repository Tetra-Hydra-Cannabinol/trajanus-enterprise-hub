"""
Morning Research Agent for Trajanus Command Center
Runs daily at 6:00 AM via Task Scheduler

Purpose: Gather intelligence on AI capabilities, construction PM tech,
and competitive landscape to support Bill's vision of a commercial
AI-augmented PM platform.

Created: 2025-12-15
"""

import os
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any
import hashlib

# Third-party imports
try:
    from tavily import TavilyClient
    TAVILY_AVAILABLE = True
except ImportError:
    TAVILY_AVAILABLE = False
    print("Warning: Tavily not installed. Run: pip install tavily-python")

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    print("Warning: Supabase not installed. Run: pip install supabase")

# Setup logging
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f"research_agent_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# =============================================================================
# CONFIGURATION
# =============================================================================

# Load environment variables from .env
def load_env():
    env_path = Path(__file__).parent.parent / ".env"
    env_vars = {}
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    return env_vars

ENV = load_env()

# API Keys
TAVILY_API_KEY = ENV.get('TAVILY_API_KEY', os.environ.get('TAVILY_API_KEY', ''))
SUPABASE_URL = ENV.get('SUPABASE_URL', '')
SUPABASE_KEY = ENV.get('SUPABASE_ANON_KEY', '')

# Output paths
OUTPUT_DIR = Path(__file__).parent.parent / "research_output"
OUTPUT_DIR.mkdir(exist_ok=True)

# =============================================================================
# SEARCH TOPICS
# =============================================================================

CORE_TOPICS = [
    # AI/Claude capabilities
    'Claude Sonnet 4.5 new features capabilities',
    'Claude API updates computer use',
    'Anthropic API changes December 2025',
    'MCP protocol servers production',
    'Claude extended thinking',
    'Claude Code CLI new features',

    # Construction PM tech
    'construction project management AI automation',
    'Primavera P6 API integration',
    'Procore API automation',
    'construction QCM automation',
    'earned value management automation',
    'construction submittal management software',

    # Technical stack
    'Electron Python IPC production patterns',
    'Supabase pgvector optimization',
    'Google Drive API rate limits',
    'Node.js Electron security best practices',

    # Competitive intelligence
    'AI construction management platforms',
    'project management automation tools',
    'construction tech startups 2025',
    'AI project management software',

    # Integration patterns
    'multi-agent orchestration patterns',
    'autonomous agent workflows',
    'agent memory systems',
    'RAG retrieval optimization',
    'LangChain production patterns'
]

# Additional topics for recent 30 days
RECENT_TOPICS = [
    'Claude December 2025 announcements',
    'Anthropic announcements December 2025',
    'construction AI news December 2025',
    'project management trends December 2025',
    'AI agent frameworks December 2025',
    'MCP servers new December 2025'
]

# Categories for classification
CATEGORIES = {
    'NEW_CAPABILITIES': [
        'claude', 'anthropic', 'api', 'mcp', 'feature', 'update',
        'capability', 'release', 'launch', 'announcement'
    ],
    'COMPETITIVE_INTEL': [
        'competitor', 'startup', 'platform', 'market', 'company',
        'funding', 'acquisition', 'partnership'
    ],
    'TECH_IMPROVEMENTS': [
        'optimization', 'performance', 'integration', 'pattern',
        'best practice', 'architecture', 'framework'
    ],
    'INDUSTRY_TRENDS': [
        'trend', 'adoption', 'industry', 'construction', 'pm',
        'project management', 'digital transformation'
    ]
}

# =============================================================================
# SEARCH FUNCTIONS
# =============================================================================

class ResearchAgent:
    def __init__(self):
        self.tavily = TavilyClient(api_key=TAVILY_API_KEY) if TAVILY_AVAILABLE and TAVILY_API_KEY else None
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_AVAILABLE and SUPABASE_URL else None
        self.findings = []
        self.seen_urls = set()

    def search_topic(self, query: str, days_back: int = 30) -> List[Dict]:
        """Search a single topic using Tavily API."""
        if not self.tavily:
            logger.warning("Tavily client not available")
            return []

        try:
            # Calculate date filter
            since_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

            response = self.tavily.search(
                query=query,
                search_depth="advanced",
                max_results=10,
                include_answer=True,
                include_raw_content=False,
                include_domains=[],
                exclude_domains=[]
            )

            results = []
            for result in response.get('results', []):
                url = result.get('url', '')

                # Skip duplicates
                if url in self.seen_urls:
                    continue
                self.seen_urls.add(url)

                results.append({
                    'title': result.get('title', ''),
                    'url': url,
                    'content': result.get('content', ''),
                    'score': result.get('score', 0),
                    'query': query,
                    'retrieved_at': datetime.now().isoformat()
                })

            logger.info(f"Found {len(results)} results for: {query}")
            return results

        except Exception as e:
            logger.error(f"Search error for '{query}': {e}")
            return []

    def categorize_finding(self, finding: Dict) -> str:
        """Categorize a finding based on keywords."""
        text = (finding.get('title', '') + ' ' + finding.get('content', '')).lower()

        scores = {}
        for category, keywords in CATEGORIES.items():
            score = sum(1 for kw in keywords if kw in text)
            scores[category] = score

        # Return category with highest score, default to INDUSTRY_TRENDS
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        return 'INDUSTRY_TRENDS'

    def search_all_topics(self) -> List[Dict]:
        """Search all topics with time-weighted emphasis."""
        all_findings = []

        # Search recent topics (last 30 days) - more emphasis
        logger.info("Searching recent topics (30 days)...")
        for topic in RECENT_TOPICS:
            findings = self.search_topic(topic, days_back=30)
            for f in findings:
                f['time_weight'] = 'recent'
                f['category'] = self.categorize_finding(f)
            all_findings.extend(findings)

        # Search core topics (120 days)
        logger.info("Searching core topics (120 days)...")
        for topic in CORE_TOPICS:
            findings = self.search_topic(topic, days_back=120)
            for f in findings:
                f['time_weight'] = 'standard'
                f['category'] = self.categorize_finding(f)
            all_findings.extend(findings)

        self.findings = all_findings
        return all_findings

    def deduplicate_findings(self) -> List[Dict]:
        """Remove duplicate findings based on URL and content similarity."""
        seen_hashes = set()
        unique = []

        for finding in self.findings:
            # Create content hash
            content_hash = hashlib.md5(
                (finding.get('url', '') + finding.get('title', '')).encode()
            ).hexdigest()

            if content_hash not in seen_hashes:
                seen_hashes.add(content_hash)
                unique.append(finding)

        self.findings = unique
        logger.info(f"Deduplicated to {len(unique)} unique findings")
        return unique

    def rank_findings(self) -> List[Dict]:
        """Rank findings by relevance and recency."""
        def score(f):
            base_score = f.get('score', 0.5)
            # Boost recent findings
            if f.get('time_weight') == 'recent':
                base_score *= 1.5
            # Boost NEW_CAPABILITIES
            if f.get('category') == 'NEW_CAPABILITIES':
                base_score *= 1.3
            return base_score

        self.findings.sort(key=score, reverse=True)
        return self.findings

    def generate_morning_brief(self) -> str:
        """Generate the morning intelligence brief."""
        date_str = datetime.now().strftime('%Y-%m-%d')

        # Group by category
        by_category = {}
        for f in self.findings:
            cat = f.get('category', 'INDUSTRY_TRENDS')
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(f)

        # Build brief
        brief = f"""
================================================================================
MORNING INTELLIGENCE BRIEF - {date_str}
================================================================================

NEW KNOWLEDGE (Last 30 Days):
"""
        # Add top 3 NEW_CAPABILITIES
        new_caps = by_category.get('NEW_CAPABILITIES', [])[:3]
        for i, f in enumerate(new_caps, 1):
            brief += f"  {i}. {f['title'][:80]}\n"
            brief += f"     {f['content'][:150]}...\n\n"

        if not new_caps:
            brief += "  No new capabilities found in search.\n\n"

        brief += """
COMPETITIVE LANDSCAPE:
"""
        # Add top 2 COMPETITIVE_INTEL
        comp = by_category.get('COMPETITIVE_INTEL', [])[:2]
        for f in comp:
            brief += f"  - {f['title'][:80]}\n"

        if not comp:
            brief += "  No competitive updates found.\n"

        brief += """
TECHNICAL OPPORTUNITIES:
"""
        # Add top 2 TECH_IMPROVEMENTS
        tech = by_category.get('TECH_IMPROVEMENTS', [])[:2]
        for f in tech:
            brief += f"  - {f['title'][:80]}\n"

        if not tech:
            brief += "  No technical opportunities found.\n"

        brief += """
ACTION ITEMS:
"""
        # Generate action items from top findings
        if new_caps:
            brief += f"  - Investigate: {new_caps[0]['title'][:60]}\n"
        if tech:
            brief += f"  - Evaluate: {tech[0]['title'][:60]}\n"

        brief += f"""
--------------------------------------------------------------------------------
Total findings: {len(self.findings)}
Full report saved to: {OUTPUT_DIR / f'full_report_{date_str}.json'}
================================================================================
"""
        return brief

    def save_to_supabase(self) -> bool:
        """Store findings in Supabase knowledge base."""
        if not self.supabase:
            logger.warning("Supabase client not available")
            return False

        try:
            for finding in self.findings:
                # Prepare record
                record = {
                    'url': f"research://{datetime.now().strftime('%Y%m%d')}/{hashlib.md5(finding['url'].encode()).hexdigest()[:8]}",
                    'title': finding.get('title', 'Untitled'),
                    'summary': finding.get('content', '')[:500],
                    'content': json.dumps(finding),
                    'chunk_number': 0,
                    'metadata': {
                        'source': 'Morning Research Agent',
                        'category': finding.get('category', 'UNKNOWN'),
                        'original_url': finding.get('url', ''),
                        'query': finding.get('query', ''),
                        'retrieved_at': finding.get('retrieved_at', '')
                    }
                }

                # Upsert to knowledge_base
                self.supabase.table('knowledge_base').upsert(record).execute()

            logger.info(f"Saved {len(self.findings)} findings to Supabase")
            return True

        except Exception as e:
            logger.error(f"Supabase save error: {e}")
            return False

    def save_full_report(self) -> Path:
        """Save full report as JSON file."""
        date_str = datetime.now().strftime('%Y-%m-%d')
        report_path = OUTPUT_DIR / f"full_report_{date_str}.json"

        report = {
            'generated_at': datetime.now().isoformat(),
            'total_findings': len(self.findings),
            'categories': {},
            'findings': self.findings
        }

        # Count by category
        for f in self.findings:
            cat = f.get('category', 'UNKNOWN')
            report['categories'][cat] = report['categories'].get(cat, 0) + 1

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        logger.info(f"Full report saved to: {report_path}")
        return report_path

    def run(self) -> str:
        """Execute the full research workflow."""
        logger.info("=" * 60)
        logger.info("MORNING RESEARCH AGENT STARTING")
        logger.info("=" * 60)

        # Search all topics
        self.search_all_topics()

        # Process findings
        self.deduplicate_findings()
        self.rank_findings()

        # Generate outputs
        brief = self.generate_morning_brief()
        self.save_full_report()
        self.save_to_supabase()

        # Save brief to file
        brief_path = OUTPUT_DIR / f"morning_brief_{datetime.now().strftime('%Y-%m-%d')}.txt"
        with open(brief_path, 'w', encoding='utf-8') as f:
            f.write(brief)

        logger.info("=" * 60)
        logger.info("MORNING RESEARCH AGENT COMPLETE")
        logger.info("=" * 60)

        return brief


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    # Check prerequisites
    if not TAVILY_API_KEY:
        print("ERROR: TAVILY_API_KEY not set in .env file")
        print("Add to .env: TAVILY_API_KEY=your_api_key")
        exit(1)

    # Run agent
    agent = ResearchAgent()
    brief = agent.run()

    # Print brief to console
    print(brief)
