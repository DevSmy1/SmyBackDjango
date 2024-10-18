import logging
from typing import List
from django.db import transaction
from project.controle_uni.models import (
    TsmyEuArquivo,
    TsmyEuColaboradores,
    TsmyEuFichaColab,
)
from project.controle_uni.services.dados_epi import verificar_produto_epi
from project.intranet.models import SmyUsuario

logger = logging.getLogger("termo")


def adicionar_rel_arquivo_ficha(
    ids_fichas: List[int],
    matricula: int,
    recibo_uni: str,
    recibo_epi: str,
    arquivo_integracao: str,
    usuario: SmyUsuario,
):
    try:
        with transaction.atomic():
            colab = TsmyEuColaboradores.objects.get(matricula=matricula)
            fichas = TsmyEuFichaColab.objects.filter(
                reciboUni=None,
                reciboEpi=None,
                id_ficha__in=ids_fichas,
                matricula=colab,
            )
            if not fichas:
                raise Exception("Nenhuma ficha encontrada")
            fichas = sorted(fichas, key=lambda ficha: ficha.id_ficha)
            for ficha in fichas:
                arquivo_uni = TsmyEuArquivo.objects.create(
                    nome_arquivo=recibo_uni,
                    id_ficha=ficha,
                    matricula=colab,
                    tipo_arquivo="RU",
                    usuario_criacao=usuario,
                    usuario_alteracao=usuario,
                )
                ficha.reciboUni = arquivo_uni  # type: ignore
                if verificar_produto_epi(ficha.seqproduto_id):  # type: ignore
                    arquivo_epi = TsmyEuArquivo.objects.create(
                        nome_arquivo=recibo_epi,
                        id_ficha=ficha,
                        matricula=colab,
                        tipo_arquivo="RE",
                        usuario_criacao=usuario,
                        usuario_alteracao=usuario,
                    )
                    if arquivo_integracao:
                        TsmyEuArquivo.objects.create(
                            nome_arquivo=arquivo_integracao,
                            id_ficha=ficha,
                            matricula=colab,
                            tipo_arquivo="IE",
                            usuario_criacao=usuario,
                            usuario_alteracao=usuario,
                        )
                    ficha.reciboEpi = arquivo_epi  # type: ignore
                ficha.save()
            return True
    except Exception as e:
        logger.error(f"Erro ao criar relação: {e}")
        raise Exception("Erro ao adicionar ficha no termo: ", e)
