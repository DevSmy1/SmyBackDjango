from django.test import TestCase
from icecream import ic

from project.controle_uni.services.ficha import criar_ficha
from project.controle_uni.services.lancto import criar_lancto
from project.controle_uni.services.ficha_troca import (
    cancelar_troca,
    confirmar_envio,
    confirmar_recebimento,
    criar_troca,
)
from project.controle_uni.schemas import SchemaFichaIn
from project.intranet.models import TsmyIntranetusuario
from project.controle_uni.models import (
    TsmyEuColaboradores,
    TsmyEuLancto,
    TsmyEuFichaColab,
)


class TestFichaDevolucao(TestCase):
    def setUp(self) -> None:
        self.usuario = TsmyIntranetusuario.objects.get(pk=14)
        self.dadosFicha = SchemaFichaIn(
            seqproduto=19161,
            matricula=600411,
            sit_produto="C",
            nro_empresa_orig=1,
            nro_empresa_dest=2,
            quantidade=2,
            id_observacao=1,
            presencial=True,
        )
        self.fichas_criadas = criar_ficha(self.dadosFicha, self.usuario)
        self.lanctos = criar_lancto(self.dadosFicha, self.fichas_criadas, self.usuario)
        return super().setUp()

    def test_criar_ficha_devolucao(self):
        ic(TsmyEuFichaColab.objects.get(id_ficha=self.fichas_criadas[0]))
        pass
