# Local execution control plane

This directory is the durable Git-side queue/result/review surface for the ICM local execution bridge.

```text
queue/<task-id>.json
results/<task-id>.json
reviews/<task-id>.json
```

Do not commit local runner policies, credentials, tokens, worktree locks or recovery state here. Those belong under machine-local `.icm-local/` or another protected local path.

Project-specific execution rules live in `docs/portfolio-world/BLENDER-AUTONOMOUS-EXECUTION.md`.
