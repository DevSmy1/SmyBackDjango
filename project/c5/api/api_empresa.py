import logging
from typing import List

from ninja import Router, Schema

import project.schemas as SchemaBase
from project.c5.models import GeEmpresa
from project.c5.schemas import SchemaEmpresa

logger = logging.getLogger("c5")

router = Router()
CAMINHO_BASE = "/c5/empresa"


@router.get(
    "/",
    response={
        200: List[SchemaEmpresa],
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
    summary="Retorna todas as empresas",
)
def buscar_empresa(request):
    try:
        return GeEmpresa.objects.all().exclude(nroempresa__in=[901, 88, 4])
    except GeEmpresa.DoesNotExist as e:
        logger.error(f"Erro ao buscar empresas: {e}")
        return 404, {
            "erro": {"descricao": "Empresas não encontradas", "detalhes": str(e)}
        }
    except Exception as e:
        logger.error(f"Erro ao buscar empresas: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}
