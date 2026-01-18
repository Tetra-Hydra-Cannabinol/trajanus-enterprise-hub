# Trajanus Command Center

**Enterprise Hub for Construction Project Management**

A Tauri 2.0 desktop application serving as a unified command center for USACE Design-Build contracts, integrating AI-powered workflows, quality control management, and project tracking.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    TRAJANUS COMMAND CENTER                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   QCM        │  │   PM         │  │   Developer  │          │
│  │   Toolkit    │  │   Toolkit    │  │   Toolkit    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐                            │
│  │   Traffic    │  │  Healthcare  │                            │
│  │   Studies    │  │   Platform   │                            │
│  └──────────────┘  └──────────────┘                            │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  Frontend: HTML/CSS/JavaScript (Single-file architecture)      │
│  Backend: Tauri 2.0 (Rust)                                     │
│  Database: Supabase PostgreSQL + pgvector                      │
│  Storage: Google Drive API                                     │
├─────────────────────────────────────────────────────────────────┤
│  .claude.md Context System │ Sub-Agents │ Custom Commands      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites
- Node.js 18+
- Rust (for Tauri builds)
- Tauri CLI: `cargo install tauri-cli`

### Development
```bash
cd C:\Dev\trajanus-command-center
npm install
npm run dev
```

### Build
```bash
npm run build
cargo tauri build
```

---

## Project Structure

```
C:\Dev\trajanus-command-center\
├── src/
│   ├── index.html              # Main hub (SACRED FILE)
│   ├── main.css                # Global styles
│   └── toolkits/
│       ├── developer.html      # Developer Toolkit
│       ├── qcm.html            # QCM Toolkit
│       ├── pm.html             # PM Toolkit
│       ├── traffic.html        # Traffic Studies
│       └── healthcare.html     # Healthcare Platform
│
├── src-tauri/
│   └── src/
│       └── lib.rs              # Rust backend (SACRED FILE)
│
├── .claude/                    # Claude Code orchestration
│   ├── agents/                 # Sub-agents (12 agents)
│   ├── commands/               # Custom commands
│   ├── context/                # Supporting documentation
│   ├── templates/              # Acceptance criteria templates
│   └── workflows/              # Process guides
│
├── CLAUDE.md                   # Project-level instructions
├── README.md                   # This file
└── package.json
```

---

## Workspaces

### QCM Toolkit
Quality Control Management for USACE submittals.
- 6-category submittal system
- Compliance checking
- Document tracking

### PM Toolkit
Project Management tools and dashboards.
- Schedule analysis (CPM)
- Cost tracking
- Resource management

### Developer Toolkit
Development tools and automation.
- External app launchers
- Script execution
- Agent management
- Progress tracking

### Traffic Studies
USACE traffic study requirements.
- TIA workflow (10 steps)
- ITE/HCM compliance
- Study generation

### Healthcare Platform
Healthcare facility management.
- Medical compliance
- Facility tracking

---

## Claude Code Integration

### .claude.md System
Each workspace has a dedicated `.claude.md` file providing context:
- `qcm-workspace/.claude.md`
- `pm-toolkit/.claude.md`
- `developer-project/.claude.md`
- `tse-workspace/.claude.md`

### Sub-Agents
Located in `.claude/agents/`:
- `design-reviewer.md` - UI validation
- `qcm-reviewer.md` - Submittal compliance
- `security-auditor.md` - Code security
- `doc-generator.md` - Documentation
- `github-searcher.md` - Solution finding
- `knowledge-retriever.md` - KB search
- Plus 6 more specialized agents

### Custom Commands
Located in `.claude/commands/`:
- `/eos` - End of Session protocol
- `/checkpoint` - Save progress state
- `/spawn-agent` - Launch sub-agents
- `/reflect` - Capture learnings
- `/verify` - Playwright validation

### Workflows
Located in `.claude/workflows/`:
- `planner_developer.md` - CP/CC workflow
- `gsd_framework.md` - Explore → Plan → Execute → Validate
- `visual_validation.md` - Playwright iteration loop
- `context_management.md` - Rewind at 5% protocol

---

## Development Protocols

### Sacred File Protocol
**NEVER edit directly:**
- `src/index.html`
- `src-tauri/src/lib.rs`

**Edit Protocol:**
```
WRONG: Edit src/index.html directly
RIGHT: Copy → index_v2.1_FEATURE.html → Edit → Test → Replace
```

### Surgical Edit Principle
- Edit specific functions only
- Preserve surrounding code exactly
- Test change immediately
- Document why change was made

### Backup Before Major Changes
```bash
timestamp=$(date +%Y%m%d_%H%M%S)
cp src/index.html "archive/index_${timestamp}_BACKUP.html"
```

---

## Branding Standards

### Colors
```css
--silver: #C0C0C0;       /* Primary accent */
--black: #1a1a1a;        /* Background */
--blue: #00AAFF;         /* Bright blue accent */
/* NO GOLD unless explicitly requested */
```

### Button Specs
- `ext-btn`: 120×44px (external apps)
- `script-btn`: 160×50px (Trajanus scripts)
- `nav-btn`: 140×44px (navigation)

### Typography
- Font: Roboto family
- Code: SF Mono, Fira Code, Consolas

---

## Testing

### Manual Checklist
- [ ] App launches: `npm run dev`
- [ ] All tabs/workspaces accessible
- [ ] No console errors (F12)
- [ ] Branding colors correct
- [ ] Responsive behavior acceptable

### Playwright Validation
```bash
# Screenshots auto-captured to .playwright-mcp/
# Use /verify command for visual validation
```

---

## Troubleshooting

### App Won't Launch
1. Verify in correct directory: `C:\Dev\trajanus-command-center`
2. Check `npm run dev` output for errors
3. Verify Tauri CLI installed: `cargo tauri --version`

### Build Failures
1. Restore from last known good backup
2. Check `git diff` to see changes
3. Revert suspicious changes

### Google Drive Sync Issues
- Never run npm on synced folders
- Check Drive Desktop sync status

---

## Key Decisions

See `CHANGELOG.md` for detailed decision history.

- **Electron → Tauri**: Better performance, smaller bundles
- **Single-file Architecture**: Simplicity over complexity
- **Markdown → Google Docs**: Claude accessibility
- **NO OPTIONS Protocol**: Execute the right way, don't ask

---

## Contributing

1. Follow Sacred File Protocol
2. Use GSD Framework for complex changes
3. Test after every change
4. Update CHANGELOG.md with decisions

---

## Project Info

**Owner:** Bill King / Trajanus Systems
**Current Project:** SOUTHCOM Guatemala (W9127823R0034)
**Tech Stack:** Tauri 2.0, Vanilla JS, Supabase, Google Drive API

---

**Last Updated:** 2026-01-18
