from __future__ import annotations

import hashlib


def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_label(b: bytes) -> str:
    return "sha256:" + sha256_hex(b)
