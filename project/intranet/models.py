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
