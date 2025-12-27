#prepara a tipologia de erro para mapear depois para HTTP 400

class InvalidRequestError(ValueError):
    """Pedido inválido (payload/query sem parâmetros obrigatórios ou com tipo inválido)."""
