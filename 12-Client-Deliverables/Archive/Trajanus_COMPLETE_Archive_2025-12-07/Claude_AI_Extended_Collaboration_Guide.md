# CLAUDE AI EXTENDED COLLABORATION GUIDE
## Best Practices for Long-Term Project Work with AI
### Trajanus USA - Bill King
### Created: December 7, 2025

---

## EXECUTIVE SUMMARY

This guide documents proven strategies for maintaining productive, long-term collaboration with Claude AI across complex, multi-month projects. These practices were compiled from power user research, Anthropic's official documentation, and hard-won lessons from the Trajanus Enterprise Hub development project.

**The Core Problem:** AI assistants don't inherently remember between sessions. Even with memory features, context fades, details get lost, and you end up re-explaining the same things repeatedly. Extended projects require deliberate context engineering.

**The Solution:** A combination of structured documentation, strategic file organization, and disciplined session protocols that give Claude the context it needs to be an effective long-term collaborator.

---

## PART 1: THE 3-DOCUMENT SYSTEM

### Overview

The most effective AI collaboration system uses three core document types that capture different aspects of your work:

### Document 1: CONTEXT PRIMER (Your "State of the Project")

**Purpose:** Captures your current situation, project state, and active context.

**What It Contains:**
- Current project status (what's working, what's broken)
- Active priorities and immediate goals
- Key file locations and folder structures
- Technology stack and tools in use
- Team members and their roles
- Critical deadlines and milestones

**When to Update:** 
- When project status changes significantly
- When priorities shift
- Weekly at minimum, even if just to confirm "no changes"

**Your Implementation:** `Bills_POV.md` + `MASTER_INDEX`

**Example Structure:**
```markdown
# PROJECT CONTEXT PRIMER
Last Updated: 2025-12-07

## Current State
- Enterprise Hub: File browser broken, User Guides working
- QCM Toolkit: Functional, needs testing
- Traffic Studies: Placeholder only

## Active Priorities
1. Fix file browser modal
2. Compile December living documents
3. Prepare system for Tom's use

## Key Locations
- Main app: G:\My Drive\00 - Trajanus USA\00-Command-Center\
- Protocols: 01-Core-Protocols\
- Living docs: 03-Living-Documents\
```

---

### Document 2: DECISION LOG (Your "Why We Did It This Way")

**Purpose:** Records major decisions and the reasoning behind them. This is CRITICAL because AI can help you make decisions, but it won't remember WHY you made them.

**What It Contains:**
- Date of decision
- What was decided (one clear line)
- Why this choice was made (2-3 sentences)
- What alternatives were considered
- When to review/revisit the decision

**When to Update:**
- Every time you make a significant architectural decision
- When you choose one approach over another
- When you establish a new protocol or standard

**Your Implementation:** `Operational_Journal_MASTER`

**Example Entry:**
```markdown
## 2025-12-03: QCM Workspace Architecture

DECISION: Build QCM as tabbed workspace within main app, not standalone page

WHY: Standalone pages caused navigation issues and broke the integrated 
experience. Tabbed approach keeps everything in one window, matches 
Developer Toolkit pattern, and allows multiple reviews simultaneously.

ALTERNATIVES CONSIDERED:
- Standalone HTML page (rejected: navigation breaks)
- Modal popup (rejected: too small for 3-panel layout)
- New Electron window (rejected: complicates state management)

REVIEW DATE: 2025-01-15 (after 6 weeks of use)
```

---

### Document 3: INSIGHT LIBRARY (Your "What We Learned")

**Purpose:** Captures technical insights, lessons learned, and knowledge gained through the work. These are the "aha moments" that would take hours to rediscover.

**What It Contains:**
- Technical discoveries and solutions
- Patterns that work (and don't work)
- Gotchas and pitfalls to avoid
- Code patterns and snippets that solved hard problems
- Integration lessons

**When to Update:**
- When you solve a difficult problem
- When you discover why something wasn't working
- When you find a pattern worth remembering

**Your Implementation:** `Technical_Journal_MASTER` + `Personal_Diary_MASTER`

**Example Entry:**
```markdown
## 2025-12-07: JavaScript Function Conflict Resolution

INSIGHT: Duplicate function names in large JavaScript files cause silent 
failures. The LAST definition wins, so earlier functions get overwritten.

DISCOVERY PROCESS: File browser showed "Error loading files" but console 
showed the API calls were succeeding. Root cause was renderFileList() 
defined twice with different signatures.

SOLUTION PATTERN:
- Prefix functions by scope: renderBrowserFileList(), renderProjectFileList()
- Search for duplicates before adding new functions: 
  grep -n "function functionName" index.html
- Consider JavaScript modules for large files

APPLIES TO: Any JavaScript file over 1000 lines with multiple developers/sessions
```

---

### The End-of-Session Capture Routine

At the end of every valuable session, ask yourself three questions:

1. **"Did I make a decision?"** → Add to Decision Log
2. **"Did I have an insight?"** → Add to Insight Library  
3. **"Did my situation change?"** → Update Context Primer

**Pro Tip:** Ask Claude to help you capture. Use this prompt:

```
Help me capture what matters from this session:
1. What decisions did we make and why?
2. What technical insights did we discover?
3. What changed about the project state?

Format as entries for my Decision Log, Insight Library, and Context Primer.
```

---

## PART 2: THE "ADRENALINE SHOT" FILE

### What It Is

A single, comprehensive context file that you can upload at the start of ANY session to immediately restore Claude's understanding of your project. Think of it as the "previously on..." recap before a TV episode.

### Why It Works

Claude's memory features help with general context, but they can't capture:
- Specific file locations and IDs
- Current project state details
- What's broken vs. what's working
- Learned failures and anti-patterns
- Critical technical constraints

The adrenaline shot file fills these gaps instantly.

### Structure Template

```markdown
# [PROJECT NAME] CONTEXT FILE
## Quick-Start for Claude AI Sessions
Last Updated: [DATE] by [WHO]

---

## 🎯 CURRENT MISSION
[One paragraph describing what we're building and why it matters]

---

## 📊 PROJECT STATUS

### What's Working ✅
- [Component 1]: [Status details]
- [Component 2]: [Status details]

### What's Broken ❌
- [Issue 1]: [Brief description, when it broke]
- [Issue 2]: [Brief description, when it broke]

### In Progress 🔄
- [Task 1]: [Current state]
- [Task 2]: [Current state]

---

## 📁 CRITICAL FILE LOCATIONS

### Primary Workspace
- Main application: [full path]
- Configuration: [full path]
- Scripts: [full path]

### Documentation
- Living Documents: [full path]
- Session Journals: [full path]
- Protocols: [full path]

### Google Doc IDs (for Claude to fetch)
- Master Index: [Google Doc ID]
- Technical Journal: [Google Doc ID]
- Personal Diary: [Google Doc ID]
- Decision Log: [Google Doc ID]

---

## 🛠️ TECHNOLOGY STACK

- **Frontend:** [technologies]
- **Backend:** [technologies]
- **Storage:** [technologies]
- **Key Libraries:** [list]

---

## ⚠️ HARD RULES (Never Violate These)

1. **[Rule 1]:** [Explanation of why]
2. **[Rule 2]:** [Explanation of why]
3. **[Rule 3]:** [Explanation of why]

Example rules:
- All files live in Google Drive, never local storage
- Never rewrite entire code sections - surgical edits only
- Always create timestamped backup before editing
- Ask before executing any destructive operation

---

## 🚫 LEARNED FAILURES (Don't Repeat These)

| Date | What Went Wrong | Root Cause | Prevention |
|------|-----------------|------------|------------|
| [Date] | [Issue] | [Cause] | [How to avoid] |

---

## 📋 ACTIVE PROTOCOLS

### Session Start
1. [Step 1]
2. [Step 2]

### Session End
1. [Step 1]
2. [Step 2]

### Code Changes
1. [Step 1]
2. [Step 2]

---

## 👤 USER PREFERENCES

- **Communication Style:** [Description]
- **Time Format:** [24-hour/AM-PM]
- **File Naming:** [Convention]
- **Response Format:** [Preferences]

---

## 🔗 QUICK LINKS

- [Link 1 description](URL)
- [Link 2 description](URL)

---

## 📝 SESSION HANDOFF NOTES
[Notes from previous session about what to do next]
```

### How to Use It

**Option 1: Project Knowledge**
Upload to Claude Project Knowledge. It will be automatically available in every conversation within that project.

**Option 2: Manual Upload**
Keep the file in your Google Drive. At session start, either:
- Upload it directly to the chat
- Ask Claude to fetch it: "Please read the context file at [Google Doc URL]"

**Option 3: Paste Key Sections**
If starting a quick session, paste just the relevant sections (Current Status, Hard Rules, Active Task).

---

## PART 3: HIERARCHICAL DOCUMENTATION (3-Tier System)

### The Problem with Flat Documentation

Dumping everything into one giant document creates problems:
- Claude's context window fills up with irrelevant details
- Important information gets buried
- Updates require editing massive files
- No clear priority of what matters most

### The 3-Tier Solution

**Tier 1: Foundation (Always Loaded)**
- Master context file (your adrenaline shot)
- Core protocols and hard rules
- Project architecture overview
- ~100-200 lines, updated weekly

**Tier 2: Component (Loaded When Relevant)**
- System-specific documentation
- Feature specifications
- Integration guides
- ~200-500 lines per component, updated as needed

**Tier 3: Feature (Loaded On-Demand)**
- Daily session files
- Code repository entries
- Specific implementation details
- Variable length, created as needed

### How It Works in Practice

```
Session starts:
├── Tier 1 automatically loaded (from Project Knowledge/Memory)
│
├── User mentions "QCM workspace"
│   └── Claude fetches Tier 2: QCM_Workspace_Spec.md
│
└── User asks about specific function
    └── Claude fetches Tier 3: Code_Repository_2025-12-05.md
```

### Your Folder Structure Aligned to Tiers

```
G:\My Drive\00 - Trajanus USA\
│
├── 00-Command-Center\          # Application files
│
├── 01-Core-Protocols\          # TIER 1: Foundation
│   ├── TRAJANUS_CONTEXT.md     # Adrenaline shot
│   ├── Operational_Protocols.md
│   └── [Master documents]
│
├── 02-Templates\               # TIER 2: Component
│
├── 03-Living-Documents\        # TIER 1: Foundation (Masters)
│   ├── Personal_Diary_MASTER
│   ├── Technical_Journal_MASTER
│   └── [Other masters]
│
├── 07-Session-Journal\         # TIER 3: Feature
│   ├── Technical-Journals\
│   ├── Personal-Diaries\
│   ├── Session-Summaries\
│   └── Code-Repositories\
│
└── 08-EOS-Files\               # TIER 3: Feature
    └── [Daily EOS packages]
```

---

## PART 4: SESSION PROTOCOLS

### Session Start Protocol

**1. Context Check (30 seconds)**
- Claude checks memory for project context
- Claude reads Project Knowledge files
- If context seems incomplete, Claude searches past chats

**2. State Verification (1 minute)**
Ask: "Based on your context, what do you understand about:
- Current project state?
- What we're working on?
- Any blockers or issues?"

If Claude's understanding is wrong or incomplete, provide the adrenaline shot file.

**3. Session Goal Setting (1 minute)**
Clearly state: "Today we're going to [specific goal]. The success criteria is [measurable outcome]."

**4. Begin Work**
Proceed with confidence that Claude has proper context.

---

### Session End Protocol (EOS)

**1. Work Completion Check**
- Verify all tasks are complete or documented as incomplete
- Test any code changes
- Confirm files are saved to correct locations

**2. Document Creation**
Create these files (as needed):
- Session Summary: High-level overview of what was accomplished
- Technical Journal: Technical details, code changes, solutions
- Personal Diary: Reflections, frustrations, insights
- Code Repository: Actual code written during session
- Next Session Handoff: What to do next, any blockers

**3. Master Document Updates**
- Append session entries to appropriate MASTER documents
- Update TRAJANUS_CONTEXT.md if project state changed
- Update Decision Log if major decisions were made

**4. File Delivery**
- Provide download links for all created files
- Confirm user has downloaded/saved everything
- Verify files are in correct Google Drive locations

**5. Handoff Creation**
Create NEXT_SESSION_HANDOFF.md with:
- What was accomplished
- What's next
- Any blockers or issues
- Files created this session

---

### The Question Mark Protocol

When you ask Claude a question (message contains "?"), Claude should:

1. Provide Q/A response showing understanding of request
2. Ask: "Do I have green light to proceed?"
3. Wait for explicit confirmation before executing

**Why This Matters:**
- Prevents wasted effort on misunderstood instructions
- Catches errors before they compound
- Maintains human control over important decisions

---

## PART 5: MEMORY MANAGEMENT

### How Claude's Memory Works

**Built-in Memory (Automatic):**
- Claude learns patterns from your conversations
- Remembers preferences, communication style, project context
- Scoped per-project in Claude Projects
- Updated periodically in background (not instant)

**Project Knowledge (Manual):**
- Files you upload to Project Knowledge
- Always available in that project's conversations
- You control what's included
- Can be updated anytime

**Past Chat Search (On-Demand):**
- Claude can search previous conversations
- Useful for finding specific discussions
- Not automatic - must be triggered

### Memory Limitations to Understand

1. **Memory is summative, not verbatim** - Claude remembers patterns and facts, not exact conversations

2. **Recent bias** - More recent conversations are better remembered

3. **Work-focused filtering** - Claude prioritizes professional/work context over personal details

4. **Not instant** - Changes take time to propagate to memory

5. **Project-scoped** - Each project has separate memory; they don't share

### Optimizing Memory

**Do:**
- Use Project Knowledge for critical, stable information
- Explicitly tell Claude to remember important decisions
- Create structured documents Claude can reference
- Update your adrenaline shot file regularly

**Don't:**
- Rely solely on automatic memory for complex projects
- Assume Claude remembers specific details from weeks ago
- Expect instant memory updates
- Put sensitive data in memory (use incognito for confidential chats)

---

## PART 6: WHEN THINGS GO WRONG

### Symptom: Claude Seems Confused About the Project

**Diagnosis:** Context not loaded or outdated

**Fix:**
1. Upload your adrenaline shot file
2. Explicitly state current project state
3. Have Claude confirm understanding before proceeding

---

### Symptom: Claude Keeps Making the Same Mistakes

**Diagnosis:** Learned failures not documented

**Fix:**
1. Document the failure pattern in your adrenaline shot
2. Add to "Hard Rules" or "Learned Failures" section
3. Explicitly remind Claude at session start

---

### Symptom: Can't Find Previous Work

**Diagnosis:** Poor documentation or organization

**Fix:**
1. Use consistent naming conventions
2. Maintain MASTER_INDEX with all document links
3. Use Claude's past chat search feature
4. Keep files in designated folders, not scattered

---

### Symptom: Session Context Degrades Over Long Conversations

**Diagnosis:** Context window filling up

**Fix:**
1. Start new conversations for new topics
2. Summarize and "restart" for very long sessions
3. Use the 3-tier system to load only relevant context
4. For multi-hour sessions, do periodic "context refresh"

---

### Symptom: Code Changes Don't Persist

**Diagnosis:** Editing wrong files or sync issues

**Fix:**
1. Verify file paths before editing
2. Check for Google Drive sync conflicts
3. Always edit source files, not runtime copies
4. Verify changes with file system commands, not just IDE

---

## PART 7: TOOLS AND COMMANDS

### Useful Claude Commands

**Search Past Chats:**
"Search our previous conversations for [topic]"

**Fetch Google Doc:**
"Read the document at [Google Doc URL]"

**Check Memory:**
"What do you remember about [topic]?"

**Update Memory:**
"Please remember that [important fact]"

**Project Knowledge Search:**
"Search project knowledge for [topic]"

---

### PowerShell Commands for File Verification

```powershell
# Check if file exists and show size
Get-Item "G:\My Drive\00 - Trajanus USA\00-Command-Center\index.html"

# Search for text in files
Select-String -Path "*.html" -Pattern "functionName" -Context 2,2

# List recent files
Get-ChildItem -Path "G:\My Drive\00 - Trajanus USA" -Recurse | 
  Where-Object {$_.LastWriteTime -gt (Get-Date).AddDays(-1)} |
  Sort-Object LastWriteTime -Descending

# Compare file sizes (detect if file was actually modified)
(Get-Item "file.html").Length
```

---

### Google Drive Search Syntax

When asking Claude to search Google Drive:

```
# By name
name contains 'keyword'

# By content
fullText contains 'keyword'

# By date
modifiedTime > '2025-12-01'

# By type
mimeType = 'application/vnd.google-apps.document'

# Combined
name contains 'Journal' and modifiedTime > '2025-12-01'
```

---

## PART 8: QUICK REFERENCE CARD

### Session Start Checklist
- [ ] Claude has project context (check understanding)
- [ ] State session goal clearly
- [ ] Identify success criteria
- [ ] Upload adrenaline shot if needed

### Session End Checklist
- [ ] All work saved to Google Drive
- [ ] Session summary created
- [ ] Technical changes documented
- [ ] Masters updated (if applicable)
- [ ] Handoff created for next session
- [ ] All files downloaded/verified

### Before Any Major Change
- [ ] Create timestamped backup
- [ ] Confirm understanding with Claude
- [ ] Get explicit "green light"
- [ ] Test after implementation
- [ ] Document what was done

### Weekly Maintenance
- [ ] Update TRAJANUS_CONTEXT.md
- [ ] Review and clean up old files
- [ ] Verify masters are current
- [ ] Check for orphaned documents

---

## APPENDIX: TRAJANUS-SPECIFIC INFORMATION

### Folder Structure
```
G:\My Drive\00 - Trajanus USA\
├── 00-Command-Center\      (Active app files)
├── 01-Core-Protocols\      (SOPs, guides)
├── 02-Templates\           (Reusable templates)
├── 03-Living-Documents\    (MASTER files)
├── 04-Scripts\             (Automation scripts)
├── 07-Session-Journal\     (Daily entries by type)
├── 08-EOS-Files\           (End of session packages)
├── 09-Active-Projects\     (Current project work)
├── 10-Templates\           (Document templates)
├── 11-Personal\            (Personal notes)
└── 12-Credentials\         (API keys, tokens)
```

### Master Document Google Doc IDs
- Personal_Diary_November_2025_MASTER: `1HKOisNN8A5rf9YdFJnJSdgH326bdJTun2rDqObNvrM8`
- Technical_Journal_November_2025_MASTER: `1iPZAmi2bYBRmDnsgwZK3UZFCsB_YHj9RvRtKWJqDb2Q`
- Bills_Training_Log_MASTER: `1SitDxz6qUYEYL5r3eijsqmNmdogCRyg5fTYeCkKWi1c`
- MASTER_INDEX_November_2025: `1WXOqLE3WZdYaSa1OYl3fYgw-WwsNaasGsuE5znYlLRs`

### Critical Protocols
- **Question Mark Protocol:** Always confirm before executing
- **24-Hour Clock:** All timestamps in 24-hour format
- **No Local Storage:** Everything lives in Google Drive
- **Surgical Edits:** Never rewrite entire files
- **Backup First:** Always create timestamped backup

### Communication Style
- Super casual, professional collaboration
- Direct and honest
- No military jargon
- Token gauge at bottom of every response

---

## DOCUMENT HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-07 | Claude Opus 4.5 | Initial creation from research |

---

*"The best AI collaboration isn't about having the smartest AI—it's about giving the AI the context it needs to be smart about YOUR work."*
