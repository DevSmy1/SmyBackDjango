import logging
from typing import List
from django.db.models import Min, Sum
from project.controle_uni.models import (
    TsmyEuFichaColab,
)
from project.controle_uni.termo.functionsPdf import formatarDinheiro

logger = logging.getLogger("termo")


def dados_ficha_uni(ids_fichas: List[int]) -> List[List]:
    try:
        fichas = TsmyEuFichaColab.objects.filter(id_ficha__in=ids_fichas).values(
            "seqproduto", "custoAtual"
        )
        fichas = fichas.annotate(
            total_quantidade=Sum("quantidade"),
            total_custo_atual=Sum("custoAtual"),
            nome_produto=Min("seqproduto__desccompleta"),
        )
        data = [["Qtde", "Uniformes", "Valor Unitário", "Valor Total"]]
        for ficha in fichas:
            data.append(
                [
                    ficha["total_quantidade"],
                    ficha["nome_produto"].replace("(CONS) ", ""),
                    formatarDinheiro(ficha["custoAtual"]),
                    formatarDinheiro(ficha["total_custo_atual"]),
                ]  # type: ignore
            )
        if len(data) > 1:
            return data
        raise Exception("Nenhuma ficha encontrada")
    except Exception as e:
        logger.error(f"Erro criar Recibo: {e}")
        raise Exception("Erro ao carregar dados da ficha: ", e)
