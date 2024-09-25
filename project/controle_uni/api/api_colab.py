import logging
import os
from typing import List

from ninja import File, Router, Schema, UploadedFile
from ninja.pagination import paginate

from project.controle_uni.services.colab import carregar_arquivo_colab
from project.controle_uni.schemas import (
    SchemaCargo,
    SchemaColabIn,
    SchemaColabOut,
    SchemaColabOutMin,
)
import project.schemas as SchemaBase
from project.controle_uni.models import TsmyEuColaboradores

logger = logging.getLogger("colab")

router = Router()
CAMINHO_BASE = "/colab"
CAMINHO_ARQUIVO = "colab.xls"


@router.get(
    "/",
    response={200: List[SchemaColabOut], 500: SchemaBase.Erro},
    summary="Retorna todos os colaboradores",
)
@paginate()
def buscar_colabs(request):
    try:
        return TsmyEuColaboradores.objects.exclude(matricula=None)
    except Exception as e:
        logger.error(f"Erro ao buscar colaboradores: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.get(
    "/min/",
    response={200: List[SchemaColabOutMin], 500: SchemaBase.Erro},
    summary="Retorna todos os colaboradores",
)
def buscar_colabs_min(request):
    try:
        return TsmyEuColaboradores.objects.exclude(matricula=None).values(
            "id_colab",
            "matricula",
            "nome",
            "nroempresa",
            "cod_funcao_id",
            "cod_funcao__funcao",
        )
    except Exception as e:
        logger.error(f"Erro ao buscar colaboradores: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.get(
    "/{id_colab}",
    response={200: SchemaColabOut, 404: SchemaBase.RespostaErro},
    summary="Retorna um colaborador específico",
)
def buscar_colab(request, id_colab: int):
    try:
        return TsmyEuColaboradores.objects.get(id_colab=id_colab)
    except TsmyEuColaboradores.DoesNotExist as e:
        logger.error(f"Erro ao buscar colaborador {id_colab}: {e}")
        return 404, {
            "erro": {"descricao": "Colaborador não encontrado", "detalhes": str(e)}
        }
    except Exception as e:
        logger.error(f"Erro ao buscar colaborador {id_colab}: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.post(
    "/carregarArquivo/",
    response={200: SchemaBase.Sucesso, 500: SchemaBase.RespostaErro},
    summary="Carrega um arquivo com os colaboradores",
)
def carregar_arquivo_colaborador(request, arquivoColab: UploadedFile = File(...)):  # type: ignore
    try:
        with open(CAMINHO_ARQUIVO, "wb") as f:
            f.write(arquivoColab.read())
        carregar_arquivo_colab(CAMINHO_ARQUIVO, request.auth)
        os.remove(CAMINHO_ARQUIVO)
        return {"descricao": "Arquivo carregado com sucesso"}
    except Exception as e:
        logger.error(f"Erro ao carregar arquivo de colaboradores: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.post(
    "/",
    response={201: SchemaBase.Sucesso, 500: SchemaBase.RespostaErro},
    summary="Cria um novo colaborador",
)
def criar_colab(request, colab: SchemaColabIn):
    try:
        TsmyEuColaboradores.objects.create(**colab.dict())
        return {"descricao": "Colaborador criado com sucesso"}
    except Exception as e:
        logger.error(f"Erro ao criar colaborador: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.put(
    "alterar/{id_colab}",
    response={200: SchemaBase.Sucesso, 404: SchemaBase.RespostaErro},
    summary="Alterar um colaborador",
)
def alterar_colab(request, id_colab: int, data: SchemaColabIn):
    try:
        colab = TsmyEuColaboradores.objects.get(id_colab=id_colab)
        for key, value in data.dict(exclude_unset=True).items():
            setattr(colab, key, value)
        colab.usuario_alteracao = request.auth
        colab.full_clean()
        colab.save()
        return {"descricao": "Colaborador atualizado com sucesso"}
    except TsmyEuColaboradores.DoesNotExist as e:
        logger.error(f"Erro ao alterar colaborador {id_colab}: {e}")
        return 404, {
            "erro": {"descricao": "Colaborador não encontrado", "detalhes": str(e)}
        }
    except Exception as e:
        logger.error(f"Erro ao alterar colaborador {id_colab}: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.delete(
    "deletar/{id_colab}",
    response={200: SchemaBase.Sucesso, 404: SchemaBase.RespostaErro},
    summary="Deletar um colaborador",
)
def deletar_colab(request, id_colab: int):
    try:
        colab = TsmyEuColaboradores.objects.get(id_colab=id_colab)
        colab.delete()
        return {"descricao": "Colaborador deletado com sucesso"}
    except TsmyEuColaboradores.DoesNotExist as e:
        logger.error(f"Erro ao deletar colaborador {id_colab}: {e}")
        return 404, {
            "erro": {"descricao": "Colaborador não encontrado", "detalhes": str(e)}
        }
    except Exception as e:
        logger.error(f"Erro ao deletar colaborador {id_colab}: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}
