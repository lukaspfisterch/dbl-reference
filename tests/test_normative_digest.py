from ensdg.model import DblEvent, EventKind
from ensdg.replay import normative_digest, to_replay_view


def test_normative_digest_ignores_execution_and_proof():
    events_a = [
        DblEvent(1, EventKind.DECISION, "c", {"decision": "ALLOW", "policy_version": 1, "authoritative_digest": "sha256:" + "0" * 64, "rationale": {}}),
        DblEvent(2, EventKind.EXECUTION, "c", {"result": {"ok": True}}),
        DblEvent(3, EventKind.PROOF, "c", {"evidence": {"t": 1}}),
    ]
    events_b = [
        DblEvent(1, EventKind.DECISION, "c", {"decision": "ALLOW", "policy_version": 1, "authoritative_digest": "sha256:" + "0" * 64, "rationale": {}}),
        DblEvent(2, EventKind.EXECUTION, "c", {"result": {"ok": False}}),
        DblEvent(3, EventKind.PROOF, "c", {"evidence": {"t": 999}}),
    ]
    assert normative_digest(to_replay_view(events_a)) == normative_digest(to_replay_view(events_b))


def test_normative_digest_changes_with_decision():
    events_a = [
        DblEvent(1, EventKind.DECISION, "c", {"decision": "ALLOW", "policy_version": 1, "authoritative_digest": "sha256:" + "0" * 64, "rationale": {}}),
    ]
    events_b = [
        DblEvent(1, EventKind.DECISION, "c", {"decision": "DENY", "policy_version": 1, "authoritative_digest": "sha256:" + "0" * 64, "rationale": {}}),
    ]
    assert normative_digest(to_replay_view(events_a)) != normative_digest(to_replay_view(events_b))
