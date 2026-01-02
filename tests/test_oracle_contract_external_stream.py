import json
from pathlib import Path

from dbl_reference.invariants import validate_stream
from dbl_reference.model import DblEvent, EventKind
from dbl_reference.replay import normative_digest, to_replay_view


FIXTURE = Path(__file__).parent / "fixtures" / "external_stream.jsonl"
EXPECTED_DIGEST = "sha256:278687d053d8c7c82e60ffa9a16694204442dcb1568c6b2503b7865a111da4eb"


def _load_events(path: Path) -> list[DblEvent]:
    events: list[DblEvent] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        events.append(
            DblEvent(
                event_id=int(obj["event_id"]),
                kind=EventKind(obj["kind"]),
                correlation_id=str(obj["correlation_id"]),
                payload=obj["payload"],
            )
        )
    return events


def test_external_stream_oracle_contract() -> None:
    events = _load_events(FIXTURE)
    validate_stream(events)
    digest = normative_digest(to_replay_view(events))
    assert digest == EXPECTED_DIGEST
