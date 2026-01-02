# Invariants

## I-ADMISSION-1
- Owner: dbl-ingress
- Statement: Admission rejects invalid intent payloads before any append.
- Why it matters: Prevents polluted V with non-admitted inputs.
- Breaking symptom: Rejected requests still create INTENT events.
- Reference: D:\DEV\projects\dbl-ingress\src\dbl_ingress\shaping\shape.py

## I-SECRETS-1
- Owner: dbl-gateway
- Statement: Admission rejects payloads containing secret keys like api_key or authorization.
- Why it matters: Prevents secrets from entering the event log.
- Breaking symptom: API keys show up in stored payloads or snapshots.
- Reference: D:\DEV\projects\dbl-gateway\src\dbl_gateway\admission\__init__.py

## I-APPEND-1
- Owner: dbl-gateway
- Statement: The store uses AUTOINCREMENT primary key to ensure monotonic indices.
- Why it matters: Stable ordering is required for replay and digesting V.
- Breaking symptom: Duplicate or non-monotonic index values.
- Reference: D:\DEV\projects\dbl-gateway\src\dbl_gateway\store\sqlite.py

## I-ORDER-1
- Owner: dbl-reference
- Statement: event_id is the stream order key used for validation; it MUST be strictly increasing.
- Why it matters: Deterministic replay and v_digest depend on a total order.
- Breaking symptom: event_id is not monotonic or is treated as a UUID.
- Reference: D:\DEV\projects\dbl-reference\src\dbl_reference\invariants.py

## I-DECISION-1
- Owner: dbl-gateway
- Statement: EXECUTION is scheduled only after an ALLOW decision.
- Why it matters: Execution must not occur without explicit governance.
- Breaking symptom: EXECUTION events with no prior DECISION or REJECT decision.
- Reference: D:\DEV\projects\dbl-gateway\src\dbl_gateway\app.py

## I-CANON-1
- Owner: dbl-core
- Statement: Canonicalization uses deterministic ordering and ASCII JSON.
- Why it matters: Digest stability across producers and replays.
- Breaking symptom: Same input yields different digests across runs.
- Reference: D:\DEV\projects\dbl-core-dev\src\dbl_core\events\canonical.py

## I-DIGEST-1
- Owner: dbl-gateway
- Statement: Event digest is computed from dbl-core canonicalization.
- Why it matters: Prevents gateway-specific digest drift.
- Breaking symptom: Digest changes when dbl-core digest remains stable.
- Reference: D:\DEV\projects\dbl-gateway\src\dbl_gateway\digest.py

## I-V-1
- Owner: dbl-gateway
- Statement: v_digest is computed from ordered (index, digest) pairs.
- Why it matters: Stream integrity depends on ordered prefix hashing.
- Breaking symptom: v_digest changes with paging or unordered inputs.
- Reference: D:\DEV\projects\dbl-gateway\src\dbl_gateway\digest.py

## I-EVENT-KIND-1
- Owner: dbl-core
- Statement: DblEventKind enumerates the only valid event kinds.
- Why it matters: Consumers rely on a fixed event kind vocabulary.
- Breaking symptom: Unknown kind values accepted as valid.
- Reference: D:\DEV\projects\dbl-core-dev\src\dbl_core\events\model.py

## I-OBS-1
- Owner: dbl-core
- Statement: DblEvent digest excludes observational fields.
- Why it matters: Observations must not affect deterministic identity.
- Breaking symptom: Observational-only changes alter event digests.
- Reference: D:\DEV\projects\dbl-core-dev\src\dbl_core\events\model.py

## I-TRACE-DIGEST-1
- Owner: dbl-core
- Statement: trace_digest is sha256 of canonicalized trace mapping.
- Why it matters: Execution traces must be verifiable and stable.
- Breaking symptom: trace_digest mismatch for unchanged trace.
- Reference: D:\DEV\projects\dbl-core-dev\src\dbl_core\events\trace_digest.py

## I-POLICY-CTX-1
- Owner: dbl-gateway
- Statement: Policy context is restricted to ALLOWED_CONTEXT_KEYS.
- Why it matters: Prevents policy from depending on observational data.
- Breaking symptom: Policy sees fields outside the allowed context.
- Reference: D:\DEV\projects\dbl-gateway\src\dbl_gateway\governance.py

## I-POLICY-CTX-2
- Owner: dbl-policy
- Statement: PolicyContext rejects observational keys like trace and execution.
- Why it matters: Policy decisions must be based on admitted inputs only.
- Breaking symptom: PolicyContext accepts trace or execution keys.
- Reference: D:\DEV\projects\dbl-policy\src\dbl_policy\model.py

## I-DECISION-BRIDGE-1
- Owner: dbl-policy
- Statement: PolicyDecision maps to DblEvent(DECISION) via GateDecision.
- Why it matters: Ensures governance decisions are represented consistently.
- Breaking symptom: Decision mapping produces non-DECISION events or missing outcome.
- Reference: D:\DEV\projects\dbl-policy\src\dbl_policy\model.py

## I-KERNEL-1
- Owner: kl-kernel-logic
- Statement: Kernel.execute never raises and captures errors in ExecutionTrace.
- Why it matters: Execution failures remain observable and non-fatal.
- Breaking symptom: Kernel raises exceptions to callers.
- Reference: D:\DEV\projects\kl-kernel-logic-dev\src\kl_kernel_logic\kernel.py

## I-PSI-1
- Owner: kl-kernel-logic
- Statement: PsiDefinition.describe provides stable serializable metadata ordering.
- Why it matters: PSI identity must be stable across executions.
- Breaking symptom: PSI descriptions change ordering or shape.
- Reference: D:\DEV\projects\kl-kernel-logic-dev\src\kl_kernel_logic\psi.py
