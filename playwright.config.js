// @ts-check
const { defineConfig } = require('@playwright/test');

/**
 * Playwright Configuration for Trajanus Command Center
 * Supports both browser-based testing (static server) and Electron testing
 */
module.exports = defineConfig({
  testDir: './tests',

  // Run tests in parallel
  fullyParallel: false,

  // Fail the build on CI if you accidentally left test.only in the source code
  forbidOnly: !!process.env.CI,

  // Retry on CI only
  retries: process.env.CI ? 2 : 0,

  // Opt out of parallel tests for now
  workers: 1,

  // Reporter to use
  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['list']
  ],

  // Timeout settings
  timeout: 60000,
  expect: {
    timeout: 10000
  },

  use: {
    // Base URL for browser tests
    baseURL: 'http://localhost:1420',

    // Collect trace when retrying the failed test
    trace: 'on-first-retry',

    // Screenshot on failure
    screenshot: 'only-on-failure',

    // Video recording
    video: 'retain-on-failure'
  },

  // Output folder for screenshots and traces
  outputDir: 'test-results',

  // Configure projects for different testing scenarios
  projects: [
    {
      name: 'chromium',
      use: {
        browserName: 'chromium',
        viewport: { width: 1920, height: 1080 }
      }
    },
    {
      name: 'chromium-laptop',
      use: {
        browserName: 'chromium',
        viewport: { width: 1366, height: 768 }
      }
    }
  ],

  // Web server configuration
  webServer: {
    command: 'python -m http.server 1420 -d .',
    url: 'http://localhost:1420',
    reuseExistingServer: !process.env.CI,
    timeout: 30000
  }
});
