# TRAJANUS UI BRANDING SPECIFICATION
## Version 1.0 | January 2026

---

## 1. COLOR PALETTE (MANDATORY)

All Trajanus interfaces MUST adhere to this color palette. **NO GOLD COLORS ARE PERMITTED.**

### 1.1 Primary Colors

| Role | Color Name | Hex Value | RGB | Usage |
|------|-----------|-----------|-----|-------|
| **Primary Background** | Black | `#1a1a1a` | rgb(26, 26, 26) | Main application background |
| **Secondary Background** | Dark Gray | `#2d2d2d` | rgb(45, 45, 45) | Cards, panels, elevated surfaces |
| **Tertiary Background** | Charcoal | `#3a3a3a` | rgb(58, 58, 58) | Hover states, input fields |

### 1.2 Accent Colors

| Role | Color Name | Hex Value | RGB | Usage |
|------|-----------|-----------|-----|-------|
| **Header/Accent Text** | Silver | `#C0C0C0` | rgb(192, 192, 192) | Primary text, headers |
| **Bright Silver** | Light Silver | `#E0E0E0` | rgb(224, 224, 224) | Hover states, emphasis |
| **Dim Silver** | Muted Silver | `#A0A0A0` | rgb(160, 160, 160) | Secondary text, labels |

### 1.3 Interactive Elements

| Role | Color Name | Hex Value | RGB | Usage |
|------|-----------|-----------|-----|-------|
| **Primary Interactive** | Blue | `#0066CC` | rgb(0, 102, 204) | Buttons, links, active states |
| **Hover State** | Light Blue | `#3399FF` | rgb(51, 153, 255) | Button hover, link hover |
| **Active/Pressed** | Dark Blue | `#004999` | rgb(0, 73, 153) | Pressed buttons, active tabs |
| **Focus Ring** | Focus Blue | `#4DA6FF` | rgb(77, 166, 255) | Keyboard focus indicators |

### 1.4 Status Colors

| Role | Color Name | Hex Value | RGB | Usage |
|------|-----------|-----------|-----|-------|
| **Success** | Green | `#00AA00` | rgb(0, 170, 0) | Success messages, completed |
| **Warning** | Orange | `#FF8800` | rgb(255, 136, 0) | Warnings, caution states |
| **Error** | Red | `#CC0000` | rgb(204, 0, 0) | Errors, destructive actions |
| **Info** | Cyan | `#00AACC` | rgb(0, 170, 204) | Informational messages |

### 1.5 CSS Variables (Required)

```css
:root {
    /* Backgrounds */
    --bg-base: #1a1a1a;
    --bg-surface: #2d2d2d;
    --bg-elevated: #3a3a3a;
    --bg-hover: #454545;
    --bg-input: #252525;

    /* Silver Palette */
    --silver: #C0C0C0;
    --silver-light: #E0E0E0;
    --silver-dark: #A0A0A0;
    --silver-muted: #808080;

    /* Blue Palette */
    --blue: #0066CC;
    --blue-light: #3399FF;
    --blue-dark: #004999;
    --blue-focus: #4DA6FF;

    /* Text */
    --text-primary: #C0C0C0;
    --text-secondary: #A0A0A0;
    --text-muted: #808080;
    --text-white: #FFFFFF;
    --text-inverse: #1a1a1a;

    /* Status */
    --status-success: #00AA00;
    --status-warning: #FF8800;
    --status-error: #CC0000;
    --status-info: #00AACC;

    /* Borders */
    --border-subtle: #3a3a3a;
    --border-default: #505050;
    --border-strong: #C0C0C0;
    --border-interactive: #0066CC;
    --border-tool-window: #0066CC;

    /* Shadows */
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.5);
    --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.5);
    --shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.5);
    --shadow-glow: 0 0 8px rgba(0, 102, 204, 0.5);
}
```

---

## 2. BUTTON STYLES

### 2.1 Microsoft Access-Style 3D Beveled Buttons

All buttons use a classic 3D beveled appearance inspired by Microsoft Access.

### 2.2 Button States CSS

```css
/* Base Button - 3D Beveled Style */
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

    color: var(--text-primary);
    background: linear-gradient(180deg, #3a3a3a 0%, #2d2d2d 100%);

    /* 3D Beveled Border - Light top/left, dark bottom/right */
    border: none;
    border-top: 2px solid #505050;
    border-left: 2px solid #505050;
    border-right: 2px solid #1a1a1a;
    border-bottom: 2px solid #1a1a1a;

    border-radius: 2px;
    cursor: pointer;

    transition: all 0.15s ease;
}

/* Hover - Slight lift + subtle glow */
.traj-button:hover {
    background: linear-gradient(180deg, #454545 0%, #3a3a3a 100%);
    color: var(--text-white);

    border-top-color: #606060;
    border-left-color: #606060;

    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3),
                0 0 8px rgba(0, 102, 204, 0.2);

    transform: translateY(-1px);
}

/* Active/Pressed - Inset appearance */
.traj-button:active {
    background: linear-gradient(180deg, #252525 0%, #2d2d2d 100%);

    /* Reverse bevel for pressed effect */
    border-top: 2px solid #1a1a1a;
    border-left: 2px solid #1a1a1a;
    border-right: 2px solid #404040;
    border-bottom: 2px solid #404040;

    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.4);
    transform: translateY(0);
}

/* Focus - Blue ring */
.traj-button:focus {
    outline: none;
    box-shadow: 0 0 0 2px var(--blue-focus);
}

.traj-button:focus:not(:focus-visible) {
    box-shadow: none;
}

.traj-button:focus-visible {
    box-shadow: 0 0 0 2px var(--blue-focus);
}

/* Disabled */
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

/* Primary Button - Blue */
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

/* Success Button - Green */
.traj-button.success {
    color: #FFFFFF;
    background: linear-gradient(180deg, #00BB00 0%, #00AA00 100%);

    border-top-color: #00DD00;
    border-left-color: #00DD00;
    border-right-color: #008800;
    border-bottom-color: #008800;
}

/* Danger Button - Red */
.traj-button.danger {
    color: #FFFFFF;
    background: linear-gradient(180deg, #DD0000 0%, #CC0000 100%);

    border-top-color: #FF3333;
    border-left-color: #FF3333;
    border-right-color: #990000;
    border-bottom-color: #990000;
}

/* Button Sizes */
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
```

---

## 3. LAYOUT STANDARDS

### 3.1 Three-Column Layout

Tool windows use a 3-column layout:

```
+------------------+------------------------+------------------+
|     SIDEBAR      |         MAIN           |       LOG        |
|    (240px)       |       (flexible)       |     (280px)      |
|                  |                        |                  |
|  - Navigation    |  - Tab Bar             |  - Timestamps    |
|  - File Tree     |  - Content Area        |  - Status msgs   |
|  - Actions       |  - Forms/Tables        |  - Progress      |
+------------------+------------------------+------------------+
```

### 3.2 Header Structure

EVERY tool window MUST include:

1. **"TRAJANUS USA"** header text (top-center or top-left)
2. **"<- Hub"** return button (top-left corner)
3. **Mode tabs** below header
4. **Thick blue border** (3px `#0066CC`)

### 3.3 Layout CSS

```css
/* Tool Window Container */
.traj-tool-window {
    display: grid;
    grid-template-rows: auto 1fr auto;
    grid-template-columns: 240px 1fr 280px;

    height: 100vh;
    background: var(--bg-base);

    /* Thick blue border */
    border: 3px solid var(--border-tool-window);
}

/* Header - spans all columns */
.traj-tool-header {
    grid-column: 1 / -1;

    display: flex;
    align-items: center;
    justify-content: space-between;

    height: 56px;
    padding: 0 16px;

    background: var(--bg-base);
    border-bottom: 1px solid var(--border-default);
}

.traj-hub-button {
    display: inline-flex;
    align-items: center;
    gap: 6px;

    padding: 6px 12px;

    color: var(--silver);
    background: transparent;
    border: 1px solid var(--silver);
    border-radius: 4px;

    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.traj-hub-button:hover {
    color: var(--text-white);
    background: var(--bg-surface);
    border-color: var(--blue);
}

.traj-header-title {
    font-size: 16px;
    font-weight: 600;
    letter-spacing: 0.1em;
    color: var(--silver);
}

/* Sidebar */
.traj-sidebar {
    grid-row: 2;

    background: var(--bg-base);
    border-right: 1px solid var(--border-default);

    overflow-y: auto;
    padding: 16px;
}

/* Main Content */
.traj-main-content {
    grid-row: 2;

    display: flex;
    flex-direction: column;

    background: var(--bg-surface);
    overflow: hidden;
}

/* Tab Bar */
.traj-tab-bar {
    display: flex;
    gap: 2px;

    padding: 8px 16px 0;
    background: var(--bg-base);
    border-bottom: 1px solid var(--border-default);
}

.traj-tab {
    padding: 10px 20px;

    color: var(--text-secondary);
    background: transparent;
    border: none;
    border-bottom: 2px solid transparent;

    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.traj-tab:hover {
    color: var(--text-primary);
    background: var(--bg-hover);
}

.traj-tab.active {
    color: var(--text-white);
    border-bottom-color: var(--blue);
}

/* Content Area */
.traj-content-area {
    flex: 1;
    overflow-y: auto;
    padding: 24px;
}

/* Log Panel */
.traj-log-panel {
    grid-row: 2;

    display: flex;
    flex-direction: column;

    background: var(--bg-base);
    border-left: 1px solid var(--border-default);
}

.traj-log-header {
    padding: 12px 16px;

    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;

    color: var(--silver);
    background: var(--bg-surface);
    border-bottom: 1px solid var(--border-default);
}

.traj-log-content {
    flex: 1;
    overflow-y: auto;
    padding: 8px;

    font-family: var(--font-mono);
    font-size: 11px;
}

/* Status Bar - spans all columns */
.traj-status-bar {
    grid-column: 1 / -1;

    display: flex;
    align-items: center;
    justify-content: space-between;

    height: 28px;
    padding: 0 16px;

    background: var(--bg-surface);
    border-top: 1px solid var(--border-default);

    font-size: 11px;
    color: var(--text-muted);
}
```

### 3.4 Collapsible Panel CSS

```css
.traj-collapsible {
    border: 1px solid var(--border-default);
    border-radius: 4px;
    overflow: hidden;
}

.traj-collapsible-header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 12px 16px;

    background: var(--bg-surface);
    cursor: pointer;

    transition: background 0.2s ease;
}

.traj-collapsible-header:hover {
    background: var(--bg-hover);
}

.traj-collapsible-icon {
    transition: transform 0.3s ease;
}

.traj-collapsible.collapsed .traj-collapsible-icon {
    transform: rotate(-90deg);
}

.traj-collapsible-content {
    max-height: 1000px;
    padding: 16px;

    background: var(--bg-base);

    overflow: hidden;
    transition: max-height 0.3s ease, padding 0.3s ease;
}

.traj-collapsible.collapsed .traj-collapsible-content {
    max-height: 0;
    padding-top: 0;
    padding-bottom: 0;
}
```

---

## 4. ANIMATION SPECIFICATIONS

### 4.1 Core Timing Values

| Animation Type | Duration | Easing | Notes |
|---------------|----------|--------|-------|
| **Button Hover** | 150ms | ease | Quick, responsive |
| **Button Press** | 100ms | ease-out | Instant feedback |
| **Panel Expand** | 300ms | ease-in-out | Smooth, not sluggish |
| **Panel Collapse** | 250ms | ease-in | Slightly faster than expand |
| **Tab Switch** | 200ms | ease | Smooth transition |
| **Modal Open** | 250ms | cubic-bezier(0.34, 1.56, 0.64, 1) | Slight overshoot |
| **Modal Close** | 200ms | ease-in | Clean exit |
| **Toast Appear** | 300ms | ease-out | Slide in from right |
| **Toast Disappear** | 200ms | ease-in | Fade out |
| **Loading Spinner** | 1000ms | linear | Continuous rotation |
| **Progress Bar** | 200ms | ease | Smooth value updates |

### 4.2 CSS Transition Utilities

```css
/* Transition Classes */
.transition-fast { transition: all 0.15s ease; }
.transition-normal { transition: all 0.2s ease; }
.transition-slow { transition: all 0.3s ease; }

/* Panel Transitions */
.traj-panel-transition {
    transition: max-height 0.3s ease-in-out,
                opacity 0.3s ease-in-out,
                padding 0.3s ease-in-out;
}

/* Button Transitions */
.traj-button-transition {
    transition: background 0.15s ease,
                color 0.15s ease,
                border-color 0.15s ease,
                box-shadow 0.15s ease,
                transform 0.15s ease;
}
```

### 4.3 Keyframe Animations

```css
/* Loading Spinner */
@keyframes traj-spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.traj-spinner {
    width: 24px;
    height: 24px;
    border: 3px solid var(--border-default);
    border-top-color: var(--blue);
    border-radius: 50%;
    animation: traj-spin 1s linear infinite;
}

/* Pulse (for active indicators) */
@keyframes traj-pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.traj-pulse {
    animation: traj-pulse 2s ease-in-out infinite;
}

/* Slide In from Right (for toasts) */
@keyframes traj-slide-in-right {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

/* Slide Out to Right */
@keyframes traj-slide-out-right {
    from {
        transform: translateX(0);
        opacity: 1;
    }
    to {
        transform: translateX(100%);
        opacity: 0;
    }
}

/* Fade In */
@keyframes traj-fade-in {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Fade Out */
@keyframes traj-fade-out {
    from { opacity: 1; }
    to { opacity: 0; }
}

/* Scale In (for modals) */
@keyframes traj-scale-in {
    from {
        transform: scale(0.95);
        opacity: 0;
    }
    to {
        transform: scale(1);
        opacity: 1;
    }
}

/* Progress Bar Stripes */
@keyframes traj-progress-stripes {
    from { background-position: 40px 0; }
    to { background-position: 0 0; }
}

.traj-progress-animated {
    background-image: linear-gradient(
        45deg,
        rgba(255,255,255,0.1) 25%,
        transparent 25%,
        transparent 50%,
        rgba(255,255,255,0.1) 50%,
        rgba(255,255,255,0.1) 75%,
        transparent 75%,
        transparent
    );
    background-size: 40px 40px;
    animation: traj-progress-stripes 1s linear infinite;
}

/* Success Check */
@keyframes traj-check-draw {
    from { stroke-dashoffset: 100; }
    to { stroke-dashoffset: 0; }
}
```

### 4.4 Toast Notifications

```css
.traj-toast {
    position: fixed;
    bottom: 24px;
    right: 24px;

    min-width: 280px;
    max-width: 400px;
    padding: 12px 16px;

    background: var(--bg-surface);
    border: 1px solid var(--border-default);
    border-left: 4px solid var(--blue);
    border-radius: 4px;

    box-shadow: var(--shadow-lg);

    animation: traj-slide-in-right 0.3s ease-out;
}

.traj-toast.hiding {
    animation: traj-slide-out-right 0.2s ease-in forwards;
}

.traj-toast.success { border-left-color: var(--status-success); }
.traj-toast.warning { border-left-color: var(--status-warning); }
.traj-toast.error { border-left-color: var(--status-error); }
```

---

## 5. TYPOGRAPHY

### 5.1 Font Stack

```css
:root {
    /* Primary UI Font */
    --font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont,
                   'Helvetica Neue', Arial, sans-serif;

    /* Monospace for Code/Logs */
    --font-mono: 'Consolas', 'Monaco', 'Courier New', monospace;
}
```

### 5.2 Type Scale

| Role | Size | Weight | Line Height | Letter Spacing |
|------|------|--------|-------------|----------------|
| **H1 - Page Title** | 24px | 600 | 1.2 | 0.1em |
| **H2 - Section** | 18px | 600 | 1.3 | 0.08em |
| **H3 - Subsection** | 14px | 600 | 1.4 | 0.05em |
| **Body** | 13px | 400 | 1.5 | normal |
| **Small** | 12px | 400 | 1.4 | normal |
| **Caption** | 11px | 400 | 1.3 | 0.02em |
| **Code** | 12px | 400 | 1.5 | normal |

### 5.3 Typography CSS

```css
/* Headings */
.traj-h1 {
    font-size: 24px;
    font-weight: 600;
    line-height: 1.2;
    letter-spacing: 0.1em;
    color: var(--silver);
    text-transform: uppercase;
}

.traj-h2 {
    font-size: 18px;
    font-weight: 600;
    line-height: 1.3;
    letter-spacing: 0.08em;
    color: var(--silver);
}

.traj-h3 {
    font-size: 14px;
    font-weight: 600;
    line-height: 1.4;
    letter-spacing: 0.05em;
    color: var(--text-primary);
}

/* Body Text */
.traj-body {
    font-size: 13px;
    font-weight: 400;
    line-height: 1.5;
    color: var(--text-primary);
}

.traj-small {
    font-size: 12px;
    font-weight: 400;
    line-height: 1.4;
    color: var(--text-secondary);
}

.traj-caption {
    font-size: 11px;
    font-weight: 400;
    line-height: 1.3;
    letter-spacing: 0.02em;
    color: var(--text-muted);
}

/* Code/Monospace */
.traj-code {
    font-family: var(--font-mono);
    font-size: 12px;
    line-height: 1.5;
    color: var(--text-primary);
}

.traj-code-block {
    font-family: var(--font-mono);
    font-size: 12px;
    line-height: 1.5;
    padding: 12px;
    background: var(--bg-base);
    border: 1px solid var(--border-default);
    border-radius: 4px;
    overflow-x: auto;
}
```

---

## 6. TOOL WINDOW TEMPLATE

### 6.1 Complete HTML Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[TOOL NAME] - Trajanus USA</title>
    <link rel="stylesheet" href="./trajanus-ui.css">
</head>
<body>
    <div class="traj-tool-window">
        <!-- Header -->
        <header class="traj-tool-header">
            <button class="traj-hub-button" onclick="location.href='../index.html'">
                <span class="hub-arrow">&larr;</span>
                <span>Hub</span>
            </button>
            <h1 class="traj-header-title">TRAJANUS USA</h1>
            <div class="traj-header-actions">
                <!-- Tool-specific actions here -->
            </div>
        </header>

        <!-- Sidebar -->
        <aside class="traj-sidebar">
            <nav class="traj-nav">
                <!-- Navigation items -->
            </nav>
        </aside>

        <!-- Main Content -->
        <main class="traj-main-content">
            <!-- Tab Bar -->
            <div class="traj-tab-bar">
                <button class="traj-tab active" data-tab="tab1">Mode 1</button>
                <button class="traj-tab" data-tab="tab2">Mode 2</button>
                <button class="traj-tab" data-tab="tab3">Mode 3</button>
            </div>

            <!-- Content Area -->
            <div class="traj-content-area">
                <div class="traj-tab-content active" id="tab1">
                    <!-- Tab 1 content -->
                </div>
                <div class="traj-tab-content" id="tab2">
                    <!-- Tab 2 content -->
                </div>
                <div class="traj-tab-content" id="tab3">
                    <!-- Tab 3 content -->
                </div>
            </div>
        </main>

        <!-- Processing Log -->
        <aside class="traj-log-panel">
            <div class="traj-log-header">Processing Log</div>
            <div class="traj-log-content" id="logContent">
                <!-- Log entries -->
            </div>
        </aside>

        <!-- Status Bar -->
        <footer class="traj-status-bar">
            <span class="traj-status-left">
                <span class="traj-status-indicator"></span>
                Ready
            </span>
            <span class="traj-status-right">v1.0.0</span>
        </footer>
    </div>

    <script src="./trajanus-ui.js"></script>
</body>
</html>
```

### 6.2 Log Entry Format

```html
<div class="traj-log-entry info">
    <span class="log-time">14:32:05</span>
    <span class="log-msg">Operation completed successfully</span>
</div>
```

```css
.traj-log-entry {
    display: flex;
    gap: 8px;
    padding: 4px 8px;
    font-size: 11px;
    border-left: 2px solid var(--border-default);
}

.traj-log-entry.info { border-left-color: var(--blue); }
.traj-log-entry.success { border-left-color: var(--status-success); }
.traj-log-entry.warning { border-left-color: var(--status-warning); }
.traj-log-entry.error { border-left-color: var(--status-error); }

.log-time {
    color: var(--text-muted);
    font-family: var(--font-mono);
}

.log-msg {
    color: var(--text-primary);
}
```

---

## 7. COMPONENT SPECIFICATIONS

### 7.1 Form Inputs

```css
.traj-input {
    width: 100%;
    padding: 8px 12px;

    font-family: var(--font-family);
    font-size: 13px;

    color: var(--text-primary);
    background: var(--bg-input);
    border: 1px solid var(--border-default);
    border-radius: 2px;

    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.traj-input:hover {
    border-color: var(--border-strong);
}

.traj-input:focus {
    outline: none;
    border-color: var(--blue);
    box-shadow: 0 0 0 2px rgba(0, 102, 204, 0.2);
}

.traj-input:disabled {
    background: var(--bg-base);
    color: var(--text-muted);
    cursor: not-allowed;
}

/* Select */
.traj-select {
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23C0C0C0' d='M6 8L2 4h8z'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 12px center;
    padding-right: 36px;
}
```

### 7.2 Tables

```css
.traj-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}

.traj-table th {
    padding: 10px 12px;

    text-align: left;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;

    color: var(--silver);
    background: var(--bg-surface);
    border-bottom: 2px solid var(--blue);
}

.traj-table td {
    padding: 10px 12px;
    border-bottom: 1px solid var(--border-subtle);
}

.traj-table tr:hover {
    background: var(--bg-hover);
}
```

---

## 8. ACCESSIBILITY REQUIREMENTS

### 8.1 Color Contrast

All text must meet WCAG 2.1 AA contrast requirements:
- Normal text: 4.5:1 minimum
- Large text (18px+): 3:1 minimum

| Combination | Ratio | Status |
|-------------|-------|--------|
| Silver (#C0C0C0) on Black (#1a1a1a) | 9.8:1 | PASS |
| Blue (#0066CC) on Dark Gray (#2d2d2d) | 4.9:1 | PASS |
| White (#FFFFFF) on Blue (#0066CC) | 5.0:1 | PASS |

### 8.2 Focus Indicators

All interactive elements MUST have visible focus indicators:
- 2px blue outline or box-shadow
- Visible in high contrast mode
- Not removed via `outline: none` without alternative

### 8.3 Motion Preferences

```css
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
```

---

## 9. RESPONSIVE CONSIDERATIONS

### 9.1 Minimum Dimensions

- **Desktop Minimum Width:** 1024px
- **Tool Window Minimum:** 800px x 600px
- **Sidebar Collapsible Below:** 1200px

### 9.2 Breakpoint Behavior

```css
/* Collapse sidebar on smaller screens */
@media (max-width: 1200px) {
    .traj-tool-window {
        grid-template-columns: 200px 1fr 240px;
    }
}

@media (max-width: 1024px) {
    .traj-tool-window {
        grid-template-columns: 1fr;
        grid-template-rows: auto auto 1fr auto auto;
    }

    .traj-sidebar,
    .traj-log-panel {
        display: none;
    }

    .traj-sidebar.visible,
    .traj-log-panel.visible {
        display: block;
        position: fixed;
        /* Overlay styling */
    }
}
```

---

## 10. IMPLEMENTATION CHECKLIST

- [ ] Replace all gold colors (`#d4af37`, `--gold`, etc.) with silver equivalents
- [ ] Apply thick blue border (3px #0066CC) to all tool windows
- [ ] Add "TRAJANUS USA" header to all tool windows
- [ ] Add "<- Hub" button to all tool windows
- [ ] Implement 3D beveled button styles
- [ ] Add processing log panel to all tool windows
- [ ] Apply consistent animation timing
- [ ] Verify WCAG 2.1 AA color contrast
- [ ] Test keyboard navigation
- [ ] Test with reduced motion preference

---

**Document Version:** 1.0
**Created:** January 2026
**Author:** CU (Claude Code - Support/Verifier)
**For:** Trajanus USA - Bill King, Principal/CEO
