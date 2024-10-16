import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

# X = 210 Y = 297


def mm2pt(mm):
    return mm * 2.83464567


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


def criaNomeArquivoEpi(matricula):
    try:
        # verifica se já existe um arquivo com esse nome
        if os.path.exists(f"./ReciboEntregaEpi/{matricula}EntregaEpi.pdf"):
            # se existir, criar um novo nome
            i = 1
            while os.path.exists(f"./ReciboEntregaEpi/{matricula}EntregaEpi({i}).pdf"):
                i += 1
            return f"./ReciboEntregaEpi/{matricula}EntregaEpi({i}).pdf"
        else:
            return f"./ReciboEntregaEpi/{matricula}EntregaEpi.pdf"
    except Exception as e:
        print(f"Erro: {e}")
        return False


def criarTermoEpi(data, fichas):
    try:
        filePath = criaNomeArquivoEpi(data.get("matricula"))
        pdf = canvas.Canvas(f"{filePath}", pagesize=A4)

        pdf.setFont("Helvetica-Bold", 22)
        pdf.drawAlignedString(mm2pt(145), mm2pt(280), "Recibo de Entrega EPI")

        pdf.rect(mm2pt(10), mm2pt(130), mm2pt(190), mm2pt(140))

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(mm2pt(50), mm2pt(260), "Equipamento de Proteção Individual")

        pdf.setFont("Helvetica", 13)
        pdf.drawString(
            mm2pt(24),
            mm2pt(255),
            "Setor de Segurança do Trabalho - Termo de Compromisso de Entrega de E.P.I",
        )

        # Dados do funcionario
        # Nome abaixo
        pdf.setFont("Helvetica-Bold", 12)
        # Titulo
        pdf.drawString(mm2pt(20), mm2pt(245), "Nome: ")
        pdf.drawString(mm2pt(140), mm2pt(245), "Matricula: ")
        pdf.drawString(mm2pt(140), mm2pt(238), "Loja: ")
        pdf.drawString(mm2pt(20), mm2pt(238), "Cargo: ")
        # Texto
        pdf.setFont("Helvetica", 11)
        pdf.drawString(mm2pt(40), mm2pt(245), data.get("nome").title())
        pdf.drawString(mm2pt(160), mm2pt(245), data.get("matricula"))
        pdf.drawString(mm2pt(160), mm2pt(238), data.get("nroempresa"))
        pdf.drawString(mm2pt(40), mm2pt(238), data.get("cargo"))

        pdf.drawString(mm2pt(20), mm2pt(225), "Declaro que:")

        # Criando estilo
        styles = getSampleStyleSheet()
        # Mudando fonte
        styles["Normal"].fontName = "Helvetica"
        # Mudando tamanho da fonte
        styles["Normal"].fontSize = 11

        primeiro = Paragraph(
            """1 - Recebi do Supermercados Yamauchi LTDA, os equipamentos de proteção individual – EPI, abaixo relacionados, nas datas ali registradas, o qual, desde já, comprometo-me a usá-los na execução de minhas tarefas e atividades, zelando pela sua perfeita guarda, conservação, uso e funcionamento, assumindo também o compromisso de os devolver quando solicitados ou por ocasião de rescisão de contrato de trabalho; """,
            styles["Normal"],
            encoding="utf8",
        )

        # Add the Paragraph to the PDF
        primeiro.wrapOn(pdf, mm2pt(170), mm2pt(10))
        primeiro.drawOn(pdf, mm2pt(20), mm2pt(200))

        segundo = Paragraph(
            """2 - O descumprimento dos termos aqui estabelecidos, importará em ato faltoso do empregado, com aplicação de penalidades, que a critério do empregador, poderão variar de advertência por escrito à rescisão do contrato de trabalho, independentemente de outras medidas de ordem jurídica aplicáveis com base especialmente no Art. 158 da CLT e NR-1 da Portaria do MTE 3.214/78 (1.8 e 1.8.1);  """,
            styles["Normal"],
            encoding="utf8",
        )

        segundo.wrapOn(pdf, mm2pt(170), mm2pt(10))
        segundo.drawOn(pdf, mm2pt(20), mm2pt(175))

        terceiro = Paragraph(
            """3 - No caso de perda, dano, extravio ou avarias dos equipamentos referidos no item 1, autorizo desde já, a dedução do valor correspondente do meu salário; """,
            styles["Normal"],
            encoding="utf8",
        )

        terceiro.wrapOn(pdf, mm2pt(170), mm2pt(10))
        terceiro.drawOn(pdf, mm2pt(20), mm2pt(162))

        quatro = Paragraph(
            """4 - Declaro que os equipamentos que me foram entregues estão em perfeitas condições e que os utilizo conforme as normas de segurança e treinamentos realizados pela empresa.""",
            styles["Normal"],
            encoding="utf8",
        )

        quatro.wrapOn(pdf, mm2pt(170), mm2pt(10))
        quatro.drawOn(pdf, mm2pt(20), mm2pt(149))

        # Assinatura
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(mm2pt(20), mm2pt(140), "Assinatura do(a) funcionário(a): ")
        pdf.drawString(mm2pt(85), mm2pt(140), "______________________________________")

        if len(fichas) <= 23:
            for i in range(0, 23 - len(fichas)):
                fichas.append(["", "", "", "", ""])

        table = Table(
            fichas, colWidths=[mm2pt(20), mm2pt(20), mm2pt(100), mm2pt(20), mm2pt(30)]
        )

        # aumentar fonte
        table.setStyle(
            TableStyle(
                [
                    ("TOPPADDING", (0, 0), (-1, -1), 1),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                    # Cabeçalho
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("FONTSIZE", (0, 0), (-1, 0), 12),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ]
            )
        )

        # Call wrapOn() and drawOn() to format the Table
        table.wrapOn(pdf, 0, 0)
        table.drawOn(pdf, mm2pt(10), mm2pt(125 - (len(fichas) * 5)))

        pdf.save()
        return filePath
    except Exception as e:
        print(f"Erro: {e}")
        return False
