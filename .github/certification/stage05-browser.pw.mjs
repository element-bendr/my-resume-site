import assert from "node:assert/strict";
import { mkdir, writeFile } from "node:fs/promises";
import { createRequire } from "node:module";
import { join } from "node:path";

const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_PACKAGE_PATH);
const baseUrl = process.env.STAGE05_BASE_URL ?? "http://127.0.0.1:4173";
const evidenceDir = process.env.STAGE05_EVIDENCE_DIR;

assert.ok(evidenceDir, "STAGE05_EVIDENCE_DIR must be set");

const browser = await chromium.launch({
  headless: true,
  args: [
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--enable-webgl",
    "--enable-unsafe-swiftshader",
    "--use-gl=angle",
    "--use-angle=swiftshader",
  ],
});

const results = {
  browser: browser.version(),
  baseUrl,
  checks: [],
};

try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

  await page.goto(`${baseUrl}/ask`, { waitUntil: "networkidle" });
  await page.getByLabel("Your question").fill("What is PCAS?");
  const askResponsePromise = page.waitForResponse((response) =>
    response.url().endsWith("/api/ask") && response.request().method() === "POST",
  );
  await page.getByRole("button", { name: "Ask", exact: true }).click();
  const askResponse = await askResponsePromise;
  assert.equal(askResponse.status(), 200);
  const askResult = await askResponse.json();
  assert.equal(askResult.support, "grounded");
  assert.ok(askResult.matches.some((match) => match.id === "pcas"));
  await page.locator(".ask-answer-text").waitFor();
  const visibleAnswer = (await page.locator(".ask-answer-text").textContent()).trim();
  assert.equal(visibleAnswer, askResult.answer, "the UI must render the API answer verbatim");
  results.checks.push({
    name: "direct-ask-grounded-fidelity",
    support: askResult.support,
    matches: askResult.matches.length,
    answerMatchesApi: true,
  });

  await page.goto(`${baseUrl}/play?zone=command-center`, { waitUntil: "domcontentloaded" });
  await page.getByRole("button", { name: "Map" }).waitFor({ timeout: 30000 });
  const terminalLabel = page.locator(".world-station-label").filter({ hasText: "Ask" });
  await terminalLabel.waitFor({ state: "visible", timeout: 30000 });
  const terminalBounds = await terminalLabel.boundingBox();
  assert.ok(terminalBounds, "Ask Terminal label must be visible in Command Center");
  await page.mouse.click(
    terminalBounds.x + terminalBounds.width / 2,
    terminalBounds.y + terminalBounds.height / 2,
  );
  await page.getByRole("dialog").waitFor({ timeout: 5000 });
  await page.getByRole("link", { name: "Open Ask", exact: true }).click();
  await page.waitForURL("**/ask");
  await page.getByLabel("Your question").waitFor();
  results.checks.push({ name: "ask-terminal-to-canonical-route", passed: true });

  const fallbackContext = await browser.newContext();
  await fallbackContext.addInitScript(() => {
    const originalGetContext = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function (type, ...args) {
      if (["webgl2", "webgl", "experimental-webgl"].includes(String(type).toLowerCase())) {
        return null;
      }
      return originalGetContext.call(this, type, ...args);
    };
  });
  const fallbackPage = await fallbackContext.newPage();
  await fallbackPage.goto(`${baseUrl}/play?zone=command-center`, { waitUntil: "domcontentloaded" });
  const fallback = fallbackPage.getByRole("status").filter({ hasText: "3D unavailable" });
  await fallback.waitFor({ timeout: 15000 });
  const expectedLinks = [
    ["Projects", "/projects"],
    ["Resume", "/resume"],
    ["Ask", "/ask"],
    ["Contact", "/contact"],
  ];
  for (const [label, href] of expectedLinks) {
    assert.equal(await fallback.getByRole("link", { name: label, exact: true }).getAttribute("href"), href);
  }
  await fallback.getByRole("link", { name: "Ask", exact: true }).click();
  await fallbackPage.waitForURL("**/ask");
  results.checks.push({ name: "forced-non-webgl-fallback-routes", passed: true });
  await fallbackContext.close();

  await mkdir(evidenceDir, { recursive: true });
  await writeFile(join(evidenceDir, "browser-evidence.json"), `${JSON.stringify(results, null, 2)}\n`);
} finally {
  await browser.close();
}

console.log(JSON.stringify(results));
