# application/proplan_app_service.py
"""
Application Service do ProPlan.

Objetivo:
- Manter o módulo Flask (app.py) "magro" e focado em HTTP/parsing.
- Centralizar orquestração de casos de uso numa camada estável,
  sem alterar o comportamento externo dos endpoints.

Este módulo não deve conhecer detalhes de Flask, nem de request/response.
"""

from __future__ import annotations

from services.proplan_facade import ProPlanServiceFacade


class ProPlanApplicationService:
    """
    Camada de Application Service.

    Encapsula operações de alto nível consumidas pelos endpoints, delegando
    a orquestração no ProPlanServiceFacade (e, por extensão, no repositório).
    """

    def __init__(self, facade: ProPlanServiceFacade):
        self._facade = facade

    # --- Endpoints Inven!RA (operações) ---

    def get_config_page(self) -> str:
        """
        Devolve a página HTML de configuração (config_url).
        """
        return self._facade.get_config_page()

    def get_json_params(self):
        """
        Devolve a lista de parâmetros configuráveis (json_params_url).
        """
        return self._facade.get_json_params()

    def deploy_activity(self, activity_id: str) -> str:
        """
        Executa o deploy de uma instância (user_url) e devolve o access_url.

        A validação do activity_id é garantida pelo Facade, para manter os
        endpoints livres de lógica de domínio.
        """
        return self._facade.deploy_activity(activity_id)

    def get_analytics_contract(self):
        """
        Devolve o contrato (lista) de analytics disponíveis (analytics_list_url).
        """
        return self._facade.get_analytics_contract()

    def get_analytics(self, activity_id: str):
        """
        Devolve os analytics (analytics_url) para uma instância.
        """
        return self._facade.get_analytics(activity_id)
