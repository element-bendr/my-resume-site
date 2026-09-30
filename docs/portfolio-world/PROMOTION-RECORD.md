# Stage 07 promotion record

Status: **MAIN PROMOTED — production deploy pending authenticated Cloudflare execution**

- Exact preview candidate: `27989cb13b989382df69ef2a376f6314f7b9fb6c`
- Certified Stage 06 root: `fe1d15199f06a8a6a2cae22dbc7fa623e75218f6`
- Preview Worker: `vijay-kumaran-portfolio-world-stage07-27989cb`
- Preview URL: <https://vijay-kumaran-portfolio-world-stage07-27989cb.random-planzz.workers.dev>
- Worker version: `e581366f-81ec-4ee3-b0a7-9781fdb6bf19`
- Terra preview review: PASS, no required fixes.
- Stage 07 formal ICM certification: PASS against evidence candidate `9af0df349c721c29ff85c49ecc95cd7f0d63d49d` (preview runtime candidate `27989cb13b989382df69ef2a376f6314f7b9fb6c`).
- Previous `main` baseline: `63d25e7dbc3169cb41aaa181a513ca7af5860ba4`.
- Production promotion PR: #15.
- Certified application merged to `main`: `0c5131d5eb68dc566ea95422a2d80aef2126c373`.
- Production deployment/domain: unchanged after the `main` merge; no deployment evidence exists yet.

Stage 07 is formally certified and the certified application has been promoted to `main`. Production deployment remains pending because the current ChatGPT execution environment has no authenticated Cloudflare connector or repository deployment workflow, and its isolated shell cannot reach external GitHub/Cloudflare hosts. The production release must still execute the repository path `npm run deploy` / `wrangler deploy` from an authenticated Cloudflare environment, followed by health, conventional-route, Ask, `/play`, SPA-exit, fallback, and console/network smoke checks. Do not mark production promotion complete until those deployment and smoke identifiers are recorded here.
