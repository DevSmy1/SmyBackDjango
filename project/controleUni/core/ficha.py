from datetime import date

from django.db import connection
from icecream import ic

from project.c5.models import MapProduto
from project.controleUni.models import (
    TsmyEuCargoAgrup,
    TsmyEuCargoEpiUnif,
    TsmyEuColaboradores,
    TsmyEuFichaColab,
    TsmyEuParametro,
)
from project.controleUni.schemas import SchemaFichaIn
from project.intranet.models import TsmyIntranetusuario


def verificar_quantidade_fichas(dados: SchemaFichaIn) -> bool:
    cargo_colab = TsmyEuColaboradores.objects.get(matricula=dados.matricula).cod_funcao
    agrup = MapProduto.objects.get(pk=dados.seqproduto).seqfamilia.mapfamatributo.valor
    quantidade_cadastrada = TsmyEuCargoEpiUnif.objects.get(
        cod_funcao=cargo_colab, valor=agrup
    ).quantidade
    return quantidade_cadastrada >= dados.quantidade  # type: ignore


def pegar_preco_produto(seqproduto: int) -> [float, date]:  # type: ignore
    with connection.cursor() as cursor:
        if seqproduto is None or seqproduto == 0:
            return None, None
        result = cursor.execute(
            f"""select c.cmdiavlrnf, c.DTAENTRADASAIDA from mrl_custodia c
            where c.seqproduto = {seqproduto}
            and c.nroempresa in (60, 1) 
            and c.cmdiavlrnf > 0
            and rownum = 1
            order by c.dtaentradasaida desc"""
        )
        result = result.fetchall()  # type: ignore
        preco: float = round(result[0][0], 2)
        data: date = result[0][1]
        return preco, data


def pegar_percentual_atual():
    percentual3 = (
        TsmyEuParametro.objects.filter(nome_parametro="3 Meses", status="A")
        .first()
        .parametro  # type: ignore
    )
    percentual6 = (
        TsmyEuParametro.objects.filter(nome_parametro="6 Meses", status="A")
        .first()
        .parametro  # type: ignore
    )
    percentual12 = (
        TsmyEuParametro.objects.filter(nome_parametro="12 Meses", status="A")
        .first()
        .parametro  # type: ignore
    )
    percentual12Mais = (
        TsmyEuParametro.objects.filter(nome_parametro="12+ Meses", status="A")
        .first()
        .parametro  # type: ignore
    )
    return [percentual3, percentual6, percentual12, percentual12Mais]  # type: ignore


def criar_ficha(dados: SchemaFichaIn, usuario: TsmyIntranetusuario) -> list:
    fichas_criadas = []
    try:
        if not verificar_quantidade_fichas(
            dados
        ):  # Verifica se a quantidade de fichas pedidas é maior que a quantidade disponível
            raise ValueError(
                "Quantidade de fichas pedidas é maior que a quantidade disponível"
            )
        preco, dataCusto = pegar_preco_produto(
            dados.seqproduto
        )  # Pega o preço do produto e a data que foi cadastrado
        percentual = pegar_percentual_atual()  # Pega o percentual atual para desconto
        matricula = TsmyEuColaboradores.objects.get(
            matricula=dados.matricula
        )  # Pega a instancia de colaborador por meio da matricula
        for i in range(dados.quantidade):
            ficha = TsmyEuFichaColab(
                seqproduto_id=dados.seqproduto,
                matricula=matricula,
                sit_produto=dados.sit_produto,
                sit_ficha="A",
                quantidade=1,
                nro_ca=dados.nro_ca or None,
                id_observacao_id=dados.id_observacao or None,
                custoAtual=preco,
                dataCusto=dataCusto,
                percentual=percentual,
                usuarioincl=usuario,
                usuarioalt=usuario,
            )
            ficha.full_clean()
            ficha.save()
            fichas_criadas.append(ficha.id_ficha)
        return fichas_criadas
    except Exception as e:
        TsmyEuFichaColab.objects.filter(id__in=fichas_criadas).delete()
        raise e
