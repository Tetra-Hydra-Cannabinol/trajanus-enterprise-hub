---
description: End of Session Protocol - Generate all 5 living documents and run /reflect
allowed-tools: Write, Read, Bash(mkdir:*), Bash(dir:*), Skill
---

# End of Session (EOS) Protocol

## Context

- Today's date: !`powershell -Command "Get-Date -Format 'yyyy-MM-dd'"`
- Current working directory: !`cd`
- Session context gathered from conversation history

## Output Location

```
G:\My Drive\00 - Trajanus USA\00-Command-Center\08-EOS-Files\001 Claude EOS Output\
```

## Your Task

Execute the complete End of Session protocol by generating all 5 living documents. Each document should be saved with today's date in the filename.

### Step 1: Create Output Directory (if needed)

Ensure the output folder exists:
```
G:\My Drive\00 - Trajanus USA\00-Command-Center\08-EOS-Files\001 Claude EOS Output\
```

### Step 2: Generate All 5 Living Documents

Create the following files with today's date (YYYY-MM-DD format):

#### 1. Session_Summary_{date}.md
Content should include:
- Session metadata (date, duration, participants)
- Primary objectives accomplished (with status)
- Key decisions made
- Files created/modified
- Outstanding items
- Next session priorities
- Handoff notes

#### 2. Technical_Journal_{date}.md
Content should include:
- Technical work completed
- Code changes made (files, line numbers, descriptions)
- Bugs fixed or encountered
- System configurations
- Technical decisions and rationale
- Architecture notes

#### 3. Bills_Daily_Diary_{date}.md
Content should include:
- Personal reflections on the session
- Challenges faced and how they were addressed
- Wins and accomplishments to celebrate
- Insights and learnings
- Mood and energy observations
- Goals for next session

#### 4. Code_Repository_{date}.md
Content should include:
- Files modified (with paths and line numbers)
- Current state of each: Working/Broken/Partial
- Git commits made (if any)
- Known issues and bugs
- Version notes
- Rollback information if applicable

#### 5. Handoff_{date}.md
Content should include:
- Quick context summary (2-3 sentences)
- Critical items for next session
- Any blockers or urgent issues
- Files to reference at startup
- Opening message template for next session

### Step 3: Verify All Files Created

List the output directory to confirm all 5 files exist.

### Step 4: Run Reflect

After all documents are saved, invoke the `/reflect` skill to capture session reflections.

## Document Format

Each document should:
- Use Markdown formatting
- Include clear headers and sections
- Be comprehensive but concise
- Reference specific files and line numbers where applicable
- Include timestamps where relevant

## Execution Notes

- Generate documents based on the ENTIRE conversation history
- Be thorough - these documents are the primary record of this session
- If uncertain about any details, note them as "unconfirmed" rather than omitting
- Prioritize accuracy over brevity
