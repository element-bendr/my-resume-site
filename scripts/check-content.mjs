import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const contentDir = path.join(root, "src", "content");
const requiredFiles = [
  "identity.json",
  "experience.json",
  "projects.json",
  "skills.json",
  "hobbies.json",
  "links.json",
  "sources.json",
];

const failures = [];

const readJson = (name) => {
  const file = path.join(contentDir, name);
  if (!fs.existsSync(file)) {
    failures.push(`missing content file: src/content/${name}`);
    return null;
  }
  try {
    return JSON.parse(fs.readFileSync(file, "utf8"));
  } catch (error) {
    failures.push(`invalid JSON in src/content/${name}: ${error.message}`);
    return null;
  }
};

const walk = (value, cursor, visit) => {
  visit(value, cursor);
  if (Array.isArray(value)) {
    value.forEach((item, index) => walk(item, `${cursor}[${index}]`, visit));
  } else if (value && typeof value === "object") {
    Object.entries(value).forEach(([key, item]) =>
      walk(item, cursor ? `${cursor}.${key}` : key, visit),
    );
  }
};

const uniqueIds = (items, label) => {
  if (!Array.isArray(items)) {
    failures.push(`${label} must be an array`);
    return;
  }
  const seen = new Set();
  for (const item of items) {
    if (!item || typeof item.id !== "string" || !item.id) {
      failures.push(`${label} contains an entry without a non-empty id`);
      continue;
    }
    if (seen.has(item.id)) failures.push(`${label} contains duplicate id: ${item.id}`);
    seen.add(item.id);
  }
};

const identity = readJson("identity.json");
const experience = readJson("experience.json");
const projects = readJson("projects.json");
const skills = readJson("skills.json");
const hobbies = readJson("hobbies.json");
const links = readJson("links.json");
const sources = readJson("sources.json");

for (const name of requiredFiles) {
  if (!fs.existsSync(path.join(contentDir, name))) {
    failures.push(`required content file missing: ${name}`);
  }
}

const allData = { identity, experience, projects, skills, hobbies, links, sources };

walk(allData, "content", (value, cursor) => {
  if (typeof value === "string") {
    if (/vijju83@gmail\.com/i.test(value)) {
      failures.push(`${cursor} contains legacy email vijju83@gmail.com`);
    }
    if (/\b\d{1,3}\s*%\b/.test(value) || /\b\d{1,3}%/.test(value)) {
      failures.push(`${cursor} contains a numeric percentage claim: ${value}`);
    }
  }
  if (value && typeof value === "object" && !Array.isArray(value)) {
    for (const key of Object.keys(value)) {
      if (/phone/i.test(key)) failures.push(`${cursor} contains prohibited phone field: ${key}`);
      if (/education/i.test(key)) failures.push(`${cursor} contains unresolved education field: ${key}`);
      if (/score|percentage|proficiency/i.test(key)) {
        failures.push(`${cursor} contains prohibited skill-scoring field: ${key}`);
      }
    }
  }
});

if (fs.readdirSync(contentDir).some((name) => /education/i.test(name))) {
  failures.push("education content file exists before education is verified");
}

if (identity?.publicEmail !== "element.bendr@gmail.com") {
  failures.push("identity.publicEmail must be element.bendr@gmail.com");
}
if (identity?.name !== "Vijay Kumaran") failures.push("identity.name must be Vijay Kumaran");

uniqueIds(experience, "experience");
uniqueIds(projects, "projects");
uniqueIds(skills, "skills");
uniqueIds(hobbies, "hobbies");
uniqueIds(links, "links");
uniqueIds(sources, "sources");

const sourceIds = new Set(Array.isArray(sources) ? sources.map((source) => source.id) : []);
const assertSourceRefs = (record, label) => {
  if (!Array.isArray(record?.sourceRefs) || record.sourceRefs.length === 0) {
    failures.push(`${label} has no sourceRefs`);
    return;
  }
  for (const sourceRef of record.sourceRefs) {
    if (!sourceIds.has(sourceRef)) failures.push(`${label} references unknown source: ${sourceRef}`);
  }
};

if (identity) assertSourceRefs(identity, "identity");
for (const entry of experience ?? []) assertSourceRefs(entry, `experience:${entry.id}`);
for (const project of projects ?? []) {
  assertSourceRefs(project, `project:${project.id}`);
  for (const proofRef of project.proofRefs ?? []) {
    if (!sourceIds.has(proofRef)) failures.push(`project:${project.id} has unknown proofRef: ${proofRef}`);
  }
  for (const link of project.publicLinks ?? []) {
    try {
      const url = new URL(link.url);
      if (url.protocol !== "https:") failures.push(`project:${project.id} uses non-HTTPS public URL`);
    } catch {
      failures.push(`project:${project.id} has invalid URL: ${link.url}`);
    }
  }
}
for (const skill of skills ?? []) assertSourceRefs(skill, `skill:${skill.id}`);

for (const hobby of hobbies ?? []) {
  if (hobby.source !== "user-approved") failures.push(`hobby:${hobby.id} must be user-approved`);
}

for (const link of links ?? []) {
  try {
    const url = new URL(link.href);
    if (!["https:", "mailto:"].includes(url.protocol)) {
      failures.push(`link:${link.id} uses unsupported protocol: ${url.protocol}`);
    }
  } catch {
    failures.push(`link:${link.id} has invalid href: ${link.href}`);
  }
}

if (failures.length > 0) {
  console.error("CONTENT CHECK: FAIL");
  for (const failure of [...new Set(failures)]) console.error(`- ${failure}`);
  process.exit(1);
}

console.log("CONTENT CHECK: PASS");
console.log(`projects=${projects.length}`);
console.log(`experience=${experience.length}`);
console.log(`skills=${skills.length}`);
console.log(`hobbies=${hobbies.length}`);
console.log(`sources=${sources.length}`);
