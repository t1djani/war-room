STRATEGY: Two separate repos, contract-first — keep each service in its own repo and treat the shared database schema as a versioned, tested contract.
  why-it-wins: the monorepo's payoffs (shared tooling, atomic cross-service commits) are illusory across two stacks that share no code; two repos buy dead-simple CI, clean onboarding, and independent deploys, and the one real risk (schema drift) is far cheaper to neutralize with a contract test than with a polyglot monorepo.

BATTLE-PLAN:
  - Make the schema contract a first-class artifact: migrations plus generated/checked-in types live in one designated place, semver-tagged, each service pinning a known version.
  - Add a contract test to BOTH repos' CI that asserts DATA INVARIANTS, not just schema shape — a row-count/freshness floor on derived tables, cross-encoding equivalence (two encodings of the "same" concept must agree), and identity resolved only through the alias table. (This is the Tenth Man's fix, adopted.)
  - One owner per schema change, expand-then-contract migrations (additive first, consumers migrate, remove later) so the two repos never need a synchronized atomic commit.
  - Probe the contract POST-DEPLOY against production, not only in CI — a green CI check must not be the only proof both schemas were actually applied.

BASELINE:
  - "Monorepo: shared tooling / a dependency bump in one service breaks the other's build."
  - "Two repos: cross-cutting changes need synchronized PRs across both repos."
  - "Two repos: onboarding friction doubles — clone and context-switch two repos."

HOW-WE-LOSE:
  - by: The Scout
    axis: fact vs assumption
    claim: the whole call hinges on how OFTEN the schema changes and who drives it — high cadence turns two-repo coordination into real friction.
    grounding: speculative
    status: bet-accepted
  - by: The Tenth Man
    axis: refuting the consensus
    claim: "green test, dead data — a schema-contract test checks column names and types, but this boundary breaks INSIDE the values (an identity column that is really a per-credential alias; a derived table recomputed over a different row population; a stale graceful-fallback masking an empty table). CI stays green the whole time the contract is broken, and the product ships a confidently fabricated answer."
    grounding: speculative
    failure-world: "11 weeks out, a Tuesday morning: a single-repo change to a derived table's population logic (zero DDL) makes a consumer read the same column names and get quietly wrong numbers. Every CI gate is green; a stale fallback hides it for days."
    predictability: novel
    status: not-defused
  - by: The Tenth Man
    axis: refuting the consensus
    claim: "CI-green but deploy-diverged — the contract is validated in CI against a clean DB, then re-falsified at deploy when an ordered migration chain stalls on one non-idempotent step. No single artifact proves both sides' schemas were actually applied together."
    grounding: speculative
    failure-world: "Launch morning: a migration merges, both repos' CI green, the deploy still bricks the boundary for hours because the live schema never matched the contract the test certified."
    predictability: novel
    status: not-defused
