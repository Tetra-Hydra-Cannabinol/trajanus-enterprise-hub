# Trajanus Command Center - Architecture

**Purpose:** Technical architecture reference for Claude Code
**Version:** 1.0
**Last Updated:** 2026-01-17

---

## SYSTEM OVERVIEW

```
┌─────────────────────────────────────────────────────────────┐
│                    TRAJANUS COMMAND CENTER                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  index.html │  │ toolkits/*  │  │   assets/   │        │
│  │  (Hub)      │  │ (Workspaces)│  │ (Images)    │        │
│  └──────┬──────┘  └──────┬──────┘  └─────────────┘        │
│         │                │                                  │
│         └────────┬───────┘                                  │
│                  │                                          │
│         ┌───────▼────────┐                                  │
│         │   Tauri 2.0    │                                  │
│         │   (Rust Core)  │                                  │
│         └───────┬────────┘                                  │
│                 │                                           │
│    ┌────────────┼────────────┐                             │
│    │            │            │                              │
│    ▼            ▼            ▼                              │
│ ┌──────┐  ┌──────────┐  ┌──────────┐                      │
│ │ File │  │  Python  │  │  Claude  │                      │
│ │ Ops  │  │  Scripts │  │   API    │                      │
│ └──────┘  └──────────┘  └──────────┘                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │ Supabase │   │  Google  │   │  Local   │
        │    KB    │   │  Drive   │   │  Files   │
        └──────────┘   └──────────┘   └──────────┘
```

---

## FRONTEND ARCHITECTURE

### Single-File Architecture
Each workspace is a self-contained HTML file with embedded CSS and JavaScript:

```
src/
├── index.html              ← Main Hub (SACRED FILE)
├── main.css                ← Shared styles
├── toolkits/
│   ├── developer.html      ← Developer Toolkit
│   ├── qcm.html            ← QCM Workspace
│   ├── pm.html             ← PM Toolkit
│   └── traffic.html        ← Traffic Studies (TSE)
└── assets/
    ├── trajanus-logo-*.png ← Logo variants
    └── *.jpg               ← Background images
```

### Why Single-File?
- **Simplicity:** No build tools, no bundlers
- **Maintainability:** Solo developer, clear boundaries
- **Backup:** Single file to protect and version
- **Fast iteration:** Edit → Save → Refresh

### File Structure Within Each HTML
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        /* CSS Variables */
        /* Component Styles */
        /* Responsive Rules */
    </style>
</head>
<body>
    <!-- Hero Section -->
    <!-- Content Sections -->
    <!-- Modals -->

    <script>
        // Configuration
        // Tauri API Wrapper
        // Core Controllers (Objects)
        // Event Listeners (CSP-compliant)
    </script>
</body>
</html>
```

---

## TAURI BACKEND

### Overview
Tauri 2.0 provides the desktop shell and native capabilities:

```
src-tauri/
├── Cargo.toml              ← Rust dependencies
├── tauri.conf.json         ← Tauri configuration
└── src/
    └── lib.rs              ← Rust commands (SACRED FILE)
```

### Available Invoke Commands

```rust
// File Operations
invoke('open_path', { path: string })
invoke('launch_vscode', { path: string })
invoke('open_terminal', { path: string })
invoke('launch_claude_code', { path: string })

// Script Execution
invoke('run_python_script', { scriptPath: string, targetPath?: string })

// Claude Integration
invoke('chat_with_claude', { message: string, context: string })

// Webview Embedding
invoke('embed_claude', { x, y, width, height })
invoke('resize_embedded', { x, y, width, height })
invoke('close_embedded')
```

### Tauri Detection Pattern
```javascript
function getInvoke() {
    if (window.__TAURI__ && window.__TAURI__.core && window.__TAURI__.core.invoke) {
        return window.__TAURI__.core.invoke;
    }
    return null;  // Browser mode
}
```

---

## DATA FLOW

### User Action Flow
```
User Click
    │
    ▼
Event Handler (data-* attribute)
    │
    ▼
Controller Method (Apps, Scripts, etc.)
    │
    ├── Browser Mode ──► Web Fallback
    │
    └── Tauri Mode
            │
            ▼
        invoke() ──► Rust Backend
            │
            ▼
        External System (File, Python, API)
            │
            ▼
        Result ──► Terminal/UI Feedback
```

### Chat Flow
```
User Message
    │
    ▼
ChatAssistant.send()
    │
    ├── Browser Mode ──► Direct Anthropic API
    │
    └── Tauri Mode
            │
            ▼
        invoke('chat_with_claude')
            │
            ▼
        Rust HTTP Client ──► Anthropic API
            │
            ▼
        Response ──► addMessage('assistant', response)
```

---

## EXTERNAL INTEGRATIONS

### Supabase Knowledge Base
```
┌──────────────────────────────────────┐
│           Supabase Project           │
├──────────────────────────────────────┤
│  PostgreSQL + pgvector               │
│                                      │
│  Table: knowledge_base               │
│  ├── id (uuid)                       │
│  ├── content (text)                  │
│  ├── embedding (vector)              │
│  ├── metadata (jsonb)                │
│  └── created_at (timestamp)          │
│                                      │
│  Chunks: 286+ (video transcripts)    │
└──────────────────────────────────────┘
```

**Access Pattern:**
- Direct table queries (NOT RPC functions)
- Embedding: text-embedding-3-small (OpenAI)
- Query via Python scripts in 05-Scripts/

### Google Drive
```
G:\My Drive\00 - Trajanus USA\
├── 00-Command-Center/
│   ├── 05-Scripts/          ← Python automation
│   ├── 08-EOS-Files/        ← Session documentation
│   └── Foundational Files/  ← Core protocols
├── Reference/               ← Standards documents
└── [Project Folders]/       ← Active work
```

**Access Pattern:**
- Tauri `open_path` for folder navigation
- Python scripts for file operations
- Google Docs format for Claude readability

---

## JAVASCRIPT PATTERNS

### Controller Object Pattern
Each workspace uses controller objects for organization:

```javascript
const ControllerName = {
    // State
    isLoading: false,

    // Methods
    async action() {
        const invoke = getInvoke();
        if (!invoke) {
            // Browser fallback
            return;
        }

        try {
            const result = await invoke('command', { params });
            // Handle success
        } catch (e) {
            // Handle error
        }
    }
};
```

### CSP-Compliant Event Binding
No inline handlers. Use data attributes:

```html
<button data-action="launch" data-target="vscode">VS Code</button>
```

```javascript
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-action="launch"]').forEach(el => {
        el.addEventListener('click', () => {
            Apps.launch(el.dataset.target);
        });
    });
});
```

### Terminal Output Pattern
```javascript
const Terminal = {
    output(message, type = 'info') {
        const terminal = document.getElementById('terminal-output');
        const line = document.createElement('div');
        line.className = `terminal-line ${type}`;
        const timestamp = new Date().toLocaleTimeString();
        line.innerHTML = `[${timestamp}] ${message}`;
        terminal.appendChild(line);
        terminal.scrollTop = terminal.scrollHeight;
    },

    success(msg) { this.output(`✓ ${msg}`, 'success'); },
    error(msg) { this.output(`✗ ${msg}`, 'error'); },
    warning(msg) { this.output(`⚠ ${msg}`, 'warning'); },
    info(msg) { this.output(msg, 'info'); }
};
```

---

## BUILD & DEPLOYMENT

### Development
```bash
cd C:\Dev\trajanus-command-center
npm run tauri dev
```

### Production Build
```bash
npm run tauri build
# Output: src-tauri/target/release/trajanus-command-center.exe
```

### Environment Variables
```
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJ...
ANTHROPIC_API_KEY=sk-ant-...
```

Location: `G:\My Drive\00 - Trajanus USA\00-Command-Center\.env`

---

## SECURITY CONSIDERATIONS

### File Access
- Tauri sandboxing limits file access
- Explicit paths required for operations
- No arbitrary file execution

### API Keys
- Keys stored in .env (not in source)
- Tauri backend handles API calls
- Browser mode limited functionality

### Content Security Policy
- No inline scripts in production
- Data attributes for event binding
- External scripts from CDN only (GSAP)

---

## KNOWN CONSTRAINTS

### Sacred File Protection
- `src/index.html` - Never edit directly
- `src-tauri/src/lib.rs` - Minimal changes only

### Google Drive Restrictions
- No npm operations on synced folders
- File locking during sync
- TAR errors if violated

### Browser Mode Limitations
- No file system access
- No Python script execution
- Limited API access (CORS)

---

## EXTENSION POINTS

### Adding New Workspace
1. Create `src/toolkits/new-workspace.html`
2. Add navigation link in `index.html`
3. Create `new-workspace/.claude.md` context
4. Follow existing patterns for consistency

### Adding New Tauri Command
1. Add function in `lib.rs`
2. Register in Tauri builder
3. Call via `invoke()` in JavaScript
4. Handle browser fallback

### Adding New Integration
1. Create Python script in 05-Scripts/
2. Add invoke command if needed
3. Wire up in appropriate workspace
4. Document in .claude.md

---

**Remember:** Simplicity over complexity. This is a tool for one power user, not a platform for millions.
