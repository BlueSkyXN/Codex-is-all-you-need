# Modularity and Coupling Heuristics

Use this reference when module boundaries, split decisions, or dependency seams
are contested. These are engineering heuristics and review questions, not
mechanical scores or universal standards. Scale the assessment to the decision:
a small single-file tool usually does not need a domain model or a complete
coupling matrix.

## Cohesion signals

Ask which responsibilities belong together because they share:

- **Business capability**: they deliver one recognizable business outcome.
- **Data invariant**: they must protect the same consistency or policy rule.
- **Reason to change**: they are expected to evolve for the same business or
  operational reason.
- **Co-change**: repository history shows that the files often change together.

Co-change is candidate-boundary evidence only. A shared migration, mechanical
rename, framework upgrade, or cross-owner workflow can create co-change without
implying one bounded context. Combine history with capability, ownership,
invariants, and language before recommending a boundary.

## Coupling dimensions

Classify the observed dependency instead of calling a design simply "tightly"
or "loosely" coupled.

| Dimension | Review question |
|---|---|
| Code | Must one module import or understand another module's implementation? |
| Data | Do modules share mutable tables, records, schemas, or invariants? |
| Control | Does one module determine another module's branching or orchestration? |
| Temporal | Must calls, events, deployments, or jobs happen in a hidden order or time window? |
| Semantic | Must both sides interpret the same term, state, error, or policy identically? |
| Deployment | Must otherwise separate components be built, released, or rolled back together? |
| Runtime | Does availability, latency, capacity, or failure of one component directly constrain another? |
| Organizational | Do ownership, approval, or coordination paths force teams to change together? |

Some coupling is intentional and load-bearing, such as a transaction that
protects one invariant. Record why it is intentional and how it is governed.
Treat coupling as accidental when it exists because of implementation leakage,
an overly broad shared area, implicit sequencing, or unclear ownership rather
than a required product or operational constraint.

## Component heuristics

Use these named component principles as heuristic review prompts rather than
formulae:

- **Common Closure Principle (CCP)**: group elements that usually change for the
  same reason so an ordinary change does not fan out across unrelated modules.
- **Common Reuse Principle (CRP)**: avoid making consumers depend on a package
  whose unrelated parts they do not use; split broad `common` or `utils` areas
  around coherent consumers and change reasons.
- **Reuse/Release Equivalence Principle (REP)**: a reused component should have
  a coherent, supportable release boundary when independent reuse matters.
- **Acyclic Dependencies Principle (ADP)**: keep the module dependency graph
  acyclic or make a temporary cycle-breaking plan explicit.
- **Stable Dependencies Principle (SDP)**: direct dependencies toward modules
  intended to be more stable; volatile policy should not become a dependency of
  many unrelated areas.
- **Stable Abstractions Principle (SAP)**: stable modules need abstractions that
  let required variation occur without exposing their internals; do not add
  abstractions where no meaningful variation exists.

CCP and CRP can pull in different directions. Prefer a seam that minimizes the
real change and reuse cost for the current system rather than optimizing a
single principle in isolation.

## Diagnostic signals

Investigate when evidence shows:

- one ordinary change has high fan-out across unrelated modules;
- dependency cycles obscure ownership or change order;
- multiple modules mutate the same data without one accountable invariant owner;
- components require synchronized deployment or rollback without an explicit reason;
- callers rely on hidden initialization, ordering, retry, or timing assumptions;
- public interfaces expose database, framework, transport, or third-party SDK models;
- `shared`, `platform`, `common`, or `utils` collects unrelated capabilities.

For each material signal, record the coupling type, concrete evidence, risk,
and the smallest recommended seam. A seam may be an ownership rule, explicit
contract, data boundary, adapter, event, package split, or documented
co-deployment constraint; it does not have to be a new service.

## Misuse cautions

- An interface can still expose implementation concepts or preserve temporal,
  semantic, data, deployment, and runtime coupling.
- Dependency injection changes how dependencies are supplied; it does not make
  an unsuitable dependency appropriate.
- A microservice can move coupling onto the network and add operational coupling.
- DRY can increase coupling when unrelated capabilities share code that merely
  looks similar today.

Do not recommend a microservice, interface, shared abstraction, or deduplication
solely to make the design appear less coupled. Recommend it only when the
evidence, ownership model, and operating constraints support that seam.
