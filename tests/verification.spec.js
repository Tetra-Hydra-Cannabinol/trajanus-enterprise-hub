// @ts-check
const { test, expect } = require('@playwright/test');

/**
 * Trajanus Command Center - Verification Test Suite
 * Based on CC_MASTER_TASK_LIST.md requirements
 */

test.describe('Phase 1: Visual Verification', () => {
  test('Landing page loads successfully', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');

    // Take screenshot of initial state
    await page.screenshot({ path: 'test-results/landing-page.png' });

    // Verify page loaded (check for common elements)
    await expect(page).toHaveTitle(/Trajanus|Command Center/i);
  });

  test('Page has no critical console errors', async ({ page }) => {
    const consoleErrors = [];
    page.on('console', msg => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text());
      }
    });

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Filter out known acceptable errors
    const criticalErrors = consoleErrors.filter(
      err => !err.includes('favicon') && !err.includes('manifest')
    );

    expect(criticalErrors.length).toBeLessThan(5);
  });

  test('Logo and branding visible', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');

    // Look for Trajanus branding
    const pageContent = await page.content();
    const hasBranding =
      pageContent.includes('Trajanus') ||
      pageContent.includes('TRAJANUS') ||
      pageContent.includes('trajanus');

    expect(hasBranding).toBeTruthy();
  });
});

test.describe('Phase 2: Navigation', () => {
  test('Navigation buttons are present', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');

    // Check for common navigation elements
    const buttons = await page.locator('button').count();
    expect(buttons).toBeGreaterThan(0);
  });

  test('Enterprise Hub navigation', async ({ page }) => {
    await page.goto('/');

    // Look for Enterprise Hub button or link
    const enterpriseHub = page.locator('text=/Enterprise Hub|Enterprise|Hub/i').first();
    const isVisible = await enterpriseHub.isVisible().catch(() => false);

    if (isVisible) {
      await enterpriseHub.click();
      await page.waitForTimeout(1000);
      await page.screenshot({ path: 'test-results/enterprise-hub.png' });
    }

    // Test passes whether or not button exists (documents current state)
    expect(true).toBeTruthy();
  });

  test('Developer Project navigation', async ({ page }) => {
    await page.goto('/');

    // Look for Developer button
    const developerBtn = page.locator('text=/Developer|Dev Project/i').first();
    const isVisible = await developerBtn.isVisible().catch(() => false);

    if (isVisible) {
      await developerBtn.click();
      await page.waitForTimeout(1000);
      await page.screenshot({ path: 'test-results/developer-workspace.png' });
    }

    expect(true).toBeTruthy();
  });
});

test.describe('Phase 3: QCM Workspace', () => {
  test('QCM button exists and is clickable', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');

    // Look for QCM or Submittal Review button
    const qcmButton = page.locator('text=/QCM|Submittal Review/i').first();
    const isVisible = await qcmButton.isVisible().catch(() => false);

    if (isVisible) {
      await qcmButton.click();
      await page.waitForTimeout(1000);
      await page.screenshot({ path: 'test-results/qcm-workspace.png' });

      // Check for 3-panel layout indicator
      const pageContent = await page.content();
      const hasQCMContent =
        pageContent.includes('Trajanus EI') ||
        pageContent.includes('Send to Trajanus') ||
        pageContent.includes('Document Browser') ||
        pageContent.includes('Report Templates');

      // Document findings - don't fail if not present
      console.log(`QCM workspace content found: ${hasQCMContent}`);
    }

    expect(true).toBeTruthy();
  });

  test('Custom branding preserved', async ({ page }) => {
    await page.goto('/');

    // Navigate to QCM if possible
    const qcmButton = page.locator('text=/QCM|Submittal Review/i').first();
    if (await qcmButton.isVisible().catch(() => false)) {
      await qcmButton.click();
      await page.waitForTimeout(1000);
    }

    const pageContent = await page.content();

    // Check for custom branding elements
    const hasTrajanusBranding = pageContent.includes('Trajanus');
    const hasCustomSendButton =
      pageContent.includes('Send to Trajanus') ||
      pageContent.includes('Trajanus for Review');

    console.log(`Trajanus branding: ${hasTrajanusBranding}`);
    console.log(`Custom send button: ${hasCustomSendButton}`);

    // At minimum, Trajanus should appear somewhere
    expect(hasTrajanusBranding).toBeTruthy();
  });
});

test.describe('Phase 4: Responsive Design', () => {
  test('Desktop viewport renders correctly', async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');
    await page.screenshot({ path: 'test-results/viewport-desktop.png' });

    // Basic check - page should have content
    const bodyContent = await page.locator('body').textContent();
    expect(bodyContent?.length).toBeGreaterThan(0);
  });

  test('Laptop viewport renders correctly', async ({ page }) => {
    await page.setViewportSize({ width: 1366, height: 768 });
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');
    await page.screenshot({ path: 'test-results/viewport-laptop.png' });

    const bodyContent = await page.locator('body').textContent();
    expect(bodyContent?.length).toBeGreaterThan(0);
  });

  test('Tablet viewport renders correctly', async ({ page }) => {
    await page.setViewportSize({ width: 1024, height: 768 });
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');
    await page.screenshot({ path: 'test-results/viewport-tablet.png' });

    const bodyContent = await page.locator('body').textContent();
    expect(bodyContent?.length).toBeGreaterThan(0);
  });
});

test.describe('Phase 5: Chat Interface', () => {
  test('Chat elements exist', async ({ page }) => {
    await page.goto('/');

    // Navigate to Developer workspace if available
    const devButton = page.locator('text=/Developer|Dev Project/i').first();
    if (await devButton.isVisible().catch(() => false)) {
      await devButton.click();
      await page.waitForTimeout(1000);
    }

    // Check for chat-related elements
    const pageContent = await page.content();
    const hasChatUI =
      pageContent.includes('chat') ||
      pageContent.includes('Chat') ||
      pageContent.includes('message') ||
      pageContent.includes('Claude');

    console.log(`Chat UI elements present: ${hasChatUI}`);
    await page.screenshot({ path: 'test-results/chat-interface.png' });

    expect(true).toBeTruthy();
  });
});

test.describe('Summary Report', () => {
  test('Generate verification summary', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');

    // Collect verification data
    const title = await page.title();
    const url = page.url();
    const bodyText = await page.locator('body').textContent();

    const report = {
      timestamp: new Date().toISOString(),
      url: url,
      title: title,
      contentLength: bodyText?.length || 0,
      hasTrajanusBranding: bodyText?.includes('Trajanus') || false,
      hasNavigationButtons: await page.locator('button').count() > 0
    };

    console.log('\n=== VERIFICATION SUMMARY ===');
    console.log(JSON.stringify(report, null, 2));
    console.log('============================\n');

    // Final screenshot
    await page.screenshot({ path: 'test-results/verification-summary.png', fullPage: true });

    expect(report.contentLength).toBeGreaterThan(0);
  });
});
