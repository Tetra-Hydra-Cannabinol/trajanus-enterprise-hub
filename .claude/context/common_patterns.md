# Trajanus Command Center - Common Patterns

**Purpose:** Reusable code patterns and recipes for common tasks
**Version:** 1.0
**Last Updated:** 2026-01-17

---

## TAURI API PATTERNS

### Safe Invoke Wrapper
Always check for Tauri availability:

```javascript
function getInvoke() {
    if (window.__TAURI__ && window.__TAURI__.core && window.__TAURI__.core.invoke) {
        return window.__TAURI__.core.invoke;
    }
    return null;
}

// Usage
async function doSomething() {
    const invoke = getInvoke();
    if (!invoke) {
        // Browser fallback
        showNotification('This feature requires the desktop app', 'warning');
        return;
    }

    try {
        const result = await invoke('command_name', { param1: 'value' });
        // Handle success
    } catch (e) {
        Terminal.error(`Failed: ${e}`);
    }
}
```

### Open File/Folder
```javascript
async function openPath(path) {
    const invoke = getInvoke();
    if (!invoke) {
        // Browser can't open local paths
        showNotification('Requires desktop app', 'warning');
        return;
    }

    try {
        await invoke('open_path', { path: path });
        Terminal.success(`Opened: ${path}`);
    } catch (e) {
        Terminal.error(`Failed to open: ${e}`);
    }
}
```

### Run Python Script
```javascript
const SCRIPTS_PATH = 'G:\\My Drive\\00 - Trajanus USA\\00-Command-Center\\05-Scripts\\';

async function runScript(scriptName) {
    const invoke = getInvoke();
    if (!invoke) {
        showNotification('Scripts require desktop app', 'warning');
        return;
    }

    Terminal.info(`Running: ${scriptName}`);

    try {
        const result = await invoke('run_python_script', {
            scriptPath: SCRIPTS_PATH + scriptName
        });

        if (result) {
            Terminal.output('--- Output ---');
            result.split('\n').forEach(line => Terminal.output(line));
            Terminal.output('--- End ---');
        }
        Terminal.success(`Completed: ${scriptName}`);
    } catch (e) {
        Terminal.error(`Script failed: ${e}`);
    }
}
```

---

## UI COMPONENT PATTERNS

### Notification Toast
```javascript
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `<span>${message}</span>`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        border-radius: 8px;
        background: ${type === 'warning' ? '#2d2d2d' : '#1a1a1a'};
        border: 1px solid ${type === 'warning' ? '#fbbf24' : '#c0c0c0'};
        color: ${type === 'warning' ? '#fbbf24' : '#e0e0e0'};
        font-size: 14px;
        z-index: 9999;
        animation: slideIn 0.3s ease;
    `;
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 3000);
}
```

### Modal Window
```javascript
const TrajnausWindow = {
    currentWindow: null,

    open(title, content) {
        this.close();

        const overlay = document.createElement('div');
        overlay.className = 'trajanus-window-overlay';
        overlay.onclick = (e) => {
            if (e.target === overlay) this.close();
        };

        overlay.innerHTML = `
            <div class="trajanus-window">
                <div class="trajanus-window-header">
                    <span class="trajanus-window-title">${title}</span>
                    <button class="trajanus-window-close" onclick="TrajnausWindow.close()">×</button>
                </div>
                <div class="trajanus-window-body">${content}</div>
            </div>
        `;

        document.body.appendChild(overlay);
        this.currentWindow = overlay;

        // Close on Escape
        document.addEventListener('keydown', this.escHandler);
        return overlay;
    },

    close() {
        if (this.currentWindow) {
            this.currentWindow.remove();
            this.currentWindow = null;
            document.removeEventListener('keydown', this.escHandler);
        }
    },

    escHandler(e) {
        if (e.key === 'Escape') TrajnausWindow.close();
    },

    alert(title, message) {
        return this.open(title, `<p style="color: #c0c0c0;">${message}</p>`);
    }
};
```

### Collapsible Section
```javascript
function toggleSection(sectionId) {
    const content = document.getElementById(`${sectionId}-content`);
    const toggle = document.getElementById(`${sectionId}-toggle`);

    if (content && toggle) {
        content.classList.toggle('collapsed');
        toggle.classList.toggle('collapsed');
        toggle.textContent = content.classList.contains('collapsed') ? '▼' : '▲';
    }
}
```

HTML:
```html
<div class="section-header" onclick="toggleSection('intro')">
    <span class="section-title">Section Title</span>
    <span class="section-toggle" id="intro-toggle">▲</span>
</div>
<div class="section-content" id="intro-content">
    <!-- Content here -->
</div>
```

CSS:
```css
.section-content.collapsed {
    display: none;
}

.section-toggle.collapsed {
    transform: rotate(180deg);
}
```

---

## TERMINAL PATTERNS

### Terminal Controller
```javascript
const Terminal = {
    getOutput() {
        return document.getElementById('terminal-output');
    },

    output(message, className = '') {
        const output = this.getOutput();
        if (!output) {
            console.log(`[Terminal] ${message}`);
            return;
        }

        const timestamp = new Date().toLocaleTimeString();
        const line = document.createElement('div');
        line.className = `terminal-line ${className}`;
        line.innerHTML = `<span style="color:#606060;">[${timestamp}]</span> ${message}`;
        output.appendChild(line);
        output.scrollTop = output.scrollHeight;
    },

    info(msg)    { this.output(msg, 'info'); },
    success(msg) { this.output(`✓ ${msg}`, 'success'); },
    error(msg)   { this.output(`✗ ${msg}`, 'error'); },
    warning(msg) { this.output(`⚠ ${msg}`, 'warning'); },

    clear() {
        const output = this.getOutput();
        if (output) output.innerHTML = '';
    }
};
```

---

## CHAT PATTERNS

### Chat Controller
```javascript
const Chat = {
    isProcessing: false,

    addMessage(role, content) {
        const messages = document.getElementById('chat-messages');
        const msg = document.createElement('div');
        msg.className = `chat-message ${role}`;
        msg.textContent = content;
        messages.appendChild(msg);
        messages.scrollTop = messages.scrollHeight;
    },

    showTyping() {
        const messages = document.getElementById('chat-messages');
        const typing = document.createElement('div');
        typing.className = 'typing-indicator';
        typing.id = 'typing-indicator';
        typing.innerHTML = '<span></span><span></span><span></span>';
        messages.appendChild(typing);
        messages.scrollTop = messages.scrollHeight;
    },

    hideTyping() {
        document.getElementById('typing-indicator')?.remove();
    },

    async send() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();

        if (!message || this.isProcessing) return;

        this.addMessage('user', message);
        input.value = '';
        this.isProcessing = true;
        this.showTyping();

        const invoke = getInvoke();

        try {
            let response;
            if (invoke) {
                response = await invoke('chat_with_claude', {
                    message: message,
                    context: 'Your system context here'
                });
            } else {
                // Browser fallback
                response = 'Running in browser mode. Full AI requires desktop app.';
            }

            this.hideTyping();
            this.addMessage('assistant', response);
        } catch (e) {
            this.hideTyping();
            this.addMessage('assistant', `Error: ${e}`);
        } finally {
            this.isProcessing = false;
        }
    }
};
```

---

## EVENT BINDING PATTERNS

### CSP-Compliant Data Attributes
HTML:
```html
<button class="ext-btn" data-launch="vscode">VS Code</button>
<button class="script-btn" data-script="convert.py">Convert</button>
<button class="agent-btn" data-agent="research">Research</button>
```

JavaScript:
```javascript
document.addEventListener('DOMContentLoaded', () => {
    // App launchers
    document.querySelectorAll('[data-launch]').forEach(el => {
        el.addEventListener('click', () => Apps.launch(el.dataset.launch));
    });

    // Script runners
    document.querySelectorAll('[data-script]').forEach(el => {
        el.addEventListener('click', () => Scripts.run(el.dataset.script));
    });

    // Agent activators
    document.querySelectorAll('[data-agent]').forEach(el => {
        el.addEventListener('click', () => Agents.activate(el.dataset.agent));
    });
});
```

### Keyboard Shortcuts
```javascript
document.addEventListener('keydown', (e) => {
    // Escape closes modals
    if (e.key === 'Escape') {
        TrajnausWindow.close();
    }

    // Enter sends chat (without shift)
    if (e.key === 'Enter' && !e.shiftKey) {
        if (document.activeElement.id === 'chat-input') {
            e.preventDefault();
            Chat.send();
        }
    }

    // Ctrl+K for quick search (example)
    if (e.ctrlKey && e.key === 'k') {
        e.preventDefault();
        document.getElementById('search-input')?.focus();
    }
});
```

---

## BUTTON CSS PATTERNS

### V2 Synapse Neural Glow
```css
.neural-btn {
    background: #0a0a0a;
    color: #00AAFF;
    border: none;

    /* Double-ring glow effect */
    box-shadow:
        0 0 0 1px rgba(0, 170, 255, 0.5),
        0 0 0 3px #0a0a0a,
        0 0 0 4px rgba(0, 170, 255, 0.3),
        0 0 15px rgba(0, 170, 255, 0.2),
        inset 0 0 30px rgba(0, 170, 255, 0.03);
    text-shadow: 0 0 8px rgba(0, 170, 255, 0.5);

    transition: all 0.25s ease;
}

.neural-btn:hover {
    color: #fff;
    transform: translateY(-2px);
    box-shadow:
        0 0 0 1px rgba(0, 170, 255, 0.8),
        0 0 0 3px #0a0a0a,
        0 0 0 4px rgba(0, 170, 255, 0.5),
        0 0 25px rgba(0, 170, 255, 0.4),
        inset 0 0 40px rgba(0, 170, 255, 0.05);
    text-shadow: 0 0 15px rgba(0, 170, 255, 0.9);
}

.neural-btn:active {
    color: #FFB347;
    transform: translateY(1px);
    box-shadow:
        0 0 0 1px rgba(255, 149, 0, 0.8),
        0 0 0 3px #0a0a0a,
        0 0 20px rgba(255, 149, 0, 0.3),
        inset 0 0 30px rgba(255, 149, 0, 0.05);
    text-shadow: 0 0 10px rgba(255, 149, 0, 0.7);
}
```

### Top Highlight Line
```css
.btn-with-highlight::before {
    content: '';
    position: absolute;
    top: -1px;
    left: 10%;
    right: 10%;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00AAFF, transparent);
    border-radius: 2px;
}
```

---

## GRID PATTERNS

### Auto-Fill Card Grid
```css
.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 12px;
}
```

### Fixed Column Grid
```css
.fixed-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
}

@media (max-width: 1024px) {
    .fixed-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 600px) {
    .fixed-grid {
        grid-template-columns: 1fr;
    }
}
```

---

## LOADING STATE PATTERNS

### Button Loading State
```javascript
function setButtonLoading(button, loading) {
    if (loading) {
        button.disabled = true;
        button.dataset.originalText = button.textContent;
        button.textContent = 'Loading...';
        button.style.opacity = '0.7';
    } else {
        button.disabled = false;
        button.textContent = button.dataset.originalText || button.textContent;
        button.style.opacity = '1';
    }
}
```

### Typing Indicator CSS
```css
.typing-indicator {
    display: flex;
    gap: 4px;
    padding: 12px 16px;
    background: var(--bg-surface);
    border-radius: 8px;
    width: fit-content;
}

.typing-indicator span {
    width: 6px;
    height: 6px;
    background: var(--silver);
    border-radius: 50%;
    animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s; }

@keyframes typing {
    0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
    30% { transform: translateY(-4px); opacity: 1; }
}
```

---

## SCROLL PATTERNS

### Scroll to Element
```javascript
function scrollToElement(selector) {
    const element = document.querySelector(selector);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}
```

### Scroll to Top
```javascript
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
```

### Auto-scroll Container
```javascript
function autoScrollToBottom(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
}
```

---

## ERROR HANDLING PATTERNS

### Try-Catch with Logging
```javascript
async function safeOperation(operation, fallback) {
    try {
        return await operation();
    } catch (e) {
        console.error('Operation failed:', e);
        Terminal.error(`Error: ${e.message || e}`);
        if (fallback) fallback(e);
        return null;
    }
}

// Usage
const result = await safeOperation(
    () => invoke('command', { data }),
    (e) => showNotification('Operation failed', 'error')
);
```

---

## DATE/TIME PATTERNS

### Format Timestamp
```javascript
function formatTimestamp() {
    return new Date().toLocaleTimeString();
}

function formatDate() {
    return new Date().toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}
```

### Update Greeting
```javascript
function updateGreeting() {
    const hour = new Date().getHours();
    let greeting = 'Good evening';
    if (hour < 12) greeting = 'Good morning';
    else if (hour < 17) greeting = 'Good afternoon';

    const element = document.getElementById('greeting-text');
    if (element) element.textContent = greeting;
}
```

---

**Note:** All patterns follow the established architecture. Adapt as needed for specific workspaces.
