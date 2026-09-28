import fs from "node:fs";
import path from "node:path";
import zlib from "node:zlib";

const root = process.cwd();
const clientRoot = path.join(root, "dist", "client");
const budget = 3 * 1024 * 1024;

if (!fs.existsSync(clientRoot)) {
  console.error("WORLD BUDGET: FAIL");
  console.error("- dist/client is missing; run npm run build first");
  process.exit(1);
}

const jsFiles = [];
const collect = (dir) => {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) collect(full);
    else if (entry.isFile() && entry.name.endsWith(".js")) jsFiles.push(full);
  }
};
collect(clientRoot);

let gzipBytes = 0;
for (const file of jsFiles) {
  gzipBytes += zlib.gzipSync(fs.readFileSync(file), { level: 9 }).length;
}

if (gzipBytes > budget) {
  console.error("WORLD BUDGET: FAIL");
  console.error(`- total client JavaScript is ${(gzipBytes / 1024 / 1024).toFixed(2)} MiB gzip; Stage 03 ceiling is 3.00 MiB`);
  process.exit(1);
}

console.log("WORLD BUDGET: PASS");
console.log(`client_js_chunks=${jsFiles.length}`);
console.log(`total_client_js_gzip_kib=${(gzipBytes / 1024).toFixed(1)}`);
