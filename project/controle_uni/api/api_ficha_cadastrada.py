import datetime
import logging
import os
from typing import List

from django.db import connection
from ninja import File, Router, Schema, UploadedFile

from project.c5.models import MapProduto
from project.controle_uni.services.cargo import carregar_arquivo_cargo
from project.controle_uni.models import (
    TsmyEuCa,
    TsmyEuCargoEpiUnif,
    TsmyEuColaboradores,
    TsmyEuFichaColab,
)
from project.controle_uni.schemas import (
    SchemaAlterarFicha,
    SchemaFichaIn,
    SchemaFichaOut,
    SchemaVerificarQuantidade,
)
from project.controle_uni.services.dados_epi import verificarNroCa
from project.controle_uni.services.ficha import (
    alterar_ficha,
    criar_ficha,
    desativar_ficha,
)
import project.schemas as SchemaBase

logger = logging.getLogger("ficha")

router = Router()
CAMINHO_BASE = "/ficha"


@router.post(
    "/cadastrar/",
    response={
        200: SchemaBase.Sucesso,
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
    summary="Cadastrar uma ficha de cadastro",
)
def cadastrar_ficha(request, dados: SchemaFichaIn):
    try:
        fichas_criadas = criar_ficha(dados, request.auth)
        return 200, {
            "descricao": fichas_criadas.__str__(),
        }
    except Exception as e:
        logger.error(f"Erro ao cadastrar ficha de cadastro: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.post(
    "/alterar/",
    response={
        200: SchemaBase.Sucesso,
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
    summary="Alterar uma ficha de cadastro",
)
def alterar_ficha_request(request, dados: SchemaAlterarFicha):
    try:
        ficha_alterada = alterar_ficha(dados, request.auth)
        return 200, {
            "descricao": ficha_alterada.__str__(),
        }
    except Exception as e:
        logger.error(f"Erro ao alterar ficha de cadastro: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.post(
    "/desativar/",
    response={
        200: SchemaBase.Sucesso,
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
    summary="Desativar uma ficha de cadastro",
)
def desativar_ficha_request(request, id_ficha: int):
    try:
        ficha = desativar_ficha(id_ficha, request.auth)
        return 200, {"descricao": f"Ficha {ficha.id_ficha} desativada com sucesso"}
    except TsmyEuFichaColab.DoesNotExist as e:
        logger.error(f"Erro ao desativar ficha de cadastro {id_ficha}: {e}")
        return 404, {
            "erro": {
                "descricao": "Ficha de cadastro não encontrada",
                "detalhes": str(e),
            }
        }
    except Exception as e:
        logger.error(f"Erro ao desativar ficha de cadastro {id_ficha}: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}
