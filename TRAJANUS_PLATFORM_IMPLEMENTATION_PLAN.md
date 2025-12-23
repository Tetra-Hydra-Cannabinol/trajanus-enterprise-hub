# TRAJANUS ENTERPRISE PLATFORM IMPLEMENTATION PLAN
## Mission: Transform Concept to Functional Production System

**Date:** 2025-12-14  
**Duration:** 12 Hours  
**Mission Commander:** Bill King, Principal/CEO Trajanus USA  
**Technical Lead:** Claude Sonnet 4.5  
**Execution Model:** Claude Code + Specialized Agents  
**Approach:** 20-Year Veteran - Steady Advance, No Shortcuts  

---

## MISSION OVERVIEW

### Objective
Transform the Trajanus Enterprise Hub from conceptual prototype to fully functional, production-ready platform with proper infrastructure, validated integrations, and commercial-grade workflows.

### Success Criteria
1. ✅ All integrations validated and functional (Supabase KB, Google Drive, etc.)
2. ✅ Seamless chat continuity with automated TKB/living docs
3. ✅ Claude Code operating at full efficiency with agents and MCPs
4. ✅ Platform architecture enabling commercial deployment
5. ✅ Zero baseline code modifications without explicit approval
6. ✅ Complete documentation for every component
7. ✅ Replicable workflows ready for Tom and clients

### Critical Constraints
- **NO DIRECT CODE EDITING** by Claude Sonnet - all through CC/agents
- **NO BASELINE INDEX.HTML MODIFICATIONS** without warning and confirmation
- **NO ASSUMPTIONS** - verify everything before execution
- **NO OPTIONS** - single correct solution per task
- **INDUSTRY STANDARD DOCUMENTATION** for every action

---

## PHASE 1: INFRASTRUCTURE FOUNDATION
**Duration:** 3 Hours  
**Objective:** Build proper orchestration framework for AI-augmented development

### TASK-001: Create .claude.md Context System
**Issue:** No structured context for Claude Code causing assumptions and grep-heavy searches  
**Previous Attempt:** N/A - First Implementation  
**Priority:** CRITICAL - Foundation for all other work  

**Planned Actions:**
1. Analyze current project structure via CC
2. Create main `.claude.md` in root directory
3. Create workspace-specific `.claude.md` for each section:
   - `/qcm-workspace/.claude.md`
   - `/pm-toolkit/.claude.md`
   - `/developer-project/.claude.md`
4. Create `changelog.md` (decision log)
5. Create `plan.md` (task tracking)
6. Populate with comprehensive project documentation

**Reasoning:**
Patrick/Anod insight: .claude.md files become part of Claude's prompt. They eliminate grep searches, reduce cognitive load, provide persistent context. This is foundation - everything builds on this.

**Performance Criteria:**
- [ ] Main .claude.md contains: file structure, tech stack, startup process, design decisions
- [ ] Each workspace .claude.md documents: purpose, file locations, function inventory, dependencies
- [ ] changelog.md has last night's failure documented with lessons learned
- [ ] plan.md lists all 14 tasks with status tracking
- [ ] CC can locate any function/file without grepping
- [ ] Context reduction: 90% less grep operations

**Exit Criteria:**
- CC successfully uses .claude.md to answer "where is QCM workspace initialization?"
- CC references changelog.md when asked "why did we avoid npm on Google Drive?"
- plan.md accurately reflects current task status

---

### TASK-002: Install and Configure Playwright MCP
**Issue:** Claude Code designs "blind" - can't see visual output, only code  
**Previous Attempt:** N/A - New Implementation  
**Priority:** HIGH - Unlocks visual validation loop  

**Planned Actions:**
1. Research Playwright MCP installation for Electron apps
2. Install Playwright MCP via CC
3. Configure for local Electron app testing
4. Test screenshot capability
5. Create validation workflow template
6. Document configuration in .claude.md

**Reasoning:**
Patrick's key insight: Playwright gives Claude "eyes to see" via screenshots. Enables iterative loop: Code → Screenshot → Compare to Spec → Fix → Repeat. Taps into visual intelligence, not just code knowledge. Critical for UI work.

**Performance Criteria:**
- [ ] Playwright MCP installed and functional
- [ ] Can launch Electron app and capture screenshots
- [ ] Can adjust viewport sizes (desktop, tablet, mobile)
- [ ] Can navigate through app sections
- [ ] Screenshots accessible to Claude for analysis
- [ ] Configuration documented with examples

**Exit Criteria:**
- CC successfully captures screenshot of QCM workspace
- CC identifies UI discrepancy from screenshot vs. spec
- Validation loop completes: identify issue → fix → verify → confirm

---

### TASK-003: Implement "My Developer" Workflow
**Issue:** Single Claude instance handles both strategy and execution, causing context pollution  
**Previous Attempt:** N/A - New Implementation  
**Priority:** HIGH - Prevents cascading failures like last night  

**Planned Actions:**
1. Set up two-terminal workflow:
   - Terminal 1: "Planner" - Strategic oversight
   - Terminal 2: "Developer" - Tactical execution
2. Create communication protocol between instances
3. Document handoff format
4. Create workflow templates
5. Test with simple task before production use

**Reasoning:**
Galen's workflow: Separate strategic thinking from execution. Planner creates plan, Developer executes step-by-step, Planner reviews, Developer refines. Each instance has focused context. No pollution. Built-in review loop. Prevents runaway failures.

**Performance Criteria:**
- [ ] Planner can create detailed multi-step plans
- [ ] Developer executes single steps from plan
- [ ] Planner reviews Developer output with specific feedback
- [ ] Developer addresses feedback iteratively
- [ ] Context stays focused per instance
- [ ] Workflow documented with examples

**Exit Criteria:**
- Planner creates 5-step plan for simple feature
- Developer executes step 1
- Planner reviews with constructive feedback
- Developer implements feedback
- Process completes without context overflow

---

### TASK-004: Create Sub-Agent Library
**Issue:** Main context gets polluted with specialized tasks and tool documentation  
**Previous Attempt:** N/A - New Implementation  
**Priority:** MEDIUM - Enables specialized workflows  

**Planned Actions:**
1. Research Claude Code sub-agent creation
2. Design agent architecture:
   - QCM Review Agent (submittal validation)
   - Security Audit Agent (code security)
   - UI Validator Agent (design compliance)
   - Documentation Generator Agent (auto-docs)
   - GitHub Search Agent (solution research)
3. Create agent configuration files
4. Test each agent independently
5. Document usage patterns

**Reasoning:**
Patrick's insight: Sub-agents have focused context, own system prompts, can call other agents, don't pollute main context, return executive summaries. Package expertise into reusable workflows. Critical for scaling and commercialization.

**Performance Criteria:**
- [ ] Each agent has defined scope and system prompt
- [ ] Agents can be invoked independently
- [ ] Agents return structured reports
- [ ] GitHub Search Agent finds relevant solutions
- [ ] Agent library documented with examples
- [ ] Agents don't pollute main CC context

**Exit Criteria:**
- QCM Review Agent analyzes submittal and returns checklist
- Security Audit Agent identifies 3+ security considerations
- GitHub Search Agent finds relevant code examples for issue
- All agents complete without main context pollution

---

## PHASE 2: SUPABASE INTEGRATION - PROPER EXECUTION
**Duration:** 3 Hours  
**Objective:** Working Knowledge Base integration with validation

### TASK-005: Verify Supabase Schema
**Issue:** Last night assumed RPC functions existed - they don't  
**Previous Attempt:** FAILED - Called non-existent functions  
**Priority:** CRITICAL - Must verify before coding  

**Planned Actions:**
1. Connect to Supabase SQL Editor
2. Query `information_schema.routines` for RPC functions
3. Query `information_schema.columns` for table structure
4. Document actual schema vs. assumptions
5. Identify correct query approach (direct table vs. RPC)
6. Document findings in .claude.md

**Reasoning:**
Last night's failure: Assumed `list_knowledge_sources()`, `search_by_text()`, `get_url_content()` existed. They don't. Patrick's approach: VERIFY infrastructure before coding. Use SQL to check schema, not assumptions.

**Performance Criteria:**
- [ ] Complete list of existing RPC functions (if any)
- [ ] Complete `knowledge_base` table schema documented
- [ ] Column types, constraints, indexes identified
- [ ] Sample data examined
- [ ] Correct query approach determined
- [ ] Schema documented with examples

**Exit Criteria:**
- Can answer: "What RPC functions exist in Supabase?"
- Can answer: "What columns are in knowledge_base table?"
- Can answer: "What's the correct way to query documents?"
- Documentation includes working SQL examples

---

### TASK-006: Create Standalone Test Suite
**Issue:** No validation before integration causes production failures  
**Previous Attempt:** N/A - Should have done this last night  
**Priority:** CRITICAL - Test before integrate  

**Planned Actions:**
1. Create `test-supabase.js` in project root
2. Write standalone tests for each query type:
   - List all documents
   - Search by text
   - Get specific document
   - Get document chunks
3. Run tests, verify results
4. Document expected vs. actual responses
5. Only proceed to integration after ALL tests pass

**Reasoning:**
Patrick's workflow: Test standalone BEFORE integration. Verify queries return expected data. Document working patterns. Then integrate with confidence. Prevents production failures.

**Performance Criteria:**
- [ ] test-supabase.js connects to Supabase successfully
- [ ] List query returns documents array
- [ ] Search query filters correctly
- [ ] Document fetch returns expected structure
- [ ] All tests pass with sample data
- [ ] Response formats documented

**Exit Criteria:**
- `node test-supabase.js` runs without errors
- All 4 query types return expected data
- Response structures match documentation
- Ready to integrate into main.js

---

### TASK-007: Integrate Supabase into main.js
**Issue:** Need working KB integration without breaking app  
**Previous Attempt:** FAILED - Broke app, couldn't launch  
**Priority:** HIGH - Core feature requirement  

**Planned Actions:**
1. **BACKUP CURRENT WORKING STATE FIRST**
2. Use CC to modify main.js:
   - Add conditional Supabase client (graceful degradation)
   - Add IPC handlers using VERIFIED queries from TASK-006
   - Implement error handling
   - Add logging for debugging
3. Test each IPC handler independently
4. Verify app still launches
5. Only proceed if all tests pass

**Reasoning:**
Use working queries from test suite. Conditional client means app works even if Supabase fails. CC handles code edits (not me). Backup ensures rollback capability. Test incrementally, not all-at-once.

**Performance Criteria:**
- [ ] Backup created before any changes
- [ ] Supabase client initializes conditionally
- [ ] IPC handlers use verified queries
- [ ] Error handling prevents app crashes
- [ ] App launches successfully
- [ ] Each handler tested and working

**Exit Criteria:**
- App launches via `npm start`
- IPC handler `query-supabase-kb` returns documents
- IPC handler `search-supabase-kb` filters correctly
- IPC handler `get-supabase-doc` retrieves specific doc
- All handlers have error handling
- App degrades gracefully if Supabase unavailable

---

### TASK-008: Create KB Browser UI
**Issue:** Need user interface for KB search and display  
**Previous Attempt:** FAILED - Broke during last night's session  
**Priority:** HIGH - User-facing feature  

**Planned Actions:**
1. **WARNING: Will modify index.html - requires confirmation**
2. Use CC with Playwright validation:
   - Add KB Browser tab to QCM workspace
   - Create search interface
   - Create document list display
   - Create document detail view
3. Use Playwright to screenshot at each step
4. Compare to design spec (create spec first if needed)
5. Iterate until visually correct

**Reasoning:**
Patrick's workflow: Use Playwright for visual validation. Create → Screenshot → Compare → Fix → Repeat. This prevents "generic shadcn purple UI" and enables pixel-perfect results. CC handles code, Playwright validates design.

**Performance Criteria:**
- [ ] KB Browser tab renders in QCM workspace
- [ ] Search box accepts input
- [ ] Search triggers query to Supabase
- [ ] Results display in list format
- [ ] Clicking result shows document detail
- [ ] UI matches design spec via Playwright validation

**Exit Criteria:**
- Tab navigates to KB Browser
- Search for "construction" returns relevant docs
- Clicking doc displays full content
- Mobile responsive (verified via Playwright screenshots)
- No console errors
- Baseline index.html backed up before changes

---

## PHASE 3: TKB & OPERATIONAL PROTOCOLS
**Duration:** 3 Hours  
**Objective:** Seamless chat continuity and knowledge management

### TASK-009: Automated Living Docs System
**Issue:** Manual EOS protocol is time-consuming and error-prone  
**Previous Attempt:** Manual process works but not scalable  
**Priority:** HIGH - Critical for continuity  

**Planned Actions:**
1. Create `generate-living-docs.js` script via CC:
   - Session Summary generator
   - Technical Journal generator
   - Bill's Diary generator
   - Code Repository generator
   - Handoff Document generator
2. Create `convert-and-upload.ps1` for Google Drive:
   - Convert markdown to Google Docs
   - Upload to proper folders
   - Verify accessibility
3. Test complete workflow
4. Create `/eos` command in CC

**Reasoning:**
Current EOS protocol works but takes 30+ minutes manually. Automation enables consistent quality, faster execution, reduces human error. Critical for scaling to multiple sessions per day.

**Performance Criteria:**
- [ ] Script generates all 5 living docs
- [ ] Docs contain complete session information
- [ ] Markdown converts to Google Docs format
- [ ] Files upload to correct Drive folders
- [ ] Claude can read uploaded docs
- [ ] /eos command executes full workflow

**Exit Criteria:**
- Run `/eos` command
- All 5 docs generated in <2 minutes
- Docs uploaded to Google Drive
- Next Claude instance can read and reference docs
- No manual intervention required

---

### TASK-010: Session Handoff Protocol
**Issue:** New Claude instances start without context from previous sessions  
**Previous Attempt:** Handoff doc created manually  
**Priority:** HIGH - Enables true continuity  

**Planned Actions:**
1. Create standardized handoff template via CC
2. Build handoff generator that includes:
   - Current project state
   - Active issues
   - Next steps
   - Critical constraints
   - Recent failures and lessons
3. Integrate with /eos command
4. Test with simulated session handoff

**Reasoning:**
Consistent handoff format ensures new Claude instances have full context. Template ensures nothing missed. Automation ensures consistency. Enables seamless multi-day development.

**Performance Criteria:**
- [ ] Template covers all critical handoff elements
- [ ] Generator pulls from session context
- [ ] Handoff includes recent chat summaries
- [ ] New Claude can resume work immediately
- [ ] No context loss between sessions

**Exit Criteria:**
- Handoff doc generated automatically
- Contains project state, issues, next steps
- New Claude instance reads and confirms understanding
- No re-explaining of project context required

---

### TASK-011: Create Command Library
**Issue:** Repeated workflows need standardization  
**Previous Attempt:** N/A - New Implementation  
**Priority:** MEDIUM - Efficiency multiplier  

**Planned Actions:**
1. Research Claude Code custom commands
2. Create command files via CC:
   - `/analyze-workspace` - Full codebase analysis
   - `/security-review` - Security audit
   - `/generate-docs` - Documentation generation
   - `/update-tkb` - Update knowledge base
   - `/ui-validate` - Playwright UI check
3. Test each command
4. Document usage in .claude.md

**Reasoning:**
Anod's insight: Commands are shareable, reusable prompts. Package expertise once, use everywhere. Share across team. Consistent quality. Saves time on repeated tasks.

**Performance Criteria:**
- [ ] Each command has clear scope
- [ ] Commands execute consistently
- [ ] Commands save to .claudecode/commands/
- [ ] Commands documented with examples
- [ ] Commands work across sessions

**Exit Criteria:**
- `/analyze-workspace` generates comprehensive analysis
- `/security-review` identifies vulnerabilities
- All commands executable by new Claude instance
- Command library documented

---

## PHASE 4: TRAJANUS ENTERPRISE PLATFORM
**Duration:** 3 Hours  
**Objective:** Transform from prototype to production-ready commercial platform

### TASK-012: Platform Architecture Implementation
**Issue:** Hub conceptual, not functional  
**Previous Attempt:** Basic Electron app with workspaces  
**Priority:** CRITICAL - Core product architecture  

**Planned Actions:**
1. Design hub-and-spoke architecture via Planner CC:
   - Central command dashboard
   - Workspace orchestration system
   - Cross-workspace data flow
   - Settings and configuration management
2. Implement via Developer CC
3. Validate via Playwright screenshots
4. Test integration between workspaces

**Reasoning:**
Current implementation: separate workspaces, no integration. Need: unified platform where data flows between sections. QCM submittals inform schedule, schedule informs budget, etc. Hub becomes command center, not just launcher.

**Performance Criteria:**
- [ ] Central dashboard shows all workspace states
- [ ] Workspaces can share data
- [ ] Navigation between workspaces preserves context
- [ ] Settings apply across platform
- [ ] Architecture documented in .claude.md

**Exit Criteria:**
- Dashboard displays active projects
- QCM workspace can pass data to PM Toolkit
- Navigation works smoothly
- Platform feels unified, not siloed

---

### TASK-013: Create Agency Integration Templates
**Issue:** Need standardized templates for different agency requirements  
**Previous Attempt:** N/A - New Feature  
**Priority:** MEDIUM - Commercial differentiation  

**Planned Actions:**
1. Research agency-specific requirements:
   - USACE (using current SOUTHCOM project as reference)
   - NAVFAC (research via GitHub Search Agent)
   - AFCEC (research via GitHub Search Agent)
   - Generic federal (baseline)
2. Create template workspaces via CC:
   - Agency-specific forms
   - Compliance checklists
   - Submittal workflows
   - Reporting templates
3. Document in separate .claude.md per agency

**Reasoning:**
Commercial value: pre-configured templates for different agencies. Clients get instant value, not custom configuration. Demonstrate expertise in federal construction. Differentiator from generic PM tools.

**Performance Criteria:**
- [ ] USACE template matches current SOUTHCOM workflows
- [ ] Each template includes agency-specific forms
- [ ] Templates documented with examples
- [ ] Easy to switch between agency templates
- [ ] Templates exportable for client use

**Exit Criteria:**
- Load USACE template - see SOUTHCOM-style interface
- Load NAVFAC template - see NAVFAC-specific forms
- Templates demonstrate agency knowledge
- Ready for client demo

---

### TASK-014: Commercialization Packaging
**Issue:** Platform ready for Tom and clients needs packaging  
**Previous Attempt:** N/A - New Feature  
**Priority:** HIGH - Business model enablement  

**Planned Actions:**
1. Create white-label configuration system via CC:
   - Company branding settings
   - Color scheme customization
   - Logo placement
   - Custom agency templates
2. Build client onboarding workflow:
   - Setup wizard
   - Configuration import/export
   - Training materials
   - Demo environment
3. Generate documentation suite:
   - User guide
   - Admin guide
   - API documentation (if applicable)
   - Troubleshooting guide

**Reasoning:**
For Tom: Needs turnkey deployment. For clients: Needs professional onboarding. For scaling: Needs standardized process. This enables business model - not just a personal tool.

**Performance Criteria:**
- [ ] White-label system allows branding changes
- [ ] Setup wizard guides new users
- [ ] Configuration exports/imports correctly
- [ ] Documentation comprehensive and clear
- [ ] Demo environment showcases capabilities

**Exit Criteria:**
- Change branding to "Tom's Construction Management"
- Export configuration as .json
- Import configuration to new instance
- Documentation enables self-service setup
- Ready for client presentation

---

## EXECUTION PROTOCOLS

### Documentation Standard
Every action must include:
```
TASK: [ID-###]
ISSUE: [Problem being addressed]
PREVIOUS ATTEMPT: [Summary or "First Attempt"]
STATUS: [PASS/FAIL]
PLANNED ACTION: [Specific steps]
REASONING: [Why this approach]
EXECUTION: [What CC/Agent will do]
RESULT: [Outcome documentation]
```

### Code Modification Rules
1. **NO DIRECT EDITING** by Claude Sonnet
2. **ALL CHANGES VIA CC** or specialized agents
3. **BACKUP BEFORE MODIFICATIONS** especially index.html
4. **WARNING + CONFIRMATION** for baseline file changes
5. **TEST AFTER EVERY CHANGE** before proceeding

### Context Management
1. Use .claude.md files for persistent context
2. Update changelog.md with decisions
3. Update plan.md with task status
4. Planner/Developer workflow for complex tasks
5. Sub-agents for specialized work

### Failure Protocol
1. STOP immediately on failure
2. Document exact error
3. Restore from backup if code broken
4. Analyze root cause
5. Update changelog.md with lesson
6. Revise approach before retry

### Success Validation
1. Performance criteria must be met
2. Exit criteria must be satisfied
3. Documentation must be complete
4. Tests must pass
5. No regression in existing functionality

---

## RISK MITIGATION

### Known Risks
1. **Google Drive + npm**: File locking, TAR errors
   - Mitigation: Never run npm install on Drive, use existing node_modules
2. **Electron Corruption**: node_modules/.bin issues
   - Mitigation: Have backup, know manual fix procedure
3. **Context Overflow**: Claude Code runs out of context
   - Mitigation: Use Planner/Developer workflow, sub-agents, rewind at 5%
4. **Supabase Integration**: Breaking changes
   - Mitigation: Verify schema, test standalone, backup before integration
5. **Index.html Modifications**: Breaking QCM workspace
   - Mitigation: Warning + confirmation, backup, Playwright validation

### Backup Strategy
1. Before ANY major change: Create timestamped backup
2. Store in Archive folder
3. Test backup restore procedure
4. Document backup location in changelog.md

### Rollback Plan
If any phase fails critically:
1. Stop all work
2. Restore from last known good backup
3. Document failure in changelog.md
4. Analyze with GitHub Search Agent
5. Revise plan
6. Get explicit approval before retry

---

## SUCCESS METRICS

### Technical Metrics
- [ ] App launches reliably via `npm start`
- [ ] All integrations functional (Supabase, Google Drive, Playwright)
- [ ] Zero critical bugs
- [ ] All tests passing
- [ ] Documentation complete and accurate

### Operational Metrics
- [ ] EOS protocol automated (<2 minutes)
- [ ] Session handoff seamless (no context loss)
- [ ] Claude Code efficiency >90% (measured by task completion rate)
- [ ] Context management effective (minimal grep operations)

### Business Metrics
- [ ] Platform demo-ready for Tom
- [ ] Agency templates functional
- [ ] White-label system working
- [ ] Documentation enables self-service
- [ ] Ready for first client deployment

### Quality Metrics
- [ ] Code follows best practices
- [ ] Security reviewed
- [ ] UI validated via Playwright
- [ ] Performance acceptable
- [ ] Maintainable architecture

---

## TIMELINE

### Hour 1-3: Infrastructure Foundation
- TASK-001: .claude.md system
- TASK-002: Playwright MCP
- TASK-003: My Developer workflow
- TASK-004: Sub-agent library

### Hour 4-6: Supabase Integration
- TASK-005: Verify schema
- TASK-006: Standalone tests
- TASK-007: Integration
- TASK-008: KB Browser UI

### Hour 7-9: TKB & Protocols
- TASK-009: Automated living docs
- TASK-010: Session handoff
- TASK-011: Command library

### Hour 10-12: Enterprise Platform
- TASK-012: Platform architecture
- TASK-013: Agency templates
- TASK-014: Commercialization packaging

---

## DELIVERABLES

### Code
- [ ] Fully functional Trajanus Enterprise Hub
- [ ] Working Supabase KB integration
- [ ] Agency-specific templates
- [ ] White-label configuration system

### Documentation
- [ ] Complete .claude.md system
- [ ] Automated living docs
- [ ] Command library
- [ ] User guides
- [ ] Admin guides
- [ ] API documentation

### Infrastructure
- [ ] Playwright MCP configured
- [ ] Sub-agent library
- [ ] Custom commands
- [ ] Backup system
- [ ] Testing framework

### Business Assets
- [ ] Demo environment
- [ ] Client onboarding workflow
- [ ] Agency templates
- [ ] White-label system
- [ ] Training materials

---

## NEXT SESSION PREPARATION

At end of 12 hours:
1. Run `/eos` command to generate living docs
2. Create comprehensive handoff document
3. Upload all docs to Google Drive
4. Verify next Claude can access
5. Document current state in plan.md
6. List remaining tasks for future sessions

---

## APPROVAL TO PROCEED

**Mission Commander:** Bill King  
**Approval Required:** YES  

**Acknowledge:**
- All 14 tasks understood
- Execution protocols clear
- Risk mitigation in place
- Success metrics defined
- Ready to execute

**Say "WEAPONS FREE" to begin TASK-001**

---

**END IMPLEMENTATION PLAN**

Mission planning complete. Awaiting authorization to execute.
