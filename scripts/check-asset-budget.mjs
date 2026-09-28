import fs from "node:fs";
import path from "node:path";
import zlib from "node:zlib";

const root = process.cwd();
const distRoot = path.join(root, "dist");
const clientRoot = fs.existsSync(path.join(distRoot, "client"))
  ? path.join(distRoot, "client")
  : distRoot;

const mib = 1024 * 1024;
const singleAssetCeiling = 10 * mib;
const criticalCompressedBudget = 1.5 * mib;
const failures = [];

if (!fs.existsSync(clientRoot)) {
  console.error("ASSET BUDGET: FAIL");
  console.error("- build output is missing; run npm run build first");
  process.exit(1);
}

const files = [];
const collect = (dir) => {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) collect(full);
    else if (entry.isFile()) files.push(full);
  }
};
collect(clientRoot);

for (const file of files) {
  const size = fs.statSync(file).size;
  if (size > singleAssetCeiling) {
    failures.push(
      `${path.relative(clientRoot, file)} is ${(size / mib).toFixed(2)} MiB; ceiling is 10 MiB`,
    );
  }
}

const indexPath = path.join(clientRoot, "index.html");
if (!fs.existsSync(indexPath)) failures.push("client index.html is missing");

const criticalFiles = new Set();
if (fs.existsSync(indexPath)) {
  criticalFiles.add(indexPath);
  const html = fs.readFileSync(indexPath, "utf8");
  const refs = [
    ...html.matchAll(/<script[^>]+src=["']([^"']+)["']/g),
    ...html.matchAll(/<link[^>]+href=["']([^"']+)["'][^>]*>/g),
  ].map((match) => match[1]);

  for (const ref of refs) {
    if (/^(https?:|data:|#)/.test(ref)) continue;
    const clean = ref.split(/[?#]/, 1)[0].replace(/^\//, "");
    if (!clean) continue;
    const candidate = path.resolve(clientRoot, clean);
    if (candidate.startsWith(path.resolve(clientRoot)) && fs.existsSync(candidate)) {
      criticalFiles.add(candidate);
    }
  }
}

let criticalCompressedBytes = 0;
for (const file of criticalFiles) {
  criticalCompressedBytes += zlib.gzipSync(fs.readFileSync(file), { level: 9 }).length;
}

if (criticalCompressedBytes > criticalCompressedBudget) {
  failures.push(
    `critical HTML/CSS/JS shell is ${(criticalCompressedBytes / mib).toFixed(2)} MiB gzip; budget is 1.50 MiB`,
  );
}

const largest = files
  .map((file) => ({ file: path.relative(clientRoot, file), size: fs.statSync(file).size }))
  .sort((a, b) => b.size - a.size)
  .slice(0, 10);

if (failures.length > 0) {
  console.error("ASSET BUDGET: FAIL");
  failures.forEach((failure) => console.error(`- ${failure}`));
  console.error("Largest assets:");
  largest.forEach((item) => console.error(`- ${item.file}: ${(item.size / 1024).toFixed(1)} KiB`));
  process.exit(1);
}

console.log("ASSET BUDGET: PASS");
console.log(`files=${files.length}`);
console.log(`critical_gzip_kib=${(criticalCompressedBytes / 1024).toFixed(1)}`);
console.log("largest_assets:");
largest.forEach((item) => console.log(`- ${item.file}: ${(item.size / 1024).toFixed(1)} KiB`));
