from project.c5.models import MapProduto
from project.controle_uni.models import (
    TsmyEuColaboradores,
    TsmyEuFichaColab,
    TsmyEuLancto,
)
from project.controle_uni.schemas import SchemaAlterarFicha, SchemaFichaIn
from project.intranet.models import TsmyIntranetusuario


def pegar_cgo(dados: SchemaFichaIn | SchemaAlterarFicha):
    if dados.perda:
        return 722, "E"
    if dados.nro_empresa_orig == 1 and dados.nro_empresa_dest == 1:
        if dados.sit_produto in ["C", "TE"]:
            return 700, "S"
        if dados.sit_produto in ["D", "TR", "TRA"]:
            return 600, "E"
    if (
        dados.nro_empresa_orig == 1
        and dados.nro_empresa_dest != 1
        and dados.sit_produto in ["C", "TE"]
    ):
        if dados.presencial:
            return 219, "S"
        return 221, "S"
    if (
        dados.nro_empresa_orig != 1
        and dados.nro_empresa_dest == 1
        and dados.sit_produto in ["D", "TR", "TRA"]
    ):
        if dados.presencial:
            return 219, "E"
        return 221, "E"
    raise ValueError("Situação inválida")


def criar_lancto(dados: SchemaFichaIn, id_fichas: list, usuario: TsmyIntranetusuario):
    lanctos = []
    try:
        cgo, tipo = pegar_cgo(dados)
        matricula = TsmyEuColaboradores.objects.get(matricula=dados.matricula)
        for id_ficha in id_fichas:
            lancto = TsmyEuLancto(
                seqproduto_id=dados.seqproduto,
                matricula=matricula,
                cgo_id=cgo,
                tipo=tipo,
                id_ficha_id=id_ficha,
                quantidade=1,
                nroemporig=dados.nro_empresa_orig,
                nroempdest=dados.nro_empresa_dest,
                usuarioincl=usuario,
                usuarioalt=usuario,
            )
            lancto.full_clean()
            lancto.save()
            lanctos.append(lancto.id_lancto)
        return lanctos
    except TsmyEuColaboradores.DoesNotExist:
        TsmyEuFichaColab.objects.filter(id_ficha__in=id_fichas).delete()
        raise ValueError("Matrícula não encontrada")
    except Exception as e:
        TsmyEuLancto.objects.filter(id_lancto__in=lancto).delete()
        TsmyEuFichaColab.objects.filter(id_ficha__in=id_fichas).delete()
        raise e


def alterar_lanctos(dados: SchemaAlterarFicha, usuario: TsmyIntranetusuario):
    lanctos = TsmyEuLancto.objects.filter(id_ficha_id=dados.id_ficha)
    matricula = TsmyEuColaboradores.objects.get(matricula=dados.matricula)
    for lacnto in lanctos:
        lacnto.seqproduto_id = dados.seqproduto  # type: ignore
        lacnto.matricula = matricula  # type: ignore
        lacnto.nroempdest = dados.nro_empresa_dest
        lacnto.nroemporig = dados.nro_empresa_orig
        cgo, tipo = pegar_cgo(dados)
        lacnto.cgo_id = cgo  # type: ignore
        lacnto.tipo = tipo

        lacnto.usuarioalt = usuario
        lacnto.full_clean()
        lacnto.save()
    return lanctos


def deletar_lanctos(id_ficha: int):
    try:
        lanctos = TsmyEuLancto.objects.filter(id_ficha_id=id_ficha, dt_arquivo=None)
        lanctos.delete()
        return
    except TsmyEuLancto.DoesNotExist:
        raise ValueError("Lançamento não encontrado")
    except Exception as e:
        raise e
