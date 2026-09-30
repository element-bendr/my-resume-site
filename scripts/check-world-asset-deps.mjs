import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const assetRoot = path.join(root, "public", "world", "assets");
const failures = [];
const gltfs = [];

const visit = (dir) => {
  if (!fs.existsSync(dir)) return;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) visit(full);
    else if (entry.isFile() && entry.name.endsWith(".gltf")) gltfs.push(full);
  }
};
visit(assetRoot);

for (const file of gltfs) {
  let document;
  try {
    document = JSON.parse(fs.readFileSync(file, "utf8"));
  } catch {
    failures.push(`${path.relative(root, file)} is not valid JSON`);
    continue;
  }
  const refs = [...(document.buffers ?? []), ...(document.images ?? [])]
    .map((entry) => entry.uri)
    .filter((uri) => typeof uri === "string");
  for (const uri of refs) {
    if (/^(?:data:|https?:|\/)/i.test(uri)) {
      failures.push(`${path.relative(root, file)} has remote/embedded URI: ${uri}`);
      continue;
    }
    const resolved = path.resolve(path.dirname(file), uri);
    if (!resolved.startsWith(assetRoot + path.sep) || !fs.existsSync(resolved)) {
      failures.push(`${path.relative(root, file)} missing dependency: ${uri}`);
    }
  }
}

if (failures.length) {
  console.error("WORLD ASSET DEPS: FAIL");
  failures.forEach((failure) => console.error(`- ${failure}`));
  process.exit(1);
}
console.log("WORLD ASSET DEPS: PASS");
console.log(`gltf_files_checked=${gltfs.length}`);
