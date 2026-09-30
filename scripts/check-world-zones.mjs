import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const failures = [];

const requiredDistricts = [
  "BuildLab.tsx",
  "AutomationLab.tsx",
  "ClientStreet.tsx",
  "TimelineCorridor.tsx",
  "HobbyDistrict.tsx",
];

for (const file of requiredDistricts) {
  const relative = path.join("src", "world", "districts", file);
  if (!fs.existsSync(path.join(root, relative))) failures.push(`missing district module: ${relative}`);
}

const topology = fs.readFileSync(path.join(root, "src/world/world-topology.ts"), "utf8");
for (const zone of ["command-center","build-lab","automation-lab","client-street","timeline","hobby-district"]) {
  if (!topology.includes(`id: "${zone}"`)) failures.push(`topology missing zone: ${zone}`);
}
for (const bridge of ["bridge-client","bridge-hobby","bridge-timeline","bridge-build","bridge-automation"]) {
  if (!topology.includes(`id: "${bridge}"`)) failures.push(`topology missing bridge: ${bridge}`);
}

const topologyView = fs.readFileSync(path.join(root, "src/world/WorldTopology.tsx"), "utf8");
if (!topologyView.includes('zone.id !== "command-center" ?')) {
  failures.push("non-command-center zone labels must remain mounted during fast travel");
}
if (!topologyView.includes('visibility: zone.id === currentZone ? "hidden" : "visible"')) {
  failures.push("the current zone label must be hidden without removing its Drei Html portal");
}

const districts = fs.readFileSync(path.join(root, "src/world/WorldDistricts.tsx"), "utf8");
for (const moduleName of ["BuildLab","AutomationLab","ClientStreet","TimelineCorridor","HobbyDistrict"]) {
  if (!districts.includes(`lazy(() => import("./districts/${moduleName}"))`)) {
    failures.push(`${moduleName} must remain a dynamic district boundary`);
  }
}

const entry = fs.readFileSync(path.join(root, "src/world/WorldEntry.tsx"), "utf8");
for (const token of ["loadedZones","onFastTravel={fastTravel}","parseZoneId","<WorldTopology","<WorldDistricts"]) {
  if (!entry.includes(token)) failures.push(`WorldEntry missing Stage 04 contract token: ${token}`);
}

const player = fs.readFileSync(path.join(root, "src/world/PlayerController.tsx"), "utf8");
if (!player.includes("constrainToWalkableWorld")) failures.push("PlayerController must use the shared legal-area union");
if (!player.includes("onZoneChange")) failures.push("PlayerController must publish district transitions");

const hud = fs.readFileSync(path.join(root, "src/world/WorldHud.tsx"), "utf8");
if (!hud.includes("onFastTravel")) failures.push("WorldHud must expose map fast travel");
if (!hud.includes("world-map-destination")) failures.push("WorldHud must render real district destinations");

const pkg = JSON.parse(fs.readFileSync(path.join(root, "package.json"), "utf8"));
const direct = { ...(pkg.dependencies ?? {}), ...(pkg.devDependencies ?? {}) };
for (const forbidden of ["@react-three/rapier","@react-three/cannon","cannon-es","ammo.js","recast-navigation","yuka"]) {
  if (forbidden in direct) failures.push(`Stage 04 must not add physics/navmesh dependency: ${forbidden}`);
}

if (failures.length) {
  console.error("WORLD ZONES: FAIL");
  failures.forEach((failure) => console.error(`- ${failure}`));
  process.exit(1);
}
console.log("WORLD ZONES: PASS");
console.log("district_modules=5");
console.log("bridge_contracts=5");
console.log("shared_player_controller=1");
console.log("direct_physics_navmesh_dependencies=0");
