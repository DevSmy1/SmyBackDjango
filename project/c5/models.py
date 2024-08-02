from django.db import models


class MapProduto(models.Model):
    seqproduto = models.BigIntegerField(primary_key=True)
    desccompleta = models.CharField(max_length=250)
    descreduzida = models.CharField(max_length=250)
    seqfamilia = models.ForeignKey(
        "MapFamilia", models.DO_NOTHING, db_column="seqfamilia"
    )

    class Meta:
        # managed = False
        db_table = "map_produto"


class MapFamilia(models.Model):
    seqfamilia = models.BigIntegerField(primary_key=True)
    familia = models.CharField(max_length=35)

    class Meta:
        # managed = False
        db_table = "map_familia"


class MaxCodgeraloper(models.Model):
    codgeraloper = models.IntegerField(primary_key=True)

    class Meta:
        # managed = False
        db_table = "max_codgeraloper"


class MapFamatributo(models.Model):
    # The composite primary key (seqfamilia, descatributo) found, that is not supported. The first column is selected.
    seqfamilia = models.OneToOneField(
        "MapFamilia", models.DO_NOTHING, db_column="seqfamilia", primary_key=True
    )
    descatributo = models.CharField(max_length=100)
    valor = models.CharField(max_length=15, blank=True, null=True)
    usuarioalteracao = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = "map_famatributo"
        unique_together = (("seqfamilia", "descatributo"),)


class MapProdcodigo(models.Model):
    seqproduto = models.ForeignKey(
        "MapProduto", models.DO_NOTHING, db_column="seqproduto", blank=True, null=True
    )
    codacesso = models.TextField(primary_key=True)
    tipcodigo = models.TextField()

    class Meta:
        # managed = False
        db_table = "map_prodcodigo"
        unique_together = (("codacesso"),)
