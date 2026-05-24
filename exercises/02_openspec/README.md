# Round 3 — Full SDD with OpenSpec (25 minutes)

## Your job

Same feature, third time. This time you go through OpenSpec.

1. Create a working branch:
   ```bash
   git checkout -b openspec-work
   ```
2. Create a change proposal:
   ```bash
   openspec change add add-csv-export
   ```
   This creates `openspec/changes/add-csv-export/` with three templates:
   `proposal.md`, `tasks.md`, and `specs/reports/spec.md` (the delta).
3. **Fill in the proposal and the delta spec.** (See `HOW_TO_USE_OPENSPEC.md`.) The
   delta spec uses `### Requirement: <name>` blocks with `#### Scenario:` children. The
   tooling will merge it into the live spec on archive.
4. **Validate:**
   ```bash
   openspec validate add-csv-export
   ```
5. In Cursor Composer, attach the change directory to context and ask the agent to
   implement it task by task. Cross off tasks in `tasks.md` as they complete.
6. When the feature works and tests pass:
   ```bash
   openspec archive add-csv-export
   ```
   This folds the delta into `openspec/specs/reports/spec.md` and removes the proposal.

> Do **not** paste this README into Composer — attach the `openspec/changes/add-csv-export/`
> directory instead so the agent sees the proposal, tasks, and delta spec together.

## Time-box

- 7 min — write proposal + delta spec
- 3 min — validate
- 12 min — let Cursor implement against the tasks
- 3 min — verify, archive, commit

## After the timer

```bash
git add -A && git commit -m "round 3: SDD CSV export"
```

Then ask the facilitator for the post-mortem questions, or run:

```bash
git show checks:02_openspec/checks.md
```

to view them without polluting your working tree.
