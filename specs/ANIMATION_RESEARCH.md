# ANIMATION RESEARCH
## Best Practices for Desktop Application Animations
### Trajanus Enterprise Hub | January 2026

---

## 1. EXECUTIVE SUMMARY

This document provides research-backed recommendations for implementing animations in the Trajanus Enterprise Hub. The goal is to create a **command center aesthetic** that feels professional, military-grade, and responsive—never playful or consumer-oriented.

**Key Principles:**
- Animations should enhance usability, not decorate
- Speed is more important than flourish
- Feedback should feel immediate and deliberate
- Reduce cognitive load, don't add visual noise

---

## 2. ANIMATION TIMING RESEARCH

### 2.1 Optimal Duration Guidelines

Based on research from Material Design, Apple HIG, and Microsoft Fluent Design:

| Animation Type | Optimal Duration | Rationale |
|---------------|-----------------|-----------|
| **Micro-interactions** (hover, focus) | 100-150ms | Below perception threshold; feels instant |
| **State changes** (toggle, checkbox) | 150-200ms | Noticeable but quick |
| **Revealing content** (expand, show) | 200-300ms | Allows eye to track movement |
| **Complex transitions** (page, modal) | 250-400ms | Smooth without being sluggish |
| **Continuous animations** (loading) | 800-1200ms per cycle | Steady, not frantic |

### 2.2 The 100ms Rule

Research shows that:
- **< 100ms**: User perceives as instantaneous
- **100-300ms**: User perceives cause-and-effect
- **300-1000ms**: User perceives as "processing"
- **> 1000ms**: User perceives as slow/broken

**Recommendation for Trajanus:**
Keep most UI animations in the 150-300ms range. Command center tools should feel snappy, not theatrical.

### 2.3 Easing Functions

| Easing | CSS Value | Best For |
|--------|-----------|----------|
| **Ease-out** | `cubic-bezier(0.0, 0.0, 0.2, 1)` | Elements entering (modal open, dropdown show) |
| **Ease-in** | `cubic-bezier(0.4, 0.0, 1, 1)` | Elements exiting (modal close, toast dismiss) |
| **Ease-in-out** | `cubic-bezier(0.4, 0.0, 0.2, 1)` | State transitions (toggle, tab switch) |
| **Linear** | `linear` | Continuous (spinner, progress animation) |

**Custom Easing for Trajanus:**

```css
/* Standard easing - professional, clean */
--ease-standard: cubic-bezier(0.4, 0.0, 0.2, 1);

/* Deceleration - entering elements */
--ease-decelerate: cubic-bezier(0.0, 0.0, 0.2, 1);

/* Acceleration - exiting elements */
--ease-accelerate: cubic-bezier(0.4, 0.0, 1, 1);

/* Sharp - quick state changes */
--ease-sharp: cubic-bezier(0.4, 0.0, 0.6, 1);
```

---

## 3. ACCESSIBILITY CONSIDERATIONS

### 3.1 Reduced Motion

Users may enable "Reduce Motion" in their OS for various reasons:
- Vestibular disorders (motion sickness)
- Cognitive processing differences
- Personal preference

**Required Implementation:**

```css
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
}
```

### 3.2 Safe Animation Practices

**AVOID:**
- Flashing content (seizure risk)
- Large-scale movement (> 1/3 of viewport)
- Parallax effects
- Auto-playing videos
- Infinite loops that can't be paused

**PREFER:**
- Fade transitions over sliding
- Scale from 95-100% rather than 50-100%
- Short durations (< 500ms)
- Single-axis movement when possible

---

## 4. PERFORMANCE OPTIMIZATION

### 4.1 GPU-Accelerated Properties

These CSS properties are GPU-accelerated and performant:
- `transform` (translate, scale, rotate)
- `opacity`

**Avoid animating:**
- `width`, `height` (causes reflow)
- `top`, `left`, `right`, `bottom` (causes reflow)
- `margin`, `padding` (causes reflow)
- `border-width` (causes repaint)
- `box-shadow` (expensive repaint)

### 4.2 Will-Change Optimization

Use `will-change` sparingly for known animated elements:

```css
/* Apply only when element will animate soon */
.will-animate {
    will-change: transform, opacity;
}

/* Remove after animation completes */
.animation-complete {
    will-change: auto;
}
```

### 4.3 RequestAnimationFrame Pattern

For JavaScript animations, always use `requestAnimationFrame`:

```javascript
function animate(element, property, start, end, duration) {
    const startTime = performance.now();

    function frame(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        // Ease-out cubic
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = start + (end - start) * eased;

        element.style[property] = current;

        if (progress < 1) {
            requestAnimationFrame(frame);
        }
    }

    requestAnimationFrame(frame);
}
```

---

## 5. TRAJANUS-SPECIFIC RECOMMENDATIONS

### 5.1 Command Center Aesthetic

The Trajanus Enterprise Hub should feel like:
- A military command console
- An air traffic control interface
- A mission control dashboard

**NOT like:**
- A consumer mobile app
- A social media platform
- A gaming interface

### 5.2 Animation Philosophy

1. **Functional, not decorative** - Every animation serves a purpose
2. **Immediate feedback** - Users know their action was registered
3. **Clear state communication** - Loading, success, error are obvious
4. **Predictable behavior** - No surprises, no "delightful" animations
5. **Respectful of attention** - Nothing moves unless user initiated

### 5.3 Recommended Animations by Component

#### Buttons
```css
.traj-button {
    transition: background 0.15s ease,
                border-color 0.15s ease,
                transform 0.15s ease,
                box-shadow 0.15s ease;
}

.traj-button:hover {
    transform: translateY(-1px);
}

.traj-button:active {
    transform: translateY(0);
    transition-duration: 0.05s; /* Faster on press */
}
```

#### Panels (Expand/Collapse)
```css
.traj-panel-content {
    transition: max-height 0.3s ease-in-out,
                opacity 0.2s ease-in-out;
    overflow: hidden;
}

.traj-panel.collapsed .traj-panel-content {
    max-height: 0;
    opacity: 0;
}

.traj-panel.expanded .traj-panel-content {
    max-height: 2000px; /* Large enough for content */
    opacity: 1;
}
```

#### Loading Spinner
```css
/* Simple, professional spinner */
@keyframes traj-spin {
    to { transform: rotate(360deg); }
}

.traj-spinner {
    width: 20px;
    height: 20px;
    border: 2px solid var(--border-default);
    border-top-color: var(--blue);
    border-radius: 50%;
    animation: traj-spin 1s linear infinite;
}

/* Reduced motion: show static indicator */
@media (prefers-reduced-motion: reduce) {
    .traj-spinner {
        animation: none;
        border-style: dotted;
    }
}
```

#### Progress Bar
```css
.traj-progress-bar {
    height: 8px;
    background: var(--bg-surface);
    border-radius: 4px;
    overflow: hidden;
}

.traj-progress-fill {
    height: 100%;
    background: var(--blue);
    transition: width 0.2s ease;
}

/* Animated stripes for indeterminate state */
@keyframes traj-progress-stripes {
    from { background-position: 40px 0; }
    to { background-position: 0 0; }
}

.traj-progress-fill.indeterminate {
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
```

#### Modal Open/Close
```css
/* Overlay */
.traj-modal-overlay {
    opacity: 0;
    transition: opacity 0.2s ease;
}

.traj-modal-overlay.visible {
    opacity: 1;
}

/* Modal Container */
.traj-modal {
    opacity: 0;
    transform: scale(0.95) translateY(-10px);
    transition: opacity 0.25s ease,
                transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.traj-modal.visible {
    opacity: 1;
    transform: scale(1) translateY(0);
}

/* Closing is faster, no overshoot */
.traj-modal.closing {
    transition: opacity 0.15s ease,
                transform 0.15s ease-in;
    opacity: 0;
    transform: scale(0.98);
}
```

#### Tab Switch
```css
.traj-tab-content {
    opacity: 0;
    transform: translateY(8px);
    transition: opacity 0.2s ease, transform 0.2s ease;
    position: absolute;
    pointer-events: none;
}

.traj-tab-content.active {
    opacity: 1;
    transform: translateY(0);
    position: relative;
    pointer-events: auto;
}
```

#### Toast Notifications
```css
@keyframes traj-toast-enter {
    from {
        transform: translateX(100%) translateY(0);
        opacity: 0;
    }
    to {
        transform: translateX(0) translateY(0);
        opacity: 1;
    }
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

.traj-toast {
    animation: traj-toast-enter 0.3s ease-out;
}

.traj-toast.exiting {
    animation: traj-toast-exit 0.2s ease-in forwards;
}
```

#### Success Checkmark
```css
@keyframes traj-check-draw {
    0% {
        stroke-dashoffset: 30;
    }
    100% {
        stroke-dashoffset: 0;
    }
}

.traj-success-check {
    stroke: var(--status-success);
    stroke-width: 3;
    stroke-linecap: round;
    stroke-linejoin: round;
    fill: none;
    stroke-dasharray: 30;
    stroke-dashoffset: 30;
    animation: traj-check-draw 0.3s ease-out 0.1s forwards;
}
```

---

## 6. TIMING REFERENCE TABLE

Complete timing specifications for Trajanus components:

| Component | Duration | Easing | Delay |
|-----------|----------|--------|-------|
| Button hover | 150ms | ease | 0 |
| Button active | 50ms | ease-out | 0 |
| Button focus ring | 100ms | ease | 0 |
| Panel expand | 300ms | ease-in-out | 0 |
| Panel collapse | 250ms | ease-in | 0 |
| Tab switch out | 150ms | ease-in | 0 |
| Tab switch in | 200ms | ease-out | 50ms |
| Modal overlay in | 200ms | ease | 0 |
| Modal overlay out | 150ms | ease | 0 |
| Modal scale in | 250ms | cubic-bezier(0.34, 1.56, 0.64, 1) | 50ms |
| Modal scale out | 150ms | ease-in | 0 |
| Toast enter | 300ms | ease-out | 0 |
| Toast exit | 200ms | ease-in | 0 |
| Spinner rotation | 1000ms | linear | 0 |
| Progress update | 200ms | ease | 0 |
| Dropdown open | 200ms | ease-out | 0 |
| Dropdown close | 150ms | ease-in | 0 |
| Tooltip show | 150ms | ease | 200ms |
| Tooltip hide | 100ms | ease | 0 |
| Log entry appear | 150ms | ease-out | 0 |
| Success check | 300ms | ease-out | 100ms |

---

## 7. JAVASCRIPT UTILITIES

### 7.1 Animation Helper Class

```javascript
class TrajAnimator {
    static DURATIONS = {
        fast: 150,
        normal: 250,
        slow: 400
    };

    static EASINGS = {
        standard: 'cubic-bezier(0.4, 0.0, 0.2, 1)',
        decelerate: 'cubic-bezier(0.0, 0.0, 0.2, 1)',
        accelerate: 'cubic-bezier(0.4, 0.0, 1, 1)',
        sharp: 'cubic-bezier(0.4, 0.0, 0.6, 1)'
    };

    static fadeIn(element, duration = this.DURATIONS.normal) {
        return element.animate([
            { opacity: 0 },
            { opacity: 1 }
        ], {
            duration,
            easing: this.EASINGS.decelerate,
            fill: 'forwards'
        }).finished;
    }

    static fadeOut(element, duration = this.DURATIONS.fast) {
        return element.animate([
            { opacity: 1 },
            { opacity: 0 }
        ], {
            duration,
            easing: this.EASINGS.accelerate,
            fill: 'forwards'
        }).finished;
    }

    static slideIn(element, direction = 'right', duration = this.DURATIONS.normal) {
        const transforms = {
            right: ['translateX(100%)', 'translateX(0)'],
            left: ['translateX(-100%)', 'translateX(0)'],
            top: ['translateY(-100%)', 'translateY(0)'],
            bottom: ['translateY(100%)', 'translateY(0)']
        };

        return element.animate([
            { transform: transforms[direction][0], opacity: 0 },
            { transform: transforms[direction][1], opacity: 1 }
        ], {
            duration,
            easing: this.EASINGS.decelerate,
            fill: 'forwards'
        }).finished;
    }

    static expandPanel(element, duration = 300) {
        const height = element.scrollHeight;

        return element.animate([
            { maxHeight: '0px', opacity: 0 },
            { maxHeight: `${height}px`, opacity: 1 }
        ], {
            duration,
            easing: this.EASINGS.standard,
            fill: 'forwards'
        }).finished;
    }

    static collapsePanel(element, duration = 250) {
        return element.animate([
            { maxHeight: `${element.scrollHeight}px`, opacity: 1 },
            { maxHeight: '0px', opacity: 0 }
        ], {
            duration,
            easing: this.EASINGS.accelerate,
            fill: 'forwards'
        }).finished;
    }
}
```

### 7.2 Reduced Motion Check

```javascript
const prefersReducedMotion = window.matchMedia(
    '(prefers-reduced-motion: reduce)'
).matches;

function getAnimationDuration(defaultDuration) {
    return prefersReducedMotion ? 0 : defaultDuration;
}
```

---

## 8. DO NOT USE

The following animation patterns are **NOT appropriate** for Trajanus:

- **Bounce effects** - Too playful
- **Elastic/spring physics** - Consumer app aesthetic
- **Long delays** (> 200ms) - Feels sluggish
- **Parallax scrolling** - Distracting
- **Auto-playing background animations** - Unprofessional
- **Confetti/particle effects** - Too celebratory
- **Wiggle/shake on error** - Annoying
- **Slow fade-ins on page load** - Wastes time
- **Morphing shapes** - Unnecessary complexity
- **3D transforms/rotations** - Disorienting

---

## 9. IMPLEMENTATION NOTES

### 9.1 Testing Animations

Before deploying animations:

1. **Test with reduced motion enabled**
   - macOS: System Preferences > Accessibility > Display > Reduce motion
   - Windows: Settings > Ease of Access > Display > Show animations

2. **Test at 60fps**
   - Use browser DevTools Performance tab
   - Check for dropped frames

3. **Test on target hardware**
   - Animations may perform differently on older machines

### 9.2 Progressive Enhancement

Animations should be additive, not essential:

```css
/* Base state - works without animation */
.traj-panel-content {
    overflow: hidden;
}

/* Enhanced - only if transitions supported */
@supports (transition: max-height 0.3s) {
    .traj-panel-content {
        transition: max-height 0.3s ease-in-out;
    }
}
```

---

## 10. RESOURCES

- [Material Design Motion](https://m3.material.io/styles/motion/overview)
- [Apple Human Interface Guidelines - Animation](https://developer.apple.com/design/human-interface-guidelines/animation)
- [Microsoft Fluent Design - Motion](https://docs.microsoft.com/en-us/windows/apps/design/motion/)
- [Web Animations API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API)
- [CSS Easing Functions](https://easings.net/)

---

**Document Version:** 1.0
**Created:** January 2026
**Author:** CU (Claude Code - Support/Verifier)
**For:** Trajanus USA - Bill King, Principal/CEO
