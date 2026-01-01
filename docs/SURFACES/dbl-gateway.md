# dbl-gateway Dependency Surface

## Normalized imports (usage-derived)
### dbl-core
- `dbl_core.events.canonical` -> `canonicalize_value`, `digest_bytes`, `json_dumps`

### dbl-policy
- `dbl_policy` (module import in governance evaluation)

### dbl-main
- `dbl_main` (module import in governance evaluation)

### kl-kernel-logic
- `kl_kernel_logic` (module import for `PsiDefinition`, `Kernel`)

## Public surface (from __all__)
### dbl-core
- `DblEvent`, `DblEventKind`, `BehaviorV`, `GateDecision`, `normalize_trace`

### dbl-policy
- `DecisionOutcome`, `Policy`, `PolicyContext`, `PolicyDecision`, `PolicyId`, `PolicyVersion`, `TenantId`, `decision_to_dbl_event`

### dbl-main
- `Phase`, `RunnerStatus`, `State`, `project_state`, `runner_status_from_phase`

### kl-kernel-logic
- `PsiDefinition`, `Kernel`, `ExecutionTrace`, `FailureCode`, `CAEL`, `CaelResult`

## Contract-bearing modules
### dbl-core
- Canonicalization and digest: `D:\DEV\projects\dbl-core-dev\src\dbl_core\events\canonical.py`
- Event model and invariants: `D:\DEV\projects\dbl-core-dev\src\dbl_core\events\model.py`
- Trace digest: `D:\DEV\projects\dbl-core-dev\src\dbl_core\events\trace_digest.py`
- Gate decision: `D:\DEV\projects\dbl-core-dev\src\dbl_core\gate\model.py`
- Trace normalization: `D:\DEV\projects\dbl-core-dev\src\dbl_core\normalize\trace.py`

### dbl-policy
- Policy context and decision model: `D:\DEV\projects\dbl-policy\src\dbl_policy\model.py`

### dbl-main
- Orchestrator state projection: `D:\DEV\projects\dbl-main\src\dbl_main\state_projection.py`

### kl-kernel-logic
- Kernel and execution trace: `D:\DEV\projects\kl-kernel-logic-dev\src\kl_kernel_logic\kernel.py`
- Psi definition: `D:\DEV\projects\kl-kernel-logic-dev\src\kl_kernel_logic\psi.py`
- CAEL pipeline: `D:\DEV\projects\kl-kernel-logic-dev\src\kl_kernel_logic\cael.py`

## Stability classification
### dbl-core
- Stable: `__all__` exports in `dbl_core.__init__`.
- Semi-stable: contract-bearing modules listed above.
- Internal: any other module not listed here.

### dbl-policy
- Stable: `__all__` exports in `dbl_policy.__init__`.
- Semi-stable: `dbl_policy.model` (contract-bearing).
- Internal: any other module not listed here.

### dbl-main
- Stable: `__all__` exports in `dbl_main.__init__`.
- Semi-stable: `dbl_main.state_projection` (contract-bearing).
- Internal: any other module not listed here.

### kl-kernel-logic
- Stable: `__all__` exports in `kl_kernel_logic.__init__`.
- Semi-stable: `kernel.py`, `psi.py`, `cael.py`.
- Internal: any other module not listed here.

## Allowed imports whitelist
- Allowed symbols: only the public surface above, plus the normalized imports list.
- Allowed modules: `dbl_core.events.canonical`, `dbl_policy`, `dbl_main`, `kl_kernel_logic`.

## Forbidden patterns
- Importing any `dbl_core.events.model` or `dbl_core.events.trace_digest` symbols directly from gateway code.
- Importing `dbl_policy.model` symbols directly, unless added to __all__ or explicitly whitelisted.
- Importing `kl_kernel_logic.kernel` or `kl_kernel_logic.psi` directly instead of the package root.

## Bridge section
- Only allowed policy to event conversion: `PolicyDecision` -> `DblEvent(DECISION)` via `dbl_policy.decision_to_dbl_event`.

## Drift checklist
- If gateway needs a new symbol: add it to dependency __all__ or update this whitelist.
- If an invariant changes: bump major version or add compatibility adapters.
