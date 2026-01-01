from __future__ import annotations

from dataclasses import asdict
from typing import Any, Optional

from .boundary import Boundary
from .example_governance import Governance
from .model import DblEvent, EventKind, IntentPayload
from .stream import EventStream


class AdmissionRejected(Exception):
    pass


class DecisionPrereqError(Exception):
    pass


class DblRunner:
    def __init__(self, *, boundary: Boundary, governance: Governance, policy_version: int) -> None:
        self.boundary = boundary
        self.governance = governance
        self.policy_version = int(policy_version)
        self.V = EventStream()
        self._next_id = 0
        self._authoritative_by_corr: dict[str, Any] = {}
        self._decision_by_corr: dict[str, bool] = {}

    def submit_intent(self, correlation_id: str, raw_input: Any, *, source: Optional[str] = None) -> DblEvent:
        if not self.boundary.admit(raw_input):
            raise AdmissionRejected("boundary admission rejected (pre-ontological, non-normative)")
        if correlation_id in self._authoritative_by_corr:
            raise DecisionPrereqError(
                f"Cannot submit INTENT for correlation_id='{correlation_id}': "
                "INTENT already recorded."
            )
        authoritative = self.boundary.shape(raw_input)
        # Store shaped authoritative input (a), not raw IL.
        self._authoritative_by_corr[correlation_id] = authoritative
        intent = IntentPayload(authoritative_input=authoritative, boundary=self.boundary.config())
        e = DblEvent(
            event_id=self._alloc_id(),
            kind=EventKind.INTENT,
            correlation_id=correlation_id,
            payload=asdict(intent),
            source=source,
        )
        self.V.append(e)
        return e

    def decide(self, correlation_id: str, *, source: Optional[str] = None) -> DblEvent:
        if correlation_id not in self._authoritative_by_corr:
            raise DecisionPrereqError(
                f"Cannot decide for correlation_id='{correlation_id}': "
                "no prior INTENT event found. Submit intent first."
            )
        if self._decision_by_corr.get(correlation_id):
            raise DecisionPrereqError(
                f"Cannot decide for correlation_id='{correlation_id}': "
                "DECISION already recorded."
            )
        authoritative_input = self._authoritative_by_corr[correlation_id]
        dp = self.governance.decide(authoritative_input, self.policy_version)
        e = DblEvent(
            event_id=self._alloc_id(),
            kind=EventKind.DECISION,
            correlation_id=correlation_id,
            payload={
                "decision": dp.decision.value,
                "policy_version": dp.policy_version,
                "authoritative_digest": dp.authoritative_digest,
                "rationale": dict(dp.rationale),
            },
            source=source,
        )
        self.V.append(e)
        self._decision_by_corr[correlation_id] = True
        return e

    def record_execution(self, correlation_id: str, result: Any, *, source: Optional[str] = None) -> DblEvent:
        if correlation_id not in self._authoritative_by_corr:
            raise DecisionPrereqError(
                f"Cannot execute for correlation_id='{correlation_id}': "
                "no prior INTENT event found."
            )
        if not self._decision_by_corr.get(correlation_id):
            raise DecisionPrereqError(
                f"Cannot execute for correlation_id='{correlation_id}': "
                "no prior DECISION event found."
            )
        e = DblEvent(
            event_id=self._alloc_id(),
            kind=EventKind.EXECUTION,
            correlation_id=correlation_id,
            payload={"result": result},
            source=source,
        )
        self.V.append(e)
        return e

    def record_proof(self, correlation_id: str, evidence: Any, *, source: Optional[str] = None) -> DblEvent:
        if correlation_id not in self._authoritative_by_corr:
            raise DecisionPrereqError(
                f"Cannot record PROOF for correlation_id='{correlation_id}': "
                "no prior INTENT event found."
            )
        if not self._decision_by_corr.get(correlation_id):
            raise DecisionPrereqError(
                f"Cannot record PROOF for correlation_id='{correlation_id}': "
                "no prior DECISION event found."
            )
        e = DblEvent(
            event_id=self._alloc_id(),
            kind=EventKind.PROOF,
            correlation_id=correlation_id,
            payload={"evidence": evidence},
            source=source,
        )
        self.V.append(e)
        return e

    def _alloc_id(self) -> int:
        self._next_id += 1
        return self._next_id
