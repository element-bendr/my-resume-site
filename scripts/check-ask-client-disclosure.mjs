import assert from "node:assert/strict";
import { readdir, readFile } from "node:fs/promises";
import { join } from "node:path";

const assetsDirectory = "dist/client/assets";
const files = await readdir(assetsDirectory);
const clientBundles = files.filter((file) => file.endsWith(".js"));
assert.ok(clientBundles.length > 0, `No client JavaScript bundles found in ${assetsDirectory}`);

const bundleText = (await Promise.all(
  clientBundles.map((file) => readFile(join(assetsDirectory, file), "utf8")),
)).join("\n");

for (const forbidden of [
  "internal-reference",
  "Approved consulting positioning",
  "Verified structured employment history",
  "Direct user-approved hobby content",
]) {
  assert.ok(!bundleText.includes(forbidden), `Internal source metadata leaked into client bundle: ${forbidden}`);
}

console.log(`Ask client disclosure check passed (${clientBundles.length} JavaScript bundles scanned).`);
