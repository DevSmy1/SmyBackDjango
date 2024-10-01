import logging
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
from project.setrab.services.sincronizar_dados import atualizar_dados

logger = logging.getLogger("agrupador")

router = Router()
CAMINHO_BASE = "/setrab"
CAMINHO_ARQUIVO = "dados.xlsx"


class Importacao(Schema):
    id: int
    nome_arquivo: str
    mes: str
    usuario: str
    status: str
    resposta_servidor: str
    data_hora: str


@router.get("/", response=List[Importacao])
def get_importacoes(request):
    importacoes = [
        Importacao(
            id=1,
            nome_arquivo="arquivo1.csv",
            mes="Janeiro",
            usuario="user1",
            status="Concluído",
            resposta_servidor="Sucesso",
            data_hora="2022-01-01 10:00:00",
        ),
        Importacao(
            id=2,
            nome_arquivo="arquivo2.csv",
            mes="Fevereiro",
            usuario="user2",
            status="Em andamento",
            resposta_servidor="Aguardando",
            data_hora="2022-02-01 14:30:00",
        ),
        Importacao(
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
    "/sincronizar/",
    response={200: SchemaBase.Sucesso, 500: SchemaBase.RespostaErro},
    summary="Carrega um arquivo com os colaboradores",
)
def carregar_arquivo_colaborador(request, arquivoSinc: UploadedFile = File(...)):  # type: ignore
    try:
        with open(CAMINHO_ARQUIVO, "wb") as f:
            f.write(arquivoSinc.read())
        atualizar_dados(CAMINHO_ARQUIVO, request.auth)
        return {"descricao": "Dados Sincronizados com sucesso"}
    except Exception as e:
        logger.error(f"Erro ao sincronizar: {e}")
        return 500, {"erro": {"descricao": "Erro interno", "detalhes": str(e)}}
