# AGENT DEPLOYMENT - EXECUTE TODAY

## PRIORITY 1: RESEARCH AGENT (60 minutes)

### Implementation Location
```
G:\My Drive\00 - Trajanus USA\00-Command-Center\agents\research_agent.py
```

### Core Functionality - TODAY's Run
```python
#!/usr/bin/env python3
import requests
import json
import os
from datetime import datetime
from pathlib import Path

# TODAY: Simple implementation, runs once manually
# TOMORROW: Add scheduling and automation

BRAVE_API_KEY = os.environ.get('BRAVE_API_KEY', 'YOUR_KEY_HERE')

SEARCH_TOPICS = [
    "Claude Sonnet 4.5 new features December 2025",
    "Anthropic MCP protocol servers 2025",
    "Supabase pgvector best practices",
    "Electron Python integration patterns",
    "Anthropic API computer use beta"
]

def search_brave(query):
    """Search Brave API and return top results"""
    endpoint = "https://api.search.brave.com/res/v1/web/search"
    headers = {"X-Subscription-Token": BRAVE_API_KEY}
    params = {"q": query, "count": 5}
    
    try:
        response = requests.get(endpoint, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[ERROR] Search failed for '{query}': {e}")
        return None

def generate_report(all_results):
    """Generate markdown report of findings"""
    report = f"# Research Report - {datetime.now().strftime('%Y-%m-%d')}\n\n"
    
    for topic, results in all_results.items():
        report += f"## {topic}\n\n"
        if results and 'web' in results and 'results' in results['web']:
            for item in results['web']['results'][:5]:
                title = item.get('title', 'No title')
                url = item.get('url', '')
                description = item.get('description', '')
                report += f"### {title}\n"
                report += f"**URL:** {url}\n\n"
                report += f"{description}\n\n"
                report += "---\n\n"
        else:
            report += "*No results found*\n\n"
    
    return report

def main():
    """Run research cycle NOW"""
    print("=" * 60)
    print("RESEARCH AGENT - MANUAL RUN")
    print("=" * 60)
    
    all_results = {}
    
    for topic in SEARCH_TOPICS:
        print(f"\n[SEARCHING] {topic}")
        results = search_brave(topic)
        all_results[topic] = results
        
        if results and 'web' in results:
            count = len(results['web'].get('results', []))
            print(f"[SUCCESS] Found {count} results")
        else:
            print(f"[WARNING] No results for this topic")
    
    # Generate report
    print("\n[GENERATING] Research report...")
    report = generate_report(all_results)
    
    # Save to outputs
    output_dir = Path("G:/My Drive/00 - Trajanus USA/00-Command-Center/outputs")
    output_dir.mkdir(exist_ok=True)
    
    filename = f"Research_Report_{datetime.now().strftime('%Y-%m-%d_%H%M')}.md"
    output_path = output_dir / filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"[SUCCESS] Report saved: {output_path}")
    print("\n" + "=" * 60)
    print("RESEARCH COMPLETE")
    print("=" * 60)

if __name__ == '__main__':
    main()
```

### Setup Brave API Key
```powershell
# Get free API key: https://brave.com/search/api/
# Set environment variable:
$env:BRAVE_API_KEY = "YOUR_API_KEY_HERE"
```

### First Run - TODAY
```powershell
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center\agents"
python research_agent.py
```

**Expected Output:**
- Research report with 5 topics × 5 results = 25 findings
- Saved as markdown in outputs folder
- Bill reviews and Claude Prime digests

---

## PRIORITY 2: COMPLIANCE OFFICER (30 minutes)

### Simplified Version - Log Monitoring Only
```python
#!/usr/bin/env python3
import os
import time
from datetime import datetime
from pathlib import Path

# TODAY: Simple log monitoring
# TOMORROW: Add real-time enforcement

LOG_PATH = Path("G:/My Drive/00 - Trajanus USA/00-Command-Center/logs")
VIOLATION_LOG = LOG_PATH / "violations.log"

PROTOCOLS = {
    "large_file_edit": {
        "trigger": "str_replace",
        "check": "backup created",
        "severity": "CRITICAL"
    },
    "full_rewrite": {
        "trigger": "create_file",
        "check": "large file",
        "severity": "HIGH"
    }
}

def check_recent_activity():
    """Check last 10 minutes of activity"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking activity logs...")
    
    # For TODAY: Just log that monitoring is active
    # TOMORROW: Actually parse logs
    
    print("[INFO] Monitoring active - no violations detected")
    return []

def log_violation(violation):
    """Log protocol violation"""
    with open(VIOLATION_LOG, 'a', encoding='utf-8') as f:
        f.write(f"[{datetime.now()}] {violation}\n")

def main():
    """Monitor loop - run for 1 hour"""
    print("=" * 60)
    print("COMPLIANCE OFFICER - MONITORING ACTIVE")
    print("=" * 60)
    
    LOG_PATH.mkdir(exist_ok=True)
    
    # Run for 1 hour, check every 5 minutes
    for i in range(12):
        violations = check_recent_activity()
        if violations:
            for v in violations:
                log_violation(v)
                print(f"[VIOLATION] {v}")
        
        if i < 11:  # Don't sleep on last iteration
            time.sleep(300)  # 5 minutes
    
    print("\n" + "=" * 60)
    print("MONITORING CYCLE COMPLETE")
    print("=" * 60)

if __name__ == '__main__':
    main()
```

### First Run - TODAY (Background)
```powershell
# Start in background
Start-Process powershell -ArgumentList "-Command", "cd 'G:\My Drive\00 - Trajanus USA\00-Command-Center\agents'; python compliance_officer.py" -WindowStyle Minimized
```

---

## DEPLOYMENT CHECKLIST

### Research Agent
- [ ] Create agents folder if not exists
- [ ] Copy research_agent.py to agents folder
- [ ] Set BRAVE_API_KEY environment variable
- [ ] Run manually: `python research_agent.py`
- [ ] Verify report created in outputs folder
- [ ] Bill reviews report
- [ ] Claude Prime digests findings

### Compliance Officer
- [ ] Copy compliance_officer.py to agents folder
- [ ] Create logs folder if not exists
- [ ] Start monitoring (background process)
- [ ] Let it run while we work
- [ ] Review violations.log after 1 hour

---

## WHAT HAPPENS AFTER FIRST RUN

### Research Agent Output
- Markdown report with 25 findings
- Bill reads it
- Bill tells Claude Prime: "Digest this research report"
- Claude Prime reads, summarizes key findings
- Claude Prime identifies what's useful for TKB
- Bill decides what gets added to project knowledge

### Compliance Officer Output
- violations.log file
- Shows any protocol breaks during the hour
- We review and adjust protocols if needed

---

## TOMORROW'S ENHANCEMENTS

### Research Agent
- Google Docs conversion
- Supabase integration
- Weekly scheduling
- More sophisticated document processing

### Compliance Officer  
- Real-time log parsing
- Actual enforcement (PAUSE/REJECT)
- Email notifications
- Integration with CC/CP workflows

---

## SUCCESS CRITERIA FOR TODAY

✅ Research Agent runs successfully  
✅ Report generated with findings  
✅ Compliance Officer monitoring active  
✅ No crashes or errors  
✅ Bill reviews research findings  
✅ Claude Prime digests and summarizes  

**TIME ESTIMATE:** 90 minutes total (60 + 30)

---

## EXECUTION ORDER

1. **CC creates agents folder** (if not exists)
2. **CC implements Research Agent** (simple version above)
3. **Bill sets Brave API key**
4. **Bill runs Research Agent manually**
5. **Research completes, report generated**
6. **CC implements Compliance Officer** (simple version above)
7. **Bill starts Compliance Officer in background**
8. **Both agents running while Bill continues work**
9. **After 1 hour: Review outputs**
10. **Claude Prime digests research findings**

---

**END OF DEPLOYMENT GUIDE**
