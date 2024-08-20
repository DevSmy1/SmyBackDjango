import logging
import os
from typing import List

from ninja import File, Router, Schema, UploadedFile

from project.controle_uni.core.cargo import carregarArquivoCargo
from project.controle_uni.schemas import SchemaCargo
import project.schemas as SchemaBase
from project.controle_uni.models import TsmyEuCargos
from ninja.pagination import paginate

logger = logging.getLogger("cargo")

router = Router()
CAMINHO_BASE = "/cargo"
CAMINHO_ARQUIVO = "cargos.pdf"


@router.get(
    "/",
    response={200: List[SchemaCargo], 404: SchemaBase.Erro, 500: SchemaBase.Erro},
    summary="Retorna todos os cargos",
)
def buscar_cargos(request):
    try:
        return TsmyEuCargos.objects.all().values("cod_funcao", "funcao")
    except Exception as e:
        logger.error(f"Erro ao buscar cargos: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.get(
    "/{cod_funcao}",
    response={200: SchemaCargo, 404: SchemaBase.RespostaErro},
    summary="Retorna um cargo específico",
)
def buscar_cargo(request, cod_funcao: int):
    try:
        return TsmyEuCargos.objects.get(cod_funcao=cod_funcao)
    except TsmyEuCargos.DoesNotExist as e:
        logger.error(f"Erro ao buscar cargo {cod_funcao}: {e}")
        return 404, {"erro": {"descricao": "Cargo não encontrado", "detalhes": str(e)}}
    except Exception as e:
        logger.error(f"Erro ao buscar cargo {cod_funcao}: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.post(
    "/carregarArquivo/",
    response={200: SchemaBase.Sucesso, 404: SchemaBase.RespostaErro},
    summary="Carrega um arquivo com os cargos",
)
def carrega_arq_cargos(request, arquivoCargo: UploadedFile = File(...)):  # type: ignore
    try:
        with open(CAMINHO_ARQUIVO, "wb") as f:
            f.write(arquivoCargo.read())
        carregarArquivoCargo(CAMINHO_ARQUIVO, request.auth)
        os.remove(CAMINHO_ARQUIVO)
        return {"descricao": "Arquivo carregado com sucesso"}
    except Exception as e:
        logger.error(f"Erro ao carregar arquivo de cargos: {e}")
        return 404, {
            "erro": {"descricao": "Erro ao carregar arquivo", "detalhes": str(e)}
        }


@router.post(
    "/",
    response={201: SchemaBase.Sucesso, 404: SchemaBase.RespostaErro},
    summary="Cria um novo cargo",
)
def criar_cargo(request, data: SchemaCargo):
    try:
        TsmyEuCargos.objects.create(
            **data.dict(), usuarioincl=request.auth, usuarioalt=request.auth
        )
        return 201, {"descricao": "Cargo criado com sucesso"}
    except Exception as e:
        logger.error(f"Erro ao criar cargo: {e}")
        return 404, {"erro": {"descricao": "Erro ao criar cargo", "detalhes": str(e)}}


@router.put(
    "/alterar/",
    response={
        200: SchemaBase.Sucesso,
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
    summary="Alterar um cargo",
)
def alterar_cargo(request, data: SchemaCargo):
    try:
        cargo = TsmyEuCargos.objects.get(cod_funcao=data.cod_funcao)
        for key, value in data.dict(exclude_unset=True).items():
            setattr(cargo, key, value)
        cargo.usuarioalt = request.auth
        cargo.full_clean()
        cargo.save()
        return {"descricao": "Cargo atualizado com sucesso"}
    except TsmyEuCargos.DoesNotExist as e:
        logger.error(f"Erro ao alterar cargo {data.cod_funcao}: {e}")
        return 404, {"erro": {"descricao": "Cargo não encontrado", "detalhes": str(e)}}
    except Exception as e:
        logger.error(f"Erro ao alterar cargo: {e}")
        return 500, {"erro": {"descricao": "Erro ao alterar cargo", "detalhes": str(e)}}


@router.delete(
    "/deletar/{cod_funcao}",
    response={
        200: SchemaBase.Sucesso,
        404: SchemaBase.RespostaErro,
        500: SchemaBase.RespostaErro,
    },
    summary="Deleta um cargo",
)
def deletar_cargo(request, cod_funcao: int):
    try:
        TsmyEuCargos.objects.get(cod_funcao=cod_funcao).delete()
        return {"descricao": "Cargo deletado com sucesso"}
    except TsmyEuCargos.DoesNotExist as e:
        logger.error(f"Erro ao deletar cargo {cod_funcao}: {e}")
        return 404, {"erro": {"descricao": "Cargo não encontrado", "detalhes": str(e)}}
    except Exception as e:
        logger.error(f"Erro ao deletar cargo: {e}")
        return 500, {"erro": {"descricao": "Erro ao deletar cargo", "detalhes": str(e)}}
