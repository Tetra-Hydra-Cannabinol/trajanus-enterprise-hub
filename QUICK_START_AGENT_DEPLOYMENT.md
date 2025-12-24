# AGENT DEPLOYMENT - QUICK START

## 📋 WHAT YOU'RE DEPLOYING

1. **Research Agent** - Searches Brave API for latest Claude/MCP/Supabase info
2. **Compliance Officer** - Monitors for protocol violations (runs in background)

Both agents are SIMPLIFIED for first run. Full features come tomorrow.

---

## 🚀 STEP-BY-STEP EXECUTION

### STEP 1: Create Agents Folder (30 seconds)

```powershell
mkdir "G:\My Drive\00 - Trajanus USA\00-Command-Center\agents"
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center\agents"
```

### STEP 2: Download Files from Claude (1 minute)

Download these 3 files from Claude's outputs:
- `research_agent.py`
- `compliance_officer.py`  
- `CC_AGENT_DEPLOYMENT_TODAY.md`

Save all 3 to: `G:\My Drive\00 - Trajanus USA\00-Command-Center\agents\`

### STEP 3: Get Brave API Key (2 minutes)

1. Go to: https://brave.com/search/api/
2. Click "Get Started" 
3. Sign up with email (free tier: 2000 searches/month)
4. Copy your API key

### STEP 4: Set Environment Variable (30 seconds)

```powershell
$env:BRAVE_API_KEY = "YOUR_API_KEY_HERE"
```

### STEP 5: Run Research Agent (3 minutes)

```powershell
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center\agents"
python research_agent.py
```

**Expected Output:**
```
======================================================================
RESEARCH AGENT - MANUAL RUN
======================================================================
[SEARCHING] Claude Sonnet 4.5 new features December 2025...
[SUCCESS] Found 5 results
[SEARCHING] Anthropic MCP protocol servers 2025...
[SUCCESS] Found 5 results
...
[SUCCESS] Report saved: G:\My Drive\00 - Trajanus USA\00-Command-Center\outputs\Research_Report_20251216_1430.md
```

### STEP 6: Start Compliance Officer (30 seconds)

Open a NEW PowerShell window:

```powershell
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center\agents"
python compliance_officer.py
```

Minimize this window - let it run in background for 1 hour.

### STEP 7: Review Research Report (10 minutes)

Open the research report that was just generated:
```
G:\My Drive\00 - Trajanus USA\00-Command-Center\outputs\Research_Report_YYYYMMDD_HHMM.md
```

Read through the findings. Identify what's useful.

### STEP 8: Tell Claude Prime to Digest (RIGHT NOW)

Come back to this chat and say:

**"Claude, digest the research report that was just generated. Summarize key findings about Claude updates, MCP developments, and Supabase features. Tell me what's new and useful for our system."**

---

## ✅ SUCCESS CRITERIA

After completing steps above, you should have:

✅ Research Agent executed successfully  
✅ Report generated with ~25 findings across 5 topics  
✅ Compliance Officer running in background  
✅ Research report open for review  
✅ Claude Prime ready to digest findings  

---

## 🔍 TROUBLESHOOTING

**"BRAVE_API_KEY not set"**
- Run: `$env:BRAVE_API_KEY = "YOUR_KEY"`
- Make sure you're in the same PowerShell window

**"No module named 'requests'"**
- Run: `pip install requests`

**"Permission denied"**
- Run PowerShell as Administrator
- Or: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

**Research Agent fails to connect**
- Check internet connection
- Verify API key is correct
- Check if firewall blocking Brave API

---

## ⏱️ TIME ESTIMATE

- Setup: 5 minutes
- Research Agent run: 3 minutes  
- CO startup: 30 seconds
- Review findings: 10 minutes
- Claude digests: 5 minutes
- **Total: ~25 minutes**

---

## 📊 WHAT HAPPENS NEXT

### Immediate (Today):
1. You read research report
2. Claude Prime digests findings
3. You identify what's valuable
4. We discuss how to integrate new knowledge

### Tomorrow:
1. Add Google Docs conversion to Research Agent
2. Add Supabase integration
3. Schedule weekly runs (Monday 6 AM)
4. Add real enforcement to Compliance Officer
5. Create proper log parsing
6. Add PAUSE/REJECT functionality

### This Week:
1. Full TKB Browser functionality
2. Living docs consolidation working
3. Agents fully automated
4. Knowledge base growing automatically

---

## 🎯 THE GOAL

**By end of today:**
- Both agents operational
- First research cycle complete
- New knowledge identified
- System learning from the web

**By end of week:**
- Agents running autonomously
- TKB growing automatically
- Protocol enforcement active
- You have working AI research team

---

**START NOW - STEP 1**

```powershell
mkdir "G:\My Drive\00 - Trajanus USA\00-Command-Center\agents"
cd "G:\My Drive\00 - Trajanus USA\00-Command-Center\agents"
```

Then download the 3 files from Claude's outputs above.
