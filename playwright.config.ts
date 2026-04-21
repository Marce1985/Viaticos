import { defineConfig, devices } from "@playwright/test";

const isDemoMode = process.env.PLAYWRIGHT_DEMO === "1";
const demoSlowMo = isDemoMode ? 1800 : 0;

export default defineConfig({
  testDir: "./playwright/tests",
  timeout: isDemoMode ? 180000 : 30000,
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [["list"], ["html", { open: "never" }]],
  use: {
    baseURL: "http://127.0.0.1:8050",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
    headless: !isDemoMode,
    actionTimeout: isDemoMode ? 20000 : 10000,
    navigationTimeout: isDemoMode ? 30000 : 15000,
    launchOptions: isDemoMode ? { slowMo: demoSlowMo } : undefined,
  },
  webServer: {
    command: "python run.py",
    url: "http://127.0.0.1:8050",
    reuseExistingServer: true,
    timeout: 120000,
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
});
