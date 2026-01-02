# ENSdg
[![tests](https://github.com/lukaspfisterch/ensdg/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/lukaspfisterch/ensdg/actions/workflows/tests.yml)

**Executable Normative Semantics for Deterministic Governance**

`ensdg` exists to make the DBL papers *executable, testable, and falsifiable*.
It defines the **normative upper bound** of the DBL model in code.
ENSdg was previously developed under the working name "dbl-reference".
The rename reflects the stabilized scope and role as a semantic anchor.

This repository is **not** a product, framework, SDK, or integration layer.

---

## What this repository is

`ensdg` serves exactly three purposes:

1. **Executable reference model**  
   A minimal implementation of the DBL axioms with no discretionary behavior.

2. **Invariant oracle**  
   A canonical baseline against which other DBL-based systems can be validated.

3. **Semantic anchor**  
   A fixed point that prevents drift as higher-level tooling evolves.

If another implementation disagrees with `ensdg`, **either the implementation is wrong or the papers are**.

---

## Normative guarantees

The following properties are **normative and enforced by structure and tests**:

- Append-only, totally ordered event stream **V**
- Event kinds: **INTENT**, **DECISION**, **EXECUTION**, **PROOF**
- **DECISION primacy**: only DECISION events are normative
- Governance consumes **authoritative inputs only**
- **Pre-execution decision**:
  DECISION precedes EXECUTION for the same `correlation_id`
- **Normative replay** depends exclusively on DECISION events
- **Observational non-interference**:
  EXECUTION and PROOF events cannot affect normative state

These guarantees correspond directly to the axioms and claims of the DBL papers.
For the precise boundary of what is normative vs observational, see
`docs\normative_bounds.md`.

---

## What this repository is not

`ensdg` intentionally does **not** provide:

- Policy languages or DSLs
- Workflow engines or orchestration
- Network, infrastructure, or side effects
- Adaptive, learning, or feedback-driven policies
- Production-grade persistence or scalability
- UI, UX, or convenience abstractions

Anything that introduces **implicit normativity** is explicitly out of scope.
The `example_*` modules are test fixtures only.

---

## Position in the DBL ecosystem

`ensdg` is intentionally small and strict.
Other repositories may build *around* it without extending its scope.

- **dbl-core / kernel-logic**  
  Define execution primitives and invariants.  
  `ensdg` assumes these as given.

- **dbl-vlog**  
  Event stream and persistence abstractions.  
  `ensdg` aligns conceptually but does not provide storage backends.

- **dbl-main**  
  Integration and composition layer.  
  Real-world wiring, adapters, and domain runners belong there.  
  `dbl-main` SHOULD be validated against `ensdg`.

Educational repositories (`dbl-tutorial`, `dbl-simple`) may trade strictness for clarity,
but MUST NOT weaken DBL invariants.

---

## How this repository is used

Typical uses:

- Validate that a DBL-based system preserves:
  - DECISION primacy
  - pre-execution decision ordering
  - observational non-interference
  - normative replay equivalence
- Detect semantic drift during refactors or evolution
- Ground DBL discussions in executable semantics rather than interpretation

This repository answers one question only:

> **What does DBL mean under a minimal, interference-free implementation?**

---

## Validation workflow

Use this repo to validate an external DBL system:

1. Export the system's event stream as JSONL.
2. Run `ensdg --mode validate` to check invariants.
3. Run `ensdg --mode replay` to compute the normative projection.
4. Run `ensdg --mode replay --digest` to compute the normative digest.
5. Compare projections/digests across runs to confirm stability.

## CLI contract (normative)

The CLI is a validator/oracle surface, not a runtime or integration API.
Any deviation is a bug unless the DBL papers changed.
InvariantError and ReplayError are normative validator errors; AdmissionRejected
is demo-only and non-normative.

### Modes
- `--mode demo`  
  Emits a minimal valid DBL event stream (JSONL).
- `--mode replay`  
  Emits the normative replay projection (single JSON object),
  unless `--digest` is set.
- `--mode validate`  
  Emits nothing on success unless `--digest` is set.

### Exit codes
| Code | Name         | Meaning |
|------|--------------|---------|
| 0    | RC_OK        | Success |
| 2    | RC_USAGE     | Argument or usage error |
| 3    | RC_PARSE     | Invalid JSON/JSONL input |
| 4    | RC_INVARIANT | Invariant violation |
| 5    | RC_REPLAY    | Replayability failure |
| 6    | RC_ADMISSION | Demo admission rejected |

On failure:
- stdout MUST be empty
- stderr MUST contain exactly one prefixed error line

---

## Normative replay projection

Replay emits:

```json
{"decisions": {"<correlation_id>": "<ALLOW|DENY>"}}
```

Richer projections are allowed elsewhere,
but they MUST be reducible to this form for equivalence checks.

### Normative digest

The normative digest is computed over:

```json
{
  "decisions": {
    "<correlation_id>": {
      "decision": "<ALLOW|DENY>",
      "policy_version": "<int>",
      "authoritative_digest": "<sha256>"
    }
  }
}
```

Boundary configuration is excluded by definition.
Differences in rationale or execution artifacts are observational only.

### Stability

This repository is stable by design.

Changes should be rare and only justified by
explicit changes to the DBL papers themselves.

### References

Execution Without Normativity - A Minimal Theory of Deterministic Execution and Observation  
https://github.com/lukaspfisterch/execution-without-normativity

Deterministic Boundary Layers - Governing Non-Deterministic Execution  
https://github.com/lukaspfisterch/dbl-paper

## Private anchor

This repository is a private specification anchor and regression oracle.
See `docs\\anchor_policy.md` for the anchor policy.

- It is not intended for general consumption.
- It is not a dependency for production systems.
- Its purpose is to remain small, strict, and stable.

Changes should be rare and only justified by explicit changes to the DBL papers or dbl-core invariants.
