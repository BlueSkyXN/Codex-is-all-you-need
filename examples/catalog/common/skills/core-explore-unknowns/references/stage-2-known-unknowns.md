# Stage 2 - Known Unknowns: Close Visible Questions

This stage handles questions that are already visible. The missing answer may
come from the user, from local evidence, or it may remain explicitly open.

## Procedure

1. Make a short queue of questions that block useful progress.
2. Sort by blast radius: architecture, data contract, public behavior, and
   reversibility before small implementation preferences.
3. Resolve one question at a time. Each question should include your recommended
   answer and compact alternatives.
4. Close each question as one of:
   - **User-decided**: the user answered or corrected the recommendation.
   - **Evidence-decided**: local truth answered it; show the question, answer,
     and evidence.
   - **OPEN**: still deferred; name what would unblock it.

**Done when** the named questions are either decided in view of the user or
recorded as OPEN with a blocker. Recap the stage before moving on.

## Techniques

- **Decision interview**: one high-impact question per turn, with a recommended
  default and a final decision table.
- **Option spread**: when the blocker is "which approach?", list a small range
  from quick patch to larger bet, grounded in the current repo.
- **Reference mapping**: when another implementation is the model, summarize the
  behaviors to preserve and how each maps to the target surface.
