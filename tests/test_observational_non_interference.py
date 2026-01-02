from ensdg.boundary import Boundary
from ensdg.example_governance import ExampleGovernance
from ensdg.example_rules import AcceptAll
from ensdg.replay import replay_normative, to_replay_view
from ensdg.runner import DblRunner


def test_changing_execution_and_proof_does_not_change_normative_replay():
    r1 = DblRunner(boundary=Boundary(1, AcceptAll()), governance=ExampleGovernance(), policy_version=1)
    cid = "c-1"
    r1.submit_intent(cid, {"x": 1})
    r1.decide(cid)
    r1.record_execution(cid, {"ok": True})
    r1.record_proof(cid, {"latency_ms": 10})

    r2 = DblRunner(boundary=Boundary(1, AcceptAll()), governance=ExampleGovernance(), policy_version=1)
    r2.submit_intent(cid, {"x": 1})
    r2.decide(cid)
    r2.record_execution(cid, {"ok": False})
    r2.record_proof(cid, {"latency_ms": 9999})

    s1 = replay_normative(to_replay_view(r1.V.events())).decisions_by_correlation[cid].decision
    s2 = replay_normative(to_replay_view(r2.V.events())).decisions_by_correlation[cid].decision
    assert s1 == s2
