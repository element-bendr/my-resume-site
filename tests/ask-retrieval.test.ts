import { describe, expect, it } from "vitest";
import { evidenceRegistry } from "../src/ask/evidence";
import { normalizeText, tokenize } from "../src/ask/normalize";
import { retrieveEvidence } from "../src/ask/retrieve";
import { sources } from "../src/content";

describe("grounded Ask evidence retrieval", () => {
  it("normalizes diacritics, punctuation, and repeated whitespace deterministically", () => {
    expect(normalizeText("  Café—WORKERS   / D1! ")).toBe("cafe workers d1");
    expect(tokenize("What technologies has Vijay used?")).toEqual(["technologies", "used"]);
  });

  it("retrieves project-name and curated alias queries", () => {
    expect(retrieveEvidence("Personal Career Acquisition System")[0]).toMatchObject({ kind: "project", id: "pcas" });
    expect(retrieveEvidence("PCAS")[0]).toMatchObject({ kind: "project", id: "pcas" });
    expect(retrieveEvidence("career acquisition system")[0]).toMatchObject({ kind: "project", id: "pcas" });
  });

  it("retrieves technology queries from project evidence", () => {
    const records = retrieveEvidence("Which projects use Cloudflare Workers?");
    expect(records.map(({ id }) => id)).toEqual(["pcas"]);
    expect(records.every((record) =>
      record.kind === "project" && record.facts.type === "project" &&
      record.facts.technologies.some((technology) => normalizeText(technology) === "cloudflare workers"),
    )).toBe(true);

    expect(retrieveEvidence("Which projects use Cloudflare?").map(({ id }) => id)).toEqual(["steelmade"]);
  });

  it("retrieves experience, skill, hobby, and link evidence", () => {
    expect(retrieveEvidence("Where did Vijay work at HCL Comnet?")[0]).toMatchObject({
      kind: "experience",
      id: "hcl-cybersecurity-incident-management",
    });
    expect(retrieveEvidence("Does Vijay use TypeScript?")[0]).toMatchObject({ kind: "skill", id: "typescript" });
    expect(retrieveEvidence("What about anime?")[0]).toMatchObject({ kind: "hobby", id: "anime" });
    expect(retrieveEvidence("GitHub profile link")[0]).toMatchObject({ kind: "link", id: "github" });
  });

  it("orders ties deterministically and fails closed on unsupported queries", () => {
    const first = retrieveEvidence("Cloudflare").map(({ kind, id }) => `${kind}:${id}`);
    expect(retrieveEvidence("Cloudflare").map(({ kind, id }) => `${kind}:${id}`)).toEqual(first);
    expect(first).toEqual(["skill:d1", "skill:r2", "skill:workers", "skill:workflows", "project:newsharness"]);
    expect(retrieveEvidence("What university degree did Vijay receive?")).toEqual([]);
    expect(retrieveEvidence("the who what about")).toEqual([]);
  });

  it("contains unique public-safe records with nonempty facts and resolvable source refs", () => {
    const sourceIds = new Set(sources.map(({ id }) => id));
    const ids = evidenceRegistry.map(({ kind, id }) => `${kind}:${id}`);
    expect(new Set(ids).size).toBe(ids.length);
    for (const record of evidenceRegistry) {
      expect(record.title.trim()).not.toBe("");
      expect(record.searchText.trim()).not.toBe("");
      expect(record.sourceRefs.length).toBeGreaterThan(0);
      for (const ref of record.sourceRefs) expect(sourceIds.has(ref)).toBe(true);
      expect(record).not.toHaveProperty("visibility");
      expect(JSON.stringify(record)).not.toMatch(/\b(?:education|salary|revenue|roi|testimonial|private|internal)\b/i);
      expect(record.searchText).not.toMatch(/\d{1,3}\s*%/);
      expect(record.searchText).not.toContain("vijju83@gmail.com");
      expect(record.searchText).not.toMatch(/\+?\d[\d ()-]{7,}\d/);
    }
  });
});
