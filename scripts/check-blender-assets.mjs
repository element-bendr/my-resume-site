import crypto from "node:crypto";
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
const GLB_MAGIC = 0x46546c67;
const GLB_VERSION = 2;
const JSON_CHUNK = 0x4e4f534a;

const failures = [];
const evidence = [];
let total = 0;

function inspectGlb(file, name) {
  const data = fs.readFileSync(file);
  const size = data.byteLength;

  if (size < 20) {
    failures.push(`${name} is too small to be a valid GLB`);
    return { size, sha256: crypto.createHash("sha256").update(data).digest("hex") };
  }

  const magic = data.readUInt32LE(0);
  const version = data.readUInt32LE(4);
  const declaredLength = data.readUInt32LE(8);
  const firstChunkLength = data.readUInt32LE(12);
  const firstChunkType = data.readUInt32LE(16);

  if (magic !== GLB_MAGIC) failures.push(`${name} has invalid GLB magic`);
  if (version !== GLB_VERSION) failures.push(`${name} uses GLB version ${version}; expected 2`);
  if (declaredLength !== size) {
    failures.push(`${name} declares ${declaredLength} bytes but file contains ${size}`);
  }
  if (firstChunkType !== JSON_CHUNK) failures.push(`${name} does not start with a JSON chunk`);
  if (20 + firstChunkLength > size) failures.push(`${name} JSON chunk exceeds file length`);

  return {
    size,
    sha256: crypto.createHash("sha256").update(data).digest("hex"),
  };
}

for (const name of expected) {
  const file = path.join(assetRoot, name);
  if (!fs.existsSync(file)) {
    failures.push(`missing ${name}`);
    continue;
  }

  const result = inspectGlb(file, name);
  total += result.size;
  evidence.push({ name, ...result });

  if (result.size > perFileBudget) {
    failures.push(
      `${name} is ${(result.size / 1024).toFixed(1)} KiB; ceiling is 900 KiB`,
    );
  }
}

if (total > totalBudget) {
  failures.push(
    `total GLB size is ${(total / 1024 / 1024).toFixed(2)} MiB; ceiling is 4.00 MiB`,
  );
}

if (failures.length) {
  console.error("BLENDER ASSETS: FAIL");
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log("BLENDER ASSETS: PASS");
console.log(`asset_count=${expected.length}`);
console.log(`total_glb_kib=${(total / 1024).toFixed(1)}`);
for (const item of evidence) {
  console.log(
    `asset=${item.name} bytes=${item.size} sha256=${item.sha256}`,
  );
}
