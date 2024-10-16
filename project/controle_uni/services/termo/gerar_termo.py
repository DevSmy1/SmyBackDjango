import datetime
import logging
from typing import List
from django.db.models import Min, Sum
from project.c5.models import MapProduto
from project.controle_uni.models import (
    TsmyEuColaboradores,
    TsmyEuFichaColab,
    TsmyEuLancto,
    TsmyEuParametro,
)
from project.controle_uni.schemas import SchemaAlterarFicha, SchemaFichaIn
from project.controle_uni.services.ficha import pegar_percentual_atual
from project.controle_uni.services.termo.termoUni import dadosFichaUni
from project.controle_uni.termo.reciboEntregaUni import criarTermoUni
from project.intranet.models import SmyUsuario
from icecream import ic

logger = logging.getLogger("termo")


def formatarDinheiro(valor):
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


def converterDinheiroParaFloat(valor):
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


def pegarCustoTotal(fichas: list):
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
                custoTotal += converterDinheiroParaFloat(ficha[-1])
        return formatarDinheiro(custoTotal)
    except Exception as e:
        print(f"Erro: {e}")
        return False


def pegarDataRecibo(data_admissao: datetime.date):
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


def gerarTermoUni(matricula: int, ids_fichas: List[int]):
    try:
        fichas = dadosFichaUni(ids_fichas)
        if len(fichas) <= 1:
            raise Exception("Nenhuma ficha encontrada")
        custoTotal = pegarCustoTotal(fichas)
        fichas.append(["", "", "Total", custoTotal])
        percentual = pegar_percentual_atual()
        colab = TsmyEuColaboradores.objects.get(matricula=matricula)
        dataAtual = pegarDataRecibo(colab.dt_adm).strftime("%d/%m/%Y")  # type: ignore
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
        reciboUni = criarTermoUni(data, fichas, percentual)
        return reciboUni
    except Exception as e:
        logger.error(f"Erro criar Recibo: {e}")
        raise Exception("Erro ao carregar dados da ficha recibo uniforme: ", e)


def gerarTermoEpi(matricula: int, ids_fichas):
    try:
        pass
    except Exception as e:
        logger.error(f"Erro criar Recibo: {e}")
        raise Exception("Erro ao carregar dados da ficha recibo EPI: ", e)
