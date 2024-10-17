import logging
from typing import List

from ninja import Router

from project.controle_uni.services.termo.gerar_termo import (
    gerar_termo_epi,
    gerar_termo_uni,
)
import project.schemas as SchemaBase
from icecream import ic

logger = logging.getLogger("ficha")

router = Router()
CAMINHO_BASE = "/termo"


@router.post(
    "/criarRecibo/",
    response={
        200: SchemaBase.Sucesso,
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
    summary="Criar recibo de entrega de EPI e Uniforme",
)
def criar_recibo(
    request,
    matricula: int,
    ids_fichas: List[int],
):
    try:
        # ic(gerarTermoUni(matricula, ids_fichas))
        gerar_termo_epi(matricula, ids_fichas)
        return 200, {
            "descricao": f"Recibo para as fichas {ids_fichas.__str__()}",
        }
    except Exception as e:
        logger.error(f"Erro criar Recibo: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}
