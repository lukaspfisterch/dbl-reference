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
            if state.saw_intent:
                raise InvariantError(
                    f"multiple INTENT events for correlation_id; "
                    f"correlation_id={e.correlation_id} event_id={e.event_id}"
                )
            state = CorrelationState(saw_intent=True, saw_decision=state.saw_decision)
        elif e.kind == EventKind.DECISION:
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
