# Domain method

Shared by `ads-domain`, `ads-architecture`, and `sdlc-solve`. Make business
concepts, rules, and ownership explicit so code and specs agree with the
business.

## Steps

1. **Terms.** List the business terms the change touches. For each: a
   definition in business language, synonyms in use, and where it appears in
   code. Flag one word used for two concepts and two words used for one.
2. **Rules.** Write the rules and invariants: what must always hold, what is
   allowed, and what is forbidden, with an example and a counterexample.
   Include edge cases such as partial, duplicate, concurrent, expired, and
   reversed operations.
3. **States.** For a concept with a lifecycle, list its states, the allowed
   transitions, and who or what triggers each one.
4. **Ownership.** Which module, service, or team owns each concept and its
   rules, and who may change them. A concept with two owners is a finding.
5. **Boundaries.** Where a term changes meaning, for example between billing
   and support, name the boundary and the translation across it.
6. **Verify.** Check each rule against the code, the data, and an
   authoritative source. Mark it confirmed, inferred from code, or open.

## Record

Keep the glossary and rule list as a design record, as described in
[the shared conventions](../../sdlc-solve/references/conventions.md). Use the
same terms in code, specs, and tests.

## User decisions

Business rules and ownership belong to the user or stakeholders. When the code
and a stated rule disagree, report both; do not pick one silently.

## Done

Every touched term is defined, every rule has examples and a status, ownership
is assigned, and disagreements are listed.
