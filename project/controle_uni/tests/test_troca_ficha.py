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


class TestTrocaFicha(TestCase):
    def setUp(self) -> None:
        self.matricula = TsmyEuColaboradores.objects.get(matricula=600411)
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
            sit_produto="TR",
            nro_empresa_orig=2,
            nro_empresa_dest=1,
            quantidade=1,
            id_observacao=1,
            presencial=False,
        )
        self.dadosFichaEnvio = SchemaFichaIn(
            seqproduto=13942,
            matricula=600411,
            sit_produto="TE",
            nro_empresa_orig=1,
            nro_empresa_dest=2,
            quantidade=1,
            id_observacao=1,
            presencial=False,
        )
        self.fichas_criadas = criar_ficha(self.dadosFicha, self.usuario)
        self.fichas_troca = criar_troca(
            self.fichas_criadas[0], self.dadosFichaEnvio, self.usuario
        )
        self.lanctos = criar_lancto(self.dadosFicha, self.fichas_criadas, self.usuario)
        return super().setUp()

    def test_criar_troca(self):
        """Criar uma troca que consiste em uma ficha de recebimento e outra de envio"""

        self.assertEqual(
            TsmyEuFichaColab.objects.filter(
                matricula=self.matricula, sit_produto="TE"
            ).count(),
            1,
        )
        self.assertEqual(
            TsmyEuFichaColab.objects.filter(
                matricula=self.matricula, sit_produto="TR"
            ).count(),
            1,
        )
        self.assertEqual(
            TsmyEuFichaColab.objects.get(id_ficha=self.fichas_troca[0]).sit_produto,
            "TR",
        )
        self.assertEqual(
            TsmyEuFichaColab.objects.get(id_ficha=self.fichas_troca[1]).sit_produto,
            "TE",
        )

    def test_confirmar_recebimento(self):
        """Confirmar Recebimento da forma padrão"""
        confirmar_recebimento(
            self.fichas_troca[0], self.dadosFichaRecebimento, self.usuario
        )
        self.assertEqual(
            TsmyEuLancto.objects.filter(
                id_ficha=self.fichas_troca[0], cgo_id=221, tipo="E"
            ).count(),
            1,
        )
        self.assertEqual(
            TsmyEuFichaColab.objects.get(id_ficha=self.fichas_troca[0]).sit_ficha, "D"
        )

    def test_confirmar_recebimento_presencial(self):
        """Confirmar Recebimento Presencial onde o Colaborador veio entregar"""
        self.dadosFichaRecebimento.presencial = True
        confirmar_recebimento(
            self.fichas_troca[0], self.dadosFichaRecebimento, self.usuario
        )
        self.assertEqual(
            TsmyEuLancto.objects.filter(
                id_ficha=self.fichas_troca[0], cgo_id=219, tipo="E"
            ).count(),
            1,
        )
        self.assertEqual(
            TsmyEuFichaColab.objects.get(id_ficha=self.fichas_troca[0]).sit_ficha, "D"
        )

    def test_confirmar_recebimento_mov_interno(self):
        """Confirmar recebimento de um item que será movimentado internamente"""
        self.dadosFichaRecebimento.nro_empresa_orig = 1
        confirmar_recebimento(
            self.fichas_troca[0], self.dadosFichaRecebimento, self.usuario
        )
        self.assertEqual(
            TsmyEuLancto.objects.filter(
                id_ficha=self.fichas_troca[0], cgo_id=600, tipo="E"
            ).count(),
            1,
        )
        self.assertEqual(
            TsmyEuFichaColab.objects.get(id_ficha=self.fichas_troca[0]).sit_ficha, "D"
        )

    def test_confirmar_recebimento_perda(self):
        """Confirmar recebimento de um objeto de perda onde espera ser gerado dois lançamentos"""
        self.dadosFichaRecebimento.perda = True
        confirmar_recebimento(
            self.fichas_troca[0], self.dadosFichaRecebimento, self.usuario
        )
        self.assertEqual(
            TsmyEuLancto.objects.filter(
                id_ficha=self.fichas_troca[0], cgo_id=221, tipo="E"
            ).count(),
            1,
        )
        self.assertEqual(
            TsmyEuLancto.objects.filter(
                id_ficha=self.fichas_troca[0], cgo_id=722, tipo="E"
            ).count(),
            1,
        )
        self.assertEqual(
            TsmyEuFichaColab.objects.get(id_ficha=self.fichas_troca[0]).sit_ficha, "D"
        )

    def test_confirmar_envio(self):
        """Confirmar envio do modo esperado"""
        confirmar_envio(self.fichas_troca[1], self.dadosFichaEnvio, self.usuario)
        self.assertEqual(
            TsmyEuLancto.objects.filter(
                id_ficha=self.fichas_troca[1], cgo_id=221, tipo="S"
            ).count(),
            1,
        )
        self.assertEqual(
            TsmyEuFichaColab.objects.get(id_ficha=self.fichas_troca[1]).sit_ficha, "D"
        )

    def test_confirmar_envio_presencial(self):
        """Confirmar envio que seja presencial(Colaborador vem pegar o item)"""
        self.dadosFichaEnvio.presencial = True
        confirmar_envio(self.fichas_troca[1], self.dadosFichaEnvio, self.usuario)
        self.assertEqual(
            TsmyEuLancto.objects.filter(
                id_ficha=self.fichas_troca[1], cgo_id=219, tipo="S"
            ).count(),
            1,
        )
        self.assertEqual(
            TsmyEuFichaColab.objects.get(id_ficha=self.fichas_troca[1]).sit_ficha, "D"
        )

    def test_confirmar_envio_mov_interno(self):
        """Confirmar Envio como movimento interno"""
        self.dadosFichaEnvio.nro_empresa_dest = 1
        confirmar_envio(self.fichas_troca[1], self.dadosFichaEnvio, self.usuario)
        self.assertEqual(
            TsmyEuLancto.objects.filter(
                id_ficha=self.fichas_troca[1], cgo_id=700, tipo="S"
            ).count(),
            1,
        )
        self.assertEqual(
            TsmyEuFichaColab.objects.get(id_ficha=self.fichas_troca[1]).sit_ficha, "D"
        )

    def test_confirmar_envio_perda(self):
        """Testa se retorna um erro ao tentar enviar um item como perda"""
        self.dadosFichaEnvio.perda = True
        self.assertRaises(
            ValueError,
            lambda: confirmar_envio(
                self.fichas_troca[1], self.dadosFichaEnvio, self.usuario
            ),
        )

    def test_cancelar_recebimento(self):
        cancelar_troca(self.fichas_troca[0])
        self.assertEqual(
            TsmyEuFichaColab.objects.get(id_ficha=self.fichas_troca[0]).sit_ficha, "C"
        )

        pass

    def test_cancelar_envio(self):
        cancelar_troca(self.fichas_troca[1])
        self.assertEqual(
            TsmyEuFichaColab.objects.get(id_ficha=self.fichas_troca[1]).sit_ficha, "C"
        )
        pass


class TestTrocaAntiga(TestCase):
    def setUp(self) -> None:
        self.matricula = TsmyEuColaboradores.objects.get(matricula=600411)
        self.usuario = TsmyIntranetusuario.objects.get(pk=14)
        self.dadosFichaRecebimento = SchemaFichaIn(
            seqproduto=19161,
            matricula=600411,
            sit_produto="TRA",
            nro_empresa_orig=2,
            nro_empresa_dest=1,
            quantidade=1,
            id_observacao=1,
            presencial=False,
        )
        self.dadosFichaEnvio = SchemaFichaIn(
            seqproduto=13942,
            matricula=600411,
            sit_produto="TE",
            nro_empresa_orig=1,
            nro_empresa_dest=2,
            quantidade=1,
            id_observacao=1,
            presencial=False,
        )
        self.ficha = criar_ficha(self.dadosFichaRecebimento, self.usuario)
        return super().setUp()

    def test_criar_troca_antiga(self):
        fichas_troca = criar_troca(self.ficha[0], self.dadosFichaEnvio, self.usuario)
        self.assertEqual(
            TsmyEuFichaColab.objects.filter(
                matricula=self.matricula, sit_produto="TE"
            ).count(),
            1,
        )
        self.assertEqual(
            TsmyEuFichaColab.objects.filter(
                matricula=self.matricula, sit_produto="TRA"
            ).count(),
            1,
        )
        self.assertEqual(
            TsmyEuFichaColab.objects.get(id_ficha=fichas_troca[0]).sit_produto,
            "TRA",
        )
        self.assertEqual(
            TsmyEuFichaColab.objects.get(id_ficha=fichas_troca[1]).sit_produto,
            "TE",
        )
