import os
from PyPDF2 import PdfReader
import pandas as pd

from project.controle_uni.models import TsmyEuCargos
from project.intranet.models import TsmyIntranetusuario


def carregarArquivoCargo(caminho: str, usuario: TsmyIntranetusuario):
    try:
        pdf = PdfReader(caminho)
        tabela = []
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            linhas = texto.split("\n")
            linhas = linhas[7:]
            linhas = linhas[:-3]
            for linha in linhas:
                rows = linha.strip().split("|")
                tabela.append(rows)

        df = pd.DataFrame(tabela)

        df.to_csv(f"{caminho}.csv", index=False, header=False)

        df = pd.read_csv(
            f"{caminho}.csv",
            header=None,
            sep=",",
            usecols=[0, 1],
            skipfooter=2,
            engine="python",
        )
        try:
            for _, row in df.iterrows():
                cargo = TsmyEuCargos(
                    cod_funcao=row[0],
                    funcao=row[1].strip(),
                    usuarioalt=usuario,
                )
                if not TsmyEuCargos.objects.get(cod_funcao=row[0]):
                    cargo.usuarioincl = usuario
                cargo.save()
        except Exception as e:
            raise Exception("Erro ao carregar cargo: ", e)
        os.remove(f"{caminho}.csv")
    except Exception as e:
        raise Exception("Erro ao carregar arquivo: ", e)
