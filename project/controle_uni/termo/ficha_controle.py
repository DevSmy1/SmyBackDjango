import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle
from project.controle_uni.termo.functionsPdf import mm2pt
import logging

logger = logging.getLogger("termo")


def criar_nome_arquivo_epi(matricula):
    try:
        if not os.path.exists("./ReciboEpi"):
            os.makedirs("./ReciboEpi")
        # verifica se já existe um arquivo com esse nome
        if os.path.exists(f"./ReciboEpi/{matricula}FichaControle.pdf"):
            # se existir, criar um novo nome
            i = 1
            while os.path.exists(f"./ReciboEpi/{matricula}FichaControle({i}).pdf"):
                i += 1
            return f"./ReciboEpi/{matricula}FichaControle({i}).pdf"
        else:
            return f"./ReciboEpi/{matricula}FichaControle.pdf"
    except Exception as e:
        print(f"Erro: {e}")
        return False


def criar_ficha_controle(dadosColab: dict, dados: list):
    try:
        filePath = criar_nome_arquivo_epi(dadosColab["matricula"])
        pdf = canvas.Canvas(filePath, pagesize=landscape(A4))  # type: ignore
        # Criando estilo
        styles = getSampleStyleSheet()
        # Mudando fonte
        styles["Normal"].fontName = "Helvetica"
        # Mudando tamanho da fonte
        styles["Normal"].fontSize = 12

        stylesDados = getSampleStyleSheet()
        stylesDados["Normal"].fontName = "Helvetica"
        stylesDados["Normal"].fontSize = 12

        # Logo da empresa
        pdf.rect(mm2pt(10), mm2pt(180), mm2pt(50), mm2pt(22))
        pdf.drawImage(
            "./project/controle_uni/termo/logo.png",
            mm2pt(22),
            mm2pt(181),
            mm2pt(22),
            mm2pt(20),
        )

        # Box do título
        styles["Normal"].fontSize = 16
        styles["Normal"].fontName = "Helvetica-Bold"
        styles["Normal"].alignment = 1
        pdf.rect(mm2pt(60), mm2pt(180), mm2pt(230), mm2pt(22))
        # Titulo
        add_titulo(pdf, styles)
        styles["Normal"].alignment = 0

        # Logo da empresa
        pdf.rect(mm2pt(240), mm2pt(180), mm2pt(50), mm2pt(22))
        pdf.drawImage(
            "./project/controle_uni/termo/st.png",
            mm2pt(255),
            mm2pt(182),
            mm2pt(20),
            mm2pt(18),
            mask="auto",
        )

        # Escopo do Documento
        pdf.rect(mm2pt(10), mm2pt(15), mm2pt(280), mm2pt(187))

        styles["Normal"].fontSize = 13
        styles["Normal"].fontName = "Helvetica-Bold"

        # Nome
        add_dados_colab(dadosColab, pdf, styles, stylesDados)

        # Termo de Responsabilidade
        add_termo(pdf, styles)

        # Data e Assinatura
        add_data_assinatura(pdf, styles)

        if len(dados) > 11:
            dados1 = dados[:11]
            add_tabela(dados1, pdf, 70)
        elif len(dados) < 11:
            while len(dados) < 11:
                dados.append([])
            add_tabela(dados, pdf, 70)

        # Legenda
        add_legenda(pdf, styles)

        # # Criar Segunda Página
        # pdf.showPage()

        # dados2 = [dados[0]]
        # dados2 = dados2 + dados[11:]

        # # Tabela
        # while len(dados2) < 28:
        #     dados2.append([])

        # addTabela(dados2, pdf, 155)

        # addLegenda(pdf, styles)

        pdf.save()
        return filePath
    except Exception as erro:
        logger.error(f"Erro ao criar ficha de controle: {erro}")
        raise Exception("Erro ao criar ficha de controle")


def add_tabela(dados, pdf, alturaInicial):
    tabela = Table(
        dados,
        colWidths=[
            mm2pt(30),
            mm2pt(20),
            mm2pt(80),
            mm2pt(40),
            mm2pt(20),
            mm2pt(30),
            mm2pt(20),
            mm2pt(40),
        ],
    )

    # Estilizando Tabela
    tabela.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
        )
    )

    tabela.wrapOn(pdf, 10, 290)
    tabela.drawOn(pdf, mm2pt(10), mm2pt(alturaInicial - (len(dados) * 5)))


def add_legenda(pdf, styles):
    styles["Normal"].fontSize = 12
    styles["Normal"].fontName = "Helvetica-Bold"
    legenda = Paragraph(
        """Legenda: E=Entrega; T=Troca; D=Devolução; P=Perca; R= Rescisão; N/A=Não se Aplica""",
        style=styles["Normal"],
        encoding="utf-8",
    )
    legenda.wrapOn(pdf, mm2pt(270), mm2pt(10))
    legenda.drawOn(pdf, mm2pt(10), mm2pt(10))
    return legenda


def add_data_assinatura(pdf, styles):
    styles["Normal"].fontSize = 13
    styles["Normal"].fontName = "Helvetica-Bold"
    dataAss = Paragraph(
        """SÂO PAULO, 12 DE DEZEMBRO 2023""",
        style=styles["Normal"],
        encoding="utf-8",
    )
    dataAss.wrapOn(pdf, mm2pt(270), mm2pt(10))
    dataAss.drawOn(pdf, mm2pt(15), mm2pt(100))

    assinatura = Paragraph(
        """ASSINATURA DO FUNCIONÁRIO:___________________________""",
        style=styles["Normal"],
        encoding="utf-8",
    )
    assinatura.wrapOn(pdf, mm2pt(270), mm2pt(10))
    assinatura.drawOn(pdf, mm2pt(120), mm2pt(100))


def add_termo(pdf, styles):
    tituloTermo = Paragraph(
        """Termo de Responsabilidade""",
        style=styles["Normal"],
        encoding="utf-8",
    )
    tituloTermo.wrapOn(pdf, mm2pt(280), mm2pt(10))
    tituloTermo.drawOn(pdf, mm2pt(115), mm2pt(150))

    # Texto de responsabilidade
    styles["Normal"].fontSize = 12
    styles["Normal"].fontName = "Helvetica"
    textoResponsabilidade = Paragraph(
        """Declaro sob minha inteira responsabilidade, a guarda e conservação dos equipamentos de proteção individual constantes nesta ficha. Assumo também, a responsabilidade de devolvê-los quando solicitados ou por ocasião de eventual rescisão de contrato de trabalho, na data do respectivo aviso de qualquer das partes. Também estou ciente que, na eventualidade de danificar ou extraviar o equipamento por ato doloso ou culposo, estarei sujeito ao desconto do valor em meu salário, conforme parágrafo único do art. 158 da CLT. Declaro ainda, ter recebido orientação quanto ao uso correto, guarda, conservação e higienização dos EPIs. Também estou ciente que a não utilização destes em minhas atividades profissionais, é ato faltoso e passível de punições legais e disciplinares de acordo com a Consolidação das Leis do Trábalho (CLT) — Capítulo V — Seção I - Art 158 e Norma Regulamentadora (NR) — 01 e 06, alínea 6.7, disciplinadas pela Portaria MTB nº 3.214/78 e artigo 191, itens I e II da CLT e súmula nº 80 do TST. Declaro que os equipamentos que me foram entregues estão em perfeitas condições e que os utilizarei conforme as normas de segurança e treinamentos realizados pela empresa.""",
        style=styles["Normal"],
        encoding="utf-8",
    )
    textoResponsabilidade.wrapOn(pdf, mm2pt(270), mm2pt(140))
    textoResponsabilidade.drawOn(pdf, mm2pt(15), mm2pt(110))


def add_titulo(pdf, styles):
    titulo = Paragraph(
        ("""Ficha de Controle e Entrega de Equipamento""").upper(),
        style=styles["Normal"],
        encoding="utf-8",
    )
    titulo.wrapOn(pdf, mm2pt(170), mm2pt(22))
    titulo.drawOn(pdf, mm2pt(62), mm2pt(195))

    titulo = Paragraph(
        ("""de proteção individual E.P.I""").upper(),
        style=styles["Normal"],
        encoding="utf-8",
    )
    titulo.wrapOn(pdf, mm2pt(170), mm2pt(22))
    titulo.drawOn(pdf, mm2pt(62), mm2pt(190))


def add_dados_colab(dadosColab, pdf, styles, stylesDados):
    pdf.rect(mm2pt(10), mm2pt(170), mm2pt(120), mm2pt(10))
    nome = Paragraph(
        """Nome:""",
        style=styles["Normal"],
        encoding="utf-8",
    )
    nome.wrapOn(pdf, mm2pt(93), mm2pt(10))
    nome.drawOn(pdf, mm2pt(13), mm2pt(172))

    nomeDados = Paragraph(
        f"""{dadosColab.get("nome")}""",
        style=stylesDados["Normal"],
        encoding="utf-8",
    )
    nomeDados.wrapOn(pdf, mm2pt(93), mm2pt(10))
    nomeDados.drawOn(pdf, mm2pt(30), mm2pt(172))

    # Matricula
    pdf.rect(mm2pt(130), mm2pt(170), mm2pt(80), mm2pt(10))
    matricula = Paragraph(
        """Matricula:""",
        style=styles["Normal"],
        encoding="utf-8",
    )
    matricula.wrapOn(pdf, mm2pt(93), mm2pt(10))
    matricula.drawOn(pdf, mm2pt(133), mm2pt(172))

    matriculaDados = Paragraph(
        f"""{dadosColab.get("matricula")}""",
        style=stylesDados["Normal"],
        encoding="utf-8",
    )
    matriculaDados.wrapOn(pdf, mm2pt(93), mm2pt(10))
    matriculaDados.drawOn(pdf, mm2pt(155), mm2pt(172))

    # Loja
    pdf.rect(mm2pt(210), mm2pt(170), mm2pt(80), mm2pt(10))
    loja = Paragraph(
        """Loja:""",
        style=styles["Normal"],
        encoding="utf-8",
    )
    loja.wrapOn(pdf, mm2pt(93), mm2pt(10))
    loja.drawOn(pdf, mm2pt(212), mm2pt(172))

    lojaDados = Paragraph(
        f"""{dadosColab.get("nroempresa")}""",
        style=stylesDados["Normal"],
        encoding="utf-8",
    )
    lojaDados.wrapOn(pdf, mm2pt(93), mm2pt(10))
    lojaDados.drawOn(pdf, mm2pt(223), mm2pt(172))

    # Funcao
    pdf.rect(mm2pt(10), mm2pt(160), mm2pt(120), mm2pt(10))
    funcao = Paragraph(
        """Função:""",
        style=styles["Normal"],
        encoding="utf-8",
    )
    funcao.wrapOn(pdf, mm2pt(93), mm2pt(10))
    funcao.drawOn(pdf, mm2pt(13), mm2pt(162))

    funcaoDados = Paragraph(
        f"""{dadosColab.get("cargo")}""",
        style=stylesDados["Normal"],
        encoding="utf-8",
    )
    funcaoDados.wrapOn(pdf, mm2pt(93), mm2pt(10))
    funcaoDados.drawOn(pdf, mm2pt(32), mm2pt(162))

    # Setor
    pdf.rect(mm2pt(80), mm2pt(160), mm2pt(50), mm2pt(10))
    setor = Paragraph(
        """Setor:""",
        style=styles["Normal"],
        encoding="utf-8",
    )
    setor.wrapOn(pdf, mm2pt(93), mm2pt(10))
    setor.drawOn(pdf, mm2pt(82), mm2pt(162))

    setorDados = Paragraph(
        f"""{dadosColab.get("setor")}""",
        style=stylesDados["Normal"],
        encoding="utf-8",
    )
    setorDados.wrapOn(pdf, mm2pt(93), mm2pt(10))
    setorDados.drawOn(pdf, mm2pt(96), mm2pt(162))

    # Data Admissão
    pdf.rect(mm2pt(130), mm2pt(160), mm2pt(80), mm2pt(10))
    dtAdm = Paragraph(
        """Data Admissão:""",
        style=styles["Normal"],
        encoding="utf-8",
    )
    dtAdm.wrapOn(pdf, mm2pt(62), mm2pt(10))
    dtAdm.drawOn(pdf, mm2pt(133), mm2pt(162))

    dtAdmDados = Paragraph(
        f"""{dadosColab.get("dataAtual")}""",
        style=stylesDados["Normal"],
        encoding="utf-8",
    )
    dtAdmDados.wrapOn(pdf, mm2pt(62), mm2pt(10))
    dtAdmDados.drawOn(pdf, mm2pt(168), mm2pt(162))

    # Data Demissão
    pdf.rect(mm2pt(210), mm2pt(160), mm2pt(80), mm2pt(10))
    dtDem = Paragraph(
        """Data Demissão:""",
        style=styles["Normal"],
        encoding="utf-8",
    )
    dtDem.wrapOn(pdf, mm2pt(94), mm2pt(10))
    dtDem.drawOn(pdf, mm2pt(213), mm2pt(162))
