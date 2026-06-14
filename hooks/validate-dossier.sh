#!/usr/bin/env bash
# validate-dossier.sh — deterministic structure + grounding check for a war-room dossier.
#
# It checks, mechanically:
#   1. the required sections exist (STRATEGY, BATTLE-PLAN, HOW-WE-LOSE)
#   2. every `grounding:` is either the literal `speculative` or a reference that resolves
#      (a `path` or `path:line` whose file exists on disk)
#
# It does NOT judge whether a grounding supports its claim — that is a human/model call,
# and stochastic. Determinism stops at structure and at the source existing.
#
# Usage: hooks/validate-dossier.sh <dossier-file>
# Exit:  0 = structurally valid · 1 = problems found · 2 = bad invocation

set -u

file="${1:-}"
if [ -z "$file" ] || [ ! -f "$file" ]; then
  echo "validate-dossier: need a readable dossier file (got: '${file}')" >&2
  exit 2
fi

problems=0
fail() { echo "  ✗ $1" >&2; problems=$((problems + 1)); }

echo "war-room · validating dossier: $file"

# 1. required sections
for section in "STRATEGY" "BATTLE-PLAN" "HOW-WE-LOSE"; do
  if ! grep -Eq "^[[:space:]]*${section}[:]" "$file"; then
    fail "missing required section: ${section}"
  fi
done

# A NO_CONVERGENCE strategy is legitimate, but it must be stated, not empty.
if grep -Eq "^[[:space:]]*STRATEGY[:][[:space:]]*$" "$file"; then
  fail "STRATEGY is empty — state the chosen course or NO_CONVERGENCE"
fi

# 2. groundings resolve
# Each `grounding:` value is either `speculative` or a reference `path` / `path:line`.
while IFS= read -r raw; do
  # strip the leading "grounding:" and surrounding whitespace/quotes
  val="$(printf '%s' "$raw" | sed -E 's/^[[:space:]]*grounding:[[:space:]]*//; s/^["'"'"']//; s/["'"'"'][[:space:]]*$//')"
  [ -z "$val" ] && { fail "empty grounding (use a reference or the literal 'speculative')"; continue; }
  case "$val" in
    speculative) : ;;                       # explicitly unanchored — allowed
    *)
      ref_path="${val%%:*}"                 # drop :line if present
      if [ ! -e "$ref_path" ]; then
        fail "grounding does not resolve: '${val}' — downgrade to 'speculative' or fix the reference"
      fi
      ;;
  esac
done < <(grep -E "^[[:space:]]*grounding:" "$file")

if [ "$problems" -eq 0 ]; then
  echo "  ✓ structure and groundings valid"
  exit 0
fi
echo "validate-dossier: ${problems} problem(s)" >&2
exit 1
