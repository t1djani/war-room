---
name: discover-roster
description: Use ONLY when the user explicitly asks to build a project-specific war-room roster (e.g. via /war-room-roster). Scans the project to infer its domains and proposes a `.war-room/roster.yaml` of domain officers. This is opt-in and heavier than a normal war-room run — never run it automatically, and never write the roster without the user's confirmation.
---

# discover-roster

The default war-room runs five generic officers with zero config — fast, no scan. This skill is the **opt-in upgrade**: it scans the project once, infers its real domains, and proposes a roster where each officer reads a genuine slice of *this* codebase instead of a generic frame. Run it only when the user asks; keep the default light.

The output is a *proposal*. Nothing is written until the user accepts.

## Procedure

1. **Reuse before you scan.** If a `.servo/manifest.yaml` exists, derive the roster from its `experts` (domains + source pointers) — no scan needed. This is the cheap path; prefer it.

2. **Otherwise, scan — once, shallowly.** Read the project's shape, not its contents: top-level layout, the package/build manifest, the `docs/` index, the main source directories. You are looking for **distinct domains** (data, API, frontend, infra, billing…), not every file. Stop once you can name 3–5 domains; do not read the whole tree.

3. **Map each domain to an officer — persona + real slice.** For each domain, propose:
   - a **persona** (the skin) — an evocative war-council title that fits the domain;
   - the **slice** (the skeleton) — the real paths/docs that domain owns;
   - what it **optimizes** and its **signature question**, derived from the domain.

   Keep the rule that makes a roster worth having: two officers must not share a model of the problem. If two candidate domains would ask the same question, merge them. Cap at 5 substantive officers.

4. **Do NOT seat the Marshal or the Tenth Man.** war-room always seats those itself (synthesis and mandated dissent are structural, not domains). The roster file lists only the substantive officers.

5. **Propose, then confirm.** Show the user the proposed roster — personas, slices, signature questions — and ask them to accept or adjust. Surface anything ambiguous as a question (a domain you weren't sure about, two that might be one). **Never write the file without an explicit OK.**

6. **Write `.war-room/roster.yaml`** in the shape of [`examples/roster.example.yaml`](../../examples/roster.example.yaml). Confirm where it landed and that the next `/war-room` run will use it.

## Keep it honest

- A scan is a guess at the project's structure, not ground truth. Present the roster as inferred, and let the user correct it — they know the domains; the scan only proposes.
- If the project is small or single-domain, say so and recommend the generic five rather than forcing a thin roster. A roster with one real officer plus filler is worse than the default.
