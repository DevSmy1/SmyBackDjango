import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from reportlab.platypus import Table, TableStyle

# X = 210 Y = 297
# ("BOTTOMPADDING", (0, 0), (-1, 0), 17),
# O primeiro valor é o tipo de estilo
# O segundo é a posição inicial da célula
# O terceiro é a posição final da célula.
# Dentro do 1º parenteses, o primeiro valor é a linha e o segundo é a coluna.
# Dentro do 2º parenteses, o primeiro valor é a linha e o segundo é a coluna.


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


def criar_nome_arquivo_uni(matricula):
    try:
        # verifica se já existe um arquivo com esse nome
        if not os.path.exists("./ReciboEntregaUni"):
            os.makedirs("./ReciboEntregaUni")
        if os.path.exists(f"./ReciboEntregaUni/{matricula}EntregaUni.pdf"):
            # se existir, criar um novo nome
            i = 1
            while os.path.exists(f"./ReciboEntregaUni/{matricula}EntregaUni({i}).pdf"):
                i += 1
            return f"./ReciboEntregaUni/{matricula}EntregaUni({i}).pdf"
        else:
            return f"./ReciboEntregaUni/{matricula}EntregaUni.pdf"
    except Exception as e:
        print(f"Erro: {e}")
        return False


def criar_termo_uni(data: dict, fichas: list, percentual: list):
    try:
        filePath = criar_nome_arquivo_uni(data.get("matricula"))
        pdf = canvas.Canvas(f"{filePath}", pagesize=A4)

        # Inicio do documento
        pdf.rect(mm2pt(10), mm2pt(255), mm2pt(50), mm2pt(30))
        # Adicionar uma imagem ao bloco acima
        pdf.drawImage(
            "./project/controle_uni/termo/logo.png",
            mm2pt(19),
            mm2pt(256),
            mm2pt(30),
            mm2pt(28),
        )

        pdf.setFont("Helvetica-Bold", 16)
        pdf.rect(mm2pt(60), mm2pt(255), mm2pt(140), mm2pt(30))
        pdf.drawString(mm2pt(80), mm2pt(267), "Recibo de Entrega de Uniforme e EPI")

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
        pdf.drawString(mm2pt(40), mm2pt(245), data.get("nome").title())  # type: ignore
        pdf.drawString(mm2pt(160), mm2pt(245), data.get("matricula"))  # type: ignore
        pdf.drawString(mm2pt(160), mm2pt(235), data.get("nroempresa"))  # type: ignore
        pdf.drawString(mm2pt(40), mm2pt(235), data.get("cargo"))  # type: ignore

        # Create a Table object with the data
        table = Table(fichas, colWidths=[mm2pt(10), mm2pt(100), mm2pt(40), mm2pt(30)])

        # aumentar fonte
        table.setStyle(
            TableStyle(
                [
                    ("FONTSIZE", (0, 1), (-1, -1), 11),
                    ("FONTSIZE", (0, 0), (-1, 0), 12),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (2, -1), (2, -1), "Helvetica-Bold"),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("TOPPADDING", (0, 0), (-1, -1), 1),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                    # linha acima da linha de total
                    # ("LINEABOVE", (3, -1), (-1, -1), 1, colors.black),
                    ("BOX", (0, 0), (-1, 1), 0.5, colors.black),
                    ("GRID", (0, 0), (-1, -2), 0.5, colors.black),
                    ("LINEBEFORE", (0, -1), (0, -1), 0.5, colors.black),
                    ("LINEBEFORE", (2, -1), (4, -1), 0.5, colors.black),
                    ("LINEBEFORE", (-1, -1), (-1, -1), 0.5, colors.black),
                    ("BOX", (0, -1), (-1, -1), 0.5, colors.black),
                ]
            )
        )

        # Call wrapOn() and drawOn() to format the Table
        table.wrapOn(pdf, 0, 0)
        table.drawOn(pdf, mm2pt(18), mm2pt(230 - (len(fichas) * 5)))

        # Avisos
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(
            mm2pt(17),
            mm2pt(165),
            "* Para Sapato, bota e luva (exeto luva de malha de aço), considerar a quantidade em pares.",
        )
        pdf.drawString(
            mm2pt(17),
            mm2pt(155),
            "Recebi do SUPERMERCADO YAMAUCHI LTDA. nesta data, os uniformes acima ",
        )
        pdf.drawString(
            mm2pt(17),
            mm2pt(150),
            "relacionados e declaro estar ciente que:",
        )

        # Paragrafos
        pdf.drawString(mm2pt(25), mm2pt(145), "a.")
        pdf.drawString(mm2pt(25), mm2pt(130), "b.")
        pdf.drawString(mm2pt(25), mm2pt(115), "c.")
        pdf.drawString(mm2pt(25), mm2pt(100), "d.")

        # Termos
        pdf.setFont("Helvetica", 12)
        # A
        pdf.drawString(
            mm2pt(30),
            mm2pt(145),
            "No encerramento do meu Contrato de Trabalho devo devolver todos os uniformes que  ",
        )
        pdf.drawString(
            mm2pt(30),
            mm2pt(140),
            "recebi durante o tempo de permanência na empresa.",
        )
        # B
        pdf.drawString(
            mm2pt(30),
            mm2pt(130),
            "Caso não devolva, estarei sujeito ao desconto do valor conforme critérios de  ",
        )
        pdf.drawString(
            mm2pt(30),
            mm2pt(125),
            "proporcionalidade de tempo de uso.",
        )
        # C
        pdf.drawString(
            mm2pt(30),
            mm2pt(115),
            "A má utilização (manchar com cândida na lavagem, por exemplo) também estará sujeita  ",
        )
        pdf.drawString(
            mm2pt(30),
            mm2pt(110),
            "ao desconto.",
        )
        # D
        pdf.drawString(
            mm2pt(30),
            mm2pt(100),
            "Os uniformes são para uso exclusivo nas dependências da empresa e dentro do horário  ",
        )
        pdf.drawString(
            mm2pt(30),
            mm2pt(95),
            "de trabalho.",
        )

        # percentual de desconto
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(
            mm2pt(17),
            mm2pt(85),
            "Critérios de proporcionalidade dos descontos por tempo de uso:",
        )

        pdf.setFont("Helvetica", 12)
        pdf.drawString(
            mm2pt(17),
            mm2pt(75),
            f"- Até 3 meses, descontar {percentual[0]} do valor unitário;",
        )
        pdf.drawString(
            mm2pt(17),
            mm2pt(65),
            f"- Até 6 meses, {percentual[1]} do valor unitário;",
        )
        pdf.drawString(
            mm2pt(17),
            mm2pt(55),
            f"- Até 9 meses, {percentual[2]} do valor unitário;",
        )
        pdf.drawString(
            mm2pt(17),
            mm2pt(45),
            f"- Acima de 12 meses, {percentual[3]} do valor unitário;",
        )

        nome = f"{data.get('nome').title()}"  # type: ignore
        linha = "_" * 70
        cpf = f"CPF: {data.get('cpf')}"
        data = f"Data: {data.get('dataAtual')}"  # type: ignore

        tamanhoLinha = pdf.stringWidth(linha, "Helvetica-Bold", 12)
        tamanhoNome = pdf.stringWidth(nome, "Helvetica-Bold", 12)
        tamanhoCpf = pdf.stringWidth(cpf, "Helvetica-Bold", 12)
        tamanhoData = pdf.stringWidth(data, "Helvetica-Bold", 12)  # type: ignore

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
            data,  # type: ignore
        )

        pdf.save()

        return filePath
    except Exception as e:
        raise Exception("Erro ao criar termo: ", e)
