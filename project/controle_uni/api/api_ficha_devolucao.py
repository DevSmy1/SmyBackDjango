import logging
from typing import List

from ninja import Router

import project.schemas as SchemaBase
from project.controle_uni.services.ficha_devolucao import criar_devolucao

logger = logging.getLogger("ficha")

router = Router()
CAMINHO_BASE = "/ficha"


@router.post(
    "/criarDevolucao/",
    response={
        200: SchemaBase.Sucesso,
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
    summary="Cadastrar uma devolução de ficha ",
)
def cadastrar_ficha(request, ids_fichas: List[int]):
    try:
        ids_fichas_desativados = []
        for id_ficha in ids_fichas:
            ficha_devolucao = criar_devolucao(id_ficha, request.auth)
            ids_fichas_desativados.append(ficha_devolucao)
        return 200, {
            "descricao": f"Fichas desativadas: {ids_fichas_desativados.__str__()}",
        }
    except Exception as e:
        logger.error(f"Erro criar Devolução: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}
