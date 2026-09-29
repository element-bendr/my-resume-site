import experienceData from "./experience.json";
import hobbiesData from "./hobbies.json";
import identityData from "./identity.json";
import linksData from "./links.json";
import projectsData from "./projects.json";
import skillsData from "./skills.json";
import sourcesData from "./sources.json";
import type {
  ExperienceContent,
  HobbyContent,
  IdentityContent,
  LinkContent,
  ProjectContent,
  SkillContent,
  SourceContent,
} from "./types";

export const identity = identityData as IdentityContent;
export const experience = experienceData as ExperienceContent[];
export const projects = projectsData as ProjectContent[];
export const skills = skillsData as SkillContent[];
export const hobbies = hobbiesData as HobbyContent[];
export const links = linksData as LinkContent[];
export const sources = sourcesData as SourceContent[];

export const featuredProjects = projects.filter((project) => project.featured);
