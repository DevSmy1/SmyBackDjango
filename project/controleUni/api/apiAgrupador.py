import logging
from typing import List

from ninja import Router, Schema
from ninja.pagination import paginate

# from project.controleUni.schemas import SchemaCargo
from project.controleUni.schemas import (
    SchemaAgrupador,
    SchemaRelAgrupadorCargoOut,
    SchemaRelAgrupadorCargoin,
)
import project.schemas as SchemaBase
from project.controleUni.models import (
    TsmyEuCargoAgrup,
    TsmyEuCargoEpiUnif,
    TsmyEuCargos,
)

logger = logging.getLogger("agrupador")

router = Router()
CAMINHO_BASE = "/agrupador"


# Agrupador
@router.get(
    "/",
    response={
        200: List[SchemaAgrupador],
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
    summary="Retorna todos os agrupadores",
)
@paginate()
def buscar_agrupadores(request):
    try:
        return (
            TsmyEuCargoAgrup.objects.all()
            .values("codigo", "descricao")
            .order_by("descricao")
        )
    except Exception as e:
        logger.error(f"Erro ao buscar agrupadores: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.get(
    "/{codigo}",
    response={
        200: SchemaAgrupador,
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
    summary="Retorna um agrupador",
)
def buscar_agrupador(request, codigo: int):
    try:
        return TsmyEuCargoAgrup.objects.get(codigo=codigo)
    except TsmyEuCargoAgrup.DoesNotExist as e:
        return 404, {
            "erro": {"descricao": "Colaborador não encontrado", "detalhes": str(e)}
        }
    except Exception as e:
        logger.error(f"Erro ao buscar agrupador: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.post(
    "/",
    response={200: SchemaBase.Sucesso, 500: SchemaBase.RespostaErro},
    summary="Cria um novo agrupador",
)
def criar_agrupador(request, data: SchemaAgrupador):
    try:
        TsmyEuCargoAgrup.objects.create(
            **data.dict(), usuarioincl=request.auth, usuarioalt=request.auth
        )
        return {"descricao": "Agrupador criado com sucesso"}
    except Exception as e:
        logger.error(f"Erro ao criar agrupador: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.put(
    "atualizar/{codigo}",
    response={
        200: SchemaBase.Sucesso,
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
    summary="Atualiza um agrupador",
)
def atualizar_agrupador(request, codigo: int, data: SchemaAgrupador):
    try:
        obj = TsmyEuCargoAgrup.objects.get(codigo=codigo)
        obj.descricao = data.descricao
        obj.usuarioalt = request.auth
        obj.save()
        return {"descricao": "Cargo atualizado com sucesso"}
    except TsmyEuCargoAgrup.DoesNotExist as e:
        return 404, {
            "erro": {"descricao": "Agrupador não encontrado", "detalhes": str(e)}
        }
    except Exception as e:
        logger.error(f"Erro ao atualizar agrupador: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.delete(
    "deletar/{codigo}",
    response={
        200: SchemaBase.Sucesso,
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
    summary="Deletar um agrupador",
)
def deletar_agrupador(request, codigo: int):
    try:
        obj = TsmyEuCargoAgrup.objects.get(codigo=codigo)
        obj.delete()
        return {"descricao": "Agrupador deletado com sucesso"}
    except TsmyEuCargoAgrup.DoesNotExist as e:
        return 404, {
            "erro": {"descricao": "Agrupador não encontrado", "detalhes": str(e)}
        }
    except Exception as e:
        logger.error(f"Erro ao deletar agrupador: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


# Relacionamento Agrupador x Cargo
@router.get(
    "relacionamento/{cargo}",
    response={
        200: List[SchemaRelAgrupadorCargoOut],
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
    summary="Retorna os agrupadores de um cargo",
    tags=["Relacionamento Cargo x Agrupador"],
)
def buscar_agrupadores_cargo(request, cargo: int):
    try:
        return TsmyEuCargoEpiUnif.objects.filter(cod_funcao=cargo)
    except Exception as e:
        logger.error(f"Erro ao buscar agrupadores de um cargo: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.post(
    "relacionamento/{cargo}",
    response={
        200: SchemaBase.Sucesso,
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
    summary="Relaciona um agrupador a um cargo",
    tags=["Relacionamento Cargo x Agrupador"],
)
def criar_relacionamento_agrupador_cargo(
    request, cargo: int, data: SchemaRelAgrupadorCargoin
):
    try:
        if TsmyEuCargoEpiUnif.objects.filter(cod_funcao_id=cargo, valor_id=data.valor):
            return 404, {
                "erro": {"descricao": "Relacionamento ja existente", "detalhes": ""}
            }
        TsmyEuCargoEpiUnif.objects.create(
            cod_funcao_id=cargo,
            valor_id=data.valor,
            quantidade=data.quantidade,
            usuarioincl=request.auth,
            usuarioalt=request.auth,
        )
        return {"descricao": "Relacionamento criado com sucesso"}
    except TsmyEuCargos.DoesNotExist as e:
        return 404, {"erro": {"descricao": "Cargo não encontrado", "detalhes": str(e)}}
    except TsmyEuCargoAgrup.DoesNotExist as e:
        return 404, {
            "erro": {"descricao": "Agrupador não encontrado", "detalhes": str(e)}
        }
    except Exception as e:
        logger.error(f"Erro ao criar relacionamento cargo x agrupador: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.put(
    "relacionamento/atualizar/{cargo}",
    response={
        200: SchemaBase.Sucesso,
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
    summary="Atualiza um relacionamento entre um agrupador e um cargo",
    tags=["Relacionamento Cargo x Agrupador"],
)
def atualizar_relacionamento_agrupador_cargo(
    request, cargo: int, data: SchemaRelAgrupadorCargoin
):
    try:
        obj = TsmyEuCargoEpiUnif.objects.get(cod_funcao_id=cargo, valor_id=data.valor)
        obj.quantidade = data.quantidade
        obj.usuarioalt = request.auth
        obj.save()
        return {"descricao": "Relacionamento atualizado com sucesso"}
    except TsmyEuCargoEpiUnif.DoesNotExist as e:
        return 404, {
            "erro": {"descricao": "Relacionamento não encontrado", "detalhes": str(e)}
        }
    except Exception as e:
        logger.error(f"Erro ao atualizar relacionamento cargo x agrupador: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.delete(
    "relacionamento/deletar/{cargo}",
    response={
        200: SchemaBase.Sucesso,
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
    summary="Deleta um relacionamento entre um agrupador e um cargo",
    tags=["Relacionamento Cargo x Agrupador"],
)
def deletar_relacionamento_agrupador_cargo(request, cargo: int, valor: int):
    try:
        obj = TsmyEuCargoEpiUnif.objects.get(cod_funcao_id=cargo, valor_id=valor)
        obj.delete()
        return {"descricao": "Relacionamento deletado com sucesso"}
    except TsmyEuCargoEpiUnif.DoesNotExist as e:
        return 404, {
            "erro": {"descricao": "Relacionamento não encontrado", "detalhes": str(e)}
        }
    except Exception as e:
        logger.error(f"Erro ao deletar relacionamento cargo x agrupador: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}
