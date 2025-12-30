from __future__ import annotations

from typing import Any


class AcceptAll:
    def admit(self, raw: Any) -> bool:
        return True

    def shape(self, raw: Any) -> Any:
        return raw

    def rules_canon(self) -> Any:
        return {"rules": "accept_all"}
