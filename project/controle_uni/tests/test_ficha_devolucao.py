from django.test import TestCase
from icecream import ic

from project.controle_uni.models import (
    TsmyEuColaboradores,
    TsmyEuFichaColab,
    TsmyEuLancto,
)
from project.controle_uni.schemas import SchemaFichaIn
from project.controle_uni.services.ficha import criar_ficha
from project.controle_uni.services.ficha_devolucao import (
    confirmar_devolucao,
    criar_devolucao,
    criar_devolucao_antiga,
)
from project.controle_uni.services.lancto import criar_lancto
from project.intranet.models import TsmyIntranetusuario


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
        self.dadosFichaRecebimento = SchemaFichaIn(
            seqproduto=19161,
            matricula=600411,
            sit_produto="D",
            nro_empresa_orig=2,
            nro_empresa_dest=1,
            quantidade=1,
            id_observacao=1,
            presencial=False,
        )
        self.fichas_criadas = criar_ficha(self.dadosFicha, self.usuario)
        self.lanctos = criar_lancto(self.dadosFicha, self.fichas_criadas, self.usuario)
        return super().setUp()

    def test_criar_ficha_devolucao(self):
        criar_devolucao(self.fichas_criadas[0], self.usuario)
        self.assertEqual(
            TsmyEuFichaColab.objects.get(id_ficha=self.fichas_criadas[0]).sit_produto,
            "D",
        )

    def test_criar_devolucao_antiga(self):
        self.dadosFicha.quantidade = 1
        ficha = criar_devolucao_antiga(self.dadosFicha, self.usuario)
        self.assertEqual(
            TsmyEuFichaColab.objects.get(id_ficha=ficha).sit_produto,
            "DA",
        )

    def test_confirmar_devolucao(self):
        criar_devolucao(self.fichas_criadas[0], self.usuario)
        self.assertEqual(
            TsmyEuFichaColab.objects.get(id_ficha=self.fichas_criadas[0]).sit_produto,
            "D",
        )
        confirmar_devolucao(
            self.fichas_criadas[0], self.dadosFichaRecebimento, self.usuario
        )
        self.assertEqual(
            TsmyEuFichaColab.objects.get(id_ficha=self.fichas_criadas[0]).sit_ficha,
            "D",
        )
        self.assertEqual(
            TsmyEuLancto.objects.filter(
                id_ficha=self.fichas_criadas[0], tipo="E", cgo=221
            ).count(),
            1,
        )

    def test_confirmar_devolucao_perda(self):
        criar_devolucao(self.fichas_criadas[0], self.usuario)
        self.assertEqual(
            TsmyEuFichaColab.objects.get(id_ficha=self.fichas_criadas[0]).sit_produto,
            "D",
        )
        self.dadosFichaRecebimento.perda = True
        confirmar_devolucao(
            self.fichas_criadas[0], self.dadosFichaRecebimento, self.usuario
        )
        self.assertEqual(
            TsmyEuFichaColab.objects.get(id_ficha=self.fichas_criadas[0]).sit_ficha,
            "D",
        )
        self.assertEqual(
            TsmyEuLancto.objects.filter(
                id_ficha=self.fichas_criadas[0], tipo="E", cgo=221
            ).count(),
            1,
        )
        self.assertEqual(
            TsmyEuLancto.objects.filter(
                id_ficha=self.fichas_criadas[0], tipo="E", cgo=722
            ).count(),
            1,
        )

    def test_confirmar_devolucao_presencial(self):
        criar_devolucao(self.fichas_criadas[0], self.usuario)
        self.assertEqual(
            TsmyEuFichaColab.objects.get(id_ficha=self.fichas_criadas[0]).sit_produto,
            "D",
        )
        self.dadosFichaRecebimento.presencial = True
        confirmar_devolucao(
            self.fichas_criadas[0], self.dadosFichaRecebimento, self.usuario
        )
        self.assertEqual(
            TsmyEuFichaColab.objects.get(id_ficha=self.fichas_criadas[0]).sit_ficha,
            "D",
        )
        self.assertEqual(
            TsmyEuLancto.objects.filter(
                id_ficha=self.fichas_criadas[0], tipo="E", cgo=219
            ).count(),
            1,
        )

    def test_confirmar_devolucao_mov_interno(self):
        criar_devolucao(self.fichas_criadas[0], self.usuario)
        self.assertEqual(
            TsmyEuFichaColab.objects.get(id_ficha=self.fichas_criadas[0]).sit_produto,
            "D",
        )
        self.dadosFichaRecebimento.nro_empresa_orig = 1
        confirmar_devolucao(
            self.fichas_criadas[0], self.dadosFichaRecebimento, self.usuario
        )
        self.assertEqual(
            TsmyEuFichaColab.objects.get(id_ficha=self.fichas_criadas[0]).sit_ficha,
            "D",
        )
        self.assertEqual(
            TsmyEuLancto.objects.filter(
                id_ficha=self.fichas_criadas[0], tipo="E", cgo=600
            ).count(),
            1,
        )

    def test_confirmar_devolucao_antiga(self):
        self.dadosFicha.quantidade = 1
        ficha = criar_devolucao_antiga(self.dadosFicha, self.usuario)
        self.assertEqual(
            TsmyEuFichaColab.objects.get(id_ficha=ficha).sit_produto,
            "DA",
        )
        confirmar_devolucao(ficha, self.dadosFichaRecebimento, self.usuario)
        self.assertEqual(
            TsmyEuFichaColab.objects.get(id_ficha=ficha).sit_ficha,
            "D",
        )
        self.assertEqual(
            TsmyEuLancto.objects.filter(id_ficha=ficha, tipo="E", cgo=221).count(),
            1,
        )
