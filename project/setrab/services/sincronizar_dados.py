import json
import logging

import pandas as pd
import requests
from django.db import transaction

from project.controle_uni.models import TsmyEuCargos, TsmyEuFuncao, TsmyEuSetor
from project.setrab.models import SetrabCargoRel, SetrabFuncaoRel, SetrabSetorRel

logger = logging.getLogger("sgg")


def sincronizar_colaboradores():
    try:
        url = "https://app.sgg.net.br/api/v3/funcionario/"

        payload = json.dumps({"paginador": {"pagina": 0, "tamanho": 100}})
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "••••••",
            "Cookie": "SGG=ng70cf060tskpebo6u3l8civi6",
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)
        pass
    except Exception as e:
        logger.warning(f"Erro ao sincronizar colaboradores: {e}")
        raise Exception("Erro ao sincronizar colaboradores: ", e)


def obter_objeto(modelo, **kwargs):
    try:
        return modelo.objects.get(**kwargs)
    except modelo.DoesNotExist:
        logger.warning(f"{modelo.__name__} não encontrado")
    except modelo.MultipleObjectsReturned:
        logger.warning(f"Mais de um {modelo.__name__} encontrado")
    return None


def processar_chunk(chunk, usuario):
    try:
        cargos_cache = {}
        funcoes_cache = {}
        setores_cache = {}
        user_data = {
            "usuario_criacao": usuario,
            "usuario_alteracao": usuario,
        }

        with transaction.atomic():
            for linha in range(len(chunk)):
                if len(str(chunk.iloc[linha][3])) <= 6:
                    cod_funcao = chunk.iloc[linha][1]
                    if cod_funcao not in cargos_cache:
                        cargos_cache[cod_funcao] = obter_objeto(
                            TsmyEuCargos, cod_funcao=cod_funcao
                        )
                    cargo = cargos_cache[cod_funcao]
                    if not cargo:
                        continue

                    SetrabCargoRel.objects.update_or_create(
                        id_cargo=cargo,
                        id_cargo_setrab=chunk.iloc[linha][3],
                        nro_empresa=chunk.iloc[linha][0],
                        defaults=user_data,
                    )

                    nome_funcao = cargo.funcao
                    if nome_funcao not in funcoes_cache:
                        funcoes_cache[nome_funcao] = obter_objeto(
                            TsmyEuFuncao, nome_funcao=nome_funcao
                        )

                    funcao = funcoes_cache[nome_funcao]
                    if not funcao:
                        continue

                    SetrabFuncaoRel.objects.update_or_create(
                        id_funcao=funcao,
                        id_funcao_setrab=chunk.iloc[linha][3],
                        nro_empresa=chunk.iloc[linha][0],
                        defaults=user_data,
                    )

                if len(str(chunk.iloc[linha][7])) <= 6:
                    cod_setor = chunk.iloc[linha][5]
                    if cod_setor not in setores_cache:
                        setores_cache[cod_setor] = obter_objeto(
                            TsmyEuSetor, cod_setor=cod_setor
                        )

                    setor = setores_cache[cod_setor]
                    if not setor:
                        continue

                    SetrabSetorRel.objects.update_or_create(
                        id_setor=setor,
                        id_setor_setrab=chunk.iloc[linha][7],
                        nro_empresa=chunk.iloc[linha][0],
                        defaults=user_data,
                    )
    except Exception as e:
        logger.warning(f"Erro ao processar chunk: {e}")
        raise Exception("Erro ao processar chunk: ", e)


def atualizar_dados(arquivo, usuario):
    try:
        xls = pd.ExcelFile(arquivo)
        num_planilhas = len(xls.sheet_names)
        for i in range(num_planilhas):
            df = pd.read_excel(arquivo, sheet_name=i)
            chunk_size = 10000
            for start in range(0, len(df), chunk_size):
                end = start + chunk_size
                chunk = df[start:end]
                processar_chunk(chunk, usuario)
    except Exception as e:
        logger.warning(f"Erro ao atualizar dados: {e}")
        raise Exception("Erro ao atualizar dados: ", e)
