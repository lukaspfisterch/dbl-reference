from __future__ import annotations

import json
from typing import Any


class CanonError(Exception):
    """
    Raised when payload contains non-canonical types.
    Common fixes: floats as strings, scaled integers, or rational objects.
    """


def _validate_json_safe(v: Any) -> None:
    if v is None or isinstance(v, (str, int, bool)):
        return
    if isinstance(v, float):
        raise CanonError("float is not allowed (DBL canonical payloads must be integer-safe)")
    if isinstance(v, list):
        for x in v:
            _validate_json_safe(x)
        return
    if isinstance(v, dict):
        for k, x in v.items():
            if not isinstance(k, str):
                raise CanonError("object keys must be strings")
            _validate_json_safe(x)
        return
    raise CanonError("payload contains non-JSON-safe value")


def canon_bytes(payload: Any) -> bytes:
    _validate_json_safe(payload)
    try:
        return json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("utf-8")
    except ValueError as exc:
        raise CanonError(str(exc)) from exc
