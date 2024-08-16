from django.test import TestCase
from icecream import ic

from project.controleUni.core.lancto import criar_lancto
from project.controleUni.models import TsmyEuFichaColab, TsmyEuLancto
from project.controleUni.schemas import SchemaFichaIn
from project.controleUni.core.ficha import criar_ficha, verificar_quantidade_fichas
from project.intranet.models import TsmyIntranetusuario


class TestFicha(TestCase):
    def setUp(self) -> None:
        self.usuario = TsmyIntranetusuario.objects.get(pk=14)
        self.dadosFicha = SchemaFichaIn(
            seqproduto=19161,
            matricula=600411,
            sit_produto="TE",
            nro_empresa_orig=1,
            nro_empresa_dest=2,
            quantidade=2,
            id_observacao=1,
            presencial=True,
        )
        self.fichas_criadas = criar_ficha(self.dadosFicha, self.usuario)
        self.lanctos = criar_lancto(self.dadosFicha, self.fichas_criadas, self.usuario)
        return super().setUp()

    def test_validar_quantidade_pedida(self):
        """Verificar se o colaborador pode pedir a quantidade de fichas"""
        self.assertTrue(verificar_quantidade_fichas(self.dadosFicha))
        self.dadosFicha.quantidade = 4
        self.assertFalse(verificar_quantidade_fichas(self.dadosFicha))

    def test_criar_ficha(self):
        """Testar a criação de uma ficha"""
        ficha = TsmyEuFichaColab.objects.get(id_ficha=self.fichas_criadas[0])  # type: ignore
        self.assertEqual(ficha.seqproduto_id, self.dadosFicha.seqproduto)  # type: ignore
        self.assertEqual(ficha.matricula.matricula, self.dadosFicha.matricula)  # type: ignore
        self.assertEqual(ficha.sit_produto, self.dadosFicha.sit_produto)
        self.assertEqual(ficha.sit_ficha, "A")

    def test_criar_lancto(self):
        """Testar a criação de um lançamento"""
        lanctos = criar_lancto(self.dadosFicha, self.fichas_criadas, self.usuario)
        self.assertEqual(
            TsmyEuFichaColab.objects.filter(id_ficha__in=self.fichas_criadas).count(), 2
        )
        self.assertEqual(TsmyEuLancto.objects.filter(id_lancto__in=lanctos).count(), 2)
        lancto = TsmyEuLancto.objects.get(id_lancto=lanctos[0])  # type: ignore
        self.assertEqual(lancto.seqproduto_id, self.dadosFicha.seqproduto)  # type: ignore
        self.assertEqual(lancto.matricula.matricula, self.dadosFicha.matricula)  # type: ignore
        self.assertEqual(lancto.cgo_id, 219)  # type: ignore
        self.assertEqual(lancto.quantidade, 1)  # type: ignore

    def test_criar_lancto_erro(self):
        """Testar a criação de um lançamento com erro"""
        self.dadosFicha.matricula = 600
        self.assertRaises(
            ValueError,
            lambda: criar_lancto(self.dadosFicha, self.fichas_criadas, self.usuario),
        )
        self.assertEqual(
            TsmyEuFichaColab.objects.filter(id_ficha__in=self.fichas_criadas).count(), 0
        )

    def test_alterar_ficha(self):
        """Testar a alteração de uma ficha"""
        ficha = TsmyEuFichaColab.objects.get(id_ficha=self.fichas_criadas[0])  # type: ignore
