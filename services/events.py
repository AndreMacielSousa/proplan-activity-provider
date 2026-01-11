from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Protocol


@dataclass(frozen=True)
class DomainEvent:
    name: str
    activity_id: str
    payload: Dict[str, Any] = field(default_factory=dict)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class Observer(Protocol):
    def update(self, event: DomainEvent) -> None:
        ...


class EventPublisher:
    """Subject do Observer: gere subscritores e notifica-os."""

    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event: DomainEvent) -> None:
        for obs in list(self._observers):
            obs.update(event)
