from __future__ import annotations

import hashlib
from typing import Iterable

from .canon import canon_bytes
from .model import DblEvent


def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_label(b: bytes) -> str:
    return "sha256:" + sha256_hex(b)


def event_digest(event: DblEvent) -> str:
    payload = {
        "event_id": event.event_id,
        "kind": event.kind.value,
        "correlation_id": event.correlation_id,
        "payload": event.payload,
    }
    return sha256_label(canon_bytes(payload))


def v_digest(events: Iterable[DblEvent]) -> str:
    payload = [
        {"event_id": event.event_id, "event_digest": event_digest(event)}
        for event in events
    ]
    return sha256_label(canon_bytes(payload))
