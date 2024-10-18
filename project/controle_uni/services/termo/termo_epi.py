import logging
from typing import List
from django.db.models import Sum
from project.controle_uni.models import (
    TsmyEuFichaColab,
)
from project.controle_uni.services.dados_epi import verificar_produto_epi

logger = logging.getLogger("termo")


def dados_ficha_epi(ids_fichas: List[int]) -> List[List]:
    try:
        fichas = TsmyEuFichaColab.objects.filter(id_ficha__in=ids_fichas).values(
            "seqproduto", "seqproduto__desccompleta", "custoAtual", "nro_ca"
        )
        fichas = fichas.annotate(total_quantidade=Sum("quantidade"))
        data = [
            [
                """Data 
Entrega""",
                "Qtd",
                "Descrição do E.P.I",
                "Assinatura",
                "CA",
                """Data 
Devolução""",
                "Motivo",
                "Assinatura",
            ],
        ]
        for ficha in fichas:
            if verificar_produto_epi(ficha["seqproduto"]):
                data.append(
                    [
                        "",
                        ficha["total_quantidade"],
                        ficha["seqproduto__desccompleta"].replace("(CONS) ", ""),
                        "",
                        ficha["nro_ca"] if ficha["nro_ca"] else "",
                        "",
                        "",
                        "",
                    ]
                )
        if len(data) == 1:
            return None  # type: ignore
        return data
    except Exception as e:
        print(f"Erro: {e}")
        return False  # type: ignore


def transformar_lista_para_troca_epi(fichas: list):
    try:
        fichasTroca = [
            [
                "C.A",
                "Qtd",
                "Descrição de material",
                "Data",
                "Motivo",
                "Assinatura",
            ]
        ]
        for itens in fichas:
            if itens[1] != "Qtd":
                fichasTroca.append(
                    [
                        itens[4],
                        itens[1],
                        itens[2],
                        itens[0],
                        itens[6],
                        itens[7],
                    ]
                )
        return fichasTroca
    except Exception as e:
        print(f"Erro: {e}")
        logger.error(e)
        return None
