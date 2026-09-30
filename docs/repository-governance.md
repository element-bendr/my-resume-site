# Canonical Repository Governance

This policy applies to `element-bendr/icm-repo-template` itself. Child repositories may tailor governance to their own risk tier.

## Maintainer context versus inherited payload

The canonical template repository has one deliberate exception to the ordinary root-context rule:

- root `CONTEXT.md` and `HANDOFF.md` are child-repository bootstrap payloads and intentionally retain placeholders;
- current template-maintainer state lives in `PROVENANCE.md`, `workflow/index.json`, the active workflow context, and completed workflow evidence;
- maintainers must not replace the inherited root payload with transient template-repository state.

This exception applies only to `element-bendr/icm-repo-template`. Repositories created from the template replace the placeholders and then use the normal root context/handoff sequence.

## Main branch

`main` is the canonical released template baseline.

Desired GitHub ruleset for `main`:

- require pull requests before merge;
- require the canonical template self-test check to pass;
- require branches to be up to date before merge when GitHub can evaluate the check reliably;
- block force pushes;
- block branch deletion;
- restrict bypasses to explicit repository administration/emergency use;
- use squash merge for hardening/feature branches so canonical history remains compact;
- delete merged head branches after merge.

Direct implementation work on `main` is not part of the operating model. Emergency administration must be documented afterward in a decision record.

## Template repository setting

GitHub's **Template repository** setting must be enabled for the canonical repository. Verification is complete only when the repository API reports `is_template: true`.

## Releases

A canonical release requires:

1. all template certification gates green;
2. final `main` commit verified;
3. `VERSION` and `CHANGELOG.md` updated;
4. semantic tag `icm-v<version>` created on the validated `main` commit;
5. temporary merged hardening branches deleted.

## Required check

The canonical self-test workflow is `.github/workflows/template-self-test.yml`. It is guarded with a repository-name condition so copies inherited by child repositories do not run as canonical-template self-tests.

## Verification

Repository-side policy files do not prove GitHub settings. Rulesets, branch protection, template flag, branch deletion, and release/tag existence must be verified through GitHub repository metadata or administration UI/API.
