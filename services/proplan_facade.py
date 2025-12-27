# O Facade recebe um repo abstrato 
# (pode ser uma classe simples que vamos criar depois, 
# ou até funções que já existam). 
# Evitamos “refatoração big-bang”.

from exceptions import InvalidRequestError
from serializers.analytics_serializer import serialize_analytics, serialize_contract

class ProPlanServiceFacade:
    """
    Fachada virada para dentro: concentra orquestração interna,
    mantendo os endpoints Flask reduzidos a parsing e HTTP.
    """

    def __init__(self, repo):
        # 'repo' será, por agora, um objeto com funções já existentes no app.py
        # (no próximo passo substituímos por uma classe/repositório dedicado).
        self._repo = repo

    def get_analytics(self, activity_id: str):
        if not activity_id or not isinstance(activity_id, str):
            raise InvalidRequestError("Campo 'activityID' em falta ou inválido.")
        raw = self._repo.get_analytics(activity_id)
        return serialize_analytics(raw)

    def get_analytics_contract(self):
        raw = self._repo.get_analytics_contract()
        return serialize_contract(raw)

    def get_json_params(self):
        return self._repo.get_json_params()

    def get_config_page(self):
        return self._repo.get_config_page()

    def deploy_activity(self, activity_id: str):
        if not activity_id or not isinstance(activity_id, str):
            raise InvalidRequestError("Query param 'activityID' em falta ou inválido.")
        return self._repo.deploy_activity(activity_id)
