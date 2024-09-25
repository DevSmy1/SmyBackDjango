from django.test import TestCase
from icecream import ic

from project.controle_uni.services.dados_epi import verificar_produto_epi
from project.controle_uni.services.lancto import (
    alterar_lanctos,
    criar_lancto,
    deletar_lanctos,
)
from project.controle_uni.models import TsmyEuFichaColab, TsmyEuLancto
from project.controle_uni.schemas import SchemaAlterarFicha, SchemaFichaIn
from project.controle_uni.services.ficha import (
    alterar_ficha,
    criar_ficha,
    desativar_ficha,
    verificar_quantidade_fichas,
)
from project.intranet.models import SmyUsuario


class TestFicha(TestCase):
    def setUp(self) -> None:
        self.usuario = SmyUsuario.objects.get(pk=14)
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
        dadosAlterar = self.dadosFicha.dict()
        dadosAlterar["id_ficha"] = self.fichas_criadas[0]
        dadosAlterar["sit_produto"] = "TE"
        dadosAlterar["matricula"] = 121523
        dadosAlterar = SchemaAlterarFicha(**dadosAlterar)
        ficha = TsmyEuFichaColab.objects.get(id_ficha=dadosAlterar.id_ficha)
        fichaAlterada = alterar_ficha(dadosAlterar, self.usuario)
        self.assertEqual(fichaAlterada.id_ficha, ficha.id_ficha)
        self.assertNotEqual(fichaAlterada.sit_produto, ficha.sit_produto)
        self.assertNotEqual(fichaAlterada.matricula, ficha.matricula)
        lanctos = TsmyEuLancto.objects.filter(id_ficha=dadosAlterar.id_ficha)
        lanctosAlterados = alterar_lanctos(dadosAlterar, self.usuario)
        self.assertEqual(lanctos.count(), lanctosAlterados.count())
        self.assertEqual(
            lanctos.first().matricula,  # type: ignore
            lanctosAlterados.first().matricula,  # type: ignore
        )

    def test_desativar_ficha(self):
        """Testar a desativação de uma ficha"""
        ficha = desativar_ficha(self.fichas_criadas[0], self.usuario)
        self.assertEqual(ficha.sit_ficha, "D")
        self.assertEqual(
            TsmyEuLancto.objects.filter(id_ficha=ficha.id_ficha).count(), 1
        )
        deletar_lanctos(ficha.id_ficha)
        self.assertEqual(
            TsmyEuLancto.objects.filter(id_ficha=ficha.id_ficha).count(), 0
        )


class TestFichaOrdemRequisicao(TestCase):
    def setUp(self) -> None:
        self.usuario = SmyUsuario.objects.get(pk=14)
        self.dadosFicha = SchemaFichaIn(
            seqproduto=19161,
            cpf=14918877885,
            sit_produto="OR",
            nro_empresa_orig=1,
            nro_empresa_dest=2,
            quantidade=2,
            id_observacao=1,
            presencial=False,
        )
        return super().setUp()

    def test_criar_ordem_requisicao(self):
        fichas = criar_ficha(self.dadosFicha, self.usuario)
        ficha = TsmyEuFichaColab.objects.get(id_ficha=fichas[0])  # type: ignore
        self.assertEqual(ficha.sit_produto, "OR")
        self.assertEqual(ficha.sit_ficha, "A")
        self.assertEqual(ficha.matricula, None)
        self.assertEqual(ficha.cpf.cpf, self.dadosFicha.cpf)  # type: ignore

    def test_lanctos_ordem_requisicao(self):
        fichas = criar_ficha(self.dadosFicha, self.usuario)
        lanctos = criar_lancto(self.dadosFicha, fichas, self.usuario)
        self.assertEqual(
            TsmyEuLancto.objects.filter(id_lancto__in=lanctos, cgo=219).count(), 2
        )
        self.assertEqual(
            TsmyEuFichaColab.objects.filter(id_ficha__in=fichas).count(), 2
        )
