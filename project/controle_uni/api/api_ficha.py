import logging
import os
from typing import List

from ninja import File, Router, Schema, UploadedFile

from project.controle_uni.services.cargo import carregarArquivoCargo
from project.controle_uni.models import TsmyEuFichaColab
from project.controle_uni.schemas import SchemaFichaOut
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
        return TsmyEuFichaColab.objects.filter(
            matricula__matricula=matricula, sit_produto=tipo_ficha
        )
    except Exception as e:
        logger.error(f"Erro ao buscar fichas de cadastro: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.get(
    "/{id_ficha}",
    response={200: SchemaFichaOut, 404: SchemaBase.RespostaErro},
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
