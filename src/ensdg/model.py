from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Optional


class EventKind(str, Enum):
    INTENT = "INTENT"
    DECISION = "DECISION"
    EXECUTION = "EXECUTION"
    PROOF = "PROOF"


class Decision(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"


@dataclass(frozen=True)
class BoundaryConfig:
    boundary_version: int
    boundary_config_hash: str


@dataclass(frozen=True)
class DblEvent:
    event_id: int
    kind: EventKind
    correlation_id: str
    payload: Any

    # observational metadata, must never affect normativity
    observed_at: Optional[str] = None
    source: Optional[str] = None


@dataclass(frozen=True)
class IntentPayload:
    authoritative_input: Any
    boundary: BoundaryConfig


@dataclass(frozen=True)
class DecisionPayload:
    decision: Decision
    policy_version: int
    authoritative_digest: str
    rationale: Mapping[str, Any]


@dataclass(frozen=True)
class ExecutionPayload:
    result: Any


@dataclass(frozen=True)
class ProofPayload:
    evidence: Any
