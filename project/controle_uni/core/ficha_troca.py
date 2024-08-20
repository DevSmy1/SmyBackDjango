from project.controle_uni.core.ficha import criar_ficha
from project.controle_uni.core.lancto import criar_lancto
from project.controle_uni.models import (
    TsmyEuColaboradores,
    TsmyEuFichaColab,
    TsmyEuLancto,
)
from project.controle_uni.schemas import SchemaFichaIn
from project.intranet.models import TsmyIntranetusuario
from django.db.models import Max

from icecream import ic


def criar_troca(id_ficha: int, dadosFicha: SchemaFichaIn, usuario: TsmyIntranetusuario):
    fichasModificadas = []
    try:
        # pegar id de troca
        dadosFicha.id_troca = (
            int(
                TsmyEuFichaColab.objects.exclude(id_troca=None).aggregate(
                    max_id_troca=Max("id_troca")
                )["max_id_troca"]
                or 0
            )
            + 1
        )

        # modificar status da ficha para TR (Troca Recibimento)
        fichaRecebimento = criar_rebimento(id_ficha, dadosFicha, usuario)
        fichasModificadas.append(fichaRecebimento)

        # criar ficha com tipo TE (Troca Envio) usando os dados recebidos
        fichaEnvio = criar_envio(dadosFicha, usuario)
        fichasModificadas.append(fichaEnvio)

        return fichasModificadas
    except Exception as e:
        raise e


def criar_rebimento(
    id_ficha: int, dadosFicha: SchemaFichaIn, usuario: TsmyIntranetusuario
):
    try:
        fichaRecebimento = TsmyEuFichaColab.objects.get(pk=id_ficha)
        fichaRecebimento.id_troca = dadosFicha.id_troca
        if dadosFicha.id_observacao:
            fichaRecebimento.id_observacao_id = dadosFicha.id_observacao  # type: ignore
        if fichaRecebimento.sit_produto != "TRA":
            fichaRecebimento.sit_produto = "TR"
        fichaRecebimento.usuarioalt = usuario
        fichaRecebimento.full_clean()
        fichaRecebimento.save()
        return fichaRecebimento.id_ficha
    except TsmyEuFichaColab.DoesNotExist:
        raise ValueError("Ficha não encontrada")
    except Exception as e:
        raise e


def criar_envio(dadosFicha: SchemaFichaIn, usuario: TsmyIntranetusuario):
    try:
        dadosFicha.sit_produto = "TE"
        dadosFicha.quantidade = 1
        fichaEnvio = criar_ficha(dadosFicha, usuario)
        return fichaEnvio[0]
    except Exception as e:
        raise e


def confirmar_recebimento(id_ficha: int, dadosRecebimento: SchemaFichaIn, usuario):
    try:
        ficha = TsmyEuFichaColab.objects.get(id_ficha=id_ficha)
        if dadosRecebimento.perda:
            criar_lancto(dadosRecebimento, [id_ficha], usuario)
            dadosRecebimento.perda = False
        if criar_lancto(dadosRecebimento, [id_ficha], usuario):
            ficha.sit_ficha = "D"
            ficha.save()
    except TsmyEuFichaColab.DoesNotExist:
        raise ValueError("Ficha não encontrada")
    except Exception as e:
        raise e


def confirmar_envio(id_ficha: int, dadosRecebimento: SchemaFichaIn, usuario):
    try:
        ficha = TsmyEuFichaColab.objects.get(id_ficha=id_ficha)
        if dadosRecebimento.perda:
            raise ValueError("Envio não pode ser uma perda")
        if criar_lancto(dadosRecebimento, [id_ficha], usuario):
            ficha.sit_ficha = "D"
            ficha.save()
    except Exception as e:
        raise e


def cancelar_troca(id_ficha: int):
    try:
        ficha = TsmyEuFichaColab.objects.get(id_ficha=id_ficha)
        ficha.sit_ficha = "C"
        ficha.save()
    except TsmyEuFichaColab.DoesNotExist:
        raise ValueError("Ficha não encontrada")
    except Exception as e:
        raise e
