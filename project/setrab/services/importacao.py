from datetime import date
import logging
from project.controle_uni.models import TsmyEuCargos, TsmyEuColaboradores  # noqa: E402
from project.setrab.models import SetrabCargoRel, SetrabEmpresaRel, SetrabSetorRel  # noqa: E402

import pandas as pd

logger = logging.getLogger("sgg")


def admissao(arquivo: str, data: date):
    """Leitura do arquivo de admissão e criação do JSON para envio a API

    Args:
        data (date): Data de admissão usado para filtrar o arquivo
    """
    try:
        dados = []
        df = pd.read_excel(arquivo)
        df = df[
            (df.iloc[:, 4].dt.month == pd.to_datetime(data).month)
            & (df.iloc[:, 4].dt.year == pd.to_datetime(data).year)
        ]
        for linha in range(len(df)):
            try:
                empresa = SetrabEmpresaRel.objects.get(id_empresa=df.iloc[linha][1])

                cpf = str(df.iloc[linha][0])
                cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

                cargo = SetrabCargoRel.objects.filter(
                    id_cargo=df.iloc[linha][7], nro_empresa=df.iloc[linha][1]
                ).first()
                if not cargo:
                    raise Exception("Cargo não encontrado")
                setor = SetrabSetorRel.objects.filter(
                    id_setor=str(df.iloc[linha][8]), nro_empresa=df.iloc[linha][1]
                ).first()
                if not setor:
                    raise Exception("Setor não encontrado")

                colab = {
                    "id_empresa": empresa.id_empresa_setrab,
                    "id_funcionario": cpf,
                    "nome": df.iloc[linha][3],
                    "data_admissao": df.iloc[linha][4].strftime("%Y-%m-%d"),
                    "data_nascimento": df.iloc[linha][5].strftime("%Y-%m-%d"),
                    "sexo": df.iloc[linha][6][0],
                    "id_cargo": cargo.id_cargo_setrab,
                    "id_setor": setor.id_setor_setrab,
                    "possui_vinculo": "S",
                    "id_empresa_rh": empresa.id_empresa,
                }
                dados.append(colab)

            except Exception as e:
                logger.warning(f"Erro ao criar json de Admissão: {e}")
                colab = {
                    "id_empresa": empresa.id_empresa_setrab,
                    "id_funcionario": cpf,
                    "nome": df.iloc[linha][3],
                    "data_admissao": df.iloc[linha][4].strftime("%Y-%m-%d"),
                    "data_nascimento": df.iloc[linha][5].strftime("%Y-%m-%d"),
                    "sexo": df.iloc[linha][6][0],
                    "id_cargo": 0,
                    "id_setor": 0,
                    "possui_vinculo": "S",
                    "id_empresa_rh": empresa.id_empresa,
                    "erro_sistema": str(e),
                }
                dados.append(colab)
        return dados
    except Exception as e:
        logger.error(f"Erro na Função admissao: {e}")
        raise e


def demissao(arquivo: str, data: date):
    """Leitura do arquivo de demissão e criação do JSON para envio a API

    Args:
        arquivo (str): Nome do arquivo de demissão
        data (date): Data de demissão usado para filtrar o arquivo
    """
    try:
        dados = []
        df = pd.read_excel(arquivo)
        df = df[
            (df.iloc[:, 2].dt.month == pd.to_datetime(data).month)
            & (df.iloc[:, 2].dt.year == pd.to_datetime(data).year)
        ]
        for linha in range(len(df)):
            try:
                colab = TsmyEuColaboradores.objects.get(matricula=df.iloc[linha][1])
                empresa = SetrabEmpresaRel.objects.get(id_empresa=colab.nroempresa)
                cpf = str(int(df.iloc[linha][0]))
                cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
                demissao = {
                    "id_empresa": empresa.id_empresa_setrab,
                    "id_funcionario": cpf,
                    "data_demissao": df.iloc[linha][2].strftime("%Y-%m-%d"),
                    "nome": colab.nome,
                    "id_empresa_rh": empresa.id_empresa,
                }
                dados.append(demissao)
            except Exception as e:
                logger.warning(f"Erro ao criar json de Demissão: {e}")
                demissao = {
                    "id_empresa": empresa.id_empresa_setrab,
                    "id_funcionario": cpf,
                    "data_demissao": df.iloc[linha][2].strftime("%Y-%m-%d"),
                    "nome": colab.nome,
                    "id_empresa_rh": empresa.id_empresa,
                    "erro_sistema": str(e),
                }
                dados.append(demissao)
        return dados
    except Exception as e:
        logger.error(f"Erro na Função demissao: {e}")
        raise e


def mudanca_funcao(arquivo: str, data: date):
    try:
        dados = []
        df = pd.read_excel(arquivo)
        df = df[
            (df.iloc[:, 5].dt.month == pd.to_datetime(data).month)
            & (df.iloc[:, 5].dt.year == pd.to_datetime(data).year)
        ]
        for linha in range(1, len(df)):
            try:
                colab = TsmyEuColaboradores.objects.get(matricula=df.iloc[linha][1])

                cpf = str(df.iloc[linha][0])
                cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

                empresa = SetrabEmpresaRel.objects.get(
                    id_empresa=int(df.iloc[linha][2])
                )
                cargo = SetrabCargoRel.objects.filter(
                    id_cargo=df.iloc[linha][3], nro_empresa=empresa.id_empresa
                ).first()
                if not cargo:
                    raise Exception("Cargo não encontrado")

                setor = SetrabSetorRel.objects.filter(
                    id_setor=str(df.iloc[linha][4]), nro_empresa=empresa.id_empresa
                ).first()
                if not setor:
                    raise Exception("Setor não encontrado")

                mudanca_funcao = {
                    "id_funcionario": cpf,
                    "id_empresa": empresa.id_empresa_setrab,
                    "id_cargo": cargo.id_cargo_setrab,
                    "id_setor": setor.id_setor_setrab,
                    "data_mud_func": df.iloc[linha][5].strftime("%Y-%m-%d"),
                    "nome": colab.nome,
                    "id_empresa_rh": empresa.id_empresa,
                }
                dados.append(mudanca_funcao)
            except Exception as e:
                logger.warning(f"Erro ao criar json de Mudança de Função: {e}")
                muda_funcao = {
                    "id_funcionario": cpf,
                    "id_empresa": empresa.id_empresa_setrab,
                    "id_cargo": 0,
                    "id_setor": 0,
                    "data_mud_func": df.iloc[linha][5].strftime("%Y-%m-%d"),
                    "nome": colab.nome,
                    "id_empresa_rh": empresa.id_empresa,
                    "erro_sistema": str(e),
                }
                dados.append(muda_funcao)
        return dados
    except Exception as e:
        logger.error(f"Eroo na Função mudanca_funcao: {e}")
        raise e


def transferencia(arquivo: str, data: date):
    try:
        dados = []
        df = pd.read_excel(arquivo)
        df = df[
            (df.iloc[:, 6].dt.month == pd.to_datetime(data).month)
            & (df.iloc[:, 6].dt.year == pd.to_datetime(data).year)
        ]
        for linha in range(1, len(df)):
            try:
                empresa_atual = SetrabEmpresaRel.objects.get(
                    id_empresa=int(df.iloc[linha][2][:2])
                )
                empresa_destino = SetrabEmpresaRel.objects.get(
                    id_empresa=int(df.iloc[linha][2][:2])
                )
                colab = TsmyEuColaboradores.objects.get(matricula=df.iloc[linha][0])
                cpf = str(colab.cpf)
                cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

                cargo = SetrabCargoRel.objects.filter(
                    id_cargo=colab.cod_funcao, nro_empresa=empresa_atual.id_empresa
                ).first()
                if not cargo:
                    raise Exception("Cargo não encontrado")

                setor = SetrabSetorRel.objects.filter(
                    id_setor=str(df.iloc[linha][5][:12]),
                ).first()
                if not setor:
                    raise Exception("Setor não encontrado")

                transferencia = {
                    "id_funcionario": cpf,
                    "id_empresa": empresa_atual.id_empresa_setrab,
                    "id_empresa_destino": empresa_destino.id_empresa_setrab,
                    "id_cargo": cargo.id_cargo_setrab,
                    "id_setor": setor.id_setor_setrab,
                    "data_transferencia": df.iloc[linha][6].strftime("%Y-%m-%d"),
                    "nome": colab.nome,
                    "id_empresa_rh": empresa_atual.id_empresa,
                }
                dados.append(transferencia)
            except Exception as e:
                logger.warning(f"Erro ao criar json de Transferencia: {e}")
                transferencia = {
                    "id_funcionario": cpf,
                    "id_empresa": empresa_atual.id_empresa_setrab,
                    "id_empresa_destino": empresa_destino.id_empresa_setrab,
                    "id_cargo": 0,
                    "id_setor": 0,
                    "data_transferencia": df.iloc[linha][6].strftime("%Y-%m-%d"),
                    "nome": colab.nome,
                    "id_empresa_rh": empresa_atual.id_empresa,
                    "erro_sistema": str(e),
                }
                dados.append(transferencia)
        return dados
    except Exception as e:
        logger.error(f"Erro na Função transferencia: {e}")
        raise e
