# Changelog

All notable changes to war-room are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/), and versions follow [SemVer](https://semver.org/).

## [0.3.1] — 2026-06-14

### Added
- **Live progress checklist.** The `war-room` skill now drives a TodoWrite checklist — one todo to frame the war, one per officer, one for the Marshal's synthesis, one for the Tenth Man, one to assemble and validate the dossier — so the Commander watches the council convene and resolve instead of waiting on a silent block.

## [0.3.0] — 2026-06-14

### Added
- **Opt-in roster discovery** (`/war-room-roster`, `discover-roster` skill). Scans the project (or reuses a `.servo/manifest.yaml`) to infer 3–5 domains, *proposes* a roster of domain officers, and writes `.war-room/roster.yaml` only after the user confirms. The default `/war-room` never scans — a normal run stays instant.

## [0.2.0] — 2026-06-14

### Added
- **Predictability scoring for the Tenth Man.** Before he speaks, an independent agent (blind to him) records the top-3 predictable objections as a `BASELINE`. Each Tenth Man objection is then scored `predictable` (a shared blind spot) or `novel`; a predictable one sends him back once for a failure mechanism outside the obvious. The score is a classification grounded in the recorded baseline, not a number.
- Dossier gains a `BASELINE` section and a `predictability` field; `validate-dossier.sh` enforces both (the section is required, and a Tenth Man entry must carry a valid `novel`/`predictable` score).

## [0.1.0] — 2026-06-14

First public alpha.

### Added
- **The council** (`war-room` skill) — five officers, each a distinct model of the problem (the Scout, the Strategist, the Marshal, the Quartermaster), grounded in decision science (Six Thinking Hats, Belbin, military staff functions, OODA).
- **The Tenth Man** — the mandated dissenter: rotates, runs last against the emerging consensus, delivers a dated pre-mortem, and is allowed to stay silent.
- **The dossier** — `STRATEGY` / `BATTLE-PLAN` / `HOW-WE-LOSE`, with external grounding (openable reference or `speculative`) and no aggregate score.
- **`validate-dossier.sh`** — a deterministic hook checking dossier structure and that every grounding resolves.
- **`/war-room`** command, an example roster, and the roster reference with sources.
