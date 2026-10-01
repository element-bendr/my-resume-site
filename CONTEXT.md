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

This repository is authoritative for implementation, decisions, content contracts, validation evidence, visual-source contracts, and durable project context. Reusable ICM mechanics are governed by `element-bendr/icm-repo-template`.

## Current baseline and active phase

- Certified runtime baseline: `main` at `5f4de7ace37bfd843ef13f035a3b16ddb61f28d7`.
- Earlier Portfolio World workflow `portfolio-world-rebuild`: certified.
- Previous certified application is on `main`; its production deployment/smoke evidence is still pending and remains a separate release concern.
- Current implementation branch: `feat/blender-world-art-pipeline`.
- Current primary workflow: `portfolio-world-blender-art`.
- Current objective: replace primitive-heavy scenery with reproducible Blender-authored GLB assets without changing certified interaction authority.

## Architecture boundaries

In scope:

- React + TypeScript + Vite;
- Three.js via React Three Fiber/Drei;
- Blender 4.5 LTS as the authored scenery toolchain;
- GLB/glTF 2.0 as the browser asset boundary;
- six 3D zones plus Ask Terminal;
- first-class conventional HTML resume/project/contact/Ask routes;
- Cloudflare Workers Static Assets plus Worker API only where needed;
- progressive loading, mobile/low-power/reduced-motion behavior, strict asset budgets;
- production visual QA and rollback/fallback behavior.

Out of scope:

- deriving navigation/collision from Blender meshes;
- changing verified resume/project facts to suit visual design;
- multiplayer, accounts, persistent achievements;
- heavyweight physics without a concrete interaction requirement;
- WebGPU as a mandatory production dependency;
- D1/KV/Durable Objects/R2 without measured need;
- unrelated repository or client-site changes.

## Authority split

React/runtime owns:

- world topology and walkable bounds;
- movement and fast travel;
- interaction station coordinates;
- camera;
- routes;
- content authority;
- accessibility and fallback.

Blender owns:

- authored scenery geometry;
- bevels/curves;
- visual prop placement inside each zone;
- material/UV/bake source;
- later LOD source geometry.

The generated concept art is a visual target only. It is not executable geometry and not a factual source.

## Protected state

- `main` and current production deployment/domain;
- certified movement/topology/camera/interaction semantics;
- verified public resume/project claims;
- Ask grounding/disclosure contract;
- secrets and credentials;
- external client sites/repositories;
- historical certification evidence.

## Entry path

Read:

1. `AGENTS.md`
2. this file
3. `HANDOFF.md`
4. `workflow/active/portfolio-world-blender-art/CONTEXT.md`
5. current stage context only
6. only references explicitly required by that stage

## Template adoption

Adopted template: ICM 2.1.0  
Template source commit: `90322a2441539f24eafdbd2c8a36bc6392192af4`.
