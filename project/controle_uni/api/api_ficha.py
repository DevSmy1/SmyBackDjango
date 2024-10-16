import datetime
import logging
from typing import List

from django.db import connection
from ninja import Router

from project.controle_uni.models import (
    TsmyEuCa,
    TsmyEuCargoEpiUnif,
    TsmyEuColaboradores,
    TsmyEuFichaColab,
)
from project.controle_uni.schemas import (
    SchemaFichaOut,
    SchemaFichaUnitOut,
    SchemaVerificarQuantidade,
)
from project.controle_uni.services.dados_epi import (
    verificar_produto_epi,
    verificarNroCa,
)
import project.schemas as SchemaBase

logger = logging.getLogger("ficha")

router = Router()
CAMINHO_BASE = "/ficha"


@router.get(
    "/",
    response={
        200: List[SchemaFichaOut],
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
    summary="Retorna todas as fichas de cadastro",
)
def buscar_fichas(request, matricula: int, tipo_ficha: str):
    try:
        if tipo_ficha == "C":
            tipos = ["C"]
        if tipo_ficha == "TE":
            tipos = ["TE"]
        if tipo_ficha == "TR":
            tipos = ["TR", "TRA"]
        if tipo_ficha == "D":
            tipos = ["D", "DC", "DA", "DM"]
        if tipo_ficha == "OR":
            tipos = ["OR"]
        return TsmyEuFichaColab.objects.filter(
            matricula__matricula=matricula, sit_produto__in=tipos, sit_ficha="A"
        )
    except Exception as e:
        logger.error(f"Erro ao buscar fichas de cadastro: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.get(
    "/desativadas/",
    response={
        200: List[SchemaFichaOut],
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
    summary="Retorna todas as fichas de cadastro",
)
def buscar_fichas_desativadas(request, matricula: int):
    try:
        return TsmyEuFichaColab.objects.filter(
            matricula__matricula=matricula, sit_ficha="D"
        )
    except Exception as e:
        logger.error(f"Erro ao buscar fichas de cadastro: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.get(
    "/{id_ficha}",
    response={200: SchemaFichaUnitOut, 404: SchemaBase.RespostaErro},
    summary="Retorna uma ficha de cadastro específica",
)
def buscar_ficha(request, id_ficha: int):
    try:
        return TsmyEuFichaColab.objects.get(id_ficha=id_ficha)
    except TsmyEuFichaColab.DoesNotExist as e:
        logger.error(f"Erro ao buscar ficha de cadastro {id_ficha}: {e}")
        return 404, {
            "erro": {
                "descricao": "Ficha de cadastro não encontrada",
                "detalhes": str(e),
            }
        }


@router.post(
    "/verificar/",
    response={
        200: SchemaBase.Sucesso,
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
    summary="Verifica se a quantidade de fichas pedidas é maior que a quantidade disponível para o cargo",
)
def verificar_quantidade_fichas(request, dados: SchemaVerificarQuantidade):
    try:
        colab = TsmyEuColaboradores.objects.get(matricula=dados.matricula)
        quantidade_cadastrada = TsmyEuCargoEpiUnif.objects.get(
            cod_funcao=colab.cod_funcao, valor=dados.agrup
        ).quantidade
        quantidade_atual: int = (
            TsmyEuFichaColab.objects.select_related(
                "seqproduto__seqfamilia__mapfamatributo"
            )
            .filter(
                matricula__matricula=colab.matricula,
                seqproduto__seqfamilia__mapfamatributo__valor=dados.agrup,
                sit_ficha="A",
            )
            .exclude(sit_produto__in=["TE"])
            .count()
        )
        return {
            "descricao": str(
                quantidade_cadastrada >= dados.quantidade + quantidade_atual  # type: ignore
            )
        }
    except TsmyEuColaboradores.DoesNotExist:
        logger.error(f"Colaborador não encontrado: {dados.matricula}")
        return 404, {
            "erro": {"descricao": "Colaborador não encontrado", "detalhes": ""}
        }
    except Exception as e:
        logger.error(f"Erro ao verificar quantidade de fichas: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.get(
    "/validarCa/{nro_ca}",
    response={
        200: SchemaBase.Sucesso,
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
)
def validar_ca(request, nro_ca: int):
    try:
        if TsmyEuCa.objects.filter(ca=nro_ca).exists():
            ca = TsmyEuCa.objects.get(ca=nro_ca)
            if ca.dt_validade < datetime.datetime.now().replace(  # type: ignore
                tzinfo=ca.dt_validade.tzinfo  # type: ignore
            ):
                return {"descricao": "True"}
            return {"descricao": "True"}
        if verificarNroCa(nro_ca, request.auth):
            return {"descricao": "True"}
    except ValueError as e:
        return 404, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}
    except Exception as e:
        logger.error(f"Erro ao testar: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.get(
    "/verificarProdutoEpi/{seq_produto}",
    response={
        200: SchemaBase.Sucesso,
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
    tags=["Produtos"],
)
def verificar_produto_epi_request(request, seq_produto: int):
    try:
        epi = verificar_produto_epi(seq_produto)
        return {"descricao": f"{epi}"}
    except Exception as e:
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}
