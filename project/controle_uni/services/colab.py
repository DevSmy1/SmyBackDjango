import logging
from django.db import IntegrityError
from ninja import Schema
import pandas as pd
from project.controle_uni.models import (
    TsmyEuCargos,
    TsmyEuColaboradores,
    TsmyEuFuncao,
    TsmyEuSetor,
)

logger = logging.getLogger("colab")


class CargoColabSchema(Schema):
    cod_cargo: int
    nome_cargo: str


class FuncaoColabSchema(Schema):
    cod_funcao: int
    nome_funcao: str


class SetorColabSchema(Schema):
    cod_setor: str
    nome_setor: str


def carregar_arquivo_colab(caminhoArquivo, usuario):
    try:
        tabela = pd.read_excel(caminhoArquivo)
        for linha in range(0, len(tabela)):
            try:
                colab_data = {
                    "nroempresa": tabela.iloc[linha, 0],
                    "matricula": tabela.iloc[linha, 1],
                    "cpf": tabela.iloc[linha, 3],
                    "nome": tabela.iloc[linha, 2],
                    "genero": tabela.iloc[linha, 5][0],  # type: ignore
                    "dt_adm": tabela.iloc[linha, 4],
                    "cod_funcao_id": tabela.iloc[linha, 6],
                    "usuario_alteracao": usuario,
                }

                cargo_data = CargoColabSchema(
                    cod_cargo=tabela.iloc[linha, 6],  # type: ignore
                    nome_cargo=tabela.iloc[linha, 7],  # type: ignore
                )

                criar_cargo(cargo_data, usuario)

                funcao_data = FuncaoColabSchema(
                    cod_funcao=tabela.iloc[linha, 8],  # type: ignore
                    nome_funcao=tabela.iloc[linha, 9],  # type: ignore
                )

                criar_funcao(funcao_data, usuario)

                setor_data = SetorColabSchema(
                    cod_setor=tabela.iloc[linha, 10],  # type: ignore
                    nome_setor=tabela.iloc[linha, 11],  # type: ignore
                )

                criar_setor(setor_data, usuario)

                colab, created = TsmyEuColaboradores.objects.update_or_create(
                    matricula=colab_data["matricula"],
                    defaults=colab_data,
                )

                if created:
                    colab.usuario_criacao = usuario

                colab.full_clean()
                colab.save()
            except IntegrityError as e:
                logger.error(f"Erro de violação de unicidade: {e}")
            except Exception as e:
                logger.error(f"Erro ao carregar colaborador: {e}")
    except Exception as e:
        raise Exception("Erro ao carregar arquivo: ", e)


def criar_cargo(cargo_data: CargoColabSchema, usuario):
    try:
        cargo = TsmyEuCargos.objects.get_or_create(
            cod_funcao=cargo_data.cod_cargo,
            defaults={"funcao": cargo_data.nome_cargo},
        )
        cargo[0].usuario_alteracao = usuario
        if cargo[1]:
            cargo[0].usuario_criacao = usuario
        cargo[0].save()
    except Exception as e:
        logger.error(f"Erro ao criar cargo: {e}")
        raise Exception("Erro ao criar cargo: ", e)


def criar_funcao(funcao_data: FuncaoColabSchema, usuario):
    try:
        funcao = TsmyEuFuncao.objects.get_or_create(
            cod_funcao=funcao_data.cod_funcao,
            defaults={"nome_funcao": funcao_data.nome_funcao},
        )
        funcao[0].usuario_alteracao = usuario
        if funcao[1]:
            funcao[0].usuario_criacao = usuario
        funcao[0].save()
    except Exception as e:
        logger.error(f"Erro ao criar funcao: {e}")
        raise Exception("Erro ao criar funcao: ", e)


def criar_setor(setor_data: SetorColabSchema, usuario):
    try:
        setor = TsmyEuSetor.objects.get_or_create(
            cod_setor=setor_data.cod_setor,
            defaults={"nome_setor": setor_data.nome_setor},
        )
        setor[0].usuario_alteracao = usuario
        if setor[1]:
            setor[0].usuario_criacao = usuario
        setor[0].save()
    except Exception as e:
        logger.error(f"Erro ao criar setor: {e}")
        raise Exception("Erro ao criar setor: ", e)
