import logging
import os
from typing import List

from ninja import Router

from project.controle_uni.services.termo.arquivo import adicionar_rel_arquivo_ficha
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
        recibo_uni = gerar_termo_uni(matricula, ids_fichas)
        recibo_epi, arquivo_integracao = gerar_termo_epi(
            matricula, ids_fichas, request.auth
        )
        adicionar_rel_arquivo_ficha(
            ids_fichas,
            matricula,
            recibo_uni,  # type: ignore
            recibo_epi,  # type: ignore
            arquivo_integracao,  # type: ignore
            request.auth,
        )
        return 200, {
            "descricao": f"Recibo para as fichas {ids_fichas.__str__()}",
        }
    except Exception as e:
        if "recibo_uni" in locals():
            os.remove(recibo_uni)  # type: ignore
        if "recibo_epi" in locals():
            os.remove(recibo_epi)  # type: ignore
        if "arquivo_integracao" in locals():
            os.remove(arquivo_integracao)  # type: ignore
        logger.error(f"Erro criar Recibo: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}
