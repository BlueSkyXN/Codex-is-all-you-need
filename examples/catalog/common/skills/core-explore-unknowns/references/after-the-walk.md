# After the Walk

The map remains the source of truth after planning ends. Apply the move that
matches the phase the work has entered.

- **Deviation log (during the build).** When implementation contradicts a map
  entry, record the original entry, the evidence that overruled it, and the
  safer path chosen, then keep building. Tag entries that need a user ruling.
  Every logged deviation is a gap the walk missed: file it back into the map
  so the record stays truthful for the next consumer.
- **Buy-in package (before shipping).** Approvers inherit whatever stayed
  open. Compress prototype, spec, and deviation log into a short review
  bundle: demonstrate working behavior up front, attach evidence beside each
  objection you expect, and assign an owner to every approval.
- **Merge-readiness check (before merging a long or unfamiliar diff).**
  Summarize how the change works, which behavior shifts are easy to overlook,
  and which signals need monitoring once released. Close with a few
  verification questions for whoever merges; a wrong answer routes the reader
  to the exact section to re-read, not to a broader summary.
