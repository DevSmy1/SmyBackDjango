from project.controleUni.models import (
    TsmyEuColaboradores,
    TsmyEuFichaColab,
    TsmyEuLancto,
)
from project.controleUni.schemas import SchemaFichaIn
from project.intranet.models import TsmyIntranetusuario


def pegar_cgo(dados: SchemaFichaIn):
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
