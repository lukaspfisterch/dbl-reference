# dbl-reference

Reference-grade implementation of **Deterministic Boundary Layers (DBL)**.

This repository is a **reference implementation and specification anchor** for DBL.
It exists to make the axioms and guarantees of the DBL papers executable,
testable, and falsifiable in code.

It is **not** a product, framework, or integration layer.

---

## Purpose

`dbl-reference` serves three roles:

1. **Executable reference model**  
   A minimal, explicit implementation of the DBL axioms.

2. **Specification validator**  
   A concrete oracle against which other DBL-based implementations
   (e.g. `dbl-main`, domain runners) can be tested for invariant violations.

3. **Conceptual anchor**  
   A stable point that prevents semantic drift as higher-level tooling evolves.

If an implementation disagrees with `dbl-reference`, either the implementation
is wrong or the paper is.

---

## Guarantees (per papers)

The following guarantees are **enforced structurally and by tests**:

- Append-only, totally ordered event stream **V**
- Event kinds: **INTENT**, **DECISION**, **EXECUTION**, **PROOF**
- **DECISION primacy**: only DECISION events are normative
- Governance consumes **authoritative inputs IL only**
  (no observational data)
- **Pre-execution decision**:
  DECISION is written before EXECUTION for the same `correlation_id`
- **Normative replay** depends exclusively on DECISION events
- **Observational non-interference**:
  EXECUTION and PROOF events cannot affect normative state

These guarantees correspond directly to the axioms and claims
in the DBL papers.

---

## Implementation notes (reference-grade)

- Boundary configuration hashes are derived from canonicalized rule data (`rules_canon()`), not class names.
- Governance decisions require a prior INTENT; authoritative inputs are captured at admission time.
- A DECISION-only normative digest is available for replay equivalence checks.
- Canonical payloads are stricter than JSON: floats are rejected and must be normalized at the boundary.
- The `authoritative_input` stored at INTENT is the shaped input `a`, not raw `IL`.
- `event_id` defines the total order of V; it is a logical stream order, not wall-clock time.
- `correlation_id` is treated as a request identifier and must be globally unique.
- `policy_version` is stable per runner instance; per-request versioning is out of scope.
- Boundary hashes are identity fingerprints, not ontological replay validation.
- Replay validates DECISION payloads strictly; other kinds are observational and only require dict-compatibility.

---

## Non-goals

This repository explicitly does **not** provide:

- No policy language or DSL
- No workflow or orchestration engine
- No network or infrastructure side effects
- No adaptive, learning, or feedback-driven policy loops
- No production-grade persistence or scalability features
- No UX, UI, or convenience abstractions

Anything that introduces implicit normativity is intentionally excluded.

---

## Relation to other repositories

This repository is intentionally small and strict.
Other repositories may build *around* it without modifying its scope.

- **dbl-vlog**  
  Append-only event stream interfaces and persistence contracts.  
  `dbl-reference` aligns with the same conceptual **V** abstraction,
  but does not provide storage backends.

- **dbl-main**  
  Integration and composition layer for DBL-based systems.  
  Adapters, domain runners, configuration, and real-world wiring belong there.  
  `dbl-main` should be testable against `dbl-reference`.

- **dbl-tutorial / dbl-simple**  
  Educational and didactic material.  
  Examples, walkthroughs, and guided explanations live there.  
  These repositories may trade strict minimalism for clarity,
  but must not weaken DBL invariants.

---

## How to use this repository

Typical uses:

- Validate that a DBL implementation preserves:
  - DECISION primacy
  - observational non-interference
  - replay equivalence
- Compare alternative governance or boundary implementations
  against a fixed normative baseline
- Ground discussions about DBL semantics in executable reality,
  not interpretation

This repository answers the question:

> "What does DBL mean under a minimal, interference-free implementation?"

---

## Usage (Normative)

This repository is intended to be used as a **reference and validator**, not as a runtime component.

Typical usage patterns include:

### 1. Invariant validation
Use `dbl-reference` to verify that another DBL-based implementation preserves
the core invariants:

- DECISION primacy
- pre-execution decision ordering
- observational non-interference
- normative replay equivalence

Event streams produced by other systems can be replayed or checked against
the reference semantics defined here.

### 2. Regression anchor
When evolving `dbl-main`, domain runners, or governance logic,
`dbl-reference` serves as a fixed baseline to detect semantic drift.

If a change causes disagreement with `dbl-reference`,
the change must be justified explicitly or rejected.

### 3. Specification grounding
Use this repository to ground discussions about DBL behavior
in executable semantics rather than interpretation.

If something cannot be expressed or validated here,
it is likely outside the DBL model.

---

## Explicit non-usage

`dbl-reference` is **not** intended to be:

- embedded as a library in production systems
- extended with domain-specific logic
- used as a policy engine or workflow system
- modified to “support” additional features

If you need integration, composition, or infrastructure support,
use `dbl-main` instead.

Validation mode runs invariants and replayability checks; `--digest` prints the normative digest.
Replayability means DECISION payloads are parseable under the reference schema and a normative digest is computable.
Validation and replay are linear in stream size and in-memory by design; use for spot checks and regression validation,
not continuous large-scale processing.

## Status

Stable by design.

Changes to this repository should be rare, explicit, and justified
by changes to the formal DBL papers themselves.

---

## References

Normative definitions and proofs are provided in the papers:

- *Execution Without Normativity - A Minimal Theory of Deterministic Execution and Observation*  
  https://github.com/lukaspfisterch/execution-without-normativity
- *Deterministic Boundary Layers - Governing Non-Deterministic Execution*  
  https://github.com/lukaspfisterch/dbl-paper

## Related repositories
- dbl-main: https://github.com/lukaspfisterch/dbl-main
- dbl-vlog: https://github.com/lukaspfisterch/dbl-vlog

## CLI Contract (stable)

The CLI is a validator/oracle surface. This section is normative for `dbl-reference`.
If behavior differs, it is a bug unless the DBL papers changed.

### Modes
- `--mode demo` emits a minimal valid V stream to stdout (JSONL).
- `--mode replay` emits a replay projection to stdout (single JSON object) unless `--digest` is set.
- `--mode validate` emits nothing on success unless `--digest` is set.

### Exit codes
| Code | Name         | Meaning |
|------|--------------|---------|
| 0    | RC_OK        | Success. |
| 2    | RC_USAGE     | Argument/usage error. |
| 3    | RC_PARSE     | Input parse error (invalid JSON/JSONL or wrong per-line type). |
| 4    | RC_INVARIANT | Invariant violation (ordering, missing prerequisites, duplicates). |
| 5    | RC_REPLAY    | Replayability failure (DECISION payload not parseable under reference schema, or digest cannot be computed). |
| 6    | RC_ADMISSION | Demo admission rejected (boundary admission failed). |

### stdout / stderr rules
- On success:
  - `demo`: stdout is JSONL events, one object per line.
  - `replay`: stdout is a single JSON object (projection), newline terminated, unless `--digest` is set.
  - `validate`: stdout is empty unless `--digest` is set, then stdout is a single `sha256:` label, newline terminated.
- On failure:
  - stdout MUST be empty.
  - stderr MUST contain exactly one human-readable error line prefixed with:
    - `parse error:` for RC_PARSE
    - `invariant error:` for RC_INVARIANT
    - `replay error:` for RC_REPLAY
  - RC_USAGE is exempt from the single-line rule; `argparse` may emit usage text.

### Replay projection shape
`--mode replay` emits:
```json
{"decisions": {"<correlation_id>": "<ALLOW|DENY>", "...": "..."}}
```
This projection is normative for this reference; other systems may emit richer projections,
but they MUST be reducible to this form for equivalence checks.

### Normative digest
`--mode validate --digest` prints the normative digest:

Digest input is the canonical JSON encoding of:
`{"decisions": {correlation_id: {decision, policy_version, authoritative_digest}}}`

Boundary configuration is excluded (INTENT-only audit context).
Rationale is observational: two systems producing identical decisions but different rationales
are normatively equivalent under DBL.

### Input format (JSONL)
One JSON object per line.

Required keys per line: event_id, kind, correlation_id, payload.

Unknown additional keys are allowed and treated as observational.
INTENT, EXECUTION, and PROOF payloads are only validated for being JSON objects; their correctness is non-normative.

## Code-to-Axiom Mapping
- Decision primacy: `src/dbl_reference/replay.py` + `tests/test_decision_primacy.py`
- Pre-execution decision: `src/dbl_reference/invariants.py` + `tests/test_pre_execution_decision.py`
- Observational non-interference: `src/dbl_reference/replay.py` + `tests/test_observational_non_interference.py`

## Normative Digest Contract
The normative digest is the canonical JSON encoding of:
`{"decisions": {correlation_id: {decision, policy_version, authoritative_digest}}}`.
Any change to this shape is a specification change.

Boundary configuration is not part of the normative digest; it is carried in INTENT
as an identity fingerprint for audit context only.

## Canonicalization Contract (bytes)
Canonical bytes are the UTF-8 encoding of JSON text with ASCII escaping enabled (`ensure_ascii=True`).

## Boundary Config Hash
`boundary_config_hash = sha256(canon({boundary_version, rules_digest}))`.
