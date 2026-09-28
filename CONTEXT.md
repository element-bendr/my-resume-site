# Repository Context

## Identity
Project: Vijay Kumaran Portfolio World
Repository: element-bendr/my-resume-site
Purpose: Build and operate a recruiter-friendly interactive 3D portfolio/resume world while preserving a conventional portfolio fallback.

Repository class: production-system
Risk tier: medium
Runtime/dependency role: standalone
CI policy: required

## Authority
This repository is authoritative for implementation, decisions, content contracts, validation evidence, and durable project context. Reusable ICM mechanics are governed by `element-bendr/icm-repo-template`.

## Architecture boundaries
In scope:
- preserve `main` until the rebuild is certified;
- build on `feat/portfolio-world-icm-rebuild`;
- React + TypeScript + Vite;
- Three.js via React Three Fiber/Drei;
- 3D command center, project/build/automation/client/timeline/hobby zones, and Ask terminal;
- first-class conventional HTML resume/project/contact routes;
- Cloudflare Workers Static Assets plus Worker API only where needed;
- progressive loading, mobile/low-power/reduced-motion behavior, strict asset budgets.

Out of scope:
- multiplayer, accounts, persistent achievements;
- D1/KV/Durable Objects/R2 without measured need;
- changes to unrelated repositories;
- fabricated resume claims, project metrics, skills, or outcomes.

## Protected state
- `main` and current production baseline;
- verified public resume/project claims;
- secrets and credentials;
- external client sites/repositories;
- deployment/domain configuration until promotion.

## Entry path
Read `AGENTS.md`, then this file, then `HANDOFF.md`, then the active workflow contract.

## Template adoption
Adopted template: ICM 2.1.0
Template source commit: 90322a2441539f24eafdbd2c8a36bc6392192af4
Adoption branch: feat/portfolio-world-icm-rebuild

This repository predates the canonical template, so adoption is a deliberate isolated-branch migration.
