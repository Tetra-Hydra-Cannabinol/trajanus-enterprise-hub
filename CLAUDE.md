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
