import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const worldDirectory = path.join(root, "src/world");
const sourceFiles = [];
const collectSources = (directory) => {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const file = path.join(directory, entry.name);
    if (entry.isDirectory()) collectSources(file);
    else if (/\.tsx?$/.test(entry.name)) sourceFiles.push(file);
  }
};
collectSources(worldDirectory);

const failures = [];
for (const file of sourceFiles) {
  const source = fs.readFileSync(file, "utf8");
  if (/\/api\/ask|ask\/client/.test(source)) {
    failures.push(`${path.relative(root, file)} couples the world layer to the Ask API/client`);
  }
}

const overlay = fs.readFileSync(path.join(worldDirectory, "InteractionOverlay.tsx"), "utf8");
if (!/station\.kind === "ask"[\s\S]*?<Link\b[^>]*to="\/ask"[^>]*onClick=\{onClose\}[^>]*>[\s\S]*?Open Ask/.test(overlay)) {
  failures.push("The Ask Terminal must expose an Open Ask router link that closes its overlay");
}

if (failures.length) {
  console.error("WORLD ASK BOUNDARY: FAIL");
  failures.forEach((failure) => console.error(`- ${failure}`));
  process.exit(1);
}

console.log("WORLD ASK BOUNDARY: PASS");
console.log(`world_source_files_checked=${sourceFiles.length}`);
console.log("world_ask_api_client_imports=0");
console.log("terminal_action=/ask");
