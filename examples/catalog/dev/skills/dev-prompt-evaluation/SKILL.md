---
name: dev-prompt-evaluation
description: Use to design, test, compare, version, and validate prompts or LLM behavior with measurable criteria and datasets.
---

# Prompt evaluation workflow

Use this workflow when prompts, agent instructions, LLM outputs, or AI app behavior need systematic evaluation.

## Steps

1. Define the prompt surface.
   - System, developer, user, tool, retrieval, memory, and output-format instructions.
   - Runtime model, temperature or reasoning settings, tool access, and context limits when known.
   - Current failure modes or quality goals.

2. Define success criteria.
   - Correctness, completeness, citation quality, format compliance, tone, latency, cost, refusal behavior, or safety.
   - Pass/fail checks where possible.
   - Human review rubric when automated scoring is not enough.

3. Build an evaluation set.
   - Representative normal cases.
   - Edge cases and adversarial cases.
   - Regression cases from previous failures.
   - Expected outputs, constraints, or scoring notes.

4. Compare prompt variants.
   - Keep one controlled change per variant when feasible.
   - Track version, rationale, expected improvement, and observed outcome.
   - Measure token usage and latency if available.

5. Validate tool and retrieval behavior.
   - Check whether the prompt asks for unavailable tools or hidden context.
   - Verify citations, file references, and retrieved evidence.
   - Confirm that fallback behavior is explicit.

6. Decide deployment readiness.
   - Keep the simplest prompt that meets quality goals.
   - Document known weaknesses and monitoring signals.
   - Add regression examples for failures that should not return.

## Output

Return:

1. Prompt surface reviewed
2. Evaluation criteria
3. Test set or representative cases
4. Variant comparison
5. Recommended prompt version
6. Cost, latency, safety, and monitoring notes

## Do not

- Do not optimize by vibes only.
- Do not compare multiple changes without recording what changed.
- Do not claim robustness from a tiny or unrepresentative test set.
- Do not assume a model, tool, or retrieval source exists without checking runtime evidence.
