# Trajanus Command Center - Style Guide

**Purpose:** Definitive CSS and visual styling reference
**Version:** 1.0
**Last Updated:** 2026-01-17

---

## COLOR PALETTE

### Primary Colors
```css
/* Core Palette - BLACK/SILVER/BLUE */
--bg-base: #0a0a0a;          /* Primary background */
--bg-surface: #0a0a0a;       /* Card backgrounds */
--bg-elevated: #1a1a1a;      /* Elevated surfaces */
--bg-hover: #2a2a2a;         /* Hover states */

--silver: #c0c0c0;           /* Primary text/accents */
--silver-light: #e0e0e0;     /* Highlighted text */
--silver-dark: #a0a0a0;      /* Muted text */

--gold: #00AAFF;             /* Primary accent (legacy name, actually blue) */
--gold-light: #33BBFF;       /* Accent hover */
--gold-dark: #0088CC;        /* Accent pressed */
```

### Semantic Colors
```css
--success: #4ade80;          /* Green - completion, valid */
--info: #60a5fa;             /* Blue - informational */
--warning: #fbbf24;          /* Yellow - caution */
--error: #f87171;            /* Red - errors, critical */
```

### Border Colors
```css
--border-subtle: #c0c0c0;    /* Standard borders */
--border-accent: #00AAFF;    /* Emphasized borders */
--border-muted: #4a4a4a;     /* Subtle dividers */
```

---

## TYPOGRAPHY

### Font Stack
```css
/* Primary */
font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;

/* Headers */
font-family: Tahoma, 'Segoe UI', sans-serif;

/* Monospace */
font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
```

### Type Scale
```css
/* Hero Title */
.hero-title {
    font-family: Tahoma, sans-serif;
    font-size: 28px;
    font-weight: 300;
    letter-spacing: 6px;
    color: #00AAFF;
}

/* Section Title */
.section-title {
    font-size: 13px;
    font-weight: 600;
    color: #00AAFF;
    text-transform: uppercase;
    letter-spacing: 2px;
}

/* Card Title */
.card-title {
    font-size: 14px;
    font-weight: 500;
    color: #c0c0c0;
}

/* Body Text */
.body-text {
    font-size: 13px;
    color: #c0c0c0;
    line-height: 1.5;
}

/* Label */
.label {
    font-size: 11px;
    font-weight: 600;
    color: #00AAFF;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Muted Text */
.muted {
    font-size: 12px;
    color: #808080;
}
```

---

## BUTTON SPECIFICATIONS

### External Program Buttons (.ext-btn)
```css
.ext-btn {
    width: 120px;
    height: 44px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.8rem;
    font-weight: 600;
    color: #C0C0C0;
    background: #0d0d0d;
    transition: all 0.2s ease;

    /* V2 Synapse Neural Glow */
    box-shadow:
        0 0 0 1px rgba(0, 170, 255, 0.5),
        0 0 0 3px #0a0a0a,
        0 0 15px rgba(0, 170, 255, 0.15),
        inset 0 0 20px rgba(0, 170, 255, 0.03);
    text-shadow: 0 0 8px rgba(0, 170, 255, 0.5);
}

.ext-btn:hover {
    box-shadow:
        0 0 0 1px rgba(0, 170, 255, 0.8),
        0 0 0 3px #0a0a0a,
        0 0 25px rgba(0, 170, 255, 0.3),
        inset 0 0 30px rgba(0, 170, 255, 0.05);
    text-shadow: 0 0 12px rgba(0, 170, 255, 0.8);
    transform: translateY(-1px);
}

.ext-btn:active {
    box-shadow:
        0 0 0 1px rgba(255, 140, 0, 0.8),
        0 0 0 3px #0a0a0a,
        0 0 20px rgba(255, 140, 0, 0.3),
        inset 0 0 25px rgba(255, 140, 0, 0.05);
    text-shadow: 0 0 10px rgba(255, 140, 0, 0.6);
    transform: translateY(1px);
}
```

### Script Buttons (.script-btn)
```css
.script-btn {
    width: 160px;
    height: 50px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.8px;
    color: #00AAFF;
    background: #0a0a0a;

    /* Double-ring neural glow */
    box-shadow:
        0 0 0 1px rgba(0, 170, 255, 0.5),
        0 0 0 3px #0a0a0a,
        0 0 0 4px rgba(0, 170, 255, 0.3),
        0 0 15px rgba(0, 170, 255, 0.2),
        inset 0 0 30px rgba(0, 170, 255, 0.03);
    text-shadow: 0 0 8px rgba(0, 170, 255, 0.5);
    transition: all 0.25s ease;
}

.script-btn:hover {
    transform: translateY(-2px);
    color: #fff;
    box-shadow:
        0 0 0 1px rgba(0, 170, 255, 0.8),
        0 0 0 3px #0a0a0a,
        0 0 0 4px rgba(0, 170, 255, 0.5),
        0 0 25px rgba(0, 170, 255, 0.4),
        0 0 50px rgba(0, 170, 255, 0.15),
        inset 0 0 40px rgba(0, 170, 255, 0.05);
    text-shadow: 0 0 15px rgba(0, 170, 255, 0.9);
}

.script-btn:active {
    transform: translateY(1px);
    color: #FFB347;
    box-shadow:
        0 0 0 1px rgba(255, 149, 0, 0.8),
        0 0 0 3px #0a0a0a,
        0 0 0 4px rgba(255, 149, 0, 0.4),
        0 0 20px rgba(255, 149, 0, 0.3),
        inset 0 0 30px rgba(255, 149, 0, 0.05);
    text-shadow: 0 0 10px rgba(255, 149, 0, 0.7);
}
```

### Navigation Buttons (.nav-btn)
```css
.nav-btn {
    width: 140px;
    height: 44px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.85rem;
    font-weight: 600;
    transition: all 0.15s ease;
    border: 1px solid #6a6a6a;
    color: #C0C0C0;
    background: linear-gradient(145deg, #5a5a5a, #3a3a3a);
    box-shadow: 0 3px 0 #2a2a2a, 0 4px 8px rgba(0,0,0,0.3);
}

.nav-btn:hover {
    transform: translateY(-2px);
    color: #ffffff;
    filter: brightness(1.15);
}

.nav-btn:active {
    transform: translateY(2px);
    box-shadow: 0 1px 0 #2a2a2a, 0 1px 4px rgba(0,0,0,0.3);
}
```

### Action Buttons (.action-btn)
```css
.action-btn {
    padding: 12px 24px;
    background: linear-gradient(145deg, #00BBFF, #0088CC);
    border: 1px solid #00CCFF;
    color: #ffffff;
    font-size: 14px;
    font-weight: 600;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.15s ease;
    box-shadow: 0 3px 0 #005588, 0 4px 8px rgba(0, 0, 0, 0.3);
}

.action-btn:hover {
    background: linear-gradient(145deg, #33CCFF, #00AAFF);
    box-shadow: 0 2px 0 #005588, 0 3px 6px rgba(0, 0, 0, 0.3);
    transform: translateY(1px);
}

.action-btn:active {
    transform: translateY(3px);
    box-shadow: 0 0 0 #005588, 0 1px 3px rgba(0, 0, 0, 0.3);
}
```

---

## CARD STYLES

### Standard Card
```css
.card {
    padding: 16px;
    background: #0a0a0a;
    border: 1px solid #4a90d9;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
}

.card:hover {
    background: #2a2a2a;
    border-color: #6ab0f9;
    transform: translateY(-2px);
}
```

### Agent Card
```css
.agent-card {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 16px;
    background: #0a0a0a;
    border: 1px solid #4a90d9;
    border-radius: 8px;
}
```

---

## SECTION DIVIDERS

```css
.section-divider {
    display: flex;
    align-items: center;
    gap: 16px;
    margin: 32px 0 20px 0;
}

.section-title {
    font-size: 13px;
    font-weight: 600;
    color: #00AAFF;
    text-transform: uppercase;
    letter-spacing: 2px;
    white-space: nowrap;
}

.section-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #00AAFF 0%, transparent 100%);
}
```

---

## CHAT MESSAGE STYLES

```css
/* Assistant Messages */
.chat-message.assistant {
    background: rgba(0, 170, 255, 0.1);
    border-left: 3px solid #00AAFF;
    color: #00AAFF;
    font-family: Tahoma, sans-serif;
    margin-right: 15%;
    padding: 12px 16px;
    border-radius: 8px;
}

/* User Messages */
.chat-message.user {
    background: rgba(46, 204, 113, 0.15);
    border: 1px solid rgba(46, 204, 113, 0.3);
    color: #2ECC71;
    font-family: Arial, sans-serif;
    margin-left: 15%;
    padding: 12px 16px;
    border-radius: 8px;
}
```

---

## FORM ELEMENTS

```css
.form-input, .form-select {
    width: 100%;
    padding: 10px 12px;
    background: #0a0a0a;
    border: 1px solid #4a90d9;
    border-radius: 6px;
    color: #c0c0c0;
    font-size: 14px;
}

.form-input:focus, .form-select:focus {
    outline: none;
    border-color: #6ab0f9;
}

.form-input::placeholder {
    color: #808080;
}
```

---

## TERMINAL STYLING

```css
.terminal-output {
    background: #0a0a0a;
    border: 1px solid #4a4a4a;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 12px;
    padding: 12px;
    overflow-y: auto;
}

.terminal-line.success { color: #4ade80; }
.terminal-line.error { color: #f87171; }
.terminal-line.info { color: #60a5fa; }
.terminal-line.warning { color: #fbbf24; }
```

---

## ANIMATIONS

### Standard Transitions
```css
transition: all 0.15s ease;      /* Quick UI feedback */
transition: all 0.2s ease;       /* Standard interactions */
transition: all 0.25s ease;      /* Emphasized effects */
transition: all 0.3s ease;       /* Smooth transitions */
```

### Slide In (Notifications)
```css
@keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}
```

### Fade In (Modals)
```css
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
```

### Typing Indicator
```css
@keyframes typing {
    0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
    30% { transform: translateY(-4px); opacity: 1; }
}
```

---

## SPACING SCALE

```css
--space-xs: 4px;
--space-sm: 8px;
--space-md: 12px;
--space-lg: 16px;
--space-xl: 24px;
--space-2xl: 32px;
```

---

## BORDER RADIUS SCALE

```css
--radius-sm: 4px;    /* Buttons, small elements */
--radius-md: 6px;    /* Inputs, cards */
--radius-lg: 8px;    /* Large cards, modals */
--radius-xl: 10px;   /* Featured elements */
```

---

## Z-INDEX SCALE

```css
--z-base: 0;
--z-dropdown: 100;
--z-sticky: 1000;
--z-modal: 10000;
--z-notification: 9999;
```

---

## RESPONSIVE BREAKPOINTS

```css
/* Mobile */
@media (max-width: 480px) { }

/* Tablet */
@media (max-width: 768px) { }

/* Small Desktop */
@media (max-width: 1024px) { }

/* Standard Desktop (target) */
@media (min-width: 1920px) { }
```

---

**Note:** All styles follow the V2 Synapse theme with neural glow effects. Gold color variable is legacy - actual color is bright blue (#00AAFF).

---

## GOOD/BAD EXAMPLES

### Button Implementation

**✅ GOOD:**
```css
/* Correct button sizing with full effect stack */
.ext-btn {
    width: 120px;
    height: 44px;
    background: #0d0d0d;
    border: none;
    border-radius: 4px;
    box-shadow:
        0 0 0 1px rgba(0, 170, 255, 0.5),
        0 0 0 3px #0a0a0a,
        0 0 15px rgba(0, 170, 255, 0.15);
    transition: all 0.2s ease;
}
```

**❌ BAD:**
```css
/* Missing neural glow, wrong colors */
.ext-btn {
    width: 100px;           /* Wrong: not canonical 120px */
    height: 40px;           /* Wrong: not canonical 44px */
    background: #333;       /* Wrong: not #0d0d0d */
    border: 1px solid blue; /* Wrong: should be box-shadow glow */
    border-radius: 8px;     /* Wrong: should be 4px */
}
```

---

### Color Usage

**✅ GOOD:**
```css
/* Correct Trajanus palette */
.header { color: #00AAFF; }           /* Primary blue accent */
.body-text { color: #C0C0C0; }        /* Silver for readability */
.background { background: #0a0a0a; }   /* Deep black */
.success { color: #4ade80; }          /* Green semantic */
```

**❌ BAD:**
```css
/* Wrong colors */
.header { color: #FFD700; }           /* Gold - FORBIDDEN */
.header { color: #0066CC; }           /* Wrong blue shade */
.body-text { color: #ffffff; }        /* Too harsh - use silver */
.background { background: #000000; }   /* Too stark - use #0a0a0a */
```

---

### Typography

**✅ GOOD:**
```css
/* Correct hierarchy and fonts */
.hero-title {
    font-family: Tahoma, sans-serif;
    font-size: 28px;
    font-weight: 300;
    letter-spacing: 6px;
    color: #00AAFF;
    text-transform: uppercase;
}

.section-title {
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2px;
}
```

**❌ BAD:**
```css
/* Wrong fonts and sizing */
.hero-title {
    font-family: Arial, sans-serif;   /* Wrong: should be Tahoma */
    font-size: 32px;                  /* Wrong: should be 28px */
    font-weight: bold;                /* Wrong: should be 300 */
    text-decoration: underline;       /* Never underline titles */
}

.section-title {
    font-size: 16px;                  /* Too large: should be 13px */
    text-transform: none;             /* Should be uppercase */
}
```

---

### Card Layout

**✅ GOOD:**
```css
/* Correct card structure */
.card {
    padding: 16px;
    background: #0a0a0a;
    border: 1px solid #4a90d9;        /* Blue border */
    border-radius: 8px;
    transition: all 0.2s;
}

.card:hover {
    background: #2a2a2a;
    border-color: #6ab0f9;            /* Lighter blue on hover */
    transform: translateY(-2px);       /* Subtle lift */
}
```

**❌ BAD:**
```css
/* Wrong card implementation */
.card {
    padding: 8px;                     /* Too tight */
    background: #1a1a1a;              /* Should be #0a0a0a */
    border: 2px solid #00AAFF;        /* Too thick, wrong color */
    border-radius: 12px;              /* Should be 8px */
}

.card:hover {
    background: #00AAFF;              /* Never fill with accent */
    transform: scale(1.1);            /* Don't scale, use translateY */
}
```

---

### Spacing

**✅ GOOD:**
```css
/* Consistent spacing scale */
.section { margin: 32px 0; }          /* Generous section gaps */
.card-grid { gap: 16px; }             /* Comfortable card gaps */
.card-content { padding: 12px; }      /* Standard internal padding */
.inline-items { gap: 8px; }           /* Compact inline spacing */
```

**❌ BAD:**
```css
/* Inconsistent arbitrary values */
.section { margin: 27px 0; }          /* Use scale: 24px or 32px */
.card-grid { gap: 15px; }             /* Use scale: 12px or 16px */
.card-content { padding: 10px; }      /* Use scale: 8px or 12px */
```

---

### Hover Effects

**✅ GOOD:**
```css
/* Correct hover with lift and glow */
.button:hover {
    transform: translateY(-2px);       /* Subtle lift */
    box-shadow:
        0 0 0 1px rgba(0, 170, 255, 0.8),
        0 0 25px rgba(0, 170, 255, 0.3);
    text-shadow: 0 0 12px rgba(0, 170, 255, 0.8);
}
```

**❌ BAD:**
```css
/* Wrong hover effects */
.button:hover {
    transform: scale(1.05);            /* Don't scale buttons */
    background: #00AAFF;               /* Don't fill with accent */
    border: 2px solid white;           /* Jarring color change */
}
```

---

### Active/Pressed States

**✅ GOOD:**
```css
/* Correct press feedback with orange accent */
.button:active {
    transform: translateY(1px);        /* Press down */
    box-shadow:
        0 0 0 1px rgba(255, 149, 0, 0.8),
        0 0 20px rgba(255, 149, 0, 0.3);
    text-shadow: 0 0 10px rgba(255, 149, 0, 0.7);
}
```

**❌ BAD:**
```css
/* Wrong press state */
.button:active {
    transform: translateY(-4px);       /* Should press DOWN */
    background: #00AAFF;               /* Don't change background */
    opacity: 0.5;                      /* Never reduce opacity */
}
```

---

### Form Inputs

**✅ GOOD:**
```css
/* Correct input styling */
.form-input {
    width: 100%;
    padding: 10px 12px;
    background: #0a0a0a;
    border: 1px solid #4a90d9;
    border-radius: 6px;
    color: #c0c0c0;
    font-size: 14px;
}

.form-input:focus {
    outline: none;
    border-color: #6ab0f9;
}
```

**❌ BAD:**
```css
/* Wrong input styling */
.form-input {
    background: white;                 /* Should be dark */
    border: none;                      /* Needs visible border */
    color: black;                      /* Should be silver */
}

.form-input:focus {
    outline: 2px solid blue;           /* Use border-color change */
    box-shadow: 0 0 10px blue;         /* Too aggressive */
}
```

---

## VISUAL REFERENCE

**Screenshots available in:** `.playwright-mcp/`
- 90+ captured screenshots demonstrating correct implementations
- Use `/verify` command to capture current state
- Compare against existing screenshots for consistency

**Component Verification:**
1. Run Trajanus Command Center
2. Navigate to target workspace
3. Execute: `mcp__plugin_playwright_playwright__browser_take_screenshot`
4. Compare against style guide CSS specifications

---

**Version:** 1.1
**Updated:** 2026-01-18
**Added:** Good/bad examples section, visual reference guide
