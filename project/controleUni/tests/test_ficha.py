from django.test import TestCase
from icecream import ic

from project.controleUni.schemas import SchemaFichaIn
from project.controleUni.core.ficha import criar_ficha, verificar_quantidade_fichas
from project.intranet.models import TsmyIntranetusuario


class TestFicha(TestCase):
    def setUp(self) -> None:
        self.usuario = TsmyIntranetusuario.objects.get(pk=14)
        self.dadosFicha = SchemaFichaIn(
            seqproduto=19161,
            matricula=600411,
            sit_produto="C",
            nro_empresa_orig=1,
            nro_empresa_dest=2,
            quantidade=1,
        )
        return super().setUp()

    def test_validar_quantidade_pedida(self):
        """Verificar se o colaborador pode pedir a quantidade de fichas"""
        self.assertTrue(verificar_quantidade_fichas(self.dadosFicha))
        self.dadosFicha.quantidade = 4
        self.assertFalse(verificar_quantidade_fichas(self.dadosFicha))

    def test_criar_ficha(self):
        criar_ficha(self.dadosFicha)
        ic("Teste")
        pass
