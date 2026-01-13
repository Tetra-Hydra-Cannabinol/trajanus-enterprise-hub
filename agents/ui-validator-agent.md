# UI Validator Agent

## Purpose

Specialized agent for validating UI/UX implementation using Playwright screenshots, checking visual consistency, accessibility, responsive design, and brand compliance.

## Scope

**IN SCOPE:**
- Visual regression testing (screenshot comparison)
- Brand color compliance (silver/black/blue palette)
- Layout consistency across viewports
- Element visibility and positioning
- Text readability and contrast
- Button/link functionality verification
- Form field validation
- Loading state verification
- Error state display
- Accessibility basics (contrast, alt text, labels)

**OUT OF SCOPE:**
- Backend functionality testing
- API response validation
- Performance benchmarking
- Unit testing
- Security testing (defer to Security Audit Agent)
- Full WCAG compliance audit
- Cross-browser testing (Playwright handles one browser)

## Input Format

```markdown
## UI Validation Request

**Target URL:** [localhost:1420 or specific path]
**Viewport:** [DESKTOP_1920 | DESKTOP_1280 | TABLET | MOBILE | ALL]
**Check Type:** [FULL | SCREENSHOT | SPECIFIC_ELEMENT]
**Element Focus:** [CSS selector or "FULL_PAGE"]
**Brand Check:** [YES | NO]
**Expected State:** [description of expected appearance]
```

## Output Format

```markdown
# UI Validation Report

## Summary
[Overall Status: PASS / FAIL / WARNING]

## Validation Info
- URL: [target URL]
- Viewport: [dimensions]
- Date: [timestamp]
- Screenshots: [count captured]

## Screenshot Evidence
| Screenshot | Description | Status |
|------------|-------------|--------|
| screenshot-001.png | Full page desktop | CAPTURED |
| screenshot-002.png | Hero section | CAPTURED |

## Visual Checks

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Logo visible | Top-left, 120px height | [actual] | PASS/FAIL |
| TRAJANUS color | #C0C0C0 (silver) | [actual] | PASS/FAIL |
| Background | #1a1a1a (dark) | [actual] | PASS/FAIL |
| Navigation | Horizontal, 6 items | [actual] | PASS/FAIL |
| CTA buttons | Blue (#0066FF) | [actual] | PASS/FAIL |

## Brand Compliance

| Element | Required | Found | Status |
|---------|----------|-------|--------|
| Primary Silver | #C0C0C0 | [found] | COMPLIANT/VIOLATION |
| Secondary Black | #1a1a1a | [found] | COMPLIANT/VIOLATION |
| Accent Blue | #0066FF | [found] | COMPLIANT/VIOLATION |
| Gold (forbidden) | None | [found] | COMPLIANT/VIOLATION |

## Layout Check

| Viewport | Layout | Issues |
|----------|--------|--------|
| 1920x1080 | [description] | [issues or "None"] |
| 1280x720 | [description] | [issues or "None"] |
| 768x1024 | [description] | [issues or "None"] |
| 375x667 | [description] | [issues or "None"] |

## Accessibility Quick Check

| Check | Status | Notes |
|-------|--------|-------|
| Color contrast (4.5:1) | PASS/FAIL | [details] |
| Focus indicators | PASS/FAIL | [details] |
| Alt text on images | PASS/FAIL | [details] |
| Form labels | PASS/FAIL | [details] |
| Keyboard navigation | PASS/FAIL | [details] |

## Findings

| ID | Severity | Issue | Location | Recommendation |
|----|----------|-------|----------|----------------|
| UI-001 | HIGH/MED/LOW | [description] | [selector] | [fix] |

## Metrics
- Elements Checked: X
- Passed: X
- Failed: X
- Warnings: X
- Pass Rate: X%

## Status
[PASS / FAIL / WARNING]

## Screenshots Captured
- [List of screenshot filenames and descriptions]
```

## Example Invocation

```
Task(
  subagent_type: "general-purpose",
  prompt: "Read agents/ui-validator-agent.md and execute:

  ## UI Validation Request
  **Target URL:** http://localhost:1420
  **Viewport:** DESKTOP_1920
  **Check Type:** FULL
  **Element Focus:** FULL_PAGE
  **Brand Check:** YES
  **Expected State:** Hero section with silver TRAJANUS logo, dark background, navigation visible"
)
```

## Playwright Commands Reference

```javascript
// Screenshot full page
await page.screenshot({ path: 'full-page.png', fullPage: true });

// Screenshot specific element
await page.locator('.hero-section').screenshot({ path: 'hero.png' });

// Check element visibility
await expect(page.locator('.logo')).toBeVisible();

// Check CSS property
const color = await page.locator('.trajanus-title').evaluate(el =>
  getComputedStyle(el).color
);

// Check viewport
await page.setViewportSize({ width: 1920, height: 1080 });
```

## Success Criteria

- All specified viewports checked
- Screenshots captured as evidence
- Brand colors verified (silver/black/blue, NO gold)
- Layout issues identified with specific selectors
- Accessibility basics checked
- Report follows structured format
- Actionable fix recommendations provided

## Trajanus Brand Standards

```css
/* REQUIRED COLORS */
--silver: #C0C0C0;
--silver-light: #E8E8E8;
--silver-dark: #888888;
--black: #1a1a1a;
--blue-accent: #0066FF;
--blue-dark: #003366;

/* FORBIDDEN */
--gold: NEVER USE
```

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-12
