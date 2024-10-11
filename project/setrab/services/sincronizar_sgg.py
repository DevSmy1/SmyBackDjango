import logging
from typing import List
import requests
import json
import base64
from decouple import config
import random
import os
from datetime import datetime

from project.setrab.schemas import (
    AdmissaoSchema,
    DemissaoSchema,
    MudFuncaoSchema,
    TransferenciaSchema,
)

logger = logging.getLogger("sgg")


url = f"{config('URL_SGG')}"
erros_gen = [
    "Erro ao processar a requisição",
    "Falha na conexão com o servidor",
    "Dados inválidos",
    "Erro interno do servidor",
    "Requisição expirada",
    "Erro desconhecido",
]


def criar_autenticacao():
    username = config("URL_SGG_TOKEN")
    password = ""

    # Concatena username e password com dois pontos
    credentials = f"{username}:{password}"

    # Codifica as credenciais em Base64
    credencial_codificada = base64.b64encode(credentials.encode()).decode()
    return f"Basic {credencial_codificada}"


def sincronizar_admissao_sgg(dados: List[AdmissaoSchema]):
    try:
        url = f"{config('URL_SGG')}/funcionario/"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": criar_autenticacao(),
        }
        erros = []
        for colab in dados:
            try:
                # payload = json.dumps(colab.dict(), default=str)
                # response = requests.post(url, headers=headers, data=payload)
                # if response.status_code != 200:
                #     resposta = response.json()
                #     mensagem = json.loads(resposta["returnInfo"])
                #     raise Exception(mensagem["msg"])
                if random.choice([True, False]):
                    raise Exception(erros_gen[random.randint(0, 5)])
            except Exception as e:
                erros.append({"Funcionario": colab.nome, "Erro": str(e)})
        if erros:
            nome_arquivo = gerar_erros(erros)
            return (
                f"Houveram {len(erros)} erros ao sincronizar os dados de admissão",
                nome_arquivo,
            )
        return "Sincronização Sem Erros", None
    except Exception as e:
        logger.warning(f"Erro ao sincronizar admissão: {e}")
        raise e


def sincronizar_demissao_sgg(dados: List[DemissaoSchema]):
    try:
        url = f"{config('URL_SGG')}/demissao/"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": criar_autenticacao(),
        }
        erros = []
        for colab in dados:
            try:
                # payload = json.dumps(colab.dict(), default=str)
                # response = requests.post(url, headers=headers, data=payload)
                # if response.status_code != 200:
                #     resposta = response.json()
                #     mensagem = json.loads(resposta["returnInfo"])
                #     raise Exception(mensagem["msg"])

                if random.choice([True, False]):
                    raise Exception(erros_gen[random.randint(0, 5)])
            except Exception as e:
                erros.append({"Funcionario": colab.nome, "Erro": str(e)})
        if erros:
            nome_arquivo = gerar_erros(erros)
            return (
                f"Houveram {len(erros)} erros ao sincronizar os dados de demissão",
                nome_arquivo,
            )
        return "Sincronização Sem Erros", None
    except Exception as e:
        logger.warning(f"Erro ao sincronizar demissão: {e}")
        raise e


def sincronizar_mudanca_funcao_sgg(dados: List[MudFuncaoSchema]):
    try:
        url = f"{config('URL_SGG')}/mudFuncao/"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": criar_autenticacao(),
        }
        erros = []
        for colab in dados:
            try:
                # payload = json.dumps(colab.dict(), default=str)
                # response = requests.post(url, headers=headers, data=payload)
                # if response.status_code != 200:
                #     resposta = response.json()
                #     mensagem = json.loads(resposta["returnInfo"])
                #     raise Exception(mensagem["msg"])
                if random.choice([True, False]):
                    raise Exception(erros_gen[random.randint(0, 5)])
            except Exception as e:
                erros.append({"Funcionario": colab.nome, "Erro": str(e)})
        if erros:
            nome_arquivo = gerar_erros(erros)
            return (
                f"Houveram {len(erros)} erros ao sincronizar os dados de mudança de função",
                nome_arquivo,
            )
        return "Sincronização Sem Erros", None
    except Exception as e:
        logger.warning(f"Erro ao sincronizar mudança de função: {e}")
        raise e


def sincronizar_transferencia_sgg(dados: List[TransferenciaSchema]):
    try:
        url = f"{config('URL_SGG')}/transferencia/"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": criar_autenticacao(),
        }
        erros = []
        for colab in dados:
            try:
                # payload = json.dumps(colab.dict(), default=str)
                # response = requests.post(url, headers=headers, data=payload)
                # if response.status_code != 200:
                #     resposta = response.json()
                #     mensagem = json.loads(resposta["returnInfo"])
                #     raise Exception(mensagem["msg"])
                if random.choice([True, False]):
                    raise Exception(erros_gen[random.randint(0, 5)])
            except Exception as e:
                erros.append({"Funcionario": colab.nome, "Erro": str(e)})
        if erros:
            nome_arquivo = gerar_erros(erros)
            return (
                f"Houveram {len(erros)} erros ao sincronizar os dados de transferência",
                nome_arquivo,
            )
        return "Sincronização Sem Erros", None
    except Exception as e:
        logger.warning(f"Erro ao sincronizar transferência: {e}")
        raise e


def gerar_erros(erros: List[str]):
    try:
        os.makedirs("./erro_sincronizacao", exist_ok=True)
        now = datetime.now()

        nome_arquivo = now.strftime("erros_%Y%m%d_%H%M%S.txt")

        caminho_arquivo = os.path.join("./erro_sincronizacao", nome_arquivo)

        with open(caminho_arquivo, "w") as file:
            file.write(json.dumps(erros, indent=4))
        return nome_arquivo
    except Exception as e:
        logger.warning(f"Erro ao ler os erros: {e}")
        raise e
