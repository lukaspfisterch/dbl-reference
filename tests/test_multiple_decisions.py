import pytest

from ensdg.boundary import Boundary
from ensdg.example_governance import ExampleGovernance
from ensdg.example_rules import AcceptAll
from ensdg.runner import DecisionPrereqError, DblRunner


def test_multiple_decisions_are_rejected():
    runner = DblRunner(boundary=Boundary(1, AcceptAll()), governance=ExampleGovernance(), policy_version=1)
    runner.submit_intent("c-1", {"x": 1})
    runner.decide("c-1")
    with pytest.raises(DecisionPrereqError):
        runner.decide("c-1")
