# Contributing to war-room

Early days, and ideas are welcome. A few things that keep the project coherent.

## The one rule

Every officer must be a **distinct model of the problem**, not a mood. Before proposing a new seat, ask: does it read a slice of context the others don't, or optimize an objective the others don't? If it's the same model of the problem with a different tone, it's cosmetic diversity — it adds noise, and war-room refuses it. (See [docs/roster.md](docs/roster.md) for the traps already ruled out.)

## What's easy to contribute

- **Rosters** for specific domains (a `war-room/roster.yaml` for web apps, data pipelines, infra…). These are the highest-value, lowest-risk contributions.
- **Sharper officer seeds** — a better signature question, a tighter slice.
- **The validator** (`hooks/validate-dossier.sh`) — more dossier checks that stay *deterministic* (structure, reference resolution). Anything that needs a model to judge does not belong in the hook.

## What needs discussion first

- A new officer in the **default** roster (the bar: a model of the problem the five don't cover).
- Touching the **Tenth Man**'s rules — the right to stay silent and the rotation are load-bearing; changing them changes what war-room is.
- The **dossier format** — downstream tools read it.

## How

war-room is markdown-first. There's nothing to build: edit a skill or a doc, reload the plugin, try it. Open an issue to discuss a direction before a large PR.
