# New Repository Bootstrap Contract

Every new `element-bendr` repository should originate from `element-bendr/icm-repo-template@main`.

## Required bootstrap sequence

1. Create the repository from the GitHub template.
2. Keep `main` as the clean canonical integrated baseline.
3. Replace placeholders in `CONTEXT.md` and `HANDOFF.md`.
4. Record repository class, risk tier, runtime/dependency role, CI policy, and protected state.
5. Record the inherited template `VERSION` or source commit.
6. Review `AGENTS.md` and add only project-specific policy that is genuinely needed.
7. Record durable architecture or scope decisions under `decisions/` using `templates/icm/DECISION.md` when applicable.
8. For substantial initial work, create a managed workflow with `workflow_new.py`, complete its stage contract, and activate it with `workflow_activate.py` before implementation.
9. Use isolated branches/worktrees for substantial, risky, or parallel implementation.
10. Give parallel lanes explicit ownership and non-overlapping write boundaries.
11. Run `python3 scripts/bootstrap_check.py`.
12. Run `python3 scripts/workflow_check.py`.
13. Select CI deliberately: keep it absent for low-risk repositories, or copy `templates/icm/.github/workflows/context-integrity.yml` into `.github/workflows/` when automated enforcement is justified.
14. Update `HANDOFF.md` before ending unfinished work, before delegation, and at stage/certification boundaries.
15. For managed work, use `workflow_certify_check.py` / `workflow_certify.py` before `workflow_complete.py`; do not manually bypass terminal-state checks.

## Do not inherit

New repositories must not inherit:

- ideas/research/chat archives from other repositories;
- completed workflows from the template's own development history;
- unrelated project decisions;
- credentials or environment-specific secrets.

## Default creation rule

Use this template rather than starting from an empty repository. An intentional exception must be documented in the new repository's first decision record.

## Bootstrap validation

`scripts/bootstrap_check.py` fails while required project identity, handoff values, or enums are invalid.

The canonical template itself intentionally contains placeholders, so its self-test uses:

```bash
python3 scripts/bootstrap_check.py --template
```

A child repository must use normal mode:

```bash
python3 scripts/bootstrap_check.py
```

## GitHub CLI

Once GitHub's **Template repository** setting is enabled, the canonical creation pattern is:

```bash
gh repo create element-bendr/<new-repo> --private --template element-bendr/icm-repo-template --clone
```

Adjust visibility only when explicitly required.
