import pytest

from ensdg.invariants import InvariantError, validate_stream
from ensdg.model import DblEvent, EventKind


def test_execution_before_decision_is_rejected():
    events = [DblEvent(event_id=1, kind=EventKind.EXECUTION, correlation_id="c", payload={"x": 1})]
    with pytest.raises(InvariantError):
        validate_stream(events)
