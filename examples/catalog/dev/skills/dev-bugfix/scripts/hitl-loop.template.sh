#!/usr/bin/env bash
set -euo pipefail

# Copy this file when the shortest feedback loop still needs a human action.
# Replace each placeholder step with one exact action and one exact capture.

step() {
  local instruction="$1"
  printf '\nSTEP: %s\n' "$instruction" >&2
  printf 'Press Enter when this step is complete: ' >&2
  IFS= read -r _
}

capture() {
  local key="$1"
  local prompt="$2"
  local value
  printf '%s: ' "$prompt" >&2
  IFS= read -r value
  printf '%s=%s\n' "$key" "$value"
}

step "Prepare the smallest scenario that should reproduce the bug."
# Example: start the local app, open the target URL, or run a setup command.

step "Perform the single human action that cannot yet be automated."
capture "HUMAN_ACTION_DONE" "Was the action completed? (yes/no)"

step "Record the exact observed symptom."
capture "OBSERVED_SYMPTOM" "What happened?"
capture "EXPECTED_SYMPTOM" "What should have happened?"
capture "VERDICT" "Loop verdict for the target bug (red/green/inconclusive)"
