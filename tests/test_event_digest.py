from dbl_reference.digest import event_digest, v_digest
from dbl_reference.model import DblEvent, EventKind


def test_event_digest_ignores_observational_fields():
    e1 = DblEvent(
        event_id=1,
        kind=EventKind.DECISION,
        correlation_id="c-1",
        payload={"decision": "ALLOW", "policy_version": 1, "authoritative_digest": "sha256:" + "0" * 64},
        observed_at="2026-01-01T00:00:00Z",
        source="s1",
    )
    e2 = DblEvent(
        event_id=1,
        kind=EventKind.DECISION,
        correlation_id="c-1",
        payload={"decision": "ALLOW", "policy_version": 1, "authoritative_digest": "sha256:" + "0" * 64},
        observed_at="2026-01-02T00:00:00Z",
        source="s2",
    )
    assert event_digest(e1) == event_digest(e2)


def test_v_digest_depends_on_ordered_pairs():
    e1 = DblEvent(1, EventKind.INTENT, "c-1", {"authoritative_input": {"x": 1}, "boundary": {"boundary_version": 1, "boundary_config_hash": "sha256:" + "0" * 64}})
    e2 = DblEvent(2, EventKind.DECISION, "c-1", {"decision": "ALLOW", "policy_version": 1, "authoritative_digest": "sha256:" + "0" * 64, "rationale": {}})
    assert v_digest([e1, e2]) != v_digest([e2, e1])
