# Portfolio World Content Contract

## Purpose

This document defines what content Portfolio World may publish, where each class of fact comes from, how conflicts are resolved, and how the 3D world consumes that content.

The portfolio is a presentation layer. It is not allowed to become an independent source of professional facts.

Unknown, contradictory, stale, or private information fails closed: omit it until the relevant source is resolved.

## Snapshot

Contract date: 2026-09-28

Pinned source snapshots used to establish this contract:

| Source | Snapshot | Role |
| --- | --- | --- |
| `element-bendr/element-bendr` | `508a3f69da785281684e69a69bef549401b35e8c` | current engineering positioning |
| `element-bendr/ai-automation-case-studies` | `fb03099fa3746c33a441a4cf045d9dfaccbb11e2` | public/sanitized project claims and disclosure boundary |
| `element-bendr/profile-rejig` | `8568ea2517e1558ea038a7ad6153a128d292de7b` | consulting positioning and profile-governance decisions |
| `element-bendr/monorepo-profile-content` | `d7ee030986e5248f303ebecc10e263ef9df75669` | structured employment-history content |
| `element-bendr/my-resume-site` legacy main | `63d25e7dbc3169cb41aaa181a513ca7af5860ba4` | historical presentation reference only |
| current deployed Ask portfolio | public URL observed 2026-09-28 | current presentation reference only, never fact authority |

Project repositories and retained certification evidence may supersede these snapshots for project-specific technical facts and current status.

## Authority model

Authority is category-specific. There is deliberately no single universal content file that outranks every other source.

### 1. Project technical facts

Order of authority:

1. current project repository and retained certification/evidence;
2. public sanitized case study;
3. current public GitHub profile;
4. older profile/portfolio copy.

Use the project repository for:
- architecture;
- technologies actually used;
- tests/certification;
- deployment state;
- current implementation status.

Use the sanitized case study to decide what may safely be stated publicly.

A technically true private detail is not automatically publishable.

### 2. Public disclosure boundary

`element-bendr/ai-automation-case-studies` is the default public-disclosure authority for private systems represented there.

If a private repository contains more detail than the sanitized case study, Portfolio World publishes no more than the case study unless a later explicit public decision authorizes it.

Never publish:
- private source;
- credentials;
- client-private data;
- internal URLs;
- private operational details;
- copied private Git history.

### 3. Current positioning

Two valid positioning contexts are preserved instead of forcing them into one invented universal title.

#### Consulting / client-facing

Primary title:

**AI Automation & Web Systems Consultant**

Supporting proposition:

Build practical websites, business systems, and AI automations that reduce manual work and run reliably every day.

This is the default Command Center / general portfolio positioning.

#### Engineering / role-facing

Engineering positioning:

**AI Systems Engineer · Agentic Infrastructure · Automation · Production Web Systems**

Role-facing surfaces may also describe fit for:
- AI Systems Engineer;
- Agentic Infrastructure Engineer;
- Applied AI Engineer;
- AI Automation Engineer;
- Forward-Deployed AI Engineer;
- Full-Stack AI Engineer.

These are positioning/target-role labels, not employment titles.

Do not silently combine the consulting and engineering titles into a new title.

### 4. Employment history

Primary structured source:

`element-bendr/monorepo-profile-content/apps/web/content/profile.json` at the pinned snapshot above.

Current approved historical entries:

#### V-Infinity

- role: AI Systems Architect, Workflow Orchestrator and Digital Infrastructure Builder - V-Infinity
- period: Sep 2014 - Present
- summary: designed AI-assisted systems across websites, content operations, lead workflows, and client delivery.

#### HCL Comnet Ltd

- role: Cybersecurity and IT Incident Management Specialist
- period: Dec 2009 - May 2013
- summary: process-heavy reliability, documentation, incident/escalation handling, and client-facing issue resolution.

#### NIIT Limited

- role: E-Learning and Content Development Executive
- period: Mar 2007 - Aug 2007
- summary: structured content development, revision cycles, quality checks, and documentation standards.

The legacy `my-resume-site/main` employment text is not authoritative when it conflicts with this structured source.

### 5. Education

The legacy site contains an education statement, but Stage 01 did not locate a newer authoritative source for it.

Therefore education is **unverified for this rebuild** and is excluded from production content until a current authoritative source is added.

Do not repair, infer, or silently modernize the old education wording.

### 6. Contact and identity

Approved public identity:
- name: Vijay Kumaran;
- public portfolio email: `element.bendr@gmail.com`;
- location may be shown as Mumbai, India where a location label is useful.

The old phone number is not carried forward by default.

The old LinkedIn URL is not copied into the new structured content until its current public URL is directly verified.

GitHub may link to the public `element-bendr` profile.

### 7. Skills and technologies

Skills are evidence-backed capabilities, not numerical scores.

Prohibited:
- percentage proficiency bars;
- invented levels such as 90% JavaScript;
- rankings unsupported by evidence;
- adding tools merely because they appear in an old résumé.

Current broad evidence supports categories including:
- TypeScript / JavaScript / Node.js;
- React / Next.js;
- Python;
- Cloudflare Workers / Workflows / D1 / R2;
- PostgreSQL;
- GitHub Actions;
- REST APIs;
- LLM / agent systems;
- production web applications and admin tooling.

A skill may be added when at least one current project/source supports it.

### 8. Project content

Public project cards must distinguish:

- **title** — public-safe project/system name;
- **summary** — short factual description;
- **status** — current evidence-backed state;
- **proof** — public link or evidence reference where available;
- **visibility** — public implementation, sanitized private work, or public live site;
- **technology** — only technologies supported by current evidence;
- **sourceRefs** — one or more authoritative source identifiers;
- **worldZone** — presentation location only.

Initial strong public project sources include:
- PCAS;
- Newsharness;
- Memory OS;
- Trifecta / KPDC;
- SteelMade;
- ChronoQuill;
- ArtSports Content OS;
- Mnemos;
- Governed Runtime / little-agent;
- Palimpsest.

Inclusion in the world is curated separately. The portfolio does not need to render every project just because evidence exists.

### 9. Client work

Client-facing cards may use public-safe names, live URLs, and claims that are supported by public or project evidence.

The current deployed portfolio presentation has used examples such as Sterling Synergies, Sopranos Inc., GreenShoot, and SteelMade.

Before Stage 02 structured content ships a client card, its current public URL and allowed claim set must be resolved into a source reference.

Do not copy testimonials or outcome claims merely because an older/live page contains them.

### 10. Hobbies / personal district

Hobbies are user-authored presentation content rather than externally verified professional claims.

Initial user-approved themes:
- gaming;
- anime;
- kettlebells;
- philosophy;
- tinkering / building things.

Rules:
- keep the district lightweight and personal;
- do not infer sensitive traits from hobbies;
- do not manufacture achievements, rankings, fandom history, or personal stories;
- later additions require direct user approval or an explicit project content decision.

## Legacy-content disposition

The old `my-resume-site/main` is preserved as historical evidence but is not copied wholesale.

### Preserve only after source confirmation

- name;
- historical employer names and periods where confirmed by the structured profile source;
- broad professional history where current sources agree.

### Replace

- old headline and positioning;
- old tech-stack presentation;
- old contact email where it conflicts with the current approved portfolio email;
- old LinkedIn route until verified;
- old client/project framing.

### Reject unless independently re-verified

- skill percentages;
- engagement/traffic/manual-effort/response-time/satisfaction percentage claims from the legacy HTML;
- the old phone number;
- unverified education wording;
- any old metric whose evidence is not present in the current source hierarchy.

## Structured content boundary

Stage 02 should create typed application-owned presentation records, expected to be logically equivalent to:

```text
src/content/
  identity
  experience
  projects
  skills
  hobbies
  links
  sources
```

The exact file format may be TypeScript or JSON.

The content layer must remain independent of Three.js scene components.

### Identity record

Expected fields:
- name;
- consultingTitle;
- engineeringPositioning;
- summary;
- location;
- publicEmail;
- sourceRefs.

### Experience record

Expected fields:
- id;
- organization;
- role;
- period;
- summary;
- highlights;
- sourceRefs.

### Project record

Expected fields:
- id;
- title;
- shortSummary;
- status;
- visibility;
- technologies;
- publicLinks;
- proofRefs;
- sourceRefs;
- worldZone;
- featured.

### Skill record

Expected fields:
- id;
- label;
- category;
- sourceRefs.

No percentage/score field exists in the schema.

### Hobby record

Expected fields:
- id;
- label;
- worldMotif;
- source: user-approved.

### Source registry

Each source reference should include enough data to trace the claim:
- source id;
- repository/document or public URL;
- snapshot/ref when applicable;
- authority category;
- visibility/disclosure rule;
- verification date.

## World rendering rule

3D scene objects are views over structured content.

A machine, building, hologram, timeline marker, or terminal may paraphrase content for visual brevity, but it may not create a new factual claim.

Long-form project/resume content remains HTML-over-3D or conventional HTML routes.

## Conflict resolution

When sources disagree:

1. identify the content category;
2. apply that category's authority order;
3. preserve the safer public-disclosure boundary;
4. record an unresolved state if the conflict remains material;
5. omit the disputed claim from production until resolved.

Do not average conflicting facts. Do not choose whichever copy sounds better.

## Freshness

Project status and quantitative certification claims are time-sensitive.

If surfaced publicly:
- pin them to evidence;
- describe the relevant phase/candidate when necessary;
- do not imply an old certification count is the current total unless revalidated.

Evergreen portfolio cards should prefer durable capability/proof statements over rapidly stale test counts.

## Acceptance criteria

Stage 01 passes when:

1. each content category has an explicit authority source;
2. legacy content is classified as preserve/replace/reject;
3. current public positioning is separated into consulting and engineering contexts;
4. employment history has a structured source;
5. education remains omitted until verified;
6. public contact uses the current approved email and excludes the legacy phone by default;
7. skills have no numeric proficiency scores;
8. private project disclosure is bounded by sanitized public evidence;
9. hobbies are explicitly user-approved rather than inferred;
10. Stage 02 can build typed content records without consulting conversation history;
11. unknowns fail closed rather than becoming invented copy.
