#!/usr/bin/env bash
set -euo pipefail

# Copy this file when the shortest feedback loop still needs a human action.
# Replace each placeholder step with one exact action and one exact capture.

step() {
  printf '\nSTEP: %s\n' "$1" >&2
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
capture "HUMAN_ACTION_DONE" "Did you perform the action? (yes/no)"

step "Record the exact observed symptom."
capture "OBSERVED_SYMPTOM" "What happened?"
capture "EXPECTED_SYMPTOM" "What should have happened?"
capture "VERDICT" "Did this reproduce the target bug? (red/green/inconclusive)"
