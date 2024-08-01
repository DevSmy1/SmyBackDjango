from ninja import Schema


class Error(Schema):
    """Mensagem genérica de erro."""

    message: str


class Success(Schema):
    """Mensagem genérica de sucesso."""

    message: str
