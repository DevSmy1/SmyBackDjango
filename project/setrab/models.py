from django.db import models

from project.intranet.models import SmyUsuario
from project.controle_uni.models import (
    TsmyEuCargos,
    TsmyEuColaboradores,
    TsmyEuSetor,
    TsmyEuFuncao,
)


class BaseModel(models.Model):
    usuario_criacao = models.ForeignKey(
        SmyUsuario,
        on_delete=models.DO_NOTHING,
        related_name="%(class)s_usuario_criacao",
        db_column="id_usuario_criacao",
        null=True,
    )
    data_criacao = models.DateTimeField(auto_now_add=True, null=True)
    usuario_alteracao = models.ForeignKey(
        SmyUsuario,
        on_delete=models.DO_NOTHING,
        related_name="%(class)s_usuario_alteracao",
        db_column="id_usuario_alteracao",
        null=True,
    )
    data_alteracao = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class SetrabArquivoImportacao(BaseModel):
    nome_arquivo = models.CharField(max_length=100)
    mes = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    resposta_servidor = models.CharField(max_length=100)
    arquivo_erro = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "setrab_arquivo_importacao"


class SetrabEmpresaRel(BaseModel):
    """Relacionamento entre empresa que usamos e a empresa do setrab"""

    id_empresa_setrab = models.IntegerField()
    id_empresa = models.IntegerField()

    class Meta:
        db_table = "setrab_empresa_rel"


class SetrabCargoRel(BaseModel):
    """Relacionamento entre cargo que usamos e o cargo do setrab"""

    id_cargo = models.ForeignKey(TsmyEuCargos, on_delete=models.DO_NOTHING)
    id_cargo_setrab = models.IntegerField()
    nro_empresa = models.IntegerField(null=True)

    class Meta:
        db_table = "setrab_cargo_rel"


class SetrabSetorRel(BaseModel):
    """Relacionamento entre setor que usamos e o setor do setrab"""

    id_setor = models.ForeignKey(TsmyEuSetor, on_delete=models.DO_NOTHING)
    id_setor_setrab = models.IntegerField()
    nro_empresa = models.IntegerField(null=True)

    class Meta:
        db_table = "setrab_setor_rel"


class SetrabFuncaoRel(BaseModel):
    """Relacionamento entre função que usamos e a função do setrab"""

    id_funcao = models.ForeignKey(TsmyEuFuncao, on_delete=models.DO_NOTHING)
    id_funcao_setrab = models.IntegerField()
    nro_empresa = models.IntegerField(null=True)

    class Meta:
        db_table = "setrab_funcao_rel"


# class SetrabColaboradorRel(BaseModel):
#     """Relacionamento entre colaborador que usamos e o colaborador do setrab"""

#     id_colaborador = models.ForeignKey(TsmyEuColaboradores, on_delete=models.DO_NOTHING)
#     id_colaborador_setrab = models.IntegerField()


#     class Meta:
#         db_table = "setrab_colaborador_rel"
