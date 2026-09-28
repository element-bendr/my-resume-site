# Active Workflow Selection

Managed workflows may coexist under workflow/active/.

Selection is deterministic:

1. an explicit CLI workflow id wins if it names an active workflow;
2. if exactly one active workflow exists, it may be inferred;
3. if multiple active workflows exist, workflow/index.json must declare a valid primary;
4. directory ordering is never priority;
5. an invalid/stale primary fails closed.

Blocked workflows count as active for selection because they still own unresolved work.

The primary field may be null when no active workflows exist.
