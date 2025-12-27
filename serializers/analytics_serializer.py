# cria o ponto único para normalização futura
def serialize_analytics(records):
    """
    Normaliza a resposta de analytics para o formato esperado pela Inven!RA.
    Nesta fase, funciona como "pass-through" (não altera), para manter comportamento.
    A normalização real será introduzida quando migrarmos o endpoint.
    """
    return records


def serialize_contract(contract):
    """
    Normaliza o contrato de analytics (analytics_list_url).
    Nesta fase, também é "pass-through".
    """
    return contract
