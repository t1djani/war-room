---
name: war-room
description: Use when a decision has no right answer yet — a design fork, an architecture call, a hard tradeoff with no test or spec to check against. Convenes a council of non-colluding officers plus a mandated dissenter, and produces a winning strategy with the failure-worlds that would beat it. Do NOT use when an oracle (a test, a spec, an invariant) can settle it — that is verification, not a war.
---

# war-room

A war-room war-games a hard call. Not a poll, not a vote — a council of officers who each see the problem through a *different model*, argue toward a strategy, and a mandated dissenter whose duty is to show how that strategy loses. The output is a battle plan: what wins, how to run it, and what would make it fail.

The failure this prevents: one model picking the first plausible option with false confidence — and a panel of same-context models politely agreeing with it.

## When this applies (and when it does not)

- **Use war-room** when the *criterion of success is itself in debate*: which architecture, which approach, which tradeoff. There is no reference to point at.
- **Do NOT use war-room** when you can name an oracle — a test, a spec, an invariant, a ticket's acceptance criteria. That is a *verification*, and a debate over a decidable fact is theater. Verify it instead.

The hard routing rule: **if you can name the oracle, you may not convene the war-room.**

## The council

The human is **the Commander**: they preside, hear the council, and *make the call*. The officers advise; the Commander decides and seals. Nothing ships without the Commander's OK.

The **default council** is the five officers below — each a distinct *model of the problem*, not a mood (different tone with the same model is cosmetic diversity: noise, not signal). Treat this table as the **seed roster and a worked example, not a fixed law**: every run *musters* a council for the decision at hand (see *Mustering the council*), and these five are what it composes from.

| Officer | Optimizes | Signature question |
|---|---|---|
| **The Scout** | epistemic certainty — fact vs assumption | "Do we *know* this or *assume* it — and what falls if the assumption is wrong?" |
| **The Strategist** | the option space — reframes, finds the third door (*generates*, does not choose) | "What if the real problem isn't the one we think — what's the third option?" |
| **The Marshal** | the comparative verdict — payoff vs opportunity cost (*advises* the winning course, does not seal) | "Which option has the best payoff, and what do we lose by doing nothing?" |
| **The Quartermaster** | feasibility — resources, logistics, what breaks at delivery | "Who does what with what, and which link snaps first?" |
| **The Tenth Man** | refuting the consensus *itself* | "We all agree — so what are we refusing to see? Assume we already lost." |

The four cover the decision cycle (know → imagine → decide → execute). The Tenth Man stands structurally apart: if he dissolves into the four, groupthink crushes him.

A **Specialist** seat is injectable when the subject demands a domain (security, data, perf) — never hardwired in the seed, because its slice varies with the decision. Mustering is how the right specialist gets a seat.

## Mustering the council

Every run composes a council *for this decision* — the five seed officers are a default, not a default-only. Before convening, **propose the roster to the Commander and let them choose** (one `AskUserQuestion`, three options — last one only if a saved roster exists):

- **Tailored (recommended)** — a **light, question-scoped recon**, not a project scan. From the decision text, infer the 2-4 subjects the war actually turns on, then `grep`/read **only those precise slices** of the code/docs to ground the officers and decide whether to swap or add a seat (e.g. a security officer for a security call). Targeted retrieval, not a tree walk — cheap, and it makes each officer cite real references instead of guessing.
- **Base roster** — the generic five, instantly, no reading. For a fast or low-stakes call.
- **Saved roster** *(shown only if `.war-room/roster.yaml` exists)* — use the persisted project roster as the seed.

The tailored option is the lightweight cousin of `discover-roster`: it reads only what *this question* needs and persists nothing. **Building a durable, project-wide roster is the separate heavy opt-in** — `/war-room-roster` (the `discover-roster` skill) scans the whole project once, proposes a roster, and writes `.war-room/roster.yaml` only after the Commander confirms. war-room still **never scans the whole project on its own**; the tailored recon stays scoped to the decision.

## Procedure

Keep the council visible: open a **TodoWrite checklist** for the run — one todo to frame the war, one per officer convened, one for the Marshal's synthesis, one for the Tenth Man (with his predictability scoring), one to assemble and validate the dossier. Mark each `in_progress`/`completed` as you go. The Commander watches the council convene and resolve in real time — never run it as a silent block.

1. **Frame the war.** State the decision and its constraints in one paragraph. If a named oracle would settle it → stop, this is a verification, not a war.

2. **Muster the council** (see *Mustering the council*). Offer the Commander the roster choice — tailored (light question-scoped recon), base, or the saved roster if one exists. If tailored: infer the 2-4 subjects from the decision, fetch only those slices, and compose the seats (swap/add a specialist when the decision demands it). Add one TodoWrite item per officer once the roster is set.

3. **Pick the depth.**
   - `quick` (default): officers on a cheap, fast model; the Tenth Man on the strong model (his job is the hardest). Reason inline only for a genuinely low-stakes fork.
   - `thorough` (irreversible / expensive-to-reverse / security): every officer on the strong model, and consider a second roster pass with different context slices.

4. **Convene the officers — non-colluding.** Spawn each officer as a *separate* general subagent. Give it: the **decision to settle**, its **officer seed** (its signature question + what it optimizes + the slice it should read), and the relevant **context slice**. Do NOT give it the producer's reasoning or preferred answer — that anchors every seat on one point and turns the debate into perturbation around a single (possibly wrong) equilibrium. Each officer returns its read of the decision through its own model, citing facts by openable reference (`file:line`, a manifest entry, a doc line) or marking a claim `speculative`.

5. **The Marshal synthesizes a proposed strategy.** From the officers' reads — not your own — the Marshal names the winning course of action and a battle-plan outline (the *what* that wins, at the design level; the detailed executable plan is a separate job, downstream). It surfaces the emerging majority.

6. **The Tenth Man runs last, against the consensus** — and his dissent is scored for predictability. Spawn him *after* a majority emerges. He sees **the emerging consensus** (his target) — never the producer's reasoning. His duty, not his opinion: build the world where this strategy fails, as a **dated pre-mortem** ("it's six months out, the decision failed — tell the mechanism"), not a modal antithesis. Rotate the dissent: frame him as one who *shared* the majority and now must argue against it.

   **Predictability scoring** (this is what separates real dissent from theater — a mandated dissenter will reach for the *most probable* objection, which is the most banal, which is the shared blind spot everyone already anticipated):
   1. **Baseline the obvious — first, and independently.** Before (or in parallel with) the Tenth Man, spawn a separate, non-colluding agent that sees only the decision and the emerging consensus and lists the **top-3 objections anyone would predict**. This is the predictability baseline. The Tenth Man does NOT see it; the baseline agent does NOT see the Tenth Man.
   2. **Compare.** For each of the Tenth Man's objections, check whether it matches the baseline. Matches the baseline → `predictability: predictable` (a shared blind spot, not dissent). Outside it → `predictability: novel`.
   3. **Push once, don't fake.** If his objection is `predictable`, send him back once for a failure mechanism *outside* the baseline (or hand him a different context slice). If he still only finds predictable objections, record them as `predictable` and move on — do not invent a novel one to look good. A predictable dissent is honest signal too: it says the obvious risk is the real risk.
   4. **Record the baseline in the dossier** (the `BASELINE` section). The score is a *grounded classification*, not a number — its evidence is the recorded top-3, auditable after the fact. (war-room shows no fake aggregate scores; predictability is no exception.)

   **The right to be silent is sacred:** "I find no grounded attack → all clear" is a valid, unpenalized output. A dissenter who can never stay silent is a false-positive generator. Never force an objection.

7. **Assemble the dossier** (see Output). Every `how-we-lose` entry carries a `grounding`: an openable reference, or the literal `speculative`. An objection whose reference does not open is downgraded to `speculative`.

8. **Validate the structure (deterministic).** Run `hooks/validate-dossier.sh <dossier-file>`. It checks — mechanically — that the dossier has the required sections and that every grounding is either `speculative` or a reference that resolves. It does NOT judge whether the grounding *supports* the claim; that judgment stays with the reader and is stochastic. Determinism stops at structure and at the source existing.

9. **Present to the Commander.** Lay out the strategy, the battle plan, and how-we-lose in one batch. The Commander decides and seals. A sealed dossier is **frozen** — re-readable and auditable, not re-generable (a multi-agent debate is stochastic; do not pretend its verdict replays identically).

10. **Render to HTML on request (optional).** The text dossier is the source of truth. When the Commander wants a shareable view, run `python3 scripts/render-dossier.py <dossier-file> "<decision>" > <dossier-file>.html` — a styled, dependency-free page. It's a view, not the artifact; never let the HTML replace the text dossier.

## Output — the battle plan

A war-room produces a strategy, not a cold verdict. Zero aggregate score (correlated LLM voters make aggregation amplify the common error — a score is false objectivity a skeptic spots in seconds).

```
STRATEGY: <chosen course | NO_CONVERGENCE>
  why-it-wins: <the load-bearing argument, short>

BATTLE-PLAN:                    # the what that wins — design level, not the detailed executable plan
  - <execution line 1>
  - <execution line 2>

BASELINE:                       # the top-3 predictable objections, recorded BEFORE the Tenth Man, blind to him
  - <obvious objection 1>
  - <obvious objection 2>
  - <obvious objection 3>

HOW-WE-LOSE:                    # integrated, not an appendix
  - by: <officer / the Tenth Man>
    axis: <which model of the problem>
    claim: <what makes us lose>
    grounding: <file:line | manifest entry | speculative>
    failure-world: <dated pre-mortem, for the Tenth Man>
    predictability: <novel | predictable>   # required on Tenth Man entries; was it in the BASELINE?
    status: defused | not-defused | bet-accepted
```

A `predictable` Tenth Man entry is honest signal, not a failure — it means the obvious risk *is* the real risk. But a council whose dissenter only ever lands `predictable` objections has a blind spot it isn't escaping; surface that to the Commander.

Keep the failure-worlds even when defused: the minority signal is often the rare, correct one. A not-defused-but-accepted risk is explicit decision debt, re-openable next run.

## What this is not

- Not a verifier. It judges *opinion without ground truth*. Checking an artifact against a named source is a different job (a gate).
- Not a planner. The battle plan stays at the design level; the detailed, deterministic, executable plan is written downstream.
- Not deterministic in its verdict. The *dossier* is the durable artifact (frozen, auditable), not a replayable verdict.
