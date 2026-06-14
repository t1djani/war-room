<div align="center">

<img src="assets/banner.png" alt="war-room" width="820" />

# war-room

**War-game your hard calls.**
A council of non-colluding officers — plus a dissenter who's *required* to argue against you — returns the strategy that wins, and what would make it lose.

*Five officers, five ways of being wrong about your problem.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-d97757.svg)](https://docs.claude.com/en/docs/claude-code)
[![status: alpha](https://img.shields.io/badge/status-alpha-orange.svg)](#roadmap)

</div>

---

## Quickstart

```bash
/plugin marketplace add t1djani/war-room
/plugin install war-room@war-room
```

Then, on any hard decision:

```bash
/war-room "Postgres or a graph DB for the relationship features?"
```

You get a **STRATEGY**, a **BATTLE-PLAN**, and **HOW-WE-LOSE** — the failure-worlds that would beat the plan, each grounded in a real reference or flagged as speculative. No score. No fake consensus.

**Optional — seat officers that read *your* codebase.** Run this once to swap the generic five for officers mapped to your project's real domains:

```bash
/war-room-roster
```

It scans the project (shallowly), *proposes* a roster, and writes `.war-room/roster.yaml` only after you confirm. Skip it if you just want a fast run — the default `/war-room` never scans.

## The idea

Most "ask several LLMs" tools optimize for **consensus**: poll N models, average, let a chairman synthesize. Averaging throws away the one thing the exercise exists to produce — the angle nobody at the table was looking at.

war-room optimizes for **grounded disagreement**. The "war" is your decision; the room is a council of officers who each model the problem differently, argue toward a strategy, and a mandated dissenter — the **Tenth Man** — whose duty is to build the world where that strategy fails.

> Karpathy/AutoGen optimize consensus by aggregation. war-room produces disagreement *grounded in openable facts*, with *the right to stay silent*, frozen into an auditable dossier.

## Why it is different

Adding "a dissenter" to a prompt is one line; anyone can do it. The moat is the **bundle**, and removing any one piece drops you back to ordinary debate-and-judge:

- **The Tenth Man rotates and runs last.** He's designated *after* a majority emerges, framed as one who *shared* it and now must argue against it (the real Yom Kippour doctrine — you contradict the view you held). He delivers a **dated pre-mortem** — "it's six months out, this failed, here's the mechanism" — not a modal antithesis.
- **He can stay silent.** "No grounded attack → all clear" is a valid, unpenalized output. A dissenter who can *never* shut up is a false-positive generator. This is the load-bearing rule; without it the council manufactures noise.
- **His dissent is scored for predictability.** A mandated dissenter reaches for the *most probable* objection — which is the most banal, the blind spot everyone already anticipated. So before the Tenth Man speaks, an independent agent (blind to him) records the **top-3 objections anyone would predict**. If his objection is in that baseline, it's scored `predictable` — a shared blind spot, not dissent — and he's sent back once for a failure mechanism *outside* the obvious. The score isn't a number; it's a classification grounded in the recorded baseline, auditable after the fact. Nobody else measures whether the disagreement was *obvious*.
- **Grounding is external.** Every objection points at an openable reference (`file:line`, a manifest entry, a doc line) or is marked `speculative`. A check that re-reads the work with the same context that wrote it is theater — so a deterministic [hook](hooks/validate-dossier.sh) verifies the structure and that each reference *resolves*. (It doesn't judge whether the reference *supports* the claim — that stays human, and stays honest about being stochastic.)
- **The output is a frozen dossier.** A multi-agent debate is stochastic; war-room never pretends its verdict replays identically. The artifact is the *frozen, auditable record* — positions, grounded objections, and the Commander's sealed call.

## The council

The human is **the Commander**: presides, hears the council, and makes the call. The officers advise; the Commander seals.

| Officer | Models the problem as | Signature question |
|---|---|---|
| **The Scout** | fact vs assumption | "Do we *know* this or *assume* it?" |
| **The Strategist** | the option space | "What's the third option?" |
| **The Marshal** | payoff vs opportunity cost | "Which option wins, and what do we lose by doing nothing?" |
| **The Quartermaster** | feasibility, what breaks | "Which link snaps first?" |
| **The Tenth Man** | refuting the consensus itself | "Assume we already lost — what killed us?" |

Each officer is a *distinct model of the problem*, not a mood — different tone with the same model is cosmetic diversity, and war-room refuses it. Full reasoning and sources in [docs/roster.md](docs/roster.md).

## The output

```
STRATEGY: Postgres now; revisit a graph DB only if traversal depth > 3 becomes a hot path.
  why-it-wins: ships the relationship features on the stack the team runs, with a named exit condition.

BATTLE-PLAN:
  - model relationships as adjacency tables; add recursive CTEs behind a repository port.
  - put a benchmark gate on traversal latency so the exit condition is measurable.

BASELINE:                       # the obvious objections, recorded before the Tenth Man, blind to him
  - "a graph DB would be faster for deep traversal"
  - "migrating later will be expensive"
  - "the team has no graph experience"

HOW-WE-LOSE:
  - by: The Quartermaster
    axis: feasibility
    claim: recursive CTEs degrade past ~4 hops on the current instance size.
    grounding: docs/benchmarks/traversal.md:12
    status: not-defused
  - by: The Tenth Man
    axis: refuting the consensus
    claim: "we lock into adjacency tables, then the product pivots to graph-native features and the migration costs a quarter."
    grounding: speculative
    failure-world: "Q4 — recommendations need 6-hop traversal; we rewrite the data layer under deadline."
    predictability: novel        # not in the baseline — a real blind spot, not the obvious risk
    status: bet-accepted
```

### See it on a real decision

[`examples/sample-dossier.md`](examples/sample-dossier.md) (and its [rendered HTML](examples/sample-dossier.html)) is an actual war-room run on *"monorepo or two separate repos for a small team's two services?"*. The four officers converged on two-repos-contract-first. Then the Tenth Man scored `novel` on something the baseline missed: a schema-contract test checks column names and types, but this boundary breaks *inside the values* — a green CI check certifies a broken contract right up until the product ships a confidently wrong answer. That objection reshaped the battle plan (test data invariants, not schema shape). That is the loop working: the mandated dissent changed the decision.

## How it works

**Cost scales to the stakes.** `quick` (default) runs the officers on a fast model and reserves the strong model for the Tenth Man (his job is the hardest). `thorough` runs every officer on the strong model for irreversible, expensive-to-reverse, or security-sensitive calls.

**One file adapts it to your project.** Drop a `.war-room/roster.yaml` to swap the generic officers for your real domains — each keeps a persona, its slice becomes a real slice of your codebase. Everything else is generic. See [examples/roster.example.yaml](examples/roster.example.yaml). Don't want to write it by hand? Run `/war-room-roster` once — it scans the project, *proposes* a roster, and writes it only after you confirm. It's opt-in: the default `/war-room` never scans, so a normal run stays instant.

**It knows when *not* to run.** If a named oracle — a test, a spec, an invariant — could settle the question, war-room says so and stops. A debate over a decidable fact is theater; verify it instead.

**Text first, HTML on request.** The dossier is a plain-text file — auditable, diff-able, checked by the hook. When you want to share or screenshot it, `/war-room-render` turns it into a styled, dependency-free HTML page (the text stays the source of truth; the page is just a view).

**Plugin layout**

```
war-room/
├── .claude-plugin/{plugin.json, marketplace.json}
├── skills/war-room/      # the council and the procedure — markdown, this is the core
├── commands/             # /war-room, /war-room-roster, /war-room-render
├── hooks/                # validate-dossier.sh — deterministic structure + grounding check
├── scripts/              # render-dossier.py — dossier → self-contained HTML (stdlib)
├── examples/             # a roster to copy
└── docs/                 # the roster reference + sources
```

## Develop

war-room is markdown-first: the skill is prose, the roster is YAML, the structure check is bash. Nothing to build — edit a skill, reload the plugin, done.

## Contributing

Early days. Issues and ideas welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE) © t1djani

---

## Roadmap

- [x] **The council** · five officers, each a distinct model of the problem, grounded in decision-science.
- [x] **The Tenth Man** · rotating, dated pre-mortem, right to stay silent.
- [x] **The dossier** · STRATEGY / BATTLE-PLAN / BASELINE / HOW-WE-LOSE, with a deterministic structure check.
- [x] **Predictability scoring** · a dissent that lands in the recorded top-3 obvious objections is scored a shared blind spot, not dissent.
- [x] **Roster discovery** · opt-in `/war-room-roster` scans the project and proposes a domain roster — the default never scans.
