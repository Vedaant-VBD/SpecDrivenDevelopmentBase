# Round 1 — Vibe code it (30 minutes)

## Your job

You are the engineer. The product manager Slacks you the message in `PROMPT.md`.
Open Cursor's Composer (Cmd/Ctrl-I), paste the message verbatim, and let the agent
do its thing. Do not write or edit any spec. Do not read the agent's diff carefully.
**Accept what it generates.** Run the tests. If they fail, paste the failure into Composer
and ask the agent to fix it. Repeat.

This is "vibe coding" as Andrej Karpathy named it in February 2025: prompt, accept, run,
re-prompt.

## Rules

1. Do not write a spec, a plan, or acceptance criteria.
2. Do not write any code by hand. Everything goes through Composer.
3. Time-box yourself at **25 minutes of building** + **5 minutes of reflection**.

## Branch

Create a working branch so we can diff later:

```bash
git checkout -b vibe-work
```

## After the timer

Commit whatever you have:

```bash
git add -A && git commit -m "round 1: vibe-coded CSV export"
```

Then ask the facilitator for the post-mortem questions, or run:

```bash
git show checks:00_vibe_coding/checks.md
```

to view them without polluting your working tree.
