# Decision: Use category-specific content authority for Portfolio World

date: 2026-09-28
status: accepted
owners: coordinator
supersedes: none
superseded_by: none

## Context

The rebuild has several partially overlapping sources: a legacy 2025 resume site, a structured profile monorepo, a consulting-positioning repo, sanitized public case studies, a current engineering GitHub profile, individual project repositories, and the currently deployed Ask portfolio.

Treating any one presentation surface as universally authoritative would either preserve stale content or expose more private detail than intended.

## Decision

Portfolio World uses category-specific authority:

- project repository/certification evidence governs technical facts and current status;
- sanitized public case studies govern disclosure boundaries for private work;
- the current public GitHub profile governs current engineering positioning;
- `profile-rejig` governs approved consulting positioning/history of profile decisions;
- `monorepo-profile-content` governs the structured employment timeline;
- the current deployed portfolio is a presentation reference, not a factual source;
- legacy `my-resume-site/main` is historical input only;
- hobbies are direct user-approved content.

Unknown or conflicting information is omitted until resolved.

The application will materialize typed presentation records with source references. Three.js components consume those records and never become fact authorities.

## Consequences

- stale legacy percentages and contact data do not silently survive;
- current engineering and consulting positioning can coexist without inventing a hybrid job title;
- public/private proof boundaries remain explicit;
- content can be updated independently of world geometry;
- future agents can trace why a claim exists without replaying chat history.

## Validation / evidence

- `docs/portfolio-world/CONTENT-CONTRACT.md`
- `docs/portfolio-world/CONTENT-SOURCES.json`
- pinned source snapshots listed in those files.

## Revisit when

- an authoritative resume/CV source supersedes the structured profile history;
- a project changes public/private disclosure status;
- a current contact or public profile URL changes;
- a new canonical profile/content repository is deliberately created.
