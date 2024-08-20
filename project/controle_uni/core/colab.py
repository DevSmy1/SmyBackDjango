import logging
from django.db import IntegrityError
import pandas as pd
from project.controle_uni.models import TsmyEuColaboradores

logger = logging.getLogger("colab")


def carregarArquivoColab(caminhoArquivo, usuario):
    try:
        tabela = pd.read_excel(caminhoArquivo)
        for linha in range(0, len(tabela)):
            try:
                colab_data = {
                    "nroempresa": tabela.iloc[linha, 0],
                    "matricula": tabela.iloc[linha, 1],
                    "cpf": tabela.iloc[linha, 2],
                    "nome": tabela.iloc[linha, 4],
                    "genero": tabela.iloc[linha, 7][0],  # type: ignore
                    "dt_adm": tabela.iloc[linha, 5],
                    "cod_funcao_id": tabela.iloc[linha, 3],
                    "usuarioalt": usuario,
                }

                colab, created = TsmyEuColaboradores.objects.update_or_create(
                    matricula=colab_data["matricula"],
                    defaults=colab_data,
                )

                if created:
                    colab.usuarioincl = usuario

                colab.full_clean()
                colab.save()
            except IntegrityError as e:
                logger.error(f"Erro de violação de unicidade: {e}")
            except Exception as e:
                logger.error(f"Erro ao carregar colaborador: {e}")
    except Exception as e:
        raise Exception("Erro ao carregar arquivo: ", e)
