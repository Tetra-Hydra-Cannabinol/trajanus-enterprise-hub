# UI Feature Implementation Template

## Feature Information
- **Feature Name:** [Name]
- **Workspace:** [developer/qcm/pm/traffic/healthcare]
- **Priority:** [Critical/High/Medium/Low]
- **Estimated Complexity:** [Simple/Medium/Complex]

---

## Requirements

### Functional Requirements
- [ ] [Requirement 1]
- [ ] [Requirement 2]
- [ ] [Requirement 3]

### Visual Requirements
- [ ] Follows Trajanus style guide (Silver/Black/Blue palette)
- [ ] Uses correct button specs (ext-btn: 120×44, script-btn: 160×50, nav-btn: 140×44)
- [ ] V2 Synapse neural glow effects applied
- [ ] Responsive behavior defined

### Interaction Requirements
- [ ] Hover states specified
- [ ] Active/click states specified
- [ ] Loading states (if async)
- [ ] Error states defined

---

## Implementation Checklist

### Pre-Implementation
- [ ] Read workspace .claude.md for context
- [ ] Identify insertion point in HTML
- [ ] Review similar existing components
- [ ] Create backup if touching sacred files

### Implementation
- [ ] HTML structure added
- [ ] CSS styles added (follow style_guide.md)
- [ ] JavaScript logic added (CSP-compliant, no inline handlers)
- [ ] Event bindings via data attributes

### Post-Implementation
- [ ] `npm run tauri dev` - app launches
- [ ] Navigate to affected section
- [ ] Test all interaction states
- [ ] Check console for errors
- [ ] Playwright screenshot captured

---

## Acceptance Criteria

### Visual Validation
```
[ ] Colors match palette (#C0C0C0, #1a1a1a, #00AAFF)
[ ] Button sizes correct
[ ] Spacing consistent (12-16px gaps)
[ ] Typography matches spec
[ ] No visual regressions
```

### Functional Validation
```
[ ] Feature works as specified
[ ] Edge cases handled
[ ] Error states display correctly
[ ] Loading states show for async ops
```

### Browser Fallback
```
[ ] Graceful degradation without Tauri
[ ] Appropriate messaging for desktop-only features
```

---

## Sign-Off

### Developer
- [ ] Implementation complete
- [ ] Self-tested all criteria
- [ ] Screenshots captured

### Review (@agent design-reviewer)
- [ ] Visual compliance verified
- [ ] Interaction patterns correct
- [ ] Accessibility checked

---

## Notes
[Additional context, decisions made, issues encountered]
