from ensdg.replay import replay_normative, to_replay_view
from ensdg.model import DblEvent, EventKind


def test_replay_ignores_execution_and_proof():
    events = [
        DblEvent(1, EventKind.DECISION, "c", {"decision": "ALLOW", "policy_version": 1, "authoritative_digest": "sha256:" + "0" * 64, "rationale": {}}),
        DblEvent(2, EventKind.EXECUTION, "c", {"result": {"ok": True}}),
        DblEvent(3, EventKind.PROOF, "c", {"evidence": {"t": 1}}),
    ]
    st = replay_normative(to_replay_view(events))
    assert st.decisions_by_correlation["c"].decision.value == "ALLOW"
