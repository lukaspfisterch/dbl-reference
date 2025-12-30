import pytest

from dbl_reference.boundary import Boundary
from dbl_reference.governance import ExampleGovernance
from dbl_reference.rules import AcceptAll
from dbl_reference.runner import DecisionPrereqError, DblRunner


def test_multiple_decisions_are_rejected():
    runner = DblRunner(boundary=Boundary(1, AcceptAll()), governance=ExampleGovernance(), policy_version=1)
    runner.submit_intent("c-1", {"x": 1})
    runner.decide("c-1")
    with pytest.raises(DecisionPrereqError):
        runner.decide("c-1")
