# OpenSpec in three minutes

OpenSpec is a tiny CLI that organizes specification work the way `git` organizes code:
the current state of the spec lives somewhere stable, and changes are proposed as
*deltas* that are reviewed, implemented, and then folded back in.

## Directory layout

```
openspec/
├── project.md                       Project-level context for the AI tool
├── specs/                           THE source of truth
│   └── reports/spec.md              The live spec for the "reports" capability
└── changes/                         Pending proposals
    └── add-csv-export/              One change you're working on
        ├── proposal.md              Why this change, what it does, what's out of scope
        ├── tasks.md                 Atomic, ordered, agent-executable
        └── specs/reports/spec.md    Delta spec — adds/modifies requirements
```

## Workflow

```bash
openspec change add add-csv-export   # create skeleton
# ... edit proposal.md, tasks.md, specs/<capability>/spec.md ...
openspec validate add-csv-export     # catch malformed deltas
# ... implement, with Cursor attached to the change directory ...
openspec archive add-csv-export      # merge delta into specs/, remove proposal
```

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
- **Audit trail.** Every change to the system's behavior has a named proposal.
- **Resilient to model upgrades.** The spec survives any LLM regeneration.
