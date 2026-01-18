# Trajanus Command Center - Claude Code Guidelines

## Project Overview
Tauri desktop application serving as a command center with multiple toolkit platforms (developer, qcm, pm, traffic).

## Session Learnings - 2026-01-15

### Button Standardization Session

- CORRECTION: Used compact one-liner CSS format for brand colors → User prefers multi-line format with clear section headers (/* ============ SECTION NAME ============ */)

- CORRECTION: btn-gdrive was blue (#4285F4) → Should be green (#34A853) for proper Google Drive branding

- PREFERENCE: When user provides canonical CSS specs, implement EXACTLY as provided - no variations, reformatting, or "improvements"

- PREFERENCE: Button CSS should have explicit section headers separating: External Program Buttons, Script Buttons, Nav Buttons, Brand Colors

- PATTERN: User gives batch tasks across multiple files - process each file systematically and report counts per file

- PATTERN: Take Playwright screenshots after visual changes to verify implementation

### Canonical Button Spec Reference
- ext-btn: 120×44px (external program buttons)
- script-btn: 160×50px (Trajanus script buttons)
- nav-btn: 140×44px (navigation/hub buttons)
- All buttons use linear-gradient for 3D effect
- All buttons use box-shadow for depth
- Hover: translateY(-2px) + brightness(1.15)
- Active: translateY(2px)

### Critical Protocol Learnings

- CORRECTION: Attempted to create/overwrite CLAUDE.md → MUST always READ first and APPEND, never overwrite this file

- PREFERENCE: CLAUDE.md is a living document - always append new sections, never replace existing content

## Session Learnings - 2026-01-16

### Precision and Discipline Session

- CRITICAL: "ONLY change what is EXPLICITLY requested" - User emphasized this repeatedly

- PROTOCOL: Make one change at a time, verify, then move to next - no batching without confirmation

- PROTOCOL: Never make "helpful" additions or improvements that weren't requested

- PATTERN: User works in early morning hours (3 AM) - focused, systematic sessions

- PREFERENCE: Surgical precision over creative interpretation - implement exactly as specified

### Sacred Baseline Concept

- PATTERN: User creates "SACRED BASELINE" commits as rollback reference points

- REFERENCE: Commit 9b09fc9a87239bbd5b050c61e1ef30e9e909619a - 2026-01-16 SACRED BASELINE

- PURPOSE: Serves as known-good state for future rollback if needed

- PROTOCOL: Reference sacred baseline commits when making future changes

### UI Refinements Completed

- Global border standardization: 2px solid #0066CC across all 5 pages (index + 4 toolkits)

- Sidebar offset: Added 2px left positioning to ensure border visibility

- Logo padding: Reduced by 50% (1.5rem → 0.75rem) for header compactness

- Hero section: Reduced padding (4rem → 2.5rem), expanded content with user prose

- Platform tags: Removed from all 4 toolkit cards on index.html

- Developer buttons: Corrected colors (Terminal grey, GitHub purple, Python blue, Explorer gold, Notepad++ orange, Zoom blue)

### User Feedback Pattern

- FEEDBACK: "fantastic session, simply fantastic. same thing exactly tomorrow"

- INTERPRETATION: Precision approach validated - user wants exact same methodology continued

- PROTOCOL: Maintain systematic, one-change-at-a-time verification process

### End of Session (EOS) Protocol

- PATTERN: User requests EOS execution to generate session documentation

- PROTOCOL: EOS requires 5 documents: Session_Summary, Technical_Journal, Bills_Daily_Diary, Code_Repository, Handoff

- PROTOCOL: Save all EOS documents to `G:\My Drive\00 - Trajanus USA\08-EOS-Files\001 Claude EOS Output\`

- PROTOCOL: Filename format must be `[Type]_YYYY-MM-DD-HHMM.md` with 24-hour time

- PROTOCOL: Execute /reflect skill as part of EOS process

- PROTOCOL: Update CLAUDE.md with session learnings during EOS (READ first, APPEND new section)

- PREFERENCE: Session documentation should be thorough and detailed, capturing all work completed

- PREFERENCE: Handoff document should provide clear opening message template for next session

### Backup Verification Protocol

- PATTERN: Create dual backups (git tag + git branch) pointing to same commit for redundancy

- PATTERN: Verify backups with three commands: `git tag -l`, `git branch -a`, `git log --oneline -5`

- PREFERENCE: Backup naming convention uses date format: `SACRED_BASELINE_YYYY-MM-DD_v#` for tags, `backup-YYYY-MM-DD-v#` for branches

## Session Learnings - 2026-01-16 (Afternoon)

### Office Apps Integration

- CORRECTION: Changed Office apps to desktop launch (winword, excel) → User wanted Office ONLINE (web version) to work, not desktop apps

- CORRECTION: Tried embedding Office.com in workspace panel → Office.com blocks embedding via CSP/X-Frame-Options, must open in new window

- PATTERN: Office Online apps should open in new Tauri WebviewWindow popup (1200x800, centered) since they refuse to embed

### Landing Page Styling

- CORRECTION: Used neuron grid image for assistant panel → User specified brainwaves image (brain-8825819_1280.jpg) for landing page assistant

- CORRECTION: Assistant text color was blue (#00AAFF) → User wanted WHITE (#FFFFFF) for assistant responses on landing page

- CORRECTION: Silver/grey text (#C0C0C0) throughout landing page → User wants ALL text WHITE for better contrast, except section titles (blue) and user name (blue)

- PREFERENCE: Chat input placeholder text should be WHITE, user typed text should be BLUE (#00AAFF)

- PREFERENCE: Chat bubbles should have TRANSPARENT background with BLUE border (#00AAFF)

- PREFERENCE: Enterprise Hub title font should be Copperplate Gothic Bold (same as TRAJANUS branding)

### Desktop App Launch Strategy

- PATTERN: For Office desktop apps, use explicit path resolution checking multiple common install locations:
  - `C:\Program Files\Microsoft Office\root\Office16\`
  - `C:\Program Files (x86)\Microsoft Office\root\Office16\`

- PATTERN: Teams desktop is typically in `%LOCALAPPDATA%\Microsoft\Teams\current\Teams.exe`

### Text Color Standards (Landing Page)

- PREFERENCE: All body text, descriptions, tips, intros → WHITE (#FFFFFF)
- PREFERENCE: Section titles (ENTERPRISE HUB ASSISTANT, WORKSPACE) → BLUE (#00AAFF)
- PREFERENCE: User name in greeting → BLUE (#00AAFF)
- PREFERENCE: Tagline "ENGINEERED INTELLIGENCE™" → WHITE (#FFFFFF)
- PREFERENCE: Greeting text and date → WHITE (#FFFFFF)

## Session Learnings - 2026-01-16 (Healthcare Platform)

### Platform Identity Transformation

- PATTERN: When transforming platform purpose, update ALL related elements systematically: sidebar structure, tool names, assistant purpose, file sections, output areas

- PATTERN: Platform identity should match user's actual workflow - healthcare platform is for BUILDING apps (code factory), not processing patient reports

- PREFERENCE: Break large development goals into specific component checklists (10 components for healthcare app: PDF Upload, Text Extraction, Data Parser, Report Template, Database, Auth, Audit Logging, Azure Config, AI Agent, Admin Dashboard)

### Healthcare App Context

- PATTERN: Healthcare platform targets specific real-world project: building app for Dr. Jako Bezuidenhout (pediatrician, Johannesburg, South Africa)

- PATTERN: HIPAA compliance considerations built into development checklist (Audit Logging, HIPAA Validator tools)

### Persistent UI State

- PATTERN: Use localStorage for simple state persistence (checklist progress) when no backend needed

- PATTERN: Collapsible sections with saved state improve organization for long development roadmaps

### File Upload Strategy

- PATTERN: Support both PDF and DOCX for project documentation uploads - requirements/specs may come in either format

- PATTERN: File upload can serve different purposes based on platform identity (patient reports vs. project documentation)

## Advanced Patterns Training - 2026-01-17

### Skills Architecture

**Directory Structure:**
```
.claude/skills/
├── eos-protocol/skill.md
├── surgical-edit/skill.md
├── playwright-verify/skill.md
└── toolkit-builder/skill.md
```

**Skill File Format:**
```yaml
---
name: skill-name
description: Trigger conditions for auto-invocation
---
# Instructions
```

- PATTERN: Description field determines when skill auto-triggers
- PATTERN: Create skills from examples: provide 2-3 before/after, let Claude notice patterns
- PATTERN: Vibe check skills 2-3 times after creation, then iterate

### Context Management

- CRITICAL: Context rot - LLM performance degrades as context fills; tokens at beginning more effective than end
- PATTERN: Spawn fresh sub-agents for discrete tasks (fresh 200K context each)
- PATTERN: Progressive disclosure - load tools/context only when needed
- PATTERN: Don't reuse contexts for unrelated work

### MCP Optimization

- CRITICAL: MCPs consume 50%+ of context from tool definitions alone
- PATTERN: Enable only MCPs you're actively using
- PATTERN: Disable MCPs when not needed
- PATTERN: Use CLI tools for simple operations (better context efficiency)
- PATTERN: Add MCP discovery hints to CLAUDE.md

### Session Naming Convention

- FORMAT: `{project}-{date}-{focus}`
- EXAMPLES: `trajanus-2026-01-17-skills-setup`, `healthcare-2026-01-19-auth`
- COMMANDS: `/rename [name]` to name, `claude --resume` to continue

### Hooks Configuration

- AVAILABLE: session_start, session_end, pre_tool_use, post_tool_use, pre_compact
- USE CASE: Notification on task completion
- USE CASE: Auto-export before compaction
- USE CASE: Pull tickets on session start
- USE CASE: Run tests after code write

### GitHub Integration

- SETUP: Add Claude app at `github.com/apps/claude`, add API key to repo settings
- PATTERN: Create issues → @claude → async execution (works from phone)
- QUOTE: "Claude is fiercely competent with Git"

### Key Quotes

> "Context rot: tokens at the front are more effective than tokens at the end"
> "MCPs take up 50%+ of context window"
> "Skills are reusable SOPs for agents"
> "Just see: can I do it in Claude Code? That's my best advice."

### Trajanus Skills Reference

| Skill | Trigger | Purpose |
|-------|---------|---------|
| eos-protocol | "run eos", "end of session" | Generate session documentation |
| surgical-edit | "precise edit", "surgical change" | Minimal targeted modifications |
| playwright-verify | "verify UI", "screenshot" | UI verification with Playwright |
| toolkit-builder | "build toolkit", "new platform" | Create Trajanus toolkit pages |

### Quick Reference - Advanced Patterns

- **Skills**: `.claude/skills/[name]/skill.md` auto-triggers on description match
- **Context rot**: Performance degrades as context fills. Flag when deep, recommend fresh context.
- **Session naming**: `/rename trajanus-{date}-{focus}`
- **MCP bloat**: Disable unused MCPs - they consume 50%+ context from definitions alone
- **GSD framework**: `npx get-stuff-done-cc` for complex multi-step projects
- **Fresh contexts**: Spawn new for unrelated tasks, don't reuse bloated contexts

## Session Learnings - 2026-01-17 (UI Standardization)

### Progress Section Implementation

- PATTERN: Two-panel grid layout (1.5fr / 1fr) works well for checklist + progress tracker combination

- PATTERN: Each platform gets unique checklist items matching its domain (QCM, PM, TSE, Healthcare, Developer)

- PATTERN: localStorage persistence pattern is consistent across all platforms - copy/adapt with platform-specific key name

### Color Standardization

- CORRECTION: Progress section components still had gold (var(--gold)) colors → All converted to #00AAFF for consistency

- REFERENCE: Components needing gold→blue: `.progress-checklist`, `.progress-tracker`, `.checklist-title`, `.checklist-checkbox`, `.progress-title`, `.progress-percent`

- PREFERENCE: 2px borders are the standard - 1px borders look inconsistent (found on Claude embed wrapper)

### Checklist Persistence Pattern

```javascript
// Standard localStorage persistence pattern
const savedChecklist = localStorage.getItem('{platform}-checklist-state');
// Load, parse JSON, restore .completed classes
// On click: toggle class, update count, save to localStorage
```

- PATTERN: Use `data-task` attribute as unique identifier for each checklist item

- PATTERN: Unique localStorage keys per platform prevent state collision:
  - `developer-checklist-state`
  - `qcm-checklist-state`
  - `pm-checklist-state`
  - `traffic-checklist-state`
  - `healthcare-checklist-state`

### Session Context

- PATTERN: "the checklist keeps dissapearing" = state persistence problem, not visibility

- PREFERENCE: User expects UI state to persist across browser sessions - localStorage is appropriate for simple boolean checklist state