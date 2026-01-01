from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from .canon import canon_bytes
from .digest import sha256_label
from .model import BoundaryConfig


class BoundaryRule(Protocol):
    """NON_NORMATIVE: test fixture protocol for admission/shaping."""
    def admit(self, raw: Any) -> bool: ...
    def shape(self, raw: Any) -> Any: ...
    def rules_canon(self) -> Any: ...


@dataclass(frozen=True)
class Boundary:
    boundary_version: int
    rules: BoundaryRule

    def config(self) -> BoundaryConfig:
        # Hash is over canonical form of boundary_version + rules digest label.
        rules_digest = self.rules_digest()
        payload = {"boundary_version": self.boundary_version, "rules_digest": rules_digest}
        return BoundaryConfig(
            boundary_version=self.boundary_version,
            boundary_config_hash=sha256_label(canon_bytes(payload)),
        )

    def rules_digest(self) -> str:
        payload = self.rules.rules_canon()
        return sha256_label(canon_bytes(payload))

    def admit(self, raw: Any) -> bool:
        return bool(self.rules.admit(raw))

    def shape(self, raw: Any) -> Any:
        return self.rules.shape(raw)
