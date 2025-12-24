# Research Finding #122

**Date:** 2025-12-17 08:57
**Topic:** Playwright form filling verification
**Score:** 0.9992084

---

## Writing tests | Playwright

**URL:** https://playwright.dev/docs/writing-tests
**Published:** Unknown date

---

## Content

Playwright includes test assertions in the form of `expect` function. To make an assertion, call `expect(value)` and choose a matcher that reflects the expectation.

Playwright includes async matchers that wait until the expected condition is met. Using these matchers makes tests non-flaky and resilient. For example, this code waits until the page gets the title containing "Playwright":

```
await expect(page).toHaveTitle(/Playwright/); await  expect(page). toHaveTitle(/ Playwright/);
``` [...] Playwright also includes generic matchers like `toEqual`, `toContain`, `toBeTruthy` that can be used to assert any conditions. These assertions do not use the `await` keyword as they perform immediate synchronous checks on already available values.

```
expect(success).toBeTruthy(); expect(success). toBeTruthy();
```

### Test Isolation​ [...] | Action | Description |
 --- |
| locator.check() | Check the input checkbox |
| locator.click() | Click the element |
| locator.uncheck() | Uncheck the input checkbox |
| locator.hover() | Hover mouse over the element |
| locator.fill() | Fill the form field, input text |
| locator.focus() | Focus the element |
| locator.press() | Press single key |
| locator.setInputFiles() | Pick files to upload |
| locator.selectOption() | Select option in the drop down |

## Assertions​

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:16*
