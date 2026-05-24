# OpenSpec in three minutes (1.2.0)

OpenSpec is a tiny CLI + a set of agent slash commands that organize specification work
the way `git` organizes code: the current state of the spec lives somewhere stable, and
changes are proposed as *deltas* that are reviewed, implemented, and then folded back in.

## Directory layout

```
openspec/
├── project.md                          Project-level context (read by AI tools)
├── config.yaml                         OpenSpec schema + per-artifact rules
├── specs/                              THE source of truth
│   └── reports/spec.md                 The live spec for the "reports" capability
└── changes/                            Active proposals
    └── add-csv-export/                 One change you're working on
        ├── .openspec.yaml              Schema selection (created by `openspec new change`)
        ├── proposal.md                 Why, What Changes, Capabilities, Impact
        ├── design.md                   How — implementation approach
        ├── tasks.md                    Atomic, ordered, agent-executable
        └── specs/reports/spec.md       Delta spec — ADDED/MODIFIED/REMOVED requirements
```

After `openspec archive`, the change folder moves to
`openspec/changes/archive/YYYY-MM-DD-<name>/`.

## Recommended workflow — agent slash commands

This is the 1.2.0 path. The branch ships with the slash commands pre-installed for
your editor; you don't run `openspec init` yourself.

| Step | Command (in your editor's agent chat) | What happens |
| --- | --- | --- |
| 1 | `/opsx:propose add-csv-export` (or describe the idea — the agent will name it) | Agent runs `openspec new change`, then iteratively creates `proposal.md` → `design.md` + delta `specs/...` → `tasks.md`, asking clarifying questions when needed. |
| 2 | Review the artifacts the agent wrote. Edit anything that's off. | Re-run `openspec status --change <name>` to see what's done vs blocked. |
| 3 | `/opsx:apply` (or `/opsx:apply add-csv-export`) | Agent reads the artifacts, implements one task at a time, ticks off `- [ ]` → `- [x]` in `tasks.md`. |
| 4 | Run `pytest -q`. If failures, paste back to agent and continue. | Iterate within `/opsx:apply`. |
| 5 | `/opsx:archive add-csv-export` | Agent validates the change, offers to sync the delta into the live spec, then moves the folder under `archive/`. |

Per editor (also documented in `SETUP.md` §6):
- **Cursor**: `/opsx-propose`, `/opsx-apply`, `/opsx-archive`, `/opsx-explore`
- **Claude Code**: `/opsx:propose`, `/opsx:apply`, `/opsx:archive`, `/opsx:explore`
- **Antigravity**: invoke the workflow by name (`opsx-propose`, etc.)
- **VS Code (Copilot)**: select the `.github/prompts/opsx-*.prompt.md` file from
  Copilot Chat

## Underlying CLI (what the slash commands call)

You can also drive the workflow by hand. Useful when you want to learn what the agent
is doing, or in CI:

```bash
openspec new change add-csv-export        # creates openspec/changes/add-csv-export/ with .openspec.yaml
openspec status --change add-csv-export   # see which artifacts are ready / blocked / done

# Fetch the template + rules for one artifact, then edit the file under
# openspec/changes/add-csv-export/<path>:
openspec instructions proposal --change add-csv-export
openspec instructions design   --change add-csv-export
openspec instructions specs    --change add-csv-export
openspec instructions tasks    --change add-csv-export

openspec validate add-csv-export          # catch malformed deltas
openspec archive  add-csv-export          # move under archive/YYYY-MM-DD-<name>/
```

The validator enforces:
- Every spec has `## Purpose` and `## Requirements` sections.
- Every `### Requirement: <name>` block has at least one `#### Scenario: <name>` child.
- Delta spec files use `## ADDED Requirements`, `## MODIFIED Requirements`, and/or
  `## REMOVED Requirements` as top-level partitions.

> **Note:** `openspec change add` from earlier OpenSpec versions was removed in 1.2.0.
> Use `openspec new change <name>` instead.

## Delta-spec syntax

Inside `openspec/changes/add-csv-export/specs/reports/spec.md`:

```markdown
## ADDED Requirements

### Requirement: Export reports as CSV
THE system SHALL expose `GET /reports.csv` returning the filtered dataset as RFC 4180 CSV.

#### Scenario: filter parity
- **WHEN** the user passes the same filters as to `GET /reports`
- **THEN** the CSV SHALL contain exactly those rows

#### Scenario: row cap
- **WHEN** the matching dataset exceeds 100,000 rows
- **THEN** the response SHALL be HTTP 413 with a structured error
```

The headers `## ADDED Requirements`, `## MODIFIED Requirements`, and
`## REMOVED Requirements` partition the delta. The validator and archive step use these
to merge into the live spec.

## Why this layout matters

- **Reviewable.** Reviewers diff one short proposal, not a 500-line PR.
- **Audit trail.** Every change to the system's behavior has a named proposal that
  gets archived with the date it landed.
- **Resilient to model upgrades.** The spec survives any LLM regeneration.
