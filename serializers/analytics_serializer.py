from __future__ import annotations

from typing import Any, Dict, List


def serialize_analytics(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Normaliza a resposta de analytics para o formato esperado pela Inven!RA.

    Nota:
    - Nesta versão mantém-se intencionalmente como pass-through (não altera conteúdo),
      garantindo compatibilidade e reduzindo risco de regressão.
    - Este ponto único permite evoluir a normalização futuramente (ex.: coerção de tipos,
      ordenação, limpeza de campos), sem afetar endpoints nem a fachada.
    """
    return records


def serialize_contract(contract: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normaliza o contrato de analytics (analytics_list_url).

    Tal como serialize_analytics, mantém-se como pass-through nesta fase,
    preservando o contrato publicado.
    """
    return contract
