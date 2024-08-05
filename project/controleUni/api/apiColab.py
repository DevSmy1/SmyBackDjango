import logging
import os
from typing import List

from ninja import File, Router, Schema, UploadedFile
from ninja.pagination import paginate

from project.controleUni.core.colab import carregarArquivoColab
from project.controleUni.schemas import SchemaCargo, SchemaColabIn, SchemaColabOut
import project.schemas as SchemaBase
from project.controleUni.models import TsmyEuColaboradores

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
def carregar_arquivo_colab(request, arquivoColab: UploadedFile = File(...)):  # type: ignore
    try:
        with open(CAMINHO_ARQUIVO, "wb") as f:
            f.write(arquivoColab.read())
        carregarArquivoColab(CAMINHO_ARQUIVO, request.auth)
        os.remove(CAMINHO_ARQUIVO)
        return {"descricao": "Arquivo carregado com sucesso"}
    except Exception as e:
        logger.error(f"Erro ao carregar arquivo de colaboradores: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.post(
    "/",
    response={200: SchemaBase.Sucesso, 500: SchemaBase.RespostaErro},
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
    "atualiza/{id_colab}",
    response={200: SchemaBase.Sucesso, 404: SchemaBase.RespostaErro},
    summary="Atualiza um colaborador",
)
def atualizar_colab(request, id_colab: int, data: SchemaColabIn):
    try:
        colab = TsmyEuColaboradores.objects.get(id_colab=id_colab)
        for key, value in data.dict(exclude_unset=True).items():
            setattr(colab, key, value)
        colab.usuarioalt = request.auth
        colab.full_clean()
        colab.save()
        return {"descricao": "Colaborador atualizado com sucesso"}
    except TsmyEuColaboradores.DoesNotExist as e:
        logger.error(f"Erro ao atualizar colaborador {id_colab}: {e}")
        return 404, {
            "erro": {"descricao": "Colaborador não encontrado", "detalhes": str(e)}
        }
    except Exception as e:
        logger.error(f"Erro ao atualizar colaborador {id_colab}: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.delete(
    "deleta/{id_colab}",
    response={200: SchemaBase.Sucesso, 404: SchemaBase.RespostaErro},
    summary="Deleta um colaborador",
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
