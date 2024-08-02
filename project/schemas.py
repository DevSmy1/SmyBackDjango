from ninja import Schema
from typing import Any, Optional


class Erro(Schema):
    """Schema auxiliar, não retornado diretamente."""

    descricao: Optional[str]
    detalhes: Optional[Any] = None


class RespostaErro(Schema):
    """Schema da resposta padrão de erro. Ver smy.api_exception_handlers."""

    erro: Erro


class Sucesso(Schema):
    """Schema auxiliar, não retornado diretamente."""

    descricao: Optional[str]
