import datetime
from bs4 import BeautifulSoup
import requests
from project.controle_uni.models import TsmyEuCa
from project.intranet.models import TsmyIntranetusuario


def verificarNroCa(nro_ca: int, usuario: TsmyIntranetusuario):
    try:
        dados = consultarValidadeCa(nro_ca)
        if dados:
            if (
                datetime.datetime.strptime(dados[2], "%d/%m/%Y")
                < datetime.datetime.now()
            ):
                raise ValueError("CA vencido")
            TsmyEuCa.objects.create(
                ca=nro_ca,
                dt_validade=datetime.datetime.strptime(dados[2], "%d/%m/%Y"),
                usuarioincl=usuario,
                usuarioalt=usuario,
            )
        return True
    except ValueError as e:
        raise e
    except Exception as e:
        raise e


def consultarValidadeCa(nro_ca: int):
    try:
        response = requests.get(f"https://consultaca.com/{nro_ca}", timeout=5)

        if response.status_code != 200:
            raise ValueError("Erro ao consultar CA")

        soup = BeautifulSoup(response.text, "html.parser")
        dados = []

        paragrafos = soup.find_all("p")
        for paragrafo in paragrafos:
            span = paragrafo.find("span")
            if span:
                dados.append(span.text)

        if not dados:
            raise ValueError("CA não encontrado")

        if len(dados) == 4:
            return dados
    except Exception as e:
        raise e
