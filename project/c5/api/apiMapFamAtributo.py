import logging
from typing import List

from ninja import Router, Schema

import project.schemas as SchemaBase
from project.c5.models import MapFamatributo
from project.c5.schemas import SchemaMapFamatributo
from django.db.models import Q

logger = logging.getLogger("c5")

router = Router()
CAMINHO_BASE = "/c5/atributos"


@router.get(
    "/{valor}",
    response={
        200: List[SchemaMapFamatributo],
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
    summary="Retorna as familias dentro de um agrupador",
    tags=["Agrupador"],
)
def buscar_familias(request, valor: str):
    try:
        familias = (
            MapFamatributo.objects.filter(valor=valor)
            .exclude(Q(valor__icontains="Peso") | Q(valor__icontains="Cont"))
            .values("seqfamilia", "seqfamilia__familia", "descatributo", "valor")
        )
        # if familias.count() == 0:
        #     return 404, {
        #         "erro": {
        #             "descricao": "Familias não encontradas",
        #             "detalhes": "Nenhuma familia encontrada para o valor informado",
        #         }
        #     }
        return familias
    except MapFamatributo.DoesNotExist as e:
        logger.error(f"Erro ao buscar familias {valor}: {e}")
        return 404, {
            "erro": {"descricao": "Familias não encontradas", "detalhes": str(e)}
        }
    except Exception as e:
        logger.error(f"Erro ao buscar familias {valor}: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}
