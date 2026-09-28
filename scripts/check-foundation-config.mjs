import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const failures = [];

const read = (relative) => {
  const file = path.join(root, relative);
  if (!fs.existsSync(file)) {
    failures.push(`missing required file: ${relative}`);
    return "";
  }
  return fs.readFileSync(file, "utf8");
};

const wranglerText = read("wrangler.jsonc");
let wrangler;
try {
  wrangler = JSON.parse(wranglerText);
} catch (error) {
  failures.push(`wrangler.jsonc is not strict JSON-compatible JSONC: ${error.message}`);
}

if (wrangler) {
  if (wrangler.main !== "./worker/index.ts") failures.push("wrangler main must be ./worker/index.ts");
  if (wrangler.compatibility_date !== "2026-09-28") {
    failures.push("wrangler compatibility_date must remain frozen at 2026-09-28 during Stage 02");
  }
  if (wrangler.assets?.not_found_handling !== "single-page-application") {
    failures.push("SPA not_found_handling must be single-page-application");
  }
  const routes = wrangler.assets?.run_worker_first;
  if (!Array.isArray(routes) || routes.length !== 1 || routes[0] !== "/api/*") {
    failures.push("run_worker_first must contain only /api/* in Stage 02");
  }
  for (const key of ["d1_databases", "kv_namespaces", "r2_buckets", "durable_objects"]) {
    if (key in wrangler) failures.push(`Stage 02 must not configure Cloudflare persistence: ${key}`);
  }
}

const worker = read("worker/index.ts");
for (const expected of ['url.pathname === "/api/health"', '"cache-control": "no-store"', 'error: "not_found"']) {
  if (!worker.includes(expected)) failures.push(`worker contract missing: ${expected}`);
}

const headers = read("public/_headers");
for (const expected of [
  "Content-Security-Policy:",
  "X-Content-Type-Options: nosniff",
  "Referrer-Policy: strict-origin-when-cross-origin",
  "X-Frame-Options: DENY",
  "Permissions-Policy:",
]) {
  if (!headers.includes(expected)) failures.push(`security headers missing: ${expected}`);
}

const html = read("index.html");
if (!html.includes("<noscript>")) failures.push("index.html requires a noscript fallback");
if (!html.includes("https://github.com/element-bendr")) {
  failures.push("noscript/document fallback must expose the public GitHub proof surface");
}
if (!html.includes("mailto:element.bendr@gmail.com")) {
  failures.push("noscript/document fallback must expose the public contact email");
}

if (failures.length) {
  console.error("FOUNDATION CONFIG: FAIL");
  failures.forEach((failure) => console.error(`- ${failure}`));
  process.exit(1);
}

console.log("FOUNDATION CONFIG: PASS");
console.log("spa_fallback=single-page-application");
console.log("worker_first=/api/*");
console.log("persistence_bindings=0");
console.log("noscript_contact=present");
