/**
 * Playwright Electron Test Script
 * Tests Trajanus Command Center using Playwright's Electron API
 *
 * Run from C:\temp\electron-fix:
 *   node test-playwright-electron.js
 */

const { _electron: electron } = require('playwright');
const path = require('path');
const fs = require('fs');

// Configuration
const APP_PATH = 'G:\\My Drive\\00 - Trajanus USA\\00-Command-Center';
const SCREENSHOTS_DIR = path.join(APP_PATH, 'screenshots');

async function ensureScreenshotsDir() {
  if (!fs.existsSync(SCREENSHOTS_DIR)) {
    fs.mkdirSync(SCREENSHOTS_DIR, { recursive: true });
    console.log(`Created screenshots directory: ${SCREENSHOTS_DIR}`);
  }
}

async function testScreenshot() {
  console.log('='.repeat(60));
  console.log('Playwright Electron Test - Trajanus Command Center');
  console.log('='.repeat(60));

  await ensureScreenshotsDir();

  console.log('\n[1/5] Launching Electron app...');

  const electronApp = await electron.launch({
    args: [APP_PATH],
    executablePath: path.join(APP_PATH, 'node_modules', 'electron', 'dist', 'electron.exe')
  });

  console.log('[2/5] Waiting for first window...');
  const window = await electronApp.firstWindow();

  // Wait for app to fully load
  console.log('[3/5] Waiting for app to load...');
  await window.waitForLoadState('domcontentloaded');
  await new Promise(r => setTimeout(r, 2000)); // Extra wait for rendering

  // Get window info
  const title = await window.title();
  console.log(`    Window title: ${title}`);

  // Take main window screenshot
  console.log('\n[4/5] Taking screenshots...');

  const mainScreenshot = path.join(SCREENSHOTS_DIR, 'main-window.png');
  await window.screenshot({ path: mainScreenshot });
  console.log(`    ✓ Main window: ${mainScreenshot}`);

  // Try to find and click QCM workspace
  try {
    // Look for QCM in sidebar
    const qcmButton = await window.locator('text=QCM').first();
    if (await qcmButton.isVisible()) {
      await qcmButton.click();
      await new Promise(r => setTimeout(r, 1000));

      const qcmScreenshot = path.join(SCREENSHOTS_DIR, 'qcm-workspace.png');
      await window.screenshot({ path: qcmScreenshot });
      console.log(`    ✓ QCM Workspace: ${qcmScreenshot}`);
    }
  } catch (e) {
    console.log(`    ! Could not navigate to QCM workspace: ${e.message}`);
  }

  // Test different viewport sizes
  console.log('\n    Testing viewport sizes:');

  const viewports = [
    { width: 1920, height: 1080, name: 'desktop' },
    { width: 1366, height: 768, name: 'laptop' },
    { width: 1024, height: 768, name: 'tablet-landscape' }
  ];

  for (const vp of viewports) {
    await window.setViewportSize({ width: vp.width, height: vp.height });
    await new Promise(r => setTimeout(r, 500));
    const vpScreenshot = path.join(SCREENSHOTS_DIR, `viewport-${vp.name}.png`);
    await window.screenshot({ path: vpScreenshot });
    console.log(`    ✓ ${vp.name} (${vp.width}x${vp.height}): ${vpScreenshot}`);
  }

  // Close app
  console.log('\n[5/5] Closing app...');
  await electronApp.close();

  // Summary
  console.log('\n' + '='.repeat(60));
  console.log('TEST COMPLETE');
  console.log('='.repeat(60));
  console.log(`Screenshots saved to: ${SCREENSHOTS_DIR}`);
  console.log('\nFiles created:');
  const files = fs.readdirSync(SCREENSHOTS_DIR);
  files.forEach(f => console.log(`  - ${f}`));
}

// Run the test
testScreenshot()
  .then(() => {
    console.log('\n✓ All tests passed!');
    process.exit(0);
  })
  .catch(err => {
    console.error('\n✗ Test failed:', err.message);
    console.error(err.stack);
    process.exit(1);
  });
