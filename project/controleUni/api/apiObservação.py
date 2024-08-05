import logging
from typing import List

from ninja import Router, Schema
from ninja.pagination import paginate

# from project.controleUni.schemas import SchemaCargo
from project.controleUni.schemas import (
    SchemaObservaçãoIn,
    SchemaObservaçãoOut,
)
import project.schemas as SchemaBase
from project.controleUni.models import TsmyEuObservacaoFicha

logger = logging.getLogger("observacao")

router = Router()
CAMINHO_BASE = "/observacao"


@router.get(
    "/",
    response={
        200: List[SchemaObservaçãoOut],
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
    summary="Retorna todas as observações",
)
def buscar_observacoes(request):
    try:
        return (
            TsmyEuObservacaoFicha.objects.all()
            .values("idObservacao", "observacao")
            .order_by("observacao")
        )
    except Exception as e:
        logger.error(f"Erro ao buscar observações: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.get(
    "/{idObservacao}",
    response={
        200: SchemaObservaçãoOut,
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
    summary="Retorna uma observação",
)
def buscar_observacao(request, idObservacao: int):
    try:
        return TsmyEuObservacaoFicha.objects.get(idObservacao=idObservacao)
    except TsmyEuObservacaoFicha.DoesNotExist:
        return 404, {"erro": {"descricao": "Observação não encontrada"}}
    except Exception as e:
        logger.error(f"Erro ao buscar observação: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.post(
    "/",
    response={
        201: SchemaBase.Sucesso,
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
    summary="Cria uma observação",
)
def criar_observacao(request, data: SchemaObservaçãoIn):
    try:
        TsmyEuObservacaoFicha.objects.create(observacao=data.observacao)
        return {"descricao": "Observação criada com sucesso"}
    except Exception as e:
        logger.error(f"Erro ao criar observação: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.put(
    "/{idObservacao}",
    response={
        200: SchemaObservaçãoOut,
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
)
def atualizar_observacao(request, idObservacao: int, data: SchemaObservaçãoIn):
    try:
        obs = TsmyEuObservacaoFicha.objects.get(idObservacao=idObservacao)
        obs.usuarioalt = request.auth
        obs.observacao = data.observacao
        obs.save()
        return obs
    except TsmyEuObservacaoFicha.DoesNotExist:
        return 404, {"erro": {"descricao": "Observação não encontrada"}}
    except Exception as e:
        logger.error(f"Erro ao atualizar observação: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.delete(
    "/{idObservacao}",
    response={
        200: SchemaBase.Sucesso,
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
    summary="Deleta uma observação",
)
def deletar_observacao(request, idObservacao: int):
    try:
        TsmyEuObservacaoFicha.objects.get(idObservacao=idObservacao).delete()
        return {"descricao": "Observação deletada com sucesso"}
    except TsmyEuObservacaoFicha.DoesNotExist:
        return 404, {"erro": {"descricao": "Observação não encontrada"}}
    except Exception as e:
        logger.error(f"Erro ao deletar observação: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}
