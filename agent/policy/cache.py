"""Versioned local cache; central policy management belongs to the server."""
from typing import Any

class PolicyCache:
    def __init__(self) -> None:
        self._version = 0
        self._policies: list[dict[str, Any]] = []

    @property
    def version(self) -> int:
        return self._version

    def replace(self, version: int, policies: list[dict[str, Any]]) -> None:
        if version < self._version:
            raise ValueError("Cannot replace policy cache with an older version")
        self._policies = list(policies)
        self._version = version

    def get_all(self) -> list[dict[str, Any]]:
        return list(self._policies)
