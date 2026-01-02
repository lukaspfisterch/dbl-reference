import pytest

from dbl_reference.boundary import Boundary
from dbl_reference.example_governance import ExampleGovernance
from dbl_reference.example_rules import AcceptAll
from dbl_reference.runner import DecisionPrereqError, DblRunner


def test_decide_requires_prior_intent():
    runner = DblRunner(boundary=Boundary(1, AcceptAll()), governance=ExampleGovernance(), policy_version=1)
    with pytest.raises(DecisionPrereqError):
        runner.decide("c-1")


def test_execution_requires_prior_decision():
    runner = DblRunner(boundary=Boundary(1, AcceptAll()), governance=ExampleGovernance(), policy_version=1)
    runner.submit_intent("c-1", {"x": 1})
    with pytest.raises(DecisionPrereqError):
        runner.record_execution("c-1", {"ok": True})


def test_proof_requires_prior_decision():
    runner = DblRunner(boundary=Boundary(1, AcceptAll()), governance=ExampleGovernance(), policy_version=1)
    runner.submit_intent("c-1", {"x": 1})
    with pytest.raises(DecisionPrereqError):
        runner.record_proof("c-1", {"evidence": 1})


def test_validate_stream_requires_intent_schema():
    from dbl_reference.invariants import InvariantError, validate_stream
    from dbl_reference.model import DblEvent, EventKind

    events = [DblEvent(1, EventKind.INTENT, "c", {"boundary": {"boundary_config_hash": "sha256:" + "0" * 64}})]
    with pytest.raises(InvariantError, match="INTENT payload missing required keys"):
        validate_stream(events)


def test_validate_stream_requires_decision_schema():
    from dbl_reference.invariants import InvariantError, validate_stream
    from dbl_reference.model import DblEvent, EventKind

    events = [
        DblEvent(1, EventKind.INTENT, "c", {"authoritative_input": {"x": 1}, "boundary": {"boundary_config_hash": "sha256:" + "0" * 64}}),
        DblEvent(2, EventKind.DECISION, "c", {"decision": "ALLOW", "policy_version": True, "authoritative_digest": "sha256:" + "0" * 64, "rationale": {}}),
    ]
    with pytest.raises(InvariantError, match="DECISION policy_version must be int"):
        validate_stream(events)
