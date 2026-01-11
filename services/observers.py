from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from services.events import DomainEvent


@dataclass
class DeployRegistryObserver:
    """Regista metadados mínimos do deploy por activityID (mock em memória)."""
    deployments: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    def update(self, event: DomainEvent) -> None:
        if event.name != "ActivityDeployed":
            return
        self.deployments[event.activity_id] = {
            "access_url": event.payload.get("access_url"),
            "occurred_at": event.occurred_at.isoformat(),
        }


@dataclass
class AnalyticsRequestCounterObserver:
    """Conta pedidos ao analytics_url por activityID."""
    counters: Dict[str, int] = field(default_factory=dict)

    def update(self, event: DomainEvent) -> None:
        if event.name != "AnalyticsRequested":
            return
        self.counters[event.activity_id] = self.counters.get(event.activity_id, 0) + 1


@dataclass
class DecisionLogObserver:
    """Mantém rasto textual (mock) para suportar artefactos qualitativos."""
    logs: Dict[str, List[str]] = field(default_factory=dict)

    def update(self, event: DomainEvent) -> None:
        if event.name not in ("ActivityDeployed", "AnalyticsRequested"):
            return

        self.logs.setdefault(event.activity_id, [])
        if event.name == "ActivityDeployed":
            self.logs[event.activity_id].append(
                f"[DEPLOY] access_url={event.payload.get('access_url')}"
            )
        else:
            self.logs[event.activity_id].append("[ANALYTICS] pedido recebido")
