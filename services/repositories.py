"""
Repositórios e Factory Method do ProPlan.

Este módulo isola a infraestrutura de acesso a dados/configuração do serviço,
evitando que o ponto de entrada HTTP (app.py) acumule responsabilidades.

Objetivo: mitigar o risco de acumulação de responsabilidades (*The Blob*)
em torno do módulo de endpoints, preservando o comportamento observável
(contratos e respostas) exposto à Inven!RA.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class AnalyticsRepository(ABC):
    """Contrato para repositórios de analytics do ProPlan."""

    @abstractmethod
    def get_analytics(self, activity_id: str) -> list[dict[str, Any]]:
        raise NotImplementedError


class JsonAnalyticsRepository(AnalyticsRepository):
    """Repositório concreto que gera analytics a partir do esquema JSON."""

    def __init__(self, base_url: str, analytics_schema: dict[str, Any]):
        self._base_url = base_url
        self._schema = analytics_schema

    def get_analytics(self, activity_id: str) -> list[dict[str, Any]]:
        # Exemplo de estudante fictício (um registo)
        student_id = "1001"

        quant_values: list[dict[str, Any]] = []
        for qa in self._schema.get("quantAnalytics", []):
            name = qa.get("name")
            type_ = qa.get("type")

            # Valores ilustrativos (mock)
            example: Any = 0
            if type_ == "integer":
                mapping = {
                    "decisions_count": 12,
                    "total_time_seconds": 3600,
                    "cost_variance": -500,
                    "schedule_variance_days": 2,
                    "client_satisfaction_score": 4,
                    "replans_count": 1,
                }
                example = mapping.get(name, 0)

            quant_values.append({"name": name, "type": type_, "value": example})

        qual_values: list[dict[str, Any]] = []
        for qa in self._schema.get("qualAnalytics", []):
            name = qa.get("name")
            type_ = qa.get("type")

            if type_ == "URL":
                if name == "decision_log_url":
                    value = f"{self._base_url}/analytics/{activity_id}/{student_id}/decision-log"
                elif name == "timeline_url":
                    value = f"{self._base_url}/analytics/{activity_id}/{student_id}/timeline"
                else:
                    value = f"{self._base_url}/analytics/{activity_id}/{student_id}/{name}"
            elif type_ == "text/plain":
                if name == "postmortem_reflection":
                    value = (
                        "Reflexão de exemplo: o grupo conseguiu cumprir o prazo, "
                        "mas com ligeiro aumento de custo para manter a qualidade."
                    )
                else:
                    value = "Texto de exemplo."
            else:
                value = None

            qual_values.append({"name": name, "type": type_, "value": value})

        return [
            {
                "inveniraStdID": student_id,
                "quantAnalytics": quant_values,
                "qualAnalytics": qual_values,
            }
        ]


class RepositoryFactory:
    """Factory Method para instanciar AnalyticsRepository."""

    @staticmethod
    def create_analytics_repository(base_url: str, analytics_schema: dict[str, Any]) -> AnalyticsRepository:
        return JsonAnalyticsRepository(base_url=base_url, analytics_schema=analytics_schema)


class ProPlanRepository:
    """
    Repositório agregador do ProPlan.

    Encapsula:
      - leitura de ficheiros JSON (parâmetros e esquema de analytics)
      - geração de valores de analytics via Factory Method
      - estado de deploy em memória (mock)
      - obtenção da página de configuração (HTML)
    """

    def __init__(
        self,
        *,
        base_url: str,
        base_dir: Path,
        json_params_filename: str = "json_params_url.json",
        analytics_schema_filename: str = "analytics_url.json",
        config_template_relpath: str = "templates/config_proplan.html",
    ):
        self._base_url = base_url
        self._base_dir = base_dir

        self._json_params_path = base_dir / json_params_filename
        self._analytics_schema_path = base_dir / analytics_schema_filename
        self._config_template_path = base_dir / config_template_relpath

        self._json_params = self._load_json(self._json_params_path, default=[])
        self._analytics_schema = self._load_json(
            self._analytics_schema_path, default={"quantAnalytics": [], "qualAnalytics": []}
        )

        # Mock de deploy (estado em memória)
        self._deployed_activities: dict[str, dict[str, Any]] = {}

    @staticmethod
    def _load_json(path: Path, default: Any):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return default

    # --- Operações consumidas pelo Facade ---

    def get_json_params(self) -> list[dict[str, Any]]:
        return self._json_params

    def get_analytics_contract(self) -> dict[str, Any]:
        return self._analytics_schema

    def get_analytics(self, activity_id: str) -> list[dict[str, Any]]:
        repo = RepositoryFactory.create_analytics_repository(self._base_url, self._analytics_schema)
        return repo.get_analytics(activity_id)

    def deploy_activity(self, activity_id: str) -> str:
        access_url = f"{self._base_url}/atividade/{activity_id}"
        self._deployed_activities[activity_id] = {"access_url": access_url, "params": {}}
        return access_url

    def get_config_page(self) -> str:
        # A página de configuração não depende de renderização dinâmica.
        # Lê-se o HTML diretamente, evitando dependências Flask no repositório.
        try:
            return self._config_template_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            # fallback seguro
            return "<html><body><h1>Config ProPlan</h1><p>Template em falta.</p></body></html>"
