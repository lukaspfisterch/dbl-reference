from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Sequence

from .model import DblEvent, EventKind


class InvariantError(Exception):
    pass


@dataclass(frozen=True)
class CorrelationState:
    saw_intent: bool = False
    saw_decision: bool = False


def validate_stream(events: Sequence[DblEvent]) -> None:
    last_event_id = -1
    by_corr: Dict[str, CorrelationState] = {}

    for e in events:
        if e.event_id <= last_event_id:
            raise InvariantError(
                f"event_id must be strictly increasing (append-only order); "
                f"event_id={e.event_id} last_event_id={last_event_id}"
            )
        if not e.correlation_id:
            raise InvariantError(f"correlation_id must be non-empty; event_id={e.event_id}")

        state = by_corr.get(e.correlation_id, CorrelationState())

        if e.kind == EventKind.INTENT:
            _validate_intent_payload(e.payload, e.event_id)
            if state.saw_intent:
                raise InvariantError(
                    f"multiple INTENT events for correlation_id; "
                    f"correlation_id={e.correlation_id} event_id={e.event_id}"
                )
            state = CorrelationState(saw_intent=True, saw_decision=state.saw_decision)
        elif e.kind == EventKind.DECISION:
            _validate_decision_payload(e.payload, e.event_id)
            if not state.saw_intent:
                raise InvariantError(
                    f"DECISION observed before INTENT for correlation_id; "
                    f"correlation_id={e.correlation_id} event_id={e.event_id}"
                )
            if state.saw_decision:
                raise InvariantError(
                    f"multiple DECISION events for correlation_id; "
                    f"correlation_id={e.correlation_id} event_id={e.event_id}"
                )
            state = CorrelationState(saw_intent=state.saw_intent, saw_decision=True)
        elif e.kind in (EventKind.EXECUTION, EventKind.PROOF):
            if not state.saw_decision:
                raise InvariantError(
                    f"EXECUTION/PROOF observed before DECISION for correlation_id; "
                    f"correlation_id={e.correlation_id} event_id={e.event_id}"
                )

        by_corr[e.correlation_id] = state
        last_event_id = e.event_id


def _validate_intent_payload(payload: object, event_id: int) -> None:
    if not isinstance(payload, dict):
        raise InvariantError(f"INTENT payload must be object; event_id={event_id}")
    if "authoritative_input" not in payload or "boundary" not in payload:
        raise InvariantError(f"INTENT payload missing required keys; event_id={event_id}")
    boundary = payload["boundary"]
    if not isinstance(boundary, dict):
        raise InvariantError(f"INTENT boundary must be object; event_id={event_id}")
    if "boundary_config_hash" not in boundary:
        raise InvariantError(f"INTENT boundary missing boundary_config_hash; event_id={event_id}")
    bch = boundary["boundary_config_hash"]
    if not isinstance(bch, str) or not bch.startswith("sha256:"):
        raise InvariantError(f"INTENT boundary_config_hash must be sha256:; event_id={event_id}")


def _validate_decision_payload(payload: object, event_id: int) -> None:
    if not isinstance(payload, dict):
        raise InvariantError(f"DECISION payload must be object; event_id={event_id}")
    for key in ("decision", "policy_version", "authoritative_digest"):
        if key not in payload:
            raise InvariantError(f"DECISION payload missing {key}; event_id={event_id}")
    pv = payload["policy_version"]
    if isinstance(pv, bool) or not isinstance(pv, int):
        raise InvariantError(f"DECISION policy_version must be int; event_id={event_id}")
    ad = payload["authoritative_digest"]
    if not isinstance(ad, str) or not ad.startswith("sha256:"):
        raise InvariantError(f"DECISION authoritative_digest must be sha256:; event_id={event_id}")
