from datetime import date
import logging
import os
from typing import List

from ninja import File, Router, Schema, UploadedFile
from ninja.pagination import paginate

# from project.controle_uni.schemas import SchemaCargo
from project.c5.models import MapProduto
from project.controle_uni.schemas import (
    SchemaAgrupador,
    SchemaProdutoOut,
    SchemaRelAgrupadorCargoOut,
    SchemaRelAgrupadorCargoin,
)
import project.schemas as SchemaBase
from project.controle_uni.models import (
    TsmyEuCargoAgrup,
    TsmyEuCargoEpiUnif,
    TsmyEuCargos,
)
from project.setrab.schemas import (
    AdmissaoSchema,
    ConfirmarAdmissaoSchema,
    ConfirmarDemissaoSchema,
    ConfirmarMudFuncaoSchema,
    ConfirmarTransferenciaSchema,
    DemissaoSchema,
    ImportacaoSchema,
    MudFuncaoSchema,
    TransferenciaSchema,
)
from project.setrab.services.importacao import (
    admissao,
    demissao,
    mudanca_funcao,
    transferencia,
)
from project.setrab.services.sincronizar_dados import atualizar_dados

logger = logging.getLogger("agrupador")

router = Router()
CAMINHO_BASE = "/setrab"
CAMINHO_ARQUIVO = "dados.xlsx"
ARQUIVO_ADMISSAO = "ADMISSAO.xls"
ARQUIVO_DEMISSAO = "DEMISSAO.xls"
ARQUIVO_MOD_FUNCAO = "MODFUNCAO.xls"
ARQUIVO_TRANSFERENCIA = "TRANSFERENCIA.xls"


@router.get("/", response=List[ImportacaoSchema])
def get_importacoes(request):
    importacoes = [
        ImportacaoSchema(
            id=1,
            nome_arquivo="arquivo1.csv",
            mes="Janeiro",
            usuario="user1",
            status="Concluído",
            resposta_servidor="Sucesso",
            data_hora="2022-01-01 10:00:00",
        ),
        ImportacaoSchema(
            id=2,
            nome_arquivo="arquivo2.csv",
            mes="Fevereiro",
            usuario="user2",
            status="Em andamento",
            resposta_servidor="Aguardando",
            data_hora="2022-02-01 14:30:00",
        ),
        ImportacaoSchema(
            id=3,
            nome_arquivo="arquivo3.csv",
            mes="Março",
            usuario="user3",
            status="Falha",
            resposta_servidor="Erro",
            data_hora="2022-03-01 09:15:00",
        ),
    ]
    return importacoes


@router.post(
    "/importar/admissao/",
    response={200: List[AdmissaoSchema], 500: SchemaBase.RespostaErro},
    summary="Pega os dados do arquivo de admissão",
)
def importar_arquivo_admissao(
    request,
    data_filtro: date,
    arquivo_admissao: UploadedFile = File(...),  # type: ignore
):
    try:
        with open(ARQUIVO_ADMISSAO, "wb") as f:
            f.write(arquivo_admissao.read())
        dados = admissao(ARQUIVO_ADMISSAO, data_filtro)
        os.remove(ARQUIVO_ADMISSAO)
        return dados
    except Exception as e:
        logger.error(f"Erro ao sincronizar: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.post(
    "/sincronizar/admissao/",
    response={200: SchemaBase.Sucesso, 500: SchemaBase.RespostaErro},
    summary="Sincroniza os dados de admissão",
)
def sincronizar_admissao(request, dados: ConfirmarAdmissaoSchema):
    try:
        for dado in dados:
            print(dado)
        return {"descricao": "Dados Sincronizados com sucesso"}
    except Exception as e:
        logger.error(f"Erro ao sincronizar: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.post(
    "/importar/demissao/",
    response={200: List[DemissaoSchema], 500: SchemaBase.RespostaErro},
    summary="Pega os dados do arquivo de demissão",
)
def importar_arquivo_demissao(
    request,
    data_filtro: date,
    arquivo_demissao: UploadedFile = File(...),  # type: ignore
):
    try:
        with open(ARQUIVO_DEMISSAO, "wb") as f:
            f.write(arquivo_demissao.read())
        dados = demissao(ARQUIVO_DEMISSAO, data_filtro)
        os.remove(ARQUIVO_DEMISSAO)
        return dados
    except Exception as e:
        logger.error(f"Erro ao sincronizar: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.post(
    "/sincronizar/demissao/",
    response={200: SchemaBase.Sucesso, 500: SchemaBase.RespostaErro},
    summary="Sincroniza os dados de demissão",
)
def sincronizar_demissao(request, dados: ConfirmarDemissaoSchema):
    try:
        for dado in dados:
            print(dado)
        return {"descricao": "Dados Sincronizados com sucesso"}
    except Exception as e:
        logger.error(f"Erro ao sincronizar: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.post(
    "/importar/mudFuncao/",
    response={200: List[MudFuncaoSchema], 500: SchemaBase.RespostaErro},
    summary="Pega os dados do arquivo de mudança de função",
)
def importar_arquivo_mudanca_funcao(
    request,
    data_filtro: date,
    arquivo_mudanca_funcao: UploadedFile = File(...),  # type: ignore
):
    try:
        with open(ARQUIVO_MOD_FUNCAO, "wb") as f:
            f.write(arquivo_mudanca_funcao.read())
        dados = mudanca_funcao(ARQUIVO_MOD_FUNCAO, data_filtro)
        os.remove(ARQUIVO_MOD_FUNCAO)
        return dados
    except Exception as e:
        logger.error(f"Erro ao sincronizar: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.post(
    "/sincronizar/mudFuncao/",
    response={200: SchemaBase.Sucesso, 500: SchemaBase.RespostaErro},
    summary="Sincroniza os dados de mudança de função",
)
def sincronizar_mudanca_funcao(request, dados: ConfirmarMudFuncaoSchema):
    try:
        for dado in dados:
            print(dado)
        return {"descricao": "Dados Sincronizados com sucesso"}
    except Exception as e:
        logger.error(f"Erro ao sincronizar: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.post(
    "/importar/transferencia/",
    response={200: List[TransferenciaSchema], 500: SchemaBase.RespostaErro},
    summary="Pega os dados do arquivo de transferência",
)
def importar_arquivo_transferencia(
    request,
    data_filtro: date,
    arquivo_transferencia: UploadedFile = File(...),  # type: ignore
):
    try:
        with open(ARQUIVO_TRANSFERENCIA, "wb") as f:
            f.write(arquivo_transferencia.read())
        dados = transferencia(ARQUIVO_TRANSFERENCIA, data_filtro)
        os.remove(ARQUIVO_TRANSFERENCIA)
        return dados
    except Exception as e:
        logger.error(f"Erro ao sincronizar: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.post(
    "/sincronizar/transferencia/",
    response={200: SchemaBase.Sucesso, 500: SchemaBase.RespostaErro},
    summary="Sincroniza os dados de transferência",
)
def sincronizar_transferencia(request, dados: ConfirmarTransferenciaSchema):
    try:
        for dado in dados:
            print(dado)
        return {"descricao": "Dados Sincronizados com sucesso"}
    except Exception as e:
        logger.error(f"Erro ao sincronizar: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}


@router.post(
    "/sincronizar/",
    response={200: SchemaBase.Sucesso, 500: SchemaBase.RespostaErro},
    summary="Sincroniza os cargos e setores",
)
def sincronizar_dados(
    request,
    arquivo_sincronizacao: UploadedFile = File(...),  # type: ignore
):
    try:
        with open(CAMINHO_ARQUIVO, "wb") as f:
            f.write(arquivo_sincronizacao.read())
        atualizar_dados(CAMINHO_ARQUIVO, request.auth)
        os.remove(CAMINHO_ARQUIVO)
        return {"descricao": "Dados Sincronizados com sucesso"}
    except Exception as e:
        logger.error(f"Erro ao sincronizar: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}
