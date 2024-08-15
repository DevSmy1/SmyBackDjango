from django.db import models
from project.c5.models import MapProduto, MaxCodgeraloper
from project.intranet.models import TsmyIntranetusuario


class TsmyEuAutorizacao(models.Model):
    id_autorizacao = models.SmallAutoField(primary_key=True)
    usuarioincl = models.ForeignKey(
        TsmyIntranetusuario,
        models.CASCADE,
        related_name="fk_usuario_inclusao_autorizacao",
        db_column="usuarioincl",
        blank=True,
        null=True,
    )
    dt_inclusao = models.DateTimeField()
    matricula = models.IntegerField()
    cod_funcao = models.ForeignKey(
        "TsmyEuCargos",
        models.CASCADE,
        related_name="fk_cargo_autorizacao",
        db_column="cod_funcao",
        blank=True,
        null=True,
    )

    class Meta:
        # managed = False
        db_table = "tsmy_eu_autorizacao"


class TsmyEuColaboradores(models.Model):
    id_colab = models.SmallAutoField(primary_key=True)
    nroempresa = models.IntegerField(
        blank=True,
        null=True,
    )
    matricula = models.IntegerField(unique=True, blank=True, null=True)
    cpf = models.IntegerField(unique=True, blank=True, null=True)
    nome = models.CharField(max_length=60, blank=True, null=True)
    genero = models.CharField(max_length=1, blank=True, null=True)
    dt_adm = models.DateField(blank=True, null=True, db_column="dt_admissao")
    dt_desligamento = models.DateField(blank=True, null=True)
    cod_funcao = models.ForeignKey(
        "TsmyEuCargos",
        models.DO_NOTHING,
        related_name="fk_cargo_colab",
        db_column="id_cod_funcao",
        blank=True,
        null=True,
    )
    cod_funcao_nova = models.ForeignKey(
        "TsmyEuCargos",
        models.CASCADE,
        related_name="fk_cargo_nova_colab",
        db_column="id_cod_funcao_nova",
        blank=True,
        null=True,
    )
    cod_funcao_ant = models.ForeignKey(
        "TsmyEuCargos",
        models.CASCADE,
        related_name="fk_cargo_ant_colab",
        db_column="id_cod_funcao_ant",
        blank=True,
        null=True,
    )
    dt_inclusao = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    dt_alteracao = models.DateTimeField(blank=True, null=True, auto_now=True)
    dt_experiencia = models.DateTimeField(blank=True, null=True)
    usuarioincl = models.ForeignKey(
        TsmyIntranetusuario,
        models.CASCADE,
        related_name="fk_usuario_inclusao_colab",
        db_column="usuarioincl",
        blank=True,
        null=True,
    )
    usuarioalt = models.ForeignKey(
        TsmyIntranetusuario,
        models.CASCADE,
        related_name="fk_usuario_alteracao_colab",
        db_column="usuarioalt",
        blank=True,
        null=True,
    )

    class Meta:
        # # managed = False
        db_table = "tsmy_eu_colaboradores"

    def __str__(self):
        return self.nome


class TsmyEuCargos(models.Model):
    cod_funcao = models.SmallAutoField(primary_key=True)
    funcao = models.CharField(max_length=50, blank=True, null=True)
    dt_inclusao = models.DateTimeField(blank=True, null=True)
    dt_alteracao = models.DateTimeField(blank=True, null=True)
    usuarioincl = models.ForeignKey(
        TsmyIntranetusuario,
        models.CASCADE,
        related_name="fk_usuario_inclusao_cargo",
        db_column="usuarioincl",
        blank=True,
        null=True,
    )
    usuarioalt = models.ForeignKey(
        TsmyIntranetusuario,
        models.CASCADE,
        related_name="fk_usuario_alteracao_cargo",
        db_column="usuarioalt",
        blank=True,
        null=True,
    )

    class Meta:
        # # managed = False
        db_table = "tsmy_eu_cargos"


class TsmyEuCargoAgrup(models.Model):
    """O model de Agrupador é uma tabela que usamos para criar um valor de agrupador que será igual ao da consinco para assim ser facil o acesso as familias."""

    codigo = models.SmallAutoField(primary_key=True, db_column="valor")
    descricao = models.CharField(max_length=50)
    dt_inclusao = models.DateTimeField(blank=True, null=True)
    dt_alteracao = models.DateTimeField(blank=True, null=True)
    usuarioincl = models.ForeignKey(
        TsmyIntranetusuario,
        models.CASCADE,
        related_name="fk_usuario_inclusao_cargo_agrup",
        db_column="usuarioincl",
        blank=True,
        null=True,
    )
    usuarioalt = models.ForeignKey(
        TsmyIntranetusuario,
        models.CASCADE,
        related_name="fk_usuario_alteracao_cargo_agrup",
        db_column="usuarioalt",
        blank=True,
        null=True,
    )

    class Meta:
        # managed = False
        db_table = "tsmy_eu_cargo_agrup"


class TsmyEuCargoEpiUnif(models.Model):
    # seqfamilia = models.IntegerField(blank=True, null=True)
    cod_funcao = models.ForeignKey(
        TsmyEuCargos,
        models.CASCADE,
        db_column="id_cod_funcao",
        related_name="fk_cargo_epi_unif",
        blank=True,
        null=True,
    )
    valor = models.ForeignKey(
        "TsmyEuCargoAgrup",
        models.CASCADE,
        db_column="id_valor",
        related_name="fk_codigo_epi_unif",
        blank=True,
        null=True,
    )
    quantidade = models.IntegerField(blank=True, null=True)
    usuarioincl = models.ForeignKey(
        TsmyIntranetusuario,
        models.CASCADE,
        db_column="usuarioincl",
        related_name="fk_usuario_inclusao_epi_unif",
        blank=True,
        null=True,
    )
    usuarioalt = models.ForeignKey(
        TsmyIntranetusuario,
        models.CASCADE,
        db_column="usuarioalt",
        related_name="fk_usuario_alteracao_epi_unif",
        blank=True,
        null=True,
    )
    dt_inclusao = models.DateTimeField(blank=True, null=True)
    dt_alteracao = models.DateTimeField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = "tsmy_eu_cargo_epi_unif"


class TsmyEuFichaColab(models.Model):
    nroempresa = models.IntegerField(
        blank=True,
        null=True,
    )
    seqproduto = models.ForeignKey(
        MapProduto,
        models.DO_NOTHING,
        db_column="seqproduto",
        related_name="fk_seqproduto_ficha_colab",
        blank=True,
        null=True,
    )
    quantidade = models.IntegerField(
        blank=True,
        null=True,
    )
    dt_inclusao = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    dt_alteracao = models.DateTimeField(blank=True, null=True, auto_now=True)
    usuarioincl = models.ForeignKey(
        TsmyIntranetusuario,
        models.CASCADE,
        related_name="fk_usuario_inclusao_ficha_colab",
        db_column="usuarioincl",
        blank=True,
        null=True,
    )
    usuarioalt = models.ForeignKey(
        TsmyIntranetusuario,
        models.CASCADE,
        related_name="fk_usuario_alteracao_ficha_colab",
        db_column="usuarioalt",
        blank=True,
        null=True,
    )
    matricula = models.ForeignKey(
        "TsmyEuColaboradores",
        models.CASCADE,
        related_name="fk_matricula_ficha_colab",
        db_column="id_colab_matricula",
        blank=True,
        null=True,
    )
    cpf = models.ForeignKey(
        "TsmyEuColaboradores",
        models.CASCADE,
        related_name="fk_cpf_ficha_colab",
        db_column="id_colab_cpf",
        blank=True,
        null=True,
    )
    sit_produto = models.CharField(
        max_length=2,
        blank=True,
        null=True,
        db_comment="Tipos da Ficha: C(Cadastrada), T(Troca), A(Aguardando Aprovação de Troca), TA(Troca Antiga), D(Devolução), DC(Devolução de Cargo), DA(Devolução Antiga)",
    )
    cod_funcao = models.ForeignKey(
        "TsmyEuCargos",
        models.CASCADE,
        related_name="fk_cargo_ficha_colab",
        db_column="id_cod_funcao",
        blank=True,
        null=True,
    )
    sit_ficha = models.CharField(max_length=1, blank=True, null=True)
    id_troca = models.IntegerField(
        blank=True,
        null=True,
    )
    id_ficha = models.AutoField(primary_key=True)
    # Recibo
    reciboUni = models.ForeignKey(
        "TsmyEuArquivo",
        models.CASCADE,
        related_name="fk_recibo_uni_ficha_colab",
        db_column="id_reciboUni",
        blank=True,
        null=True,
    )
    reciboEpi = models.ForeignKey(
        "TsmyEuArquivo",
        models.CASCADE,
        related_name="fk_recibo_epi_ficha_colab",
        db_column="id_reciboEpi",
        blank=True,
        null=True,
    )
    reciboRescisao = models.ForeignKey(
        "TsmyEuArquivo",
        models.CASCADE,
        related_name="fk_recibo_recisao_ficha_colab",
        db_column="id_reciboRecisao",
        blank=True,
        null=True,
    )
    reciboPerda = models.ForeignKey(
        "TsmyEuArquivo",
        models.CASCADE,
        related_name="fk_recibo_perda_ficha_colab",
        db_column="id_reciboPerda",
        blank=True,
        null=True,
    )
    # parametros
    custoAtual = models.CharField(max_length=50, blank=True, null=True)
    dataCusto = models.DateField(blank=True, null=True)
    # o campo percentual ira guardar uma lista de ids dos percentuais
    percentual = models.CharField(max_length=50, blank=True, null=True)
    # Validade do EPI
    nro_ca = models.CharField(max_length=5, blank=True, null=True)
    dt_validade = models.DateTimeField(blank=True, null=True)
    # Campo de Observação
    id_observacao = models.ForeignKey(
        "TsmyEuObservacaoFicha",
        models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        # # managed = False
        db_table = "tsmy_eu_ficha_colab"


class TsmyEuLancto(models.Model):
    id_lancto = models.AutoField(primary_key=True)
    seqproduto = models.ForeignKey(
        MapProduto,
        models.DO_NOTHING,
        db_column="seqproduto",
        related_name="fk_seqproduto_lancto",
        blank=True,
        null=True,
    )
    usuarioincl = models.ForeignKey(
        TsmyIntranetusuario,
        models.CASCADE,
        related_name="fk_usuario_inclusao_lancto",
        db_column="usuarioincl",
        blank=True,
        null=True,
    )
    usuarioalt = models.ForeignKey(
        TsmyIntranetusuario,
        models.CASCADE,
        related_name="fk_usuario_alteracao_lancto",
        db_column="usuarioalt",
        blank=True,
        null=True,
    )
    matricula = models.ForeignKey(
        "TsmyEuColaboradores",
        models.CASCADE,
        related_name="fk_matricula_lancto",
        db_column="id_colab_matricula",
        blank=True,
        null=True,
    )
    cgo = models.ForeignKey(
        MaxCodgeraloper,
        models.CASCADE,
        related_name="fk_cgo_lancto",
        db_column="cgo",
        blank=True,
        null=True,
    )
    id_ficha = models.ForeignKey(
        "TsmyEuFichaColab",
        models.CASCADE,
        related_name="fk_id_ficha_lancto",
        db_column="id_ficha",
        blank=True,
        null=True,
    )
    nroemporig = models.IntegerField(
        blank=True,
        null=True,
    )
    nroempdest = models.IntegerField(
        blank=True,
        null=True,
    )
    dt_arquivo = models.DateField(blank=True, null=True)
    quantidade = models.IntegerField(
        blank=True,
        null=True,
    )
    tipo = models.CharField(max_length=1, blank=True, null=True)
    dt_inclusao = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    dt_alteracao = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        # # managed = False
        db_table = "tsmy_eu_lancto"


class TsmyEuCodLogInform(models.Model):
    cod_inform = models.AutoField(primary_key=True)
    informacao = models.CharField(max_length=200)

    class Meta:
        # managed = False
        db_table = "tsmy_eu_cod_log_inform"


class TsmyEuLog(models.Model):
    tabela = models.CharField(max_length=50)
    acao = models.CharField(max_length=20)
    campo = models.CharField(max_length=50)
    antes = models.CharField(max_length=50)
    depois = models.CharField(max_length=50)
    usuarioincl = models.ForeignKey(
        TsmyIntranetusuario,
        models.CASCADE,
        related_name="fk_usuario_inclusao_log",
        db_column="usuarioincl",
        blank=True,
        null=True,
    )
    dt_inclusao = models.DateTimeField()
    cod_inform = models.ForeignKey(
        TsmyEuCodLogInform,
        models.CASCADE,
        related_name="fk_cod_inform_log",
        db_column="cod_inform",
        blank=True,
        null=True,
    )

    class Meta:
        # managed = False
        db_table = "tsmy_eu_log"


class TsmyEuMovimentNf(models.Model):
    id_mov_nf = models.AutoField(primary_key=True)
    nroempresa_orig = models.IntegerField(
        blank=True,
        null=True,
    )
    nroempresa_dest = models.IntegerField(
        blank=True,
        null=True,
    )
    seqproduto = models.ForeignKey(
        MapProduto,
        models.DO_NOTHING,
        db_column="seqproduto",
        related_name="fk_seqproduto_mov_nf",
        blank=True,
        null=True,
    )
    quantidade = models.IntegerField(blank=True, null=True)
    usuarioincl = models.ForeignKey(
        TsmyIntranetusuario,
        models.CASCADE,
        related_name="fk_usuario_inclusao_mov_nf",
        db_column="usuarioincl",
        blank=True,
        null=True,
    )
    dt_inclusao = models.DateTimeField(blank=True, null=True)
    matricula = models.IntegerField(blank=True, null=True)
    notafiscal = models.IntegerField(blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)
    cgo = models.ForeignKey(
        MaxCodgeraloper,
        models.CASCADE,
        related_name="fk_cgo_mov_nf",
        db_column="cgo",
        blank=True,
        null=True,
    )
    interno = models.IntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = "tsmy_eu_moviment_nf"


class TsmyEuParametro(models.Model):
    id_parametro = models.SmallAutoField(primary_key=True)
    nome_parametro = models.CharField(max_length=25, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    parametro = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = "tsmy_eu_parametro"


class TsmyEuArquivo(models.Model):
    id_aquivo = models.AutoField(primary_key=True)
    nome_arquivo = models.CharField(max_length=100)
    arquivo_assinado = models.CharField(max_length=100, blank=True, null=True)
    id_ficha = models.ForeignKey(
        TsmyEuFichaColab,
        models.CASCADE,
        db_column="id_ficha",
        related_name="fk_id_ficha_arquivo",
        blank=True,
        null=True,
    )
    matricula = models.ForeignKey(
        TsmyEuColaboradores,
        models.CASCADE,
        db_column="id_colab_matricula",
        related_name="fk_matricula_arquivo",
        blank=True,
        null=True,
    )
    tipo_arquivo = models.CharField(
        max_length=6,
        blank=True,
        null=True,
        db_comment="Tipo de arquivo: RU(Recibo Uniforme), RE(Recibo EPI), RR(Recibo Rescisão) ",
    )
    usuarioincl = models.ForeignKey(
        TsmyIntranetusuario,
        models.CASCADE,
        related_name="fk_arquivo_inclusao_lancto",
        db_column="usuarioincl",
        blank=True,
        null=True,
    )
    usuarioalt = models.ForeignKey(
        TsmyIntranetusuario,
        models.CASCADE,
        related_name="fk_arquivo_alteracao_lancto",
        db_column="usuarioalt",
        blank=True,
        null=True,
    )

    dt_inclusao = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    dt_alteracao = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        # managed = False
        db_table = "tsmy_eu_arquivo"


class TsmyEuCa(models.Model):
    ca = models.CharField(primary_key=True, max_length=5)
    dt_validade = models.DateTimeField(blank=True, null=True)
    usuarioincl = models.ForeignKey(
        TsmyIntranetusuario,
        models.DO_NOTHING,
        related_name="fk_ca_inclusao_lancto",
        db_column="usuarioincl",
        blank=True,
        null=True,
    )
    usuarioalt = models.ForeignKey(
        TsmyIntranetusuario,
        models.DO_NOTHING,
        related_name="fk_ca_alteracao_lancto",
        db_column="usuarioalt",
        blank=True,
        null=True,
    )
    dt_inclusao = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    dt_alteracao = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        # managed = False
        db_table = "tsmy_eu_ca"


tipoObservacao = {
    "P": "Perda",
    "T": "Troca",
}


class TsmyEuObservacaoFicha(models.Model):
    id_observacao = models.AutoField(primary_key=True)
    observacao = models.CharField(max_length=200)
    tipo = models.CharField(
        max_length=4, blank=True, null=True, choices=tipoObservacao.items()
    )
    usuarioincl = models.ForeignKey(
        TsmyIntranetusuario,
        models.CASCADE,
        related_name="fk_observacao_inclusao_lancto",
        db_column="usuarioincl",
        blank=True,
        null=True,
    )
    usuarioalt = models.ForeignKey(
        TsmyIntranetusuario,
        models.CASCADE,
        related_name="fk_observacao_alteracao_lancto",
        db_column="usuarioalt",
        blank=True,
        null=True,
    )
    dt_inclusao = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    dt_alteracao = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        # managed = False
        db_table = "tsmy_eu_observacao_ficha"
