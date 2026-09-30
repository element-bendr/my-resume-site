import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const failures = [];
const pkg = JSON.parse(fs.readFileSync(path.join(root, "package.json"), "utf8"));

const expected = {
  three: "0.186.0",
  "@react-three/fiber": "9.8.0",
  "@react-three/drei": "10.7.8",
};
for (const [name, version] of Object.entries(expected)) {
  if (pkg.dependencies?.[name] !== version) {
    failures.push(`${name} must be pinned exactly to ${version}`);
  }
}
if (pkg.devDependencies?.["@types/three"] !== "0.186.0") {
  failures.push("@types/three must be pinned exactly to 0.186.0");
}

const forbiddenDirect = [
  "@react-three/rapier",
  "@react-three/cannon",
  "cannon-es",
  "ammo.js",
  "recast-navigation",
  "yuka",
];
const direct = { ...(pkg.dependencies ?? {}), ...(pkg.devDependencies ?? {}) };
for (const name of forbiddenDirect) {
  if (name in direct) failures.push(`Stage 03 must not directly depend on ${name}`);
}

const extensions = new Set([".ts", ".tsx", ".js", ".jsx", ".mjs"]);
const files = [];
const collect = (dir) => {
  if (!fs.existsSync(dir)) return;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) collect(full);
    else if (entry.isFile() && extensions.has(path.extname(entry.name))) files.push(full);
  }
};
collect(path.join(root, "src"));

const forbiddenSource = [
  /three\/webgpu/,
  /WebGPURenderer/,
  /@react-three\/rapier/,
  /@react-three\/cannon/,
  /cannon-es/,
  /recast-navigation/,
];
for (const file of files) {
  const source = fs.readFileSync(file, "utf8");
  if (forbiddenSource.some((pattern) => pattern.test(source))) {
    failures.push(`${path.relative(root, file)} violates the Stage 03 renderer/physics boundary`);
  }
}

const play = fs.readFileSync(path.join(root, "src/app/pages/PlayPage.tsx"), "utf8");
const worldEntry = fs.readFileSync(path.join(root, "src/world/WorldEntry.tsx"), "utf8");
if (!/lazy\s*\(\s*\(\)\s*=>\s*import\(["']\.\.\/\.\.\/world\/WorldEntry["']\)/.test(play)) {
  failures.push("/play must lazy-load WorldEntry so 3D code stays out of the conventional shell");
}
if (!worldEntry.includes("detectWebGLSupport")) {
  failures.push("WorldEntry must detect WebGL capability before mounting Canvas");
}
if (!worldEntry.includes("WorldCanvasBoundary")) {
  failures.push("WorldEntry must protect Canvas with a renderer error boundary");
}
if (!worldEntry.includes("<WebGLFallback")) {
  failures.push("WorldEntry must retain a direct non-WebGL fallback");
}

const publicRoot = path.join(root, "public");
const mediaExtensions = new Set([".glb", ".gltf", ".fbx", ".hdr", ".ktx2"]);
const media = [];
const collectMedia = (dir) => {
  if (!fs.existsSync(dir)) return;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) collectMedia(full);
    else if (mediaExtensions.has(path.extname(entry.name).toLowerCase())) media.push(full);
  }
};
collectMedia(publicRoot);
if (media.length) {
  failures.push(`Stage 03 must use procedural geometry only; found: ${media.map((x) => path.relative(root, x)).join(", ")}`);
}

if (failures.length) {
  console.error("WORLD BOUNDARY: FAIL");
  failures.forEach((failure) => console.error(`- ${failure}`));
  process.exit(1);
}
console.log("WORLD BOUNDARY: PASS");
console.log(`source_files_checked=${files.length}`);
console.log("direct_physics_dependencies=0");
console.log("webgpu_imports=0");
console.log("external_3d_assets=0");
