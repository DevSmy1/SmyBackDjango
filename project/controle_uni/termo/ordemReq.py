import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from reportlab.platypus import Table, TableStyle

# X = 210 Y = 297
# ("BOTTOMPADDING", (0, 0), (-1, 0), 17),
# O primeiro valor é o tipo de estilo
# O segundo é a posição inicial da célula
# Dentro do 1º parenteses, o primeiro valor é a linha e o segundo é a coluna.
# O terceiro é a posição final da célula.
# Dentro do 2º parenteses, o primeiro valor é a linha e o segundo é a coluna.
# O quarto é o valor do estilo.


def mm2pt(mm):
    return mm * 2.83464567


def pt2mm(pt):
    return pt * 0.352778


def formatarDinheiro(valor):
    valor = str(valor)
    valor = valor.replace(".", ",")
    # se não tiver casa decimal, adicionar ",00"
    if valor.find(",") == -1:
        valor += ",00"
    # se tiver mais de duas casas decimais, 39,993651 por exemplo, arredondar para 39,99
    elif len(valor[valor.find(",") :]) > 3:
        valor = valor[: valor.find(",") + 3]
    return valor


def criaNomeArquivoOrdemReq(cpf):
    try:
        # verifica se já existe um arquivo com esse nome
        if os.path.exists(f"./OrdemReq/{cpf}OrdemReq.pdf"):
            # se existir, criar um novo nome
            i = 1
            while os.path.exists(f"./OrdemReq/{cpf}OrdemReq({i}).pdf"):
                i += 1
            return f"./OrdemReq/{cpf}OrdemReq({i}).pdf"
        else:
            return f"./OrdemReq/{cpf}OrdemReq.pdf"
    except Exception as e:
        print(f"Erro: {e}")
        return False


def criarOrdemReq(data: dict, fichas: list):
    try:
        filePath = criaNomeArquivoOrdemReq(data.get("cpf"))
        pdf = canvas.Canvas(f"{filePath}", pagesize=A4)

        # Inicio do documento
        pdf.rect(mm2pt(10), mm2pt(255), mm2pt(50), mm2pt(30))
        # Adicionar uma imagem ao bloco acima
        pdf.drawImage("logo.png", mm2pt(19), mm2pt(256), mm2pt(30), mm2pt(28))

        pdf.setFont("Helvetica-Bold", 16)
        pdf.rect(mm2pt(60), mm2pt(255), mm2pt(140), mm2pt(30))
        pdf.drawString(mm2pt(80), mm2pt(267), "Ordem De Requisição de Uniformes")

        # Dados do funcionario
        # Nome abaixo
        pdf.setFont("Helvetica-Bold", 12)
        # Titulo
        pdf.drawString(mm2pt(20), mm2pt(245), "Nome: ")
        pdf.drawString(mm2pt(140), mm2pt(245), "Cargo: ")
        # Texto
        pdf.setFont("Helvetica", 11)
        pdf.drawString(mm2pt(40), mm2pt(245), data.get("nome").title())
        pdf.drawString(mm2pt(160), mm2pt(245), data.get("cargo"))

        tabela = Table(fichas, colWidths=[mm2pt(30), mm2pt(130), mm2pt(30)])

        tabela.setStyle(
            TableStyle(
                [
                    ("FONTSIZE", (0, 0), (-1, 0), 14),
                    ("FONTSIZE", (0, 1), (-1, -1), 12),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )

        tabela.wrapOn(pdf, 0, 0)
        tabela.drawOn(pdf, mm2pt(10), mm2pt(235 - (len(fichas) * 7)))

        nome = f"{data.get('nome').title()}"
        linha = "_" * 70
        cpf = f"CPF: {data.get('cpf')}"
        data = f"Data: {data.get('dataAtual')}"

        tamanhoLinha = pdf.stringWidth(linha, "Helvetica-Bold", 12)
        tamanhoNome = pdf.stringWidth(nome, "Helvetica-Bold", 12)
        tamanhoCpf = pdf.stringWidth(cpf, "Helvetica-Bold", 12)
        tamanhoData = pdf.stringWidth(data, "Helvetica-Bold", 12)

        pdf.drawString(mm2pt(23), mm2pt(25), linha)
        pdf.drawString(
            mm2pt(23 + ((pt2mm(tamanhoLinha) - pt2mm(tamanhoNome)) / 2)),
            mm2pt(20),
            nome,
        )

        # CPF
        pdf.drawString(
            mm2pt(23 + ((pt2mm(tamanhoLinha) - pt2mm(tamanhoCpf)) / 2)), mm2pt(15), cpf
        )

        # Data
        pdf.drawString(
            mm2pt(23 + ((pt2mm(tamanhoLinha) - pt2mm(tamanhoData)) / 2)),
            mm2pt(10),
            data,
        )

        pdf.save()
        return filePath
    except Exception as e:
        print(f"Erro: {e}")
        return False
