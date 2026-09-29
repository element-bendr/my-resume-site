import { experience, hobbies, identity, links, projects, skills, sourceIds } from "../content";
import type { EvidenceKind } from "./types";

type EvidenceFacts =
  | { type: "identity"; consultingTitle: string; engineeringPositioning: string; summary: string }
  | { type: "project"; summary: string; technologies: string[] }
  | { type: "experience"; role: string; organization: string; period: string; summary: string; highlights: string[] }
  | { type: "skill"; category: string }
  | { type: "hobby" }
  | { type: "link"; href: string };

export interface EvidenceRecord {
  kind: EvidenceKind;
  id: string;
  title: string;
  sourceRefs: string[];
  aliases: string[];
  searchText: string;
  facts: EvidenceFacts;
}

const projectAliases: Record<string, string[]> = {
  pcas: ["PCAS", "Personal Career Acquisition", "career acquisition system"],
  newsharness: ["news harness", "news intelligence system"],
  "memory-os": ["Memory OS", "agent memory system"],
  "trifecta-kpdc": ["Trifecta", "KPDC", "institutional publishing system"],
};

const projectSummaries: Record<string, string> = {
  // Omit the private admin detail from the public Ask corpus.
  "trifecta-kpdc": "Multi-site institutional publishing system with three public sites, shared packages, publishing workflows, and handover documentation.",
};

function checkedRefs(owner: string, refs: string[]): string[] {
  if (refs.length === 0 || refs.some((ref) => !sourceIds.has(ref))) {
    throw new Error(`Evidence source references are invalid for ${owner}`);
  }
  return [...new Set(refs)];
}

function record(
  kind: EvidenceKind,
  id: string,
  title: string,
  sourceRefs: string[],
  aliases: string[],
  searchable: string[],
  facts: EvidenceFacts,
): EvidenceRecord {
  return {
    kind,
    id,
    title,
    sourceRefs: checkedRefs(`${kind}:${id}`, sourceRefs),
    aliases,
    searchText: [title, ...aliases, ...searchable].join(" "),
    facts,
  };
}

const projectRecords = projects.map((project) =>
  record(
    "project",
    project.id,
    project.title,
    project.sourceRefs,
    projectAliases[project.id] ?? [],
    [projectSummaries[project.id] ?? project.shortSummary, ...project.technologies],
    { type: "project", summary: projectSummaries[project.id] ?? project.shortSummary, technologies: [...project.technologies] },
  ),
);

const experienceRecords = experience.map((entry) =>
  record(
    "experience",
    entry.id,
    entry.organization,
    entry.sourceRefs,
    [],
    [entry.role, entry.period, entry.summary, ...entry.highlights],
    {
      type: "experience",
      role: entry.role,
      organization: entry.organization,
      period: entry.period,
      summary: entry.summary,
      highlights: [...entry.highlights],
    },
  ),
);

const skillRecords = skills.map((skill) =>
  record("skill", skill.id, skill.label, skill.sourceRefs, [], [skill.category], { type: "skill", category: skill.category }),
);

const hobbyRecords = hobbies.map((hobby) =>
  record("hobby", hobby.id, hobby.label, ["user-approved-hobbies"], [], [], { type: "hobby" }),
);

const linkSourceRefs: Record<string, string[]> = {
  email: identity.sourceRefs,
  github: ["public-engineering-profile"],
  "case-studies": ["public-sanitized-case-studies"],
};

const linkRecords = links.map((link) =>
  record(
    "link",
    link.id,
    link.label,
    linkSourceRefs[link.id] ?? [],
    [],
    [link.href],
    { type: "link", href: link.href },
  ),
);

const identityRecord = record(
  "identity",
  "vijay-kumaran",
  identity.name,
  identity.sourceRefs,
  [],
  [identity.consultingTitle, identity.engineeringPositioning, identity.tagline, identity.summary, identity.location],
  {
    type: "identity",
    consultingTitle: identity.consultingTitle,
    engineeringPositioning: identity.engineeringPositioning,
    summary: identity.summary,
  },
);

const allRecords = [...projectRecords, ...experienceRecords, ...skillRecords, ...hobbyRecords, ...linkRecords, identityRecord];
const recordIds = new Set(allRecords.map(({ kind, id }) => `${kind}:${id}`));
if (recordIds.size !== allRecords.length) throw new Error("Evidence record IDs must be unique");

export const evidenceRegistry: readonly EvidenceRecord[] = Object.freeze(allRecords);
