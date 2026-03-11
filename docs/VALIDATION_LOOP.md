# Validation Loop (External Streams)

Single exchange format: JSONL event stream.
Everything under test MUST export event streams in JSONL.

## Oracle modes

Two commands provide feedback:
- `validate`: hard, binary invariant check
- `replay --digest`: stable, comparable authoritative digest

## Three cases (minimum)

Case A: Happy path  
Expectation: `validate` OK, digest stable  
Learn: baseline invariants hold

Case B: Observations vary (EXECUTION/PROOF change)  
Expectation: digest identical  
Learn: observational non-interference is real

Case C: DECISION or policy_version changes  
Expectation: digest changes  
Learn: governance authority is anchored in DECISION

## CLI commands

```bash
ensdg --mode validate --input stream.jsonl
ensdg --mode replay --digest --input stream.jsonl
```

## Exit codes

- `0`: success
- `2`: usage error
- `3`: parse error
- `4`: invariant violation
- `5`: replay failure

## Why this exists

This loop makes external validation reproducible and comparable across systems
without changing ensdg or introducing new semantics.
