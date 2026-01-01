# Boundary Map

## dbl-gateway
Owns:
- HTTP surfaces and request admission.
- Append-only storage and snapshot assembly.
- Orchestration of governance and execution.
Exposes:
- POST `/ingress/intent`
- GET `/snapshot`
- GET `/capabilities`
- GET `/healthz`
Forbidden:
- Re-implementing dbl-core canonicalization or digest logic.
- Re-implementing dbl-policy evaluation logic.
- Bypassing kl-kernel-logic for execution traces.
- Re-implementing admission logic outside dbl-ingress.

## dbl-core
Owns:
- Canonicalization and digest rules.
- Event model and invariants for DBL events.
Exposes:
- `DblEvent`, `DblEventKind`, `GateDecision`, `BehaviorV`, `normalize_trace`
Forbidden:
- Transport logic or gateway surfaces.

## dbl-policy
Owns:
- Policy context schema and decision model.
- Decision to DBL event bridge.
Exposes:
- `PolicyContext`, `PolicyDecision`, `DecisionOutcome`, `decision_to_dbl_event`
Forbidden:
- Execution logic or kernel trace creation.

## dbl-main
Owns:
- Orchestrator state projection and runner status.
Exposes:
- `project_state`, `runner_status_from_phase`, `State`, `Phase`, `RunnerStatus`
Forbidden:
- Event storage or digest logic.

## kl-kernel-logic
Owns:
- Execution kernel, PSI definition, CAEL pipeline.
Exposes:
- `Kernel`, `ExecutionTrace`, `PsiDefinition`, `CAEL`, `CaelResult`, `FailureCode`
Forbidden:
- Policy evaluation or DBL event creation.

## dbl-ingress
Owns:
- Admission record shaping and validation.
- Unified admission error taxonomy.
Exposes:
- `AdmissionRecord`, `AdmissionError`, `InvalidInputError`, `shape_input`
Forbidden:
- Policy evaluation, event storage, or execution.
