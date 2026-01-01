from __future__ import annotations

"""NON_NORMATIVE: test fixtures only."""

from dataclasses import dataclass
from typing import Any, Mapping, Protocol

from .canon import canon_bytes
from .digest import sha256_label
from .model import Decision, DecisionPayload


class Governance(Protocol):
    """
    Governance must be pure and stateless.
    Decision depends only on (authoritative_input, policy_version).
    """
    def decide(self, authoritative_input: Any, policy_version: int) -> DecisionPayload: ...


@dataclass(frozen=True)
class ExampleGovernance:
    """
    Reference helper: deterministic, pure governance.

    Replace with your real governance, but preserve:
    - decision depends only on authoritative_input and policy_version
    - no access to execution/proof/observations
    """

    def decide(self, authoritative_input: Any, policy_version: int) -> DecisionPayload:
        a_digest = sha256_label(canon_bytes(authoritative_input))
        decision = Decision.DENY if _contains_deny(authoritative_input) else Decision.ALLOW
        rationale: Mapping[str, Any] = {"authoritative_digest": a_digest, "rule": "contains_deny"}
        return DecisionPayload(
            decision=decision,
            policy_version=policy_version,
            authoritative_digest=a_digest,
            rationale=rationale,
        )


def _contains_deny(v: Any) -> bool:
    if isinstance(v, dict):
        if v.get("deny") is True:
            return True
        return any(_contains_deny(x) for x in v.values())
    if isinstance(v, list):
        return any(_contains_deny(x) for x in v)
    return False
