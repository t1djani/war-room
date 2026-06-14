# Changelog

All notable changes to war-room are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/), and versions follow [SemVer](https://semver.org/).

## [0.1.0] — 2026-06-14

First public alpha.

### Added
- **The council** (`war-room` skill) — five officers, each a distinct model of the problem (the Scout, the Strategist, the Marshal, the Quartermaster), grounded in decision science (Six Thinking Hats, Belbin, military staff functions, OODA).
- **The Tenth Man** — the mandated dissenter: rotates, runs last against the emerging consensus, delivers a dated pre-mortem, and is allowed to stay silent.
- **The dossier** — `STRATEGY` / `BATTLE-PLAN` / `HOW-WE-LOSE`, with external grounding (openable reference or `speculative`) and no aggregate score.
- **`validate-dossier.sh`** — a deterministic hook checking dossier structure and that every grounding resolves.
- **`/war-room`** command, an example roster, and the roster reference with sources.
