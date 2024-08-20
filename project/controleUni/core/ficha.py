from datetime import date
from typing import List, Optional

from django.db import connection
from django.core.exceptions import ValidationError
from icecream import ic

from project.c5.models import MapProduto
from project.controleUni.models import (
    TsmyEuCargoAgrup,
    TsmyEuCargoEpiUnif,
    TsmyEuColaboradores,
    TsmyEuFichaColab,
    TsmyEuObservacaoFicha,
    TsmyEuParametro,
)
from project.controleUni.schemas import SchemaAlterarFicha, SchemaFichaIn
from project.intranet.models import TsmyIntranetusuario


def verificar_quantidade_fichas(dados: SchemaFichaIn) -> bool:
    try:
        cargo_colab = TsmyEuColaboradores.objects.get(
            matricula=dados.matricula
        ).cod_funcao
        agrup = MapProduto.objects.get(
            pk=dados.seqproduto
        ).seqfamilia.mapfamatributo.valor
        quantidade_cadastrada = TsmyEuCargoEpiUnif.objects.get(
            cod_funcao=cargo_colab, valor=agrup
        ).quantidade
        return quantidade_cadastrada >= dados.quantidade  # type: ignore
    except TsmyEuColaboradores.DoesNotExist:
        raise ValueError("Colaborador não encontrado")
    except MapProduto.DoesNotExist:
        raise ValueError("Produto não encontrado")
    except TsmyEuCargoEpiUnif.DoesNotExist:
        raise ValueError("Dados de EPI/Uniforme não encontrados")


def pegar_preco_produto(seqproduto: int) -> [float, date]:  # type: ignore
    if seqproduto is None or seqproduto == 0:
        return None, None

    with connection.cursor() as cursor:
        cursor.execute(
            f"""select c.cmdiavlrnf, c.DTAENTRADASAIDA from mrl_custodia c
            where c.seqproduto = {seqproduto}
            and c.nroempresa in (60, 1) 
            and c.cmdiavlrnf > 0
            and rownum = 1
            order by c.dtaentradasaida desc"""
        )
        result = cursor.fetchone()
        if result:
            preco: float = round(result[0], 2)
            data: date = result[1]
            return preco, data
        return None, None


def pegar_percentual_atual() -> List[Optional[float]]:
    parametros = ["3 Meses", "6 Meses", "12 Meses", "12+ Meses"]
    percentuais = []
    for param in parametros:
        percentual = TsmyEuParametro.objects.filter(
            nome_parametro=param, status="A"
        ).first()
        percentuais.append(percentual.parametro if percentual else None)
    return percentuais


def criar_ficha(dados: SchemaFichaIn, usuario: TsmyIntranetusuario) -> List[int]:
    fichas_criadas = []
    try:
        if not verificar_quantidade_fichas(dados):
            raise ValueError(
                "Quantidade de fichas pedidas é maior que a quantidade disponível"
            )

        preco, dataCusto = pegar_preco_produto(dados.seqproduto)
        if preco is None or dataCusto is None:
            raise ValueError("Preço ou data de custo do produto não encontrados")

        percentual = pegar_percentual_atual()
        matricula = TsmyEuColaboradores.objects.get(matricula=dados.matricula)

        for _ in range(dados.quantidade):
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
    except ValidationError as e:
        TsmyEuFichaColab.objects.filter(id__in=fichas_criadas).delete()
        raise ValueError(f"Erro de validação: {e}")
    except Exception as e:
        TsmyEuFichaColab.objects.filter(id__in=fichas_criadas).delete()
        raise e


def alterar_ficha(dados: SchemaAlterarFicha, usuario: TsmyIntranetusuario):
    ficha = TsmyEuFichaColab.objects.get(id_ficha=dados.id_ficha)
    for key, value in dados.dict(exclude_unset=True).items():
        if key == "seqproduto":
            produto = MapProduto.objects.get(pk=value)
            setattr(ficha, key, produto)
            continue
        if key == "matricula":
            colab = TsmyEuColaboradores.objects.get(matricula=value)
            setattr(ficha, key, colab)
            continue
        if key == "id_observacao":
            observacao = TsmyEuObservacaoFicha.objects.get(pk=value)
            setattr(ficha, key, observacao)
            continue
        setattr(ficha, key, value)
    ficha.usuarioalt = usuario
    ficha.full_clean()
    ficha.save()
    return ficha


def desativar_ficha(id_ficha: int, usuario: TsmyIntranetusuario):
    ficha = TsmyEuFichaColab.objects.get(id_ficha=id_ficha)
    ficha.sit_ficha = "D"
    ficha.usuarioalt = usuario
    ficha.full_clean()
    ficha.save()
    return ficha
