from django.db import models


class TsmyIntranetusuario(models.Model):
    usuarioid = models.SmallAutoField(primary_key=True)
    usuariodescricao = models.CharField(max_length=255)
    nroempresa = models.IntegerField()
    login = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "tsmy_intranetusuario"

    def __str__(self):
        return self.usuariodescricao


class SmyUsuario(models.Model):
    idusu = models.FloatField(
        primary_key=True, db_comment="ADICIONA ID POR SMY_USUARIO_SEQ"
    )
    nome = models.CharField(max_length=100, blank=True, null=True)
    dtaatualizacao = models.DateField(blank=True, null=True)
    dtabloqueio = models.DateField(blank=True, null=True)
    login = models.CharField(max_length=100, blank=True, null=True)
    senha = models.CharField(max_length=100, blank=True, null=True)
    nroempresa = models.FloatField(blank=True, null=True)
    ramal = models.FloatField(blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "smy_usuario"
