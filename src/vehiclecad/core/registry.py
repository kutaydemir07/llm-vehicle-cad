from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Generic, TypeVar

T = TypeVar("T")


@dataclass
class Registry(Generic[T]):
    entries: dict[str, T] = field(default_factory=dict)

    def register(self, name: str, item: T) -> T:
        if name in self.entries:
            raise ValueError(f"Registry item already exists: {name}")
        self.entries[name] = item
        return item

    def get(self, name: str) -> T:
        try:
            return self.entries[name]
        except KeyError as exc:
            raise KeyError(f"Unknown registry item: {name}") from exc


Builder = Callable[..., object]

