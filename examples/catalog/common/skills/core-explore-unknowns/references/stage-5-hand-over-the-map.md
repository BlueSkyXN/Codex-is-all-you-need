# Stage 5 — Hand Over the Map

Close the walk by producing a durable map the next workflow can consume without
reconstructing the conversation.

## The map artifact

Create one self-contained artifact with:

- **Known knowns**: confirmed facts, constraints, and citations.
- **Known unknowns**: each named question, its answer or OPEN status, and the
  source of the decision.
- **Unknown knowns**: tacit context extracted from reactions, samples, or probes.
- **Unknown unknowns**: hidden risks, each with evidence and status.

Open items belong in the artifact, not only in chat history. Put pre-build
checks in their own list so implementation can start with explicit blockers.

## What rides along

- A build plan may sit below the map, but the plan does not replace the map.
  Put judgment calls and alternatives before mechanical tasks.
- A copyable implementation prompt can be included when it helps the user start
  the next workflow.

**Done when** the completed map is present and implementation can refer to it as
the source of truth. Offer to continue with the appropriate implementation skill.
