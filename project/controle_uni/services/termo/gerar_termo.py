import datetime
import logging
import os
from typing import List
from project.controle_uni.models import (
    TsmyEuArquivo,
    TsmyEuColaboradores,
    TsmyEuLancto,
)
from project.controle_uni.services.ficha import pegar_percentual_atual
from project.controle_uni.services.termo.termo_epi import (
    dados_ficha_epi,
    transformar_lista_para_troca_epi,
)
from project.controle_uni.services.termo.termo_uni import dados_ficha_uni
from project.controle_uni.termo.ficha_controle import criar_ficha_controle
from project.controle_uni.termo.integracao_epi import criar_integracao_epi
from project.controle_uni.termo.reciboEntregaUni import criar_termo_uni
from project.controle_uni.termo.troca_epi import criar_troca_epi
from project.intranet.models import SmyUsuario

logger = logging.getLogger("termo")


def formatar_dinheiro(valor):
    """Pega um valo int ou float e transforma em uma string formatada como dinheiro (R$ 0.000,00)

    Args:
        valor : Um valor inteiro ou float

    Returns:
        str : Valor formatado como dinheiro (R$ 0.000,00)
    """
    try:
        valor = str(valor)
        valor = valor.replace(".", ",")
        # se não tiver casa decimal, adicionar ",00" ou se tiver apenas uma casa decimal, adicionar o zero
        if valor.find(",") == -1:
            valor += ",00"
        elif valor.find(",") == len(valor) - 2:
            valor += "0"
        elif valor.find(",") < len(valor) - 2:
            valor = valor[: valor.find(",") + 3]
        # Adicionar os pontos de milhar (se houver)
        if len(valor) > 6:
            valor = valor[:-6] + "." + valor[-6:]
        if len(valor) > 10:
            valor = valor[:-10] + "." + valor[-10:]
        return "R$ " + valor
    except Exception as e:
        print(f"Erro: {e}")
        return False


def converter_dinheiro_para_float(valor):
    """Pega um valor formatado como dinheiro (R$ 0.000,00) e transforma em float

    Args:
        valor (str): Valo formatado como dinheiro (R$ 0.000,00)

    Returns:
        float: Valor float
    """
    try:
        valor = str(valor)
        valor = valor.replace("R$ ", "")
        valor = valor.replace(".", "")
        valor = valor.replace(",", ".")
        return float(valor)
    except Exception as e:
        print(f"Erro: {e}")
        return False


def pegar_custo_total(fichas: list):
    """Pega o custo total dos Produtos

    Args:
        fichas (list) : lista de produtos

    Returns:
        str : Custo total dos produtos
    """
    try:
        custoTotal = 0
        for ficha in fichas:
            # pular o primeiro objeto da lista (que é o cabeçalho)
            if ficha[0] == "Qtde":
                continue
            else:
                custoTotal += converter_dinheiro_para_float(ficha[-1])
        return formatar_dinheiro(custoTotal)
    except Exception as e:
        print(f"Erro: {e}")
        return False


def pegar_data_Recibo(data_admissao: datetime.date):
    """Pegar a data do recibo com base no tipo do colaborador
    pode ser um colaborador antigo ou novo, pois se for novo a data no arquivo deve ser a data de admissão senão a data atual.
    Para descobrir vou usar a data de admissão para ser mais pratico se a data for maior que hoje então é um colaborador novo senão é um colaborador antigo, então irá ter a data de hoje.

    Args:
        data_admissao (date): Data de Admissão do colaborador
    """
    try:
        data_admissao = datetime.datetime.combine(
            data_admissao, datetime.datetime.min.time()
        )
        if data_admissao > datetime.datetime.now():
            return data_admissao
        return datetime.datetime.now()
    except Exception as e:
        print(f"Erro: {e}")
        return False


def status_colab_arquivo(matricula: int):
    try:
        lanctos = TsmyEuLancto.objects.filter(id_ficha__matricula__matricula=matricula)
        if lanctos.filter(cgo=219).exists() and not lanctos.filter(cgo=221).exists():
            return "integração"
        return "troca"
    except Exception as e:
        logger.error(e)
        return None


def criar_registro_arquivo_integracao(
    dadosColab: dict, reciboEpi: str, usuario: SmyUsuario
):
    try:
        colab = TsmyEuColaboradores.objects.get(matricula=dadosColab["matricula"])
        TsmyEuArquivo.objects.create(
            nome_arquivo=reciboEpi,
            matricula=colab,
            tipo_arquivo="IE",
            usuario_criacao=usuario,
            usuario_alteracao=usuario,
        )
        return True
    except Exception as e:
        logger.error(e)
        return False


def gerar_termo_uni(matricula: int, ids_fichas: List[int]):
    try:
        fichas = dados_ficha_uni(ids_fichas)
        if len(fichas) <= 1:
            raise Exception("Nenhuma ficha encontrada")
        custoTotal = pegar_custo_total(fichas)
        fichas.append(["", "", "Total", custoTotal])
        percentual = pegar_percentual_atual()
        colab = TsmyEuColaboradores.objects.get(matricula=matricula)
        dataAtual = pegar_data_Recibo(colab.dt_adm).strftime("%d/%m/%Y")  # type: ignore
        if len(str(colab.cpf)) == 10:
            colab.cpf = "0" + str(colab.cpf)  # type: ignore
        elif len(str(colab.cpf)) == 9:
            colab.cpf = "00" + str(colab.cpf)  # type: ignore
        data = {
            "nome": colab.nome,
            "nroempresa": str(colab.nroempresa),
            "matricula": str(colab.matricula),
            "cargo": (
                colab.cod_funcao_nova.funcao
                if colab.cod_funcao_nova
                else colab.cod_funcao.funcao  # type: ignore
            ),
            "cpf": str(colab.cpf),
            "dataAtual": dataAtual,
        }
        reciboUni = criar_termo_uni(data, fichas, percentual)
        return reciboUni
    except Exception as e:
        logger.error(f"Erro criar Recibo: {e}")
        raise Exception("Erro ao carregar dados da ficha recibo uniforme: ", e)


def gerar_termo_epi(matricula: int, ids_fichas, usuario: SmyUsuario):
    try:
        fichas = dados_ficha_epi(ids_fichas)
        if not fichas:
            logger.info("Nenhum EPI encontrado")
            return None, None
        colab = TsmyEuColaboradores.objects.get(matricula=matricula)
        if len(str(colab.cpf)) == 10:
            colab.cpf = "0" + str(colab.cpf)  # type: ignore
        elif len(str(colab.cpf)) == 9:
            colab.cpf = "00" + str(colab.cpf)  # type: ignore
        data = {
            "nome": colab.nome,
            "nroempresa": str(colab.nroempresa),
            "matricula": str(colab.matricula),
            "cargo": (
                colab.cod_funcao_nova.funcao
                if colab.cod_funcao_nova
                else colab.cod_funcao.funcao  # type: ignore
            ),
            "cpf": str(colab.cpf),
            "setor": "",
            "dataAtual": datetime.date.today().strftime("%d/%m/%Y"),
        }
        if status_colab_arquivo(matricula) == "troca":
            arquivo_integracao: str = criar_integracao_epi(data)  # type: ignore
            recibo_epi = criar_ficha_controle(data, fichas)  # type: ignore
            print("Integração")
        elif status_colab_arquivo(matricula) == "integracao":
            fichas = transformar_lista_para_troca_epi(fichas)
            recibo_epi = criar_troca_epi(data, fichas)  # type: ignore
        return recibo_epi, arquivo_integracao
    except Exception as e:
        if "arquivo_integracao" in locals():
            os.remove(arquivo_integracao)
        if "recibo_epi" in locals():
            os.remove(recibo_epi)  # type: ignore
        logger.error(f"Erro criar Recibo: {e}")
        raise Exception("Erro ao carregar dados da ficha recibo EPI: ", e)
