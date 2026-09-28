import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const failures = [];

const packageJson = JSON.parse(fs.readFileSync(path.join(root, "package.json"), "utf8"));
const allDependencies = {
  ...(packageJson.dependencies ?? {}),
  ...(packageJson.devDependencies ?? {}),
};

for (const name of ["three", "@react-three/fiber", "@react-three/drei"]) {
  if (name in allDependencies) failures.push(`Stage 02 must not depend on ${name}`);
}

const sourceRoots = ["src", "worker"];
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

for (const sourceRoot of sourceRoots) collect(path.join(root, sourceRoot));

const forbiddenImports = [
  /from\s+["']three["']/,
  /from\s+["']@react-three\/fiber["']/,
  /from\s+["']@react-three\/drei["']/,
  /import\(["']three["']\)/,
  /import\(["']@react-three\/fiber["']\)/,
  /import\(["']@react-three\/drei["']\)/,
];

for (const file of files) {
  const text = fs.readFileSync(file, "utf8");
  if (forbiddenImports.some((pattern) => pattern.test(text))) {
    failures.push(`${path.relative(root, file)} imports a Stage 03 renderer dependency`);
  }
}

const requiredRoutes = ["/play", "/projects", "/resume", "/ask", "/contact"];
const routeConfig = fs.readFileSync(path.join(root, "src/app/route-config.ts"), "utf8");
for (const route of requiredRoutes) {
  if (!routeConfig.includes(`path: "${route}"`)) failures.push(`missing conventional route: ${route}`);
}

if (failures.length) {
  console.error("FOUNDATION BOUNDARY: FAIL");
  failures.forEach((failure) => console.error(`- ${failure}`));
  process.exit(1);
}

console.log("FOUNDATION BOUNDARY: PASS");
console.log(`source_files_checked=${files.length}`);
console.log("renderer_dependencies=0");
