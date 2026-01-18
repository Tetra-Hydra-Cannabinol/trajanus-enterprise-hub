# Trajanus Command Center - Design Principles

**Purpose:** Core design principles guiding all UI/UX decisions
**Version:** 1.0
**Last Updated:** 2026-01-17

---

## CORE PHILOSOPHY

### Professional Authority
The platform must convey **trust, competence, and precision**. Users are construction professionals managing federal contracts worth millions. The interface should feel like mission control, not a consumer app.

### Operational Efficiency
Every click must have purpose. Users work marathon sessions (13-16 hours). Minimize cognitive load, maximize information density without clutter.

### Military Precision
Clear hierarchies, unambiguous states, immediate feedback. No guessing what happened or what to do next.

---

## VISUAL HIERARCHY

### Information Architecture
```
Level 1: Platform Identity (Header/Logo)
Level 2: Navigation (Toolkits, Workspaces)
Level 3: Section Headers (Dividers, Titles)
Level 4: Content Cards (Tools, Actions)
Level 5: Detail Text (Descriptions, Status)
```

### Emphasis Through Color
- **Primary Actions:** Blue (#00AAFF) - Calls attention
- **Content:** Silver (#C0C0C0) - Readable, professional
- **Background:** Black (#0a0a0a) - Recedes, reduces eye strain
- **Success States:** Green (#4ade80) - Positive confirmation
- **Warnings:** Gold/Yellow (#fbbf24) - Attention required
- **Errors:** Red (#f87171) - Critical issues

### Spatial Hierarchy
- More important = More space
- Related items = Grouped together
- Actions = Right side or bottom
- Status = Top right corner

---

## INTERACTION DESIGN

### Feedback Principles

1. **Immediate Response**
   - Every click produces visual feedback within 100ms
   - Button states change instantly on interaction
   - Loading states appear for operations >500ms

2. **State Clarity**
   - Active states clearly distinguishable
   - Disabled states obvious but not invisible
   - Hover states indicate interactivity

3. **Error Prevention**
   - Destructive actions require confirmation
   - Invalid inputs prevented before submission
   - Clear constraints communicated upfront

### Button Interaction Pattern
```
Rest State     → Hover          → Active         → Complete
(default)        (lift + glow)    (press + flash)   (feedback)
```

### Animation Guidelines
- Duration: 150-300ms for UI transitions
- Easing: ease-out for entering, ease-in for exiting
- Purpose: Guide attention, confirm action, show state change
- Never: Delay critical actions, distract from content

---

## TYPOGRAPHY

### Font Hierarchy
```
Headers:     Tahoma Bold, 24-28px, letter-spacing: 1-2px
Subheaders:  Segoe UI Semibold, 14-16px
Body:        Segoe UI Regular, 13-14px
Labels:      Segoe UI, 11-12px, uppercase, letter-spacing: 1px
Code:        Consolas/Monaco, 12-13px
```

### Readability Rules
- Line height: 1.4-1.6 for body text
- Maximum line length: 80 characters
- Contrast ratio: Minimum 4.5:1 (WCAG AA)
- No pure white (#FFFFFF) on pure black - use silver tones

---

## LAYOUT PRINCIPLES

### Grid System
- 3-column layout for main workspaces
- Cards fill available width with consistent gaps (12-16px)
- Responsive: Stack columns on narrow viewports

### Spacing Scale
```
4px  - Tight (inline elements)
8px  - Compact (related items)
12px - Standard (card padding, gaps)
16px - Comfortable (section spacing)
24px - Generous (major sections)
32px - Expansive (page margins)
```

### Alignment Rules
- Left-align text content
- Center-align hero elements and logos
- Right-align actions and status indicators
- Consistent vertical rhythm throughout

---

## COMPONENT PATTERNS

### Cards
- Clear boundaries (1px border)
- Consistent padding (12-16px)
- Hover state indicates interactivity
- Icon + Label + Description structure

### Buttons
- Fixed sizes for consistency (120×44, 160×50, 140×44)
- Clear visual affordance (3D effect, glow)
- State changes on interaction
- Icon + text when possible

### Forms
- Labels above inputs
- Clear focus states
- Validation feedback inline
- Submit button at bottom right

### Modals
- Centered, dimmed overlay
- Clear close mechanism
- Action buttons at footer
- Escape key closes

---

## ACCESSIBILITY

### Keyboard Navigation
- All interactive elements focusable
- Tab order follows visual order
- Focus indicators visible
- Escape closes modals/menus

### Screen Reader Support
- Semantic HTML structure
- ARIA labels where needed
- Status announcements for dynamic content
- Alt text for images

### Visual Accessibility
- Color not sole indicator of state
- Sufficient contrast ratios
- Resizable text support
- Reduced motion option respected

---

## PLATFORM-SPECIFIC

### Desktop Focus
- Optimized for 1920×1080 and above
- Mouse-first interaction model
- Keyboard shortcuts for power users
- Multi-window workflow supported

### Dark Theme Default
- Reduces eye strain in long sessions
- Emphasizes content over chrome
- Professional, focused aesthetic
- Consistent with code editors

---

## ANTI-PATTERNS (AVOID)

### Visual
- Gradients on text
- Excessive shadows
- Inconsistent border radiuses
- Mixing warm and cool colors randomly

### Interaction
- Hidden scrollbars that affect usability
- Hover-only information disclosure
- Auto-advancing carousels
- Infinite scroll without position indicator

### Content
- Lorem ipsum in production
- Ambiguous button labels ("Click Here")
- Error messages without guidance
- Success messages that disappear too fast

---

## DECISION FRAMEWORK

When making design decisions, ask:

1. **Does it serve the professional user?**
   - Not flashy, but functional
   - Information-dense without clutter

2. **Is it consistent with existing patterns?**
   - Reuse before creating new
   - Follow established conventions

3. **Does it provide clear feedback?**
   - User always knows system state
   - Actions have visible results

4. **Is it accessible?**
   - Works with keyboard
   - Readable contrast
   - No motion sickness triggers

5. **Will it hold up in a 16-hour session?**
   - Eye strain considered
   - No attention-grabbing animations
   - Professional, calm aesthetic

---

**Remember:** Good design is invisible. The user should focus on their work, not the interface.
