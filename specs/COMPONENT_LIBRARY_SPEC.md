# COMPONENT LIBRARY SPECIFICATION
## Trajanus Enterprise Hub - Reusable UI Components
### Version 1.0 | January 2026

---

## TABLE OF CONTENTS

1. [TrajButton](#1-trajbutton)
2. [TrajPanel](#2-trajpanel)
3. [TrajToolWindow](#3-trajtoolwindow)
4. [TrajProgressBar](#4-trajprogressbar)
5. [TrajLog](#5-trajlog)
6. [TrajTabs](#6-trajtabs)
7. [TrajModal](#7-trajmodal)
8. [TrajToast](#8-trajtoast)
9. [TrajInput](#9-trajinput)
10. [TrajSelect](#10-trajselect)
11. [TrajTable](#11-trajtable)
12. [TrajSpinner](#12-trajspinner)

---

## 1. TRAJBUTTON

Microsoft Access-style 3D beveled button with multiple variants.

### HTML Structure

```html
<!-- Default Button -->
<button class="traj-button">
    Default
</button>

<!-- Primary Button -->
<button class="traj-button primary">
    Primary Action
</button>

<!-- Button with Icon -->
<button class="traj-button">
    <span class="traj-button-icon">+</span>
    <span class="traj-button-text">Add Item</span>
</button>

<!-- Small Button -->
<button class="traj-button small">
    Small
</button>

<!-- Large Button -->
<button class="traj-button large">
    Large Button
</button>

<!-- Disabled Button -->
<button class="traj-button" disabled>
    Disabled
</button>

<!-- Success Button -->
<button class="traj-button success">
    Confirm
</button>

<!-- Danger Button -->
<button class="traj-button danger">
    Delete
</button>
```

### CSS

```css
/* ========== TRAJBUTTON ========== */

.traj-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;

    padding: 8px 16px;
    min-width: 80px;

    font-family: 'Segoe UI', system-ui, sans-serif;
    font-size: 13px;
    font-weight: 500;
    line-height: 1;

    color: #C0C0C0;
    background: linear-gradient(180deg, #3a3a3a 0%, #2d2d2d 100%);

    border: none;
    border-top: 2px solid #505050;
    border-left: 2px solid #505050;
    border-right: 2px solid #1a1a1a;
    border-bottom: 2px solid #1a1a1a;

    border-radius: 2px;
    cursor: pointer;

    transition: background 0.15s ease,
                color 0.15s ease,
                border-color 0.15s ease,
                box-shadow 0.15s ease,
                transform 0.15s ease;
}

.traj-button:hover {
    color: #FFFFFF;
    background: linear-gradient(180deg, #454545 0%, #3a3a3a 100%);
    border-top-color: #606060;
    border-left-color: #606060;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3),
                0 0 8px rgba(0, 102, 204, 0.2);
    transform: translateY(-1px);
}

.traj-button:active {
    background: linear-gradient(180deg, #252525 0%, #2d2d2d 100%);
    border-top: 2px solid #1a1a1a;
    border-left: 2px solid #1a1a1a;
    border-right: 2px solid #404040;
    border-bottom: 2px solid #404040;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.4);
    transform: translateY(0);
}

.traj-button:focus {
    outline: none;
    box-shadow: 0 0 0 2px #4DA6FF;
}

.traj-button:focus:not(:focus-visible) {
    box-shadow: none;
}

.traj-button:disabled {
    background: #2a2a2a;
    color: #606060;
    border-top-color: #353535;
    border-left-color: #353535;
    border-right-color: #252525;
    border-bottom-color: #252525;
    cursor: not-allowed;
    box-shadow: none;
    transform: none;
}

/* Primary Variant */
.traj-button.primary {
    color: #FFFFFF;
    background: linear-gradient(180deg, #0077DD 0%, #0066CC 100%);
    border-top-color: #3399FF;
    border-left-color: #3399FF;
    border-right-color: #004999;
    border-bottom-color: #004999;
}

.traj-button.primary:hover {
    background: linear-gradient(180deg, #0088EE 0%, #0077DD 100%);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3),
                0 0 12px rgba(0, 102, 204, 0.4);
}

.traj-button.primary:active {
    background: linear-gradient(180deg, #004999 0%, #0055AA 100%);
    border-top-color: #003377;
    border-left-color: #003377;
    border-right-color: #0077DD;
    border-bottom-color: #0077DD;
}

/* Success Variant */
.traj-button.success {
    color: #FFFFFF;
    background: linear-gradient(180deg, #00BB00 0%, #00AA00 100%);
    border-top-color: #00DD00;
    border-left-color: #00DD00;
    border-right-color: #008800;
    border-bottom-color: #008800;
}

.traj-button.success:hover {
    background: linear-gradient(180deg, #00CC00 0%, #00BB00 100%);
}

/* Danger Variant */
.traj-button.danger {
    color: #FFFFFF;
    background: linear-gradient(180deg, #DD0000 0%, #CC0000 100%);
    border-top-color: #FF3333;
    border-left-color: #FF3333;
    border-right-color: #990000;
    border-bottom-color: #990000;
}

.traj-button.danger:hover {
    background: linear-gradient(180deg, #EE0000 0%, #DD0000 100%);
}

/* Sizes */
.traj-button.small {
    padding: 4px 10px;
    font-size: 12px;
    min-width: 60px;
}

.traj-button.large {
    padding: 12px 24px;
    font-size: 14px;
    min-width: 120px;
}

/* Icon */
.traj-button-icon {
    font-size: 14px;
    line-height: 1;
}
```

### JavaScript Behavior

```javascript
// No special JS needed - pure CSS implementation
// For loading state, add class programmatically:

function setButtonLoading(button, isLoading) {
    if (isLoading) {
        button.disabled = true;
        button.dataset.originalText = button.textContent;
        button.innerHTML = '<span class="traj-spinner small"></span> Loading...';
    } else {
        button.disabled = false;
        button.textContent = button.dataset.originalText;
    }
}
```

### Usage Example

```html
<div class="button-group">
    <button class="traj-button">Cancel</button>
    <button class="traj-button primary">Save Changes</button>
</div>
```

---

## 2. TRAJPANEL

Collapsible panel with smooth animation.

### HTML Structure

```html
<div class="traj-panel" id="panel-example">
    <div class="traj-panel-header" onclick="TrajPanel.toggle('panel-example')">
        <span class="traj-panel-title">Panel Title</span>
        <span class="traj-panel-icon">▼</span>
    </div>
    <div class="traj-panel-content">
        <p>Panel content goes here...</p>
    </div>
</div>

<!-- Initially collapsed -->
<div class="traj-panel collapsed" id="panel-collapsed">
    <div class="traj-panel-header" onclick="TrajPanel.toggle('panel-collapsed')">
        <span class="traj-panel-title">Collapsed Panel</span>
        <span class="traj-panel-icon">▼</span>
    </div>
    <div class="traj-panel-content">
        <p>This panel starts collapsed.</p>
    </div>
</div>
```

### CSS

```css
/* ========== TRAJPANEL ========== */

.traj-panel {
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 8px;
}

.traj-panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 12px 16px;

    background: #2d2d2d;
    cursor: pointer;

    transition: background 0.2s ease;
}

.traj-panel-header:hover {
    background: #3a3a3a;
}

.traj-panel-title {
    font-size: 13px;
    font-weight: 600;
    color: #C0C0C0;
    letter-spacing: 0.05em;
}

.traj-panel-icon {
    color: #808080;
    font-size: 10px;
    transition: transform 0.3s ease;
}

.traj-panel.collapsed .traj-panel-icon {
    transform: rotate(-90deg);
}

.traj-panel-content {
    padding: 16px;
    background: #1a1a1a;

    max-height: 2000px;
    opacity: 1;
    overflow: hidden;

    transition: max-height 0.3s ease-in-out,
                opacity 0.2s ease-in-out,
                padding 0.3s ease-in-out;
}

.traj-panel.collapsed .traj-panel-content {
    max-height: 0;
    opacity: 0;
    padding-top: 0;
    padding-bottom: 0;
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
    .traj-panel-icon,
    .traj-panel-content {
        transition: none;
    }
}
```

### JavaScript Behavior

```javascript
const TrajPanel = {
    toggle(panelId) {
        const panel = document.getElementById(panelId);
        if (!panel) return;

        panel.classList.toggle('collapsed');

        // Emit custom event
        panel.dispatchEvent(new CustomEvent('traj-panel-toggle', {
            detail: { collapsed: panel.classList.contains('collapsed') }
        }));
    },

    expand(panelId) {
        const panel = document.getElementById(panelId);
        if (panel) panel.classList.remove('collapsed');
    },

    collapse(panelId) {
        const panel = document.getElementById(panelId);
        if (panel) panel.classList.add('collapsed');
    },

    isCollapsed(panelId) {
        const panel = document.getElementById(panelId);
        return panel ? panel.classList.contains('collapsed') : false;
    }
};
```

### Usage Example

```html
<div class="traj-panel" id="settings-panel">
    <div class="traj-panel-header" onclick="TrajPanel.toggle('settings-panel')">
        <span class="traj-panel-title">Advanced Settings</span>
        <span class="traj-panel-icon">▼</span>
    </div>
    <div class="traj-panel-content">
        <label class="traj-label">Option 1</label>
        <input type="text" class="traj-input">
    </div>
</div>
```

---

## 3. TRAJTOOLWINDOW

Complete tool window template with header, sidebar, main content, and log panel.

### HTML Structure

```html
<div class="traj-tool-window">
    <!-- Header -->
    <header class="traj-tool-header">
        <button class="traj-hub-button" onclick="location.href='../index.html'">
            <span>&larr;</span>
            <span>Hub</span>
        </button>
        <h1 class="traj-header-title">TRAJANUS USA</h1>
        <div class="traj-header-actions">
            <button class="traj-button small">Settings</button>
        </div>
    </header>

    <!-- Sidebar -->
    <aside class="traj-sidebar">
        <nav class="traj-sidebar-nav">
            <a href="#" class="traj-nav-item active">Dashboard</a>
            <a href="#" class="traj-nav-item">Documents</a>
            <a href="#" class="traj-nav-item">Reports</a>
        </nav>
    </aside>

    <!-- Main Content -->
    <main class="traj-main-content">
        <div class="traj-tab-bar">
            <button class="traj-tab active" data-tab="overview">Overview</button>
            <button class="traj-tab" data-tab="details">Details</button>
            <button class="traj-tab" data-tab="history">History</button>
        </div>
        <div class="traj-content-area">
            <div class="traj-tab-content active" id="overview">
                <!-- Content here -->
            </div>
        </div>
    </main>

    <!-- Log Panel -->
    <aside class="traj-log-panel">
        <div class="traj-log-header">Processing Log</div>
        <div class="traj-log-content" id="logContent">
            <!-- Log entries -->
        </div>
    </aside>

    <!-- Status Bar -->
    <footer class="traj-status-bar">
        <span class="traj-status-left">
            <span class="traj-status-dot active"></span>
            Ready
        </span>
        <span class="traj-status-right">v1.0.0</span>
    </footer>
</div>
```

### CSS

```css
/* ========== TRAJTOOLWINDOW ========== */

.traj-tool-window {
    display: grid;
    grid-template-rows: 56px 1fr 28px;
    grid-template-columns: 240px 1fr 280px;
    grid-template-areas:
        "header header header"
        "sidebar main log"
        "status status status";

    height: 100vh;
    background: #1a1a1a;
    border: 3px solid #0066CC;
}

.traj-tool-header {
    grid-area: header;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 16px;
    background: #1a1a1a;
    border-bottom: 1px solid #3a3a3a;
}

.traj-hub-button {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    color: #C0C0C0;
    background: transparent;
    border: 1px solid #C0C0C0;
    border-radius: 4px;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.traj-hub-button:hover {
    color: #FFFFFF;
    background: #2d2d2d;
    border-color: #0066CC;
}

.traj-header-title {
    font-size: 16px;
    font-weight: 600;
    letter-spacing: 0.1em;
    color: #C0C0C0;
}

.traj-header-actions {
    display: flex;
    gap: 8px;
}

.traj-sidebar {
    grid-area: sidebar;
    background: #1a1a1a;
    border-right: 1px solid #3a3a3a;
    overflow-y: auto;
    padding: 16px;
}

.traj-sidebar-nav {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.traj-nav-item {
    padding: 10px 12px;
    color: #A0A0A0;
    text-decoration: none;
    border-radius: 4px;
    font-size: 13px;
    transition: all 0.2s ease;
}

.traj-nav-item:hover {
    color: #FFFFFF;
    background: #2d2d2d;
}

.traj-nav-item.active {
    color: #FFFFFF;
    background: #0066CC;
}

.traj-main-content {
    grid-area: main;
    display: flex;
    flex-direction: column;
    background: #2d2d2d;
    overflow: hidden;
}

.traj-content-area {
    flex: 1;
    overflow-y: auto;
    padding: 24px;
}

.traj-log-panel {
    grid-area: log;
    display: flex;
    flex-direction: column;
    background: #1a1a1a;
    border-left: 1px solid #3a3a3a;
}

.traj-log-header {
    padding: 12px 16px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #C0C0C0;
    background: #2d2d2d;
    border-bottom: 1px solid #3a3a3a;
}

.traj-log-content {
    flex: 1;
    overflow-y: auto;
    padding: 8px;
    font-family: 'Consolas', monospace;
    font-size: 11px;
}

.traj-status-bar {
    grid-area: status;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 16px;
    background: #2d2d2d;
    border-top: 1px solid #3a3a3a;
    font-size: 11px;
    color: #808080;
}

.traj-status-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #808080;
    margin-right: 6px;
}

.traj-status-dot.active {
    background: #00AA00;
}

.traj-status-dot.warning {
    background: #FF8800;
}

.traj-status-dot.error {
    background: #CC0000;
}
```

### JavaScript Behavior

```javascript
const TrajToolWindow = {
    init() {
        this.initTabs();
    },

    initTabs() {
        document.querySelectorAll('.traj-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                const tabId = tab.dataset.tab;
                this.switchTab(tabId);
            });
        });
    },

    switchTab(tabId) {
        // Deactivate all tabs
        document.querySelectorAll('.traj-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.traj-tab-content').forEach(c => c.classList.remove('active'));

        // Activate selected
        document.querySelector(`.traj-tab[data-tab="${tabId}"]`)?.classList.add('active');
        document.getElementById(tabId)?.classList.add('active');
    },

    setStatus(status, message) {
        const dot = document.querySelector('.traj-status-dot');
        const text = document.querySelector('.traj-status-left');

        if (dot) {
            dot.className = `traj-status-dot ${status}`;
        }
        if (text) {
            text.innerHTML = `<span class="traj-status-dot ${status}"></span>${message}`;
        }
    }
};

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => TrajToolWindow.init());
```

---

## 4. TRAJPROGRESSBAR

Progress indicator with multiple states.

### HTML Structure

```html
<!-- Determinate Progress -->
<div class="traj-progress">
    <div class="traj-progress-bar" style="width: 60%;"></div>
</div>

<!-- With Label -->
<div class="traj-progress-wrapper">
    <div class="traj-progress-label">
        <span>Uploading files...</span>
        <span>60%</span>
    </div>
    <div class="traj-progress">
        <div class="traj-progress-bar" style="width: 60%;"></div>
    </div>
</div>

<!-- Indeterminate (animated stripes) -->
<div class="traj-progress">
    <div class="traj-progress-bar indeterminate"></div>
</div>

<!-- Success State -->
<div class="traj-progress">
    <div class="traj-progress-bar success" style="width: 100%;"></div>
</div>

<!-- Error State -->
<div class="traj-progress">
    <div class="traj-progress-bar error" style="width: 45%;"></div>
</div>
```

### CSS

```css
/* ========== TRAJPROGRESSBAR ========== */

.traj-progress-wrapper {
    margin-bottom: 16px;
}

.traj-progress-label {
    display: flex;
    justify-content: space-between;
    margin-bottom: 6px;
    font-size: 12px;
    color: #A0A0A0;
}

.traj-progress {
    height: 8px;
    background: #2d2d2d;
    border-radius: 4px;
    overflow: hidden;
}

.traj-progress-bar {
    height: 100%;
    background: #0066CC;
    border-radius: 4px;
    transition: width 0.2s ease;
}

.traj-progress-bar.success {
    background: #00AA00;
}

.traj-progress-bar.error {
    background: #CC0000;
}

.traj-progress-bar.warning {
    background: #FF8800;
}

/* Indeterminate State */
@keyframes traj-progress-stripes {
    from { background-position: 40px 0; }
    to { background-position: 0 0; }
}

.traj-progress-bar.indeterminate {
    width: 100%;
    background-image: linear-gradient(
        45deg,
        rgba(255,255,255,0.15) 25%,
        transparent 25%,
        transparent 50%,
        rgba(255,255,255,0.15) 50%,
        rgba(255,255,255,0.15) 75%,
        transparent 75%,
        transparent
    );
    background-size: 40px 40px;
    animation: traj-progress-stripes 1s linear infinite;
}

/* Large variant */
.traj-progress.large {
    height: 16px;
}

.traj-progress.large .traj-progress-bar {
    border-radius: 8px;
}
```

### JavaScript Behavior

```javascript
const TrajProgress = {
    set(element, value, max = 100) {
        const bar = element.querySelector('.traj-progress-bar');
        if (!bar) return;

        const percent = Math.min(100, Math.max(0, (value / max) * 100));
        bar.style.width = `${percent}%`;

        // Update label if exists
        const label = element.closest('.traj-progress-wrapper')
            ?.querySelector('.traj-progress-label span:last-child');
        if (label) {
            label.textContent = `${Math.round(percent)}%`;
        }
    },

    setIndeterminate(element, isIndeterminate) {
        const bar = element.querySelector('.traj-progress-bar');
        if (!bar) return;

        if (isIndeterminate) {
            bar.classList.add('indeterminate');
        } else {
            bar.classList.remove('indeterminate');
        }
    },

    setStatus(element, status) {
        const bar = element.querySelector('.traj-progress-bar');
        if (!bar) return;

        bar.classList.remove('success', 'error', 'warning');
        if (status) {
            bar.classList.add(status);
        }
    }
};
```

---

## 5. TRAJLOG

Timestamped processing log component.

### HTML Structure

```html
<div class="traj-log" id="processLog">
    <div class="traj-log-entry info">
        <span class="traj-log-time">14:32:05</span>
        <span class="traj-log-message">Process started</span>
    </div>
    <div class="traj-log-entry success">
        <span class="traj-log-time">14:32:06</span>
        <span class="traj-log-message">File loaded successfully</span>
    </div>
    <div class="traj-log-entry warning">
        <span class="traj-log-time">14:32:07</span>
        <span class="traj-log-message">Missing optional field: description</span>
    </div>
    <div class="traj-log-entry error">
        <span class="traj-log-time">14:32:08</span>
        <span class="traj-log-message">Failed to parse line 42</span>
    </div>
</div>
```

### CSS

```css
/* ========== TRAJLOG ========== */

.traj-log {
    font-family: 'Consolas', monospace;
    font-size: 11px;
    line-height: 1.5;
    background: #1a1a1a;
    overflow-y: auto;
    max-height: 400px;
}

.traj-log-entry {
    display: flex;
    gap: 12px;
    padding: 6px 12px;
    border-left: 3px solid #3a3a3a;
    animation: traj-log-fade-in 0.15s ease-out;
}

@keyframes traj-log-fade-in {
    from {
        opacity: 0;
        transform: translateY(-4px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.traj-log-entry:hover {
    background: #252525;
}

.traj-log-entry.info {
    border-left-color: #0066CC;
}

.traj-log-entry.success {
    border-left-color: #00AA00;
}

.traj-log-entry.warning {
    border-left-color: #FF8800;
}

.traj-log-entry.error {
    border-left-color: #CC0000;
}

.traj-log-time {
    color: #808080;
    min-width: 60px;
}

.traj-log-message {
    color: #C0C0C0;
    word-break: break-word;
}

.traj-log-entry.error .traj-log-message {
    color: #FF6666;
}

.traj-log-entry.warning .traj-log-message {
    color: #FFAA33;
}

.traj-log-entry.success .traj-log-message {
    color: #66CC66;
}

/* Compact variant */
.traj-log.compact .traj-log-entry {
    padding: 3px 8px;
    font-size: 10px;
}
```

### JavaScript Behavior

```javascript
const TrajLog = {
    add(containerId, message, type = 'info') {
        const container = document.getElementById(containerId);
        if (!container) return;

        const time = new Date().toTimeString().split(' ')[0];

        const entry = document.createElement('div');
        entry.className = `traj-log-entry ${type}`;
        entry.innerHTML = `
            <span class="traj-log-time">${time}</span>
            <span class="traj-log-message">${this.escapeHtml(message)}</span>
        `;

        container.appendChild(entry);
        container.scrollTop = container.scrollHeight;
    },

    clear(containerId) {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = '';
        }
    },

    info(containerId, message) {
        this.add(containerId, message, 'info');
    },

    success(containerId, message) {
        this.add(containerId, message, 'success');
    },

    warning(containerId, message) {
        this.add(containerId, message, 'warning');
    },

    error(containerId, message) {
        this.add(containerId, message, 'error');
    },

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};
```

### Usage Example

```javascript
TrajLog.info('processLog', 'Starting file conversion...');
TrajLog.success('processLog', 'Converted 15 files');
TrajLog.warning('processLog', 'Skipped 2 unsupported formats');
TrajLog.error('processLog', 'Failed: permissions denied');
```

---

## 6. TRAJTABS

Tab navigation component.

### HTML Structure

```html
<div class="traj-tabs">
    <div class="traj-tab-bar">
        <button class="traj-tab active" data-tab="tab1">Overview</button>
        <button class="traj-tab" data-tab="tab2">Details</button>
        <button class="traj-tab" data-tab="tab3">Settings</button>
    </div>
    <div class="traj-tab-panels">
        <div class="traj-tab-content active" id="tab1">
            <p>Overview content</p>
        </div>
        <div class="traj-tab-content" id="tab2">
            <p>Details content</p>
        </div>
        <div class="traj-tab-content" id="tab3">
            <p>Settings content</p>
        </div>
    </div>
</div>
```

### CSS

```css
/* ========== TRAJTABS ========== */

.traj-tabs {
    display: flex;
    flex-direction: column;
}

.traj-tab-bar {
    display: flex;
    gap: 2px;
    padding: 0 16px;
    background: #1a1a1a;
    border-bottom: 1px solid #3a3a3a;
}

.traj-tab {
    padding: 12px 20px;
    font-family: inherit;
    font-size: 13px;
    font-weight: 500;
    color: #A0A0A0;
    background: transparent;
    border: none;
    border-bottom: 2px solid transparent;
    cursor: pointer;
    transition: color 0.2s ease, border-color 0.2s ease, background 0.2s ease;
}

.traj-tab:hover {
    color: #C0C0C0;
    background: #252525;
}

.traj-tab.active {
    color: #FFFFFF;
    border-bottom-color: #0066CC;
}

.traj-tab:focus {
    outline: none;
    box-shadow: inset 0 0 0 2px #4DA6FF;
}

.traj-tab-panels {
    position: relative;
}

.traj-tab-content {
    display: none;
    padding: 24px;
    animation: traj-tab-fade-in 0.2s ease;
}

.traj-tab-content.active {
    display: block;
}

@keyframes traj-tab-fade-in {
    from {
        opacity: 0;
        transform: translateY(8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Vertical Tabs Variant */
.traj-tabs.vertical {
    flex-direction: row;
}

.traj-tabs.vertical .traj-tab-bar {
    flex-direction: column;
    border-bottom: none;
    border-right: 1px solid #3a3a3a;
    padding: 16px 0;
}

.traj-tabs.vertical .traj-tab {
    border-bottom: none;
    border-left: 2px solid transparent;
    text-align: left;
}

.traj-tabs.vertical .traj-tab.active {
    border-left-color: #0066CC;
}
```

### JavaScript Behavior

```javascript
const TrajTabs = {
    init(containerSelector = '.traj-tabs') {
        document.querySelectorAll(containerSelector).forEach(container => {
            container.querySelectorAll('.traj-tab').forEach(tab => {
                tab.addEventListener('click', () => {
                    this.activate(container, tab.dataset.tab);
                });
            });
        });
    },

    activate(container, tabId) {
        // Deactivate all
        container.querySelectorAll('.traj-tab').forEach(t => t.classList.remove('active'));
        container.querySelectorAll('.traj-tab-content').forEach(c => c.classList.remove('active'));

        // Activate selected
        container.querySelector(`.traj-tab[data-tab="${tabId}"]`)?.classList.add('active');
        container.querySelector(`#${tabId}`)?.classList.add('active');

        // Emit event
        container.dispatchEvent(new CustomEvent('traj-tab-change', {
            detail: { tabId }
        }));
    }
};

document.addEventListener('DOMContentLoaded', () => TrajTabs.init());
```

---

## 7. TRAJMODAL

Modal dialog with overlay.

### HTML Structure

```html
<!-- Trigger -->
<button class="traj-button" onclick="TrajModal.open('exampleModal')">Open Modal</button>

<!-- Modal -->
<div class="traj-modal-overlay" id="exampleModal">
    <div class="traj-modal">
        <div class="traj-modal-header">
            <h3 class="traj-modal-title">Modal Title</h3>
            <button class="traj-modal-close" onclick="TrajModal.close('exampleModal')">&times;</button>
        </div>
        <div class="traj-modal-body">
            <p>Modal content goes here...</p>
        </div>
        <div class="traj-modal-footer">
            <button class="traj-button" onclick="TrajModal.close('exampleModal')">Cancel</button>
            <button class="traj-button primary">Confirm</button>
        </div>
    </div>
</div>
```

### CSS

```css
/* ========== TRAJMODAL ========== */

.traj-modal-overlay {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.7);
    z-index: 1000;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.2s ease;
}

.traj-modal-overlay.visible {
    display: flex;
    opacity: 1;
}

.traj-modal {
    width: 90%;
    max-width: 500px;
    max-height: 90vh;

    background: #2d2d2d;
    border: 1px solid #3a3a3a;
    border-radius: 8px;
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.5);

    display: flex;
    flex-direction: column;

    transform: scale(0.95);
    opacity: 0;
    transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1),
                opacity 0.25s ease;
}

.traj-modal-overlay.visible .traj-modal {
    transform: scale(1);
    opacity: 1;
}

.traj-modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 20px;
    border-bottom: 1px solid #3a3a3a;
}

.traj-modal-title {
    font-size: 16px;
    font-weight: 600;
    color: #C0C0C0;
    margin: 0;
}

.traj-modal-close {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    color: #808080;
    background: transparent;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.traj-modal-close:hover {
    color: #FFFFFF;
    background: #3a3a3a;
}

.traj-modal-body {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    color: #C0C0C0;
}

.traj-modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
    padding: 16px 20px;
    border-top: 1px solid #3a3a3a;
}

/* Size variants */
.traj-modal.small {
    max-width: 360px;
}

.traj-modal.large {
    max-width: 800px;
}

.traj-modal.fullscreen {
    width: 100%;
    height: 100%;
    max-width: none;
    max-height: none;
    border-radius: 0;
}
```

### JavaScript Behavior

```javascript
const TrajModal = {
    open(modalId) {
        const overlay = document.getElementById(modalId);
        if (!overlay) return;

        overlay.style.display = 'flex';
        // Force reflow for animation
        overlay.offsetHeight;
        overlay.classList.add('visible');

        // Close on overlay click
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                this.close(modalId);
            }
        }, { once: true });

        // Close on Escape
        const escHandler = (e) => {
            if (e.key === 'Escape') {
                this.close(modalId);
                document.removeEventListener('keydown', escHandler);
            }
        };
        document.addEventListener('keydown', escHandler);

        // Focus trap
        const focusable = overlay.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        if (focusable.length) focusable[0].focus();
    },

    close(modalId) {
        const overlay = document.getElementById(modalId);
        if (!overlay) return;

        overlay.classList.remove('visible');
        setTimeout(() => {
            overlay.style.display = 'none';
        }, 200);
    },

    confirm(title, message, onConfirm) {
        // Create temporary modal
        const id = 'traj-confirm-' + Date.now();
        const html = `
            <div class="traj-modal-overlay" id="${id}">
                <div class="traj-modal small">
                    <div class="traj-modal-header">
                        <h3 class="traj-modal-title">${title}</h3>
                    </div>
                    <div class="traj-modal-body">
                        <p>${message}</p>
                    </div>
                    <div class="traj-modal-footer">
                        <button class="traj-button" data-action="cancel">Cancel</button>
                        <button class="traj-button primary" data-action="confirm">Confirm</button>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', html);
        const overlay = document.getElementById(id);

        overlay.querySelector('[data-action="cancel"]').onclick = () => {
            this.close(id);
            setTimeout(() => overlay.remove(), 200);
        };

        overlay.querySelector('[data-action="confirm"]').onclick = () => {
            this.close(id);
            setTimeout(() => overlay.remove(), 200);
            if (onConfirm) onConfirm();
        };

        this.open(id);
    }
};
```

---

## 8. TRAJTOAST

Notification toast component.

### HTML Structure

```html
<!-- Toast Container (add to body) -->
<div class="traj-toast-container" id="toastContainer"></div>
```

### CSS

```css
/* ========== TRAJTOAST ========== */

.traj-toast-container {
    position: fixed;
    bottom: 24px;
    right: 24px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    z-index: 9999;
    pointer-events: none;
}

.traj-toast {
    display: flex;
    align-items: flex-start;
    gap: 12px;

    min-width: 280px;
    max-width: 400px;
    padding: 12px 16px;

    background: #2d2d2d;
    border: 1px solid #3a3a3a;
    border-left: 4px solid #0066CC;
    border-radius: 4px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);

    pointer-events: auto;
    animation: traj-toast-enter 0.3s ease-out;
}

@keyframes traj-toast-enter {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

.traj-toast.exiting {
    animation: traj-toast-exit 0.2s ease-in forwards;
}

@keyframes traj-toast-exit {
    from {
        transform: translateX(0);
        opacity: 1;
    }
    to {
        transform: translateX(100%);
        opacity: 0;
    }
}

.traj-toast.success { border-left-color: #00AA00; }
.traj-toast.warning { border-left-color: #FF8800; }
.traj-toast.error { border-left-color: #CC0000; }

.traj-toast-icon {
    font-size: 18px;
    line-height: 1;
}

.traj-toast.info .traj-toast-icon { color: #0066CC; }
.traj-toast.success .traj-toast-icon { color: #00AA00; }
.traj-toast.warning .traj-toast-icon { color: #FF8800; }
.traj-toast.error .traj-toast-icon { color: #CC0000; }

.traj-toast-content {
    flex: 1;
}

.traj-toast-title {
    font-size: 13px;
    font-weight: 600;
    color: #FFFFFF;
    margin-bottom: 2px;
}

.traj-toast-message {
    font-size: 12px;
    color: #A0A0A0;
}

.traj-toast-close {
    color: #808080;
    background: transparent;
    border: none;
    font-size: 16px;
    cursor: pointer;
    padding: 0;
    line-height: 1;
}

.traj-toast-close:hover {
    color: #FFFFFF;
}
```

### JavaScript Behavior

```javascript
const TrajToast = {
    container: null,
    defaultDuration: 4000,

    init() {
        if (!this.container) {
            this.container = document.getElementById('toastContainer');
            if (!this.container) {
                this.container = document.createElement('div');
                this.container.id = 'toastContainer';
                this.container.className = 'traj-toast-container';
                document.body.appendChild(this.container);
            }
        }
    },

    show(options) {
        this.init();

        const {
            title = '',
            message,
            type = 'info',
            duration = this.defaultDuration
        } = typeof options === 'string' ? { message: options } : options;

        const icons = {
            info: 'ℹ',
            success: '✓',
            warning: '⚠',
            error: '✕'
        };

        const toast = document.createElement('div');
        toast.className = `traj-toast ${type}`;
        toast.innerHTML = `
            <span class="traj-toast-icon">${icons[type]}</span>
            <div class="traj-toast-content">
                ${title ? `<div class="traj-toast-title">${title}</div>` : ''}
                <div class="traj-toast-message">${message}</div>
            </div>
            <button class="traj-toast-close">&times;</button>
        `;

        toast.querySelector('.traj-toast-close').onclick = () => this.dismiss(toast);

        this.container.appendChild(toast);

        if (duration > 0) {
            setTimeout(() => this.dismiss(toast), duration);
        }

        return toast;
    },

    dismiss(toast) {
        toast.classList.add('exiting');
        setTimeout(() => toast.remove(), 200);
    },

    info(message, title) {
        return this.show({ message, title, type: 'info' });
    },

    success(message, title) {
        return this.show({ message, title, type: 'success' });
    },

    warning(message, title) {
        return this.show({ message, title, type: 'warning' });
    },

    error(message, title) {
        return this.show({ message, title, type: 'error' });
    }
};
```

### Usage Example

```javascript
TrajToast.success('File uploaded successfully');
TrajToast.error('Failed to save changes', 'Error');
TrajToast.warning('Session expires in 5 minutes');
TrajToast.info('New version available');
```

---

## 9-12. ADDITIONAL COMPONENTS

### 9. TrajInput

```css
.traj-input {
    width: 100%;
    padding: 8px 12px;
    font-family: inherit;
    font-size: 13px;
    color: #C0C0C0;
    background: #252525;
    border: 1px solid #3a3a3a;
    border-radius: 2px;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.traj-input:hover { border-color: #505050; }
.traj-input:focus {
    outline: none;
    border-color: #0066CC;
    box-shadow: 0 0 0 2px rgba(0, 102, 204, 0.2);
}
.traj-input:disabled {
    background: #1a1a1a;
    color: #606060;
    cursor: not-allowed;
}
```

### 10. TrajSelect

```css
.traj-select {
    appearance: none;
    padding-right: 36px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23C0C0C0' d='M6 8L2 4h8z'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 12px center;
}
```

### 11. TrajTable

```css
.traj-table {
    width: 100%;
    border-collapse: collapse;
}
.traj-table th {
    padding: 10px 12px;
    text-align: left;
    font-weight: 600;
    color: #C0C0C0;
    background: #2d2d2d;
    border-bottom: 2px solid #0066CC;
}
.traj-table td {
    padding: 10px 12px;
    border-bottom: 1px solid #3a3a3a;
}
.traj-table tr:hover { background: #252525; }
```

### 12. TrajSpinner

```css
@keyframes traj-spin {
    to { transform: rotate(360deg); }
}
.traj-spinner {
    width: 24px;
    height: 24px;
    border: 3px solid #3a3a3a;
    border-top-color: #0066CC;
    border-radius: 50%;
    animation: traj-spin 1s linear infinite;
}
.traj-spinner.small { width: 16px; height: 16px; border-width: 2px; }
.traj-spinner.large { width: 40px; height: 40px; border-width: 4px; }
```

---

**Document Version:** 1.0
**Created:** January 2026
**Author:** CU (Claude Code - Support/Verifier)
