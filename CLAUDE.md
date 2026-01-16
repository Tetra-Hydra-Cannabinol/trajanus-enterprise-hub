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