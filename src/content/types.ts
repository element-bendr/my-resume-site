export type WorldZone =
  | "command-center"
  | "build-lab"
  | "automation-lab"
  | "client-street"
  | "timeline"
  | "hobby-district"
  | "ask-terminal";

export interface IdentityContent {
  name: string;
  consultingTitle: string;
  engineeringPositioning: string;
  tagline: string;
  summary: string;
  location: string;
  publicEmail: string;
  sourceRefs: string[];
}

export interface ExperienceContent {
  id: string;
  organization: string;
  role: string;
  period: string;
  summary: string;
  highlights: string[];
  sourceRefs: string[];
}

export interface PublicLink {
  label: string;
  url: string;
}

export interface ProjectContent {
  id: string;
  title: string;
  shortSummary: string;
  status: string;
  visibility: string;
  technologies: string[];
  publicLinks: PublicLink[];
  proofRefs: string[];
  sourceRefs: string[];
  worldZone: WorldZone;
  featured: boolean;
}

export interface SkillContent {
  id: string;
  label: string;
  category: string;
  sourceRefs: string[];
}

export interface HobbyContent {
  id: string;
  label: string;
  worldMotif: string;
  source: "user-approved";
}

export interface LinkContent {
  id: string;
  label: string;
  href: string;
  kind: "email" | "github" | "proof" | "website";
}

export interface SourceContent {
  id: string;
  label: string;
  visibility: "public" | "internal-reference";
  href?: string;
}
