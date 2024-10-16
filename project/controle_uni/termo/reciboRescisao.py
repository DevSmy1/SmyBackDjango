import os

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph


def transformarDinheiro(valor):
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


# X = 210 Y = 297
# ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
# O primeiro valor é o tipo de estilo
# O segundo é a posição inicial da célula
# O terceiro é a posição final da célula.
# Dentro do 1º parenteses, o primeiro valor é a linha e o segundo é a coluna.
# Dentro do 2º parenteses, o primeiro valor é a linha e o segundo é a coluna.


def mm2pt(mm):
    return mm * 2.83464567


def pt2mm(pt):
    return pt * 0.352778


def contaNovaLinha(data):
    try:
        contador = 0
        for linha in data:
            if isinstance(linha[1], str):
                if "\n" in linha[1]:
                    contador += 1
        return contador
    except Exception as e:
        print(f"Erro: {e}")
        return 0


def criaNomeArquivoRescisao(matricula):
    try:
        # verifica se já existe um arquivo com esse nome
        if os.path.exists(f"./RescisaoUni/{matricula}RescisaoUni.pdf"):
            # se existir, criar um novo nome
            i = 1
            while os.path.exists(f"./RescisaoUni/{matricula}RescisaoUni({i}).pdf"):
                i += 1
            return f"./RescisaoUni/{matricula}RescisaoUni({i}).pdf"
        else:
            return f"./RescisaoUni/{matricula}RescisaoUni.pdf"
    except Exception as e:
        print(f"Erro: {e}")
        return False


def criarRescisaoUni(data: dict, fichas: list):
    filePath = criaNomeArquivoRescisao(data.get("matricula"))
    pdf = canvas.Canvas(f"{filePath}", pagesize=A4)

    # Inicio do documento
    pdf.rect(mm2pt(10), mm2pt(255), mm2pt(50), mm2pt(30))
    # Adicionar uma imagem ao bloco acima
    pdf.drawImage("logo.png", mm2pt(19), mm2pt(256), mm2pt(30), mm2pt(28))

    pdf.setFont("Helvetica-Bold", 16)
    pdf.rect(mm2pt(60), mm2pt(255), mm2pt(140), mm2pt(30))

    # Criando estilo
    styles = getSampleStyleSheet()
    # Mudando fonte
    styles["Normal"].fontName = "Helvetica-Bold"
    # Mudando tamanho da fonte
    styles["Normal"].fontSize = 11
    # Alinhamento
    styles["Normal"].alignment = 1

    titulo = Paragraph(
        """AUTORIZAÇÃO DE DÉBITO EM RECISÃO DE CONTRATO DE TRABALHO UNIFORMES E EPI""",
        styles["Normal"],
        encoding="utf8",
    )

    titulo.wrapOn(pdf, mm2pt(140), mm2pt(10))
    titulo.drawOn(pdf, mm2pt(60), mm2pt(267))

    # Dados do funcionario
    # Nome abaixo
    pdf.setFont("Helvetica-Bold", 12)
    # Titulo
    pdf.drawString(mm2pt(20), mm2pt(245), "Nome: ")
    pdf.drawString(mm2pt(140), mm2pt(245), "Matricula: ")
    pdf.drawString(mm2pt(140), mm2pt(235), "Loja: ")
    pdf.drawString(mm2pt(20), mm2pt(235), "Cargo: ")
    # Texto
    pdf.setFont("Helvetica", 11)
    pdf.drawString(mm2pt(40), mm2pt(245), data.get("nome").title())
    pdf.drawString(mm2pt(160), mm2pt(245), data.get("matricula"))
    pdf.drawString(mm2pt(160), mm2pt(235), data.get("nroempresa"))
    pdf.drawString(mm2pt(40), mm2pt(235), data.get("cargo"))

    # Create a Table object with the data
    table = Table(
        fichas,
        colWidths=[
            mm2pt(15),  # Qtde
            mm2pt(48),  # Uniformes/ Materiais
            mm2pt(18),  # Valor Unitario
            mm2pt(18),  # Valor Total
            mm2pt(18),  # Data Receb
            mm2pt(13),  # Tempo Uso
            mm2pt(15),  # % Desc
            mm2pt(15),  # Devol
            mm2pt(15),  # Perda
            mm2pt(18),  # Desconto
        ],
    )

    # aumentar fonte
    table.setStyle(
        TableStyle(
            [
                ("FONTSIZE", (0, 2), (-1, -1), 7),
                ("FONTSIZE", (0, 0), (-1, 1), 9),
                ("FONTNAME", (0, 0), (-1, 1), "Helvetica-Bold"),
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                # grid somente no topo da linha
                ("BOX", (0, 0), (-1, 1), 0.5, colors.black),
                ("GRID", (0, 2), (-1, -2), 0.5, colors.black),
                ("LINEBEFORE", (0, 0), (-1, 1), 0.5, colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                # Ultima Linha
                ("LINEBEFORE", (0, -1), (0, -1), 0.5, colors.black),
                ("LINEBEFORE", (2, -1), (4, -1), 0.5, colors.black),
                ("LINEBEFORE", (-1, -1), (-1, -1), 0.5, colors.black),
                ("BOX", (0, -1), (-1, -1), 0.5, colors.black),
            ]
        )
    )

    # Call wrapOn() and drawOn() to format the Table
    table.wrapOn(pdf, 0, 0)
    multiLinhas = contaNovaLinha(fichas)
    table.drawOn(pdf, mm2pt(10), mm2pt(230 - ((len(fichas) + multiLinhas) * 5)))

    # Avisos
    styles["Normal"].alignment = 0
    styles["Normal"].fontSize = 11
    avisos = Paragraph(
        """* Para Sapato, bota e luva (exeto luva de malha de aço), considerar a quantidade em pares.""",
        styles["Normal"],
        encoding="utf8",
    )

    # Add the Paragraph to the PDF
    avisos.wrapOn(pdf, mm2pt(170), mm2pt(10))
    avisos.drawOn(pdf, mm2pt(10), mm2pt(220 - ((len(fichas) + multiLinhas) * 5)))

    # Termo
    styles["Normal"].fontSize = 12
    styles["Normal"].fontName = "Helvetica"
    termo = Paragraph(
        f"""DECLARO que AUTORIZO, livre e espontaneamente, meu empregador efetuar o desconto, em rescisão de contrato, acima relacionado no valor total de <b>{fichas[-1][-1]}</b>, conforme apuração de entrega de Uniformes/EPI acima relacionada.""",
        styles["Normal"],
        encoding="utf8",
    )

    # Add the Paragraph to the PDF
    termo.wrapOn(pdf, mm2pt(190), mm2pt(0))
    termo.drawOn(pdf, mm2pt(10), mm2pt(55))

    # Assinaturas
    pdf.setFont("Helvetica-Bold", 12)

    # Assinatura

    # Define the name
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
        mm2pt(23 + ((pt2mm(tamanhoLinha) - pt2mm(tamanhoNome)) / 2)), mm2pt(20), nome
    )

    # CPF
    pdf.drawString(
        mm2pt(23 + ((pt2mm(tamanhoLinha) - pt2mm(tamanhoCpf)) / 2)), mm2pt(15), cpf
    )

    # Data
    pdf.drawString(
        mm2pt(23 + ((pt2mm(tamanhoLinha) - pt2mm(tamanhoData)) / 2)), mm2pt(10), data
    )

    pdf.save()
    return filePath
