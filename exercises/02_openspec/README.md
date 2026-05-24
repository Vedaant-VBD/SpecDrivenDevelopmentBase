# Round 3 — Full SDD with OpenSpec (25 minutes)

## Your job

Same feature, third time. This time you go through OpenSpec 1.2.0.

The branch ships with the OpenSpec CLI pre-initialized for your editor —
slash commands and skills are already in place. You only need to drive the
workflow.

1. Create a working branch:
   ```bash
   git checkout -b openspec-work
   ```

2. In your editor's agent chat, kick off the change proposal. Pick the form
   for your editor:

   - **Cursor**: `/opsx-propose add-csv-export`
   - **Claude Code**: `/opsx:propose add-csv-export`
   - **Antigravity**: ask the agent to run the `opsx-propose` workflow for
     `add-csv-export`
   - **VS Code (Copilot)**: open `.github/prompts/opsx-propose.prompt.md` from
     Copilot Chat

   The agent will run `openspec new change add-csv-export` for you and then
   iteratively create the four artifacts under
   `openspec/changes/add-csv-export/`:
   - `proposal.md` — Why, What Changes, Capabilities, Impact
   - `design.md` — implementation approach
   - `specs/reports/spec.md` — delta spec (`## ADDED Requirements`, etc.)
   - `tasks.md` — atomic, ordered tasks

   The agent will pause and ask clarifying questions. **Answer them deliberately**
   — your answers become the spec.

3. **Review what the agent wrote.** Read each artifact. Edit if anything is
   missing or off. See `HOW_TO_USE_OPENSPEC.md` for the schema. Re-run the
   validator any time:
   ```bash
   openspec validate add-csv-export
   ```

4. Implement. In the agent chat:
   - **Cursor**: `/opsx-apply` (or `/opsx-apply add-csv-export`)
   - **Claude Code**: `/opsx:apply`
   - **Antigravity / VS Code**: invoke the `opsx-apply` workflow

   The agent reads the artifacts, implements one task at a time, and ticks off
   `tasks.md` checkboxes as it goes.

5. Run the tests:
   ```bash
   pytest -q
   ```
   If failures, paste them back into the agent chat and keep going.

6. When tests pass and tasks are complete, archive:
   - **Cursor**: `/opsx-archive add-csv-export`
   - **Claude Code**: `/opsx:archive add-csv-export`
   - **Antigravity / VS Code**: invoke the `opsx-archive` workflow
   - **Or CLI directly**: `openspec archive add-csv-export`

   The archive step validates the change, offers to sync the delta into
   `openspec/specs/reports/spec.md`, then moves the change folder to
   `openspec/changes/archive/YYYY-MM-DD-add-csv-export/`.

> Do **not** paste this README into the agent chat — let the slash commands and
> the OpenSpec skills drive the agent. They already include the right
> instructions.

## Time-box

- 8 min — `/opsx:propose` + answer the agent's clarifying questions + review
  artifacts
- 2 min — `openspec validate` and edit anything the validator complains about
- 12 min — `/opsx:apply` (let it run; answer if it pauses)
- 3 min — verify, `/opsx:archive`, commit

## After the timer

```bash
git add -A && git commit -m "round 3: SDD CSV export"
```

Then ask the facilitator for the post-mortem questions, or run:

```bash
git show checks:02_openspec/checks.md
```

to view them without polluting your working tree.
