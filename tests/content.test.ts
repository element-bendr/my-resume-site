import { describe, expect, it } from "vitest";
import { experience, hobbies, identity, projects, skills, sources } from "../src/content";

describe("portfolio content contract", () => {
  const sourceIds = new Set(sources.map((source) => source.id));

  it("uses the approved public identity surface", () => {
    expect(identity.name).toBe("Vijay Kumaran");
    expect(identity.publicEmail).toBe("element.bendr@gmail.com");
    expect(JSON.stringify(identity)).not.toContain("vijju83@gmail.com");
  });

  it("keeps source references resolvable", () => {
    const records = [identity, ...experience, ...projects, ...skills];
    for (const record of records) {
      expect(record.sourceRefs.length).toBeGreaterThan(0);
      for (const ref of record.sourceRefs) expect(sourceIds.has(ref)).toBe(true);
    }
    for (const project of projects) {
      for (const ref of project.proofRefs) expect(sourceIds.has(ref)).toBe(true);
    }
  });

  it("does not expose numeric proficiency scores", () => {
    for (const skill of skills) {
      expect(skill).not.toHaveProperty("score");
      expect(skill).not.toHaveProperty("percentage");
      expect(skill).not.toHaveProperty("proficiency");
      expect(skill.label).not.toMatch(/\d{1,3}\s*%/);
    }
  });

  it("keeps hobbies explicitly user approved", () => {
    expect(hobbies.length).toBeGreaterThan(0);
    for (const hobby of hobbies) expect(hobby.source).toBe("user-approved");
  });

  it("contains only the verified employment records frozen in Stage 01", () => {
    expect(experience.map((entry) => entry.organization)).toEqual([
      "V-Infinity",
      "HCL Comnet Ltd",
      "NIIT Limited",
    ]);
  });

  it("does not smuggle unresolved education into the content registry", () => {
    expect(JSON.stringify({ identity, experience, projects, skills, hobbies }).toLowerCase()).not.toContain(
      "\"education\"",
    );
  });
});
