import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const assetRoot = path.join(root, "public", "world", "art");
const expected = [
  "command-center.glb",
  "build-lab.glb",
  "automation-lab.glb",
  "client-street.glb",
  "timeline.glb",
  "hobby-district.glb",
];

const perFileBudget = 900 * 1024;
const totalBudget = 4 * 1024 * 1024;
const failures = [];
let total = 0;

for (const name of expected) {
  const file = path.join(assetRoot, name);
  if (!fs.existsSync(file)) {
    failures.push(`missing ${name}`);
    continue;
  }
  const size = fs.statSync(file).size;
  total += size;
  if (size > perFileBudget) {
    failures.push(`${name} is ${(size / 1024).toFixed(1)} KiB; ceiling is 900 KiB`);
  }
}

if (total > totalBudget) {
  failures.push(`total GLB size is ${(total / 1024 / 1024).toFixed(2)} MiB; ceiling is 4.00 MiB`);
}

if (failures.length) {
  console.error("BLENDER ASSETS: FAIL");
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log("BLENDER ASSETS: PASS");
console.log(`asset_count=${expected.length}`);
console.log(`total_glb_kib=${(total / 1024).toFixed(1)}`);
