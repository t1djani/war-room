# The roster

war-room seats a council of officers. Each is a **distinct model of the problem** — not a mood. The design rule, from Hong & Page (*Groups of diverse problem solvers can outperform groups of high-ability problem solvers*, PNAS 2004): what pays is different *representations* of the problem, not different tones. A persona without a distinct evaluation frame and a distinct slice of context is cosmetic diversity — it adds noise, not signal.

So every officer has two layers:

- **the skin** — a war-council persona (vivid, memorable);
- **the skeleton** — what it optimizes, the question it always asks, and the slice of context it reads first.

The skin sells; the skeleton is what makes the seat earn its place.

## The roster is mustered per decision

The five below are the **seed roster and a worked example, not a fixed law**. Every run *musters* a council for the decision at hand: war-room offers the Commander a **tailored** roster — a light, question-scoped recon that infers the 2-4 subjects the decision turns on, reads only those slices, and composes the seats (swapping or adding a specialist when the call demands it) — or the **base five** below, instantly. The tailored recon reads only what *one decision* needs and persists nothing; it is the lightweight cousin of `discover-roster` (`/war-room-roster`), the heavier opt-in that scans the whole project and persists a `.war-room/roster.yaml` reused on every run.

## The default five

| Officer | Optimizes | Reads first | Signature question | Grounded in |
|---|---|---|---|---|
| **The Scout** | epistemic certainty — fact vs assumption | data, sources, base rates, what's missing | "Do we *know* this or *assume* it — and what falls if the assumption is wrong?" | White Hat (de Bono) · G2 intelligence · CIA Key Assumptions Check |
| **The Strategist** | the option space — reframes, finds the third door (*generates*, does not choose) | analogies, reframings, adjacent solutions | "What if the real problem isn't the one we think — what's the third option?" | Belbin Plant · Green Hat |
| **The Marshal** | the comparative verdict — payoff vs opportunity cost (*advises*, does not seal) | decision criteria, weighted scenarios, the options on the table | "Which option has the best payoff, and what do we lose by doing nothing?" | Belbin Monitor-Evaluator · Yellow Hat |
| **The Quartermaster** | feasibility — resources, logistics, what breaks at delivery | constraints, costs, sequencing, debt | "Who does what with what, and which link snaps first?" | Belbin Implementer/Completer · G4 logistics · OODA *Act* |
| **The Tenth Man** | refuting the consensus *itself* | the blind spot of the agreement, ignored signals | "We all agree — so what are we refusing to see? Assume we already lost." | Tenth Man rule (Yom Kippour) · CIA devil's advocacy · pre-mortem (Klein) |

The first four close the decision cycle — **know → imagine → decide → execute** (Boyd's OODA). The Tenth Man stands apart by design: the lesson of Yom Kippour 1973 is that dissent must be a *role imposed by duty*, not a mood you hope emerges, or groupthink crushes it (Janis).

## Who is the human

The human is **the Commander**. They preside, hear the council, and *make the call* — the Marshal *advises* the winning course but does not seal it; the title of decider stays with the human. The Commander is also the *client* (nothing ships without their OK) and usually the *CEO* (they carry the intent).

## Seats that are NOT in the default roster

- **The facilitator** (de Bono's Blue Hat — distribute the floor, timebox, close with "disagree and commit") is the plugin's orchestrator, not an officer. Seating it would put a meta-process voice inside the debate.
- **The Specialist** (Belbin) is injectable when the subject demands a domain (security, data, perf). It is not in the base roster because its slice varies with the subject.

## Personas that look diverse but are not

These are the traps the roster avoids — each is the *same* model of the problem wearing a different costume:

- **"Emotion / gut feel"** (de Bono's Red Hat) — a tone, not a slice. It says how an option *feels*, not what model of the problem it applies.
- **"The Optimist" vs "The Pessimist"** as two seats — the same model (evaluate one option) with the sign flipped. The Marshal already weighs upside and downside; the Tenth Man covers refutation.
- **Belbin's social roles** (Coordinator, Teamworker, Resource Investigator) — they make a human group cohere. Between LLM seats there is no cohesion to manage and no new slice of information.
- **A second devil's advocate** alongside the Tenth Man — a duplicate that dilutes the mandate. Keep one adversarial seat, strong.

## Customizing

Drop a `.war-room/roster.yaml` to replace the generic officers with your project's real domains — each keeps a persona, but its slice becomes a real slice of the codebase. See [`examples/roster.example.yaml`](../examples/roster.example.yaml). Keep it to 3–5 substantive officers; the Marshal and the Tenth Man are always seated by war-room itself.

## Sources

Hong & Page, PNAS 2004 · de Bono, *Six Thinking Hats* · Belbin Team Roles (thinking / social / action) · the Tenth Man rule (Yom Kippour 1973) · CIA *Tradecraft Primer* (devil's advocacy, key assumptions check) · Klein, the pre-mortem · Boyd's OODA loop · Janis on groupthink · Bezos's 2016 letter (disagree and commit).
