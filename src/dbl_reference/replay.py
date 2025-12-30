from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Sequence

from .canon import canon_bytes
from .digest import sha256_label
from .model import DblEvent, DecisionPayload, EventKind


class ReplayError(Exception):
    pass


@dataclass(frozen=True)
class NormativeEventView:
    event_id: int
    kind: EventKind
    correlation_id: str
    payload: dict


@dataclass
class NormativeState:
    decisions_by_correlation: Dict[str, DecisionPayload]


def to_replay_view(events: Iterable[DblEvent]) -> Sequence[NormativeEventView]:
    """Prepare events for replay: no filtering, only structural payload checks."""
    out = []
    for e in events:
        if not isinstance(e.payload, dict):
            raise ReplayError(
                f"event_id={e.event_id} kind={e.kind} correlation_id={e.correlation_id} has non-dict payload"
            )
        out.append(
            NormativeEventView(
                event_id=e.event_id,
                kind=e.kind,
                correlation_id=e.correlation_id,
                payload=e.payload,
            )
        )
    return tuple(out)


def replay_normative(events: Sequence[NormativeEventView]) -> NormativeState:
    state: Dict[str, DecisionPayload] = {}
    for e in events:
        if e.kind != EventKind.DECISION:
            continue
        dp = _parse_decision_payload(e.payload, event_id=e.event_id, correlation_id=e.correlation_id)
        state[e.correlation_id] = dp
    return NormativeState(decisions_by_correlation=state)


def normative_digest(events: Sequence[NormativeEventView]) -> str:
    state = replay_normative(events)
    payload = {
        "decisions": {
            cid: {
                "decision": dp.decision.value,
                "policy_version": dp.policy_version,
                "authoritative_digest": dp.authoritative_digest,
            }
            for cid, dp in sorted(state.decisions_by_correlation.items())
        }
    }
    return sha256_label(canon_bytes(payload))


def _parse_decision_payload(obj: dict, *, event_id: int, correlation_id: str) -> DecisionPayload:
    from .model import Decision, DecisionPayload

    try:
        decision = Decision(obj["decision"])
        pv_raw = obj["policy_version"]
        if isinstance(pv_raw, bool) or not isinstance(pv_raw, int):
            raise ReplayError("policy_version must be int")
        pv = int(pv_raw)
        ad = str(obj["authoritative_digest"])
        rationale = obj.get("rationale", {})
        if not isinstance(rationale, dict):
            raise ReplayError("rationale must be object")
    except (KeyError, TypeError, ValueError, ReplayError) as exc:
        raise ReplayError(
            f"malformed DECISION payload: {exc}. "
            "Expected keys: decision, policy_version, authoritative_digest, rationale. "
            f"correlation_id={correlation_id} event_id={event_id}"
        ) from exc
    return DecisionPayload(decision=decision, policy_version=pv, authoritative_digest=ad, rationale=rationale)
