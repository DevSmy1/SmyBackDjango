from project.c5.models import MapProduto
from project.controleUni.models import (
    TsmyEuCargoAgrup,
    TsmyEuCargoEpiUnif,
    TsmyEuColaboradores,
)
from icecream import ic

from project.controleUni.schemas import SchemaFichaIn


def verificar_quantidade_fichas(dados: SchemaFichaIn) -> bool:
    cargo_colab = TsmyEuColaboradores.objects.get(matricula=dados.matricula).cod_funcao
    agrup = MapProduto.objects.get(pk=dados.seqproduto).seqfamilia.mapfamatributo.valor
    quantidade_cadastrada = TsmyEuCargoEpiUnif.objects.get(
        cod_funcao=cargo_colab, valor=agrup
    ).quantidade
    return quantidade_cadastrada >= dados.quantidade  # type: ignore


def criar_ficha(dados: SchemaFichaIn) -> None:
    if not verificar_quantidade_fichas(dados):
        raise ValueError(
            "Quantidade de fichas pedidas é maior que a quantidade disponível"
        )
    for i in range(dados.quantidade):
        ic("Ficha criada com sucesso")
