from project.controle_uni.services.ficha import criar_ficha
from project.controle_uni.services.lancto import criar_lancto
from project.controle_uni.models import (
    TsmyEuColaboradores,
    TsmyEuFichaColab,
    TsmyEuLancto,
)
from project.controle_uni.schemas import SchemaFichaIn
from project.intranet.models import TsmyIntranetusuario

from icecream import ic


def criar_devolucao(id_ficha: int, usuario: TsmyIntranetusuario):
    try:
        ficha = TsmyEuFichaColab.objects.get(pk=id_ficha)
        ficha.sit_produto = "D"
        ficha.usuarioalt = usuario
        ficha.full_clean()
        ficha.save()
        return ficha.id_ficha
    except TsmyEuFichaColab.DoesNotExist:
        raise ValueError("Ficha não encontrada")
    except Exception as e:
        raise e


def criar_devolucao_antiga(dadosFicha: SchemaFichaIn, usuario: TsmyIntranetusuario):
    try:
        dadosFicha.sit_produto = "DA"
        fichas = criar_ficha(dadosFicha, usuario)
        return fichas[0]
    except Exception as e:
        raise e


def confirmar_devolucao(id_ficha: int, dadosDevolucao: SchemaFichaIn, usuario):
    try:
        ficha = TsmyEuFichaColab.objects.get(id_ficha=id_ficha)
        dadosDevolucao.sit_produto = "D"
        if dadosDevolucao.perda:
            criar_lancto(dadosDevolucao, [id_ficha], usuario)
            dadosDevolucao.perda = False
        if criar_lancto(dadosDevolucao, [id_ficha], usuario):
            ficha.sit_ficha = "D"
            ficha.save()
    except TsmyEuFichaColab.DoesNotExist:
        raise ValueError("Ficha não encontrada")
    except Exception as e:
        raise e
