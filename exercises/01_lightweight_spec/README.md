# Round 2 — Lightweight spec (35 minutes)

## Your job

Same feature as the vibe round. Different process.

1. Create a working branch:
   ```bash
   git checkout -b lightweight-work
   ```
2. Open `SPEC_TEMPLATE.md` and fill it in. You have **15 minutes** for this. Aim for
   one page of prose — no longer. Be concrete: name endpoints, name fields, name error
   codes, write acceptance criteria as Given/When/Then or EARS.
3. In Cursor Composer, attach the spec file you just wrote to the context (the `@` menu
   in Composer) and ask the agent to implement it. **Do not paste casual instructions
   on top of the spec — let the spec do the talking.**
4. Review the diff. Run tests. Iterate.

You have **20 minutes** of building. Time-box hard.

> Do **not** paste this README into Composer — paste only your filled-in `SPEC_TEMPLATE.md`.

## After the timer

Commit whatever you have:

```bash
git add -A && git commit -m "round 2: lightweight-spec CSV export"
```

Then ask the facilitator for the post-mortem questions, or run:

```bash
git show checks:01_lightweight_spec/checks.md
```

to view them without polluting your working tree.
