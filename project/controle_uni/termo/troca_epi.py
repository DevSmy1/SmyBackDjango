import os
from typing import List
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from project.controle_uni.termo.functionsPdf import mm2pt
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle

import logging

logger = logging.getLogger("termo")


def criar_nome_arquivo_epi(matricula):
    try:
        if not os.path.exists("./ReciboEpi"):
            os.makedirs("./ReciboEpi")
        # verifica se já existe um arquivo com esse nome
        if os.path.exists(f"./ReciboEpi/{matricula}EntregaEpi.pdf"):
            # se existir, criar um novo nome
            i = 1
            while os.path.exists(f"./ReciboEpi/{matricula}EntregaEpi({i}).pdf"):
                i += 1
            return f"./ReciboEpi/{matricula}EntregaEpi({i}).pdf"
        else:
            return f"./ReciboEpi/{matricula}EntregaEpi.pdf"
    except Exception as e:
        print(f"Erro: {e}")
        return False


def criar_troca_epi(dadosColab: dict, dados: List[str]):
    try:
        filePath = criar_nome_arquivo_epi(dadosColab["matricula"])
        pdf = canvas.Canvas(filePath, pagesize=landscape(A4))  # type: ignore

        # Header do PDF
        add_header(pdf)

        # Dados do Colaborador
        add_titulo_dados(pdf)

        #  Dados do funcionario
        add_dados_colab(dadosColab, pdf)

        # Criando estilo
        styles = getSampleStyleSheet()
        # Mudando fonte
        styles["Normal"].fontName = "Helvetica"
        # Mudando tamanho da fonte
        styles["Normal"].fontSize = 11

        add_termo(pdf, styles)

        while len(dados) < 12:
            dados.append(["", "", "", "", ""])  # type: ignore

        add_tabela(dados, pdf)

        add_legenda(pdf, styles)

        pdf.save()
        return filePath
    except Exception as erro:
        print(f"Erro: {erro}")
        return None


def add_tabela(dados, pdf):
    table = Table(
        dados,
        colWidths=[mm2pt(20), mm2pt(20), mm2pt(120), mm2pt(30), mm2pt(50), mm2pt(40)],
    )

    # aumentar fonte
    table.setStyle(
        TableStyle(
            [
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                # Cabeçalho
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("FONTSIZE", (0, 0), (-1, -1), 12),
                ("FONTSIZE", (0, 0), (-1, 0), 14),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
        )
    )

    # Call wrapOn() and drawOn() to format the Table
    table.wrapOn(pdf, 0, 0)
    table.drawOn(pdf, mm2pt(10), mm2pt(70 - (len(dados) * 5)))


def add_legenda(pdf, styles):
    styles["Normal"].fontSize = 12
    styles["Normal"].fontName = "Helvetica-Bold"
    legenda = Paragraph(
        """Legenda: E=Entrega; T=Troca; D=Devolução; P=Perca; R= Rescisão; N/A=Não se Aplica""",
        style=styles["Normal"],
        encoding="utf-8",
    )
    legenda.wrapOn(pdf, mm2pt(270), mm2pt(10))
    legenda.drawOn(pdf, mm2pt(10), mm2pt(5))
    return legenda


def add_dados_colab(dadosColab, pdf):
    pdf.setFont("Helvetica-Bold", 13)
    # Titulo
    pdf.drawString(mm2pt(20), mm2pt(160), "Nome: ")
    pdf.drawString(mm2pt(120), mm2pt(160), "Matricula: ")
    pdf.drawString(mm2pt(160), mm2pt(160), "Loja: ")
    pdf.drawString(mm2pt(200), mm2pt(160), "Cargo: ")
    # Texto
    pdf.setFont("Helvetica", 12)
    pdf.drawString(mm2pt(35), mm2pt(160), dadosColab["nome"])
    pdf.drawString(mm2pt(142), mm2pt(160), dadosColab["matricula"])
    pdf.drawString(mm2pt(175), mm2pt(160), dadosColab["nroempresa"])
    pdf.drawString(mm2pt(215), mm2pt(160), dadosColab["cargo"])

    pdf.drawString(mm2pt(20), mm2pt(150), "Declaro que:")


def add_titulo_dados(pdf):
    pdf.rect(mm2pt(10), mm2pt(80), mm2pt(280), mm2pt(100))

    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(mm2pt(80), mm2pt(172), "Equipamento de Proteção Individual")

    pdf.setFont("Helvetica", 15)
    pdf.drawString(
        mm2pt(50),
        mm2pt(167),
        "Setor de Segurança do Trabalho - Termo de Compromisso de Entrega de E.P.I",
    )


def add_termo(pdf, styles):
    primeiro = Paragraph(
        """1 - Recebi do Supermercados Yamauchi LTDA, os equipamentos de proteção individual – EPI, abaixo relacionados, nas datas ali registradas, o qual, desde já, comprometo-me a usá-los na execução de minhas tarefas e atividades, zelando pela sua perfeita guarda, conservação, uso e funcionamento, assumindo também o compromisso de os devolver quando solicitados ou por ocasião de rescisão de contrato de trabalho; """,
        styles["Normal"],
        encoding="utf8",
    )

    # Add the Paragraph to the PDF
    primeiro.wrapOn(pdf, mm2pt(260), mm2pt(0))
    primeiro.drawOn(pdf, mm2pt(20), mm2pt(135))

    segundo = Paragraph(
        """2 - O descumprimento dos termos aqui estabelecidos, importará em ato faltoso do empregado, com aplicação de penalidades, que a critério do empregador, poderão variar de advertência por escrito à rescisão do contrato de trabalho, independentemente de outras medidas de ordem jurídica aplicáveis com base especialmente no Art. 158 da CLT e NR-1 da Portaria do MTE 3.214/78 (1.8 e 1.8.1);  """,
        styles["Normal"],
        encoding="utf8",
    )

    segundo.wrapOn(pdf, mm2pt(260), mm2pt(10))
    segundo.drawOn(pdf, mm2pt(20), mm2pt(120))

    terceiro = Paragraph(
        """3 - No caso de perda, dano, extravio ou avarias dos equipamentos referidos no item 1, autorizo desde já, a dedução do valor correspondente do meu salário; """,
        styles["Normal"],
        encoding="utf8",
    )

    terceiro.wrapOn(pdf, mm2pt(260), mm2pt(10))
    terceiro.drawOn(pdf, mm2pt(20), mm2pt(110))

    quatro = Paragraph(
        """4 - Declaro que os equipamentos que me foram entregues estão em perfeitas condições e que os utilizo conforme as normas de segurança e treinamentos realizados pela empresa.""",
        styles["Normal"],
        encoding="utf8",
    )

    quatro.wrapOn(pdf, mm2pt(260), mm2pt(10))
    quatro.drawOn(pdf, mm2pt(20), mm2pt(100))

    # Assinatura
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(mm2pt(20), mm2pt(90), "Assinatura do(a) funcionário(a): ")
    pdf.drawString(
        mm2pt(85),
        mm2pt(90),
        "__________________________________________________________________________________",
    )


def add_header(pdf):
    pdf.drawImage(
        "./project/controle_uni/termo/logo.png",
        mm2pt(10),
        mm2pt(180),
        mm2pt(32),
        mm2pt(30),
    )
    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawAlignedString(mm2pt(210), mm2pt(190), "Recibo de Entrega de EPI")
