from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Sequence

from .model import DblEvent


class StreamInvariantError(Exception):
    pass


@dataclass
class EventStream:
    """In-memory V with event_id as the total order (logical stream order)."""
    _events: List[DblEvent] = field(default_factory=list)
    _last_event_id: int = -1

    def append(self, e: DblEvent) -> None:
        # Append-only, ordered by event_id.
        if e.event_id <= self._last_event_id:
            raise StreamInvariantError("event_id must be strictly increasing (append-only order)")
        if not e.correlation_id:
            raise StreamInvariantError("correlation_id must be non-empty")

        self._events.append(e)
        self._last_event_id = e.event_id

    def events(self) -> Sequence[DblEvent]:
        return tuple(self._events)
