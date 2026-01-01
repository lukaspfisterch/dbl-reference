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
