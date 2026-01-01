from dbl_reference.model import EventKind
from dbl_reference.replay import replay_normative, to_replay_view
from dbl_reference.runner import DblRunner
from dbl_reference.boundary import Boundary
from dbl_reference.example_governance import ExampleGovernance
from dbl_reference.example_rules import AcceptAll


def test_only_decision_affects_normative_state():
    r = DblRunner(boundary=Boundary(1, AcceptAll()), governance=ExampleGovernance(), policy_version=1)
    cid = "c-1"
    r.submit_intent(cid, {"x": 1})
    r.decide(cid)
    r.record_execution(cid, {"ok": True})
    st = replay_normative(to_replay_view(r.V.events()))
    assert cid in st.decisions_by_correlation
