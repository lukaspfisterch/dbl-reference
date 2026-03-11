# Authoritative Bounds

This repository is constrained by the following authoritative sources and
conflict-resolution rule.

## Authoritative hierarchy (descending authority)

1. DBL papers - axioms, model, terminology
2. kernel-logic - execution substrate and primitives
3. dbl-core - event model, canonicalization, digest rules, invariants
4. ensdg - governance oracle and replay semantics only
5. Project-level contracts - wire formats, HTTP surfaces, storage

## Conflict resolution

If two sources conflict, the higher authority always wins. Any change that
introduces a conflict is invalid by definition.

Explicit rule:
- ensdg MUST NOT define new event kinds, canonicalization rules, or
  digest rules.
- ensdg only interprets and validates semantics defined in dbl-core and
  the papers.

## Observational non-interference

- Only DECISION events are authoritative.
- INTENT, EXECUTION, and PROOF are observational.
- Observational events:
  - MUST be stored for auditability
  - MUST NOT influence replay projection
  - MUST NOT be included in authoritative digest computation
  - MAY trigger boundary violations but never governance decisions

## Authoritative input

Authoritative input is the shaped, validated, deterministic input stored in the
INTENT payload and used as the sole input to governance. Raw input is never
authoritative; it is admitted and shaped by boundary rules into authoritative
input before any DECISION is produced.

## Digest Composition Rules

- Event digest: SHA256 of canonical event payload (excluding observational
  fields).
- Authoritative digest: SHA256 of the admitted authoritative input that
  triggered the decision.
- Authoritative digest: SHA256 of the replay projection over DECISION events only.

## Operational interpretation

- Boundaries (L) admit and shape authoritative inputs deterministically.
- Governance (G) is a pure, deterministic function over authoritative inputs
  and policy version.
- Execution outputs are observational only and MUST NOT back-propagate into
  decisions.
- If a new input is to be considered authoritative, it requires a versioned
  boundary update.

## Change rule

Every change must state:
1) Which invariants are impacted (KL vs DBL vs wire)
2) Why the change does not violate the bounds above
3) The minimal tests that prove the invariants still hold

This document is authoritative. If a change conflicts with this file, the change is
invalid by definition.
