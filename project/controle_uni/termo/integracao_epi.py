import os
from project.controle_uni.termo.functionsPdf import mm2pt
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
import logging

logger = logging.getLogger("termo")


def criar_nome_arquivo_epi(matricula):
    try:
        if not os.path.exists("./ReciboEpi"):
            os.makedirs("./ReciboEpi")
        # verifica se já existe um arquivo com esse nome
        if os.path.exists(f"./ReciboEpi/{matricula}Integracao.pdf"):
            # se existir, criar um novo nome
            i = 1
            while os.path.exists(f"./ReciboEpi/{matricula}Integracao({i}).pdf"):
                i += 1
            return f"./ReciboEpi/{matricula}Integracao({i}).pdf"
        else:
            return f"./ReciboEpi/{matricula}Integracao.pdf"
    except Exception as e:
        print(f"Erro: {e}")
        return False


def cria_integracao_epi(dadosColab: dict):
    try:
        filePath = criar_nome_arquivo_epi(dadosColab["matricula"])
        pdf = canvas.Canvas(filePath, pagesize=landscape(A4))  # type: ignore
        styles = getSampleStyleSheet()
        # Mudando fonte
        styles["Normal"].fontName = "Helvetica"
        # Mudando tamanho da fonte
        styles["Normal"].fontSize = 13

        # Linhas do PDF
        pdf.rect(mm2pt(5), mm2pt(5), mm2pt(287), mm2pt(200))

        # Header
        add_header(pdf)

        # Dados Colab
        add_linhas_dados_colab(pdf)
        add_dados_colab(dadosColab, pdf)

        # Termo
        pdf.setFont("Helvetica", 12)
        add_termo(dadosColab, pdf, styles)

        add_assinatura(pdf)

        pdf.save()
        return filePath
    except Exception as erro:
        logger.error(f"Erro ao criar termo de integração: {erro}")
        return None


def add_linhas_dados_colab(pdf):
    pdf.rect(mm2pt(5), mm2pt(165), mm2pt(287), mm2pt(10))

    pdf.rect(mm2pt(5), mm2pt(165), mm2pt(80), mm2pt(10))
    pdf.rect(mm2pt(5), mm2pt(165), mm2pt(140), mm2pt(10))
    pdf.rect(mm2pt(5), mm2pt(165), mm2pt(190), mm2pt(10))
    pdf.rect(mm2pt(5), mm2pt(165), mm2pt(240), mm2pt(10))


def add_dados_colab(dadosColab, pdf):
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(mm2pt(6), mm2pt(166), "Nome: ")
    pdf.drawString(mm2pt(86), mm2pt(166), "Função: ")
    pdf.drawString(mm2pt(145), mm2pt(166), "Setor: ")
    pdf.drawString(mm2pt(196), mm2pt(166), "Loja: ")
    pdf.drawString(mm2pt(245), mm2pt(166), "CBO: ")

    pdf.setFont("Helvetica", 11)
    pdf.drawString(mm2pt(20), mm2pt(166), dadosColab["nome"])
    pdf.drawString(mm2pt(102), mm2pt(166), dadosColab["cargo"])
    pdf.drawString(mm2pt(157), mm2pt(166), dadosColab["setor"])
    pdf.drawString(mm2pt(206), mm2pt(166), nome_loja(int(dadosColab["nroempresa"])))


def add_header(pdf):
    pdf.rect(mm2pt(5), mm2pt(175), mm2pt(287), mm2pt(30))
    pdf.drawImage(
        "./project/controle_uni/termo/logo.png",
        mm2pt(5),
        mm2pt(175),
        width=mm2pt(40),
        height=mm2pt(30),
    )

    pdf.rect(mm2pt(5), mm2pt(175), mm2pt(40), mm2pt(30))
    pdf.setFont("Helvetica-Bold", 19)
    pdf.drawString(mm2pt(80), mm2pt(198), "NR01- NR18")
    pdf.drawString(mm2pt(65), mm2pt(190), "Treinamento de Integração")
    pdf.drawString(mm2pt(69), mm2pt(182), "Segurança do Trabalho")

    pdf.rect(mm2pt(157), mm2pt(175), mm2pt(90), mm2pt(15))
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(mm2pt(160), mm2pt(199), "Elaborado: ")
    pdf.drawString(mm2pt(160), mm2pt(192), "Leonardo Camacho")
    pdf.drawString(mm2pt(160), mm2pt(185), "Revisao: ")
    pdf.drawString(mm2pt(160), mm2pt(179), f"{data_atual()} ")

    pdf.rect(mm2pt(157), mm2pt(175), mm2pt(50), mm2pt(30))
    pdf.rect(mm2pt(247), mm2pt(175), mm2pt(45), mm2pt(30))
    pdf.drawString(mm2pt(215), mm2pt(195), f"Ano: {data_atual()[6:]}")
    pdf.drawString(mm2pt(215), mm2pt(180), "Pagina: 1/1")

    pdf.drawImage(
        "st.png", mm2pt(250), mm2pt(175), width=mm2pt(32), height=mm2pt(30), mask="auto"
    )


def add_termo(dadosColab, pdf, styles):
    primeiro = Paragraph(
        f"""Eu  {dadosColab["nome"]}  , CPF  {dadosColab["cpf"]}  conforme preceitua a Lei nº 6.514 de 22 de dezembro de 1977 e a Portaria 3214 de 08 de junho de 1978 - Norma Regulamentadora  01 item 1.7 e 18, item 18.28,1, declaro ter recebido da Empresa Sociedade Hípica Paulista. antes de iniciar minhas atividades, todos os treinamentos necessários para executá-la de forma segura. O treinamento teve a carga horária de 02 (duas) horas.""",
        styles["Normal"],
        encoding="utf-8",
    )
    primeiro.wrapOn(pdf, mm2pt(274), mm2pt(20))
    primeiro.drawOn(pdf, mm2pt(12), mm2pt(145))

    styles["Normal"].fontName = "Helvetica-Bold"
    segundo = Paragraph(
        """Os assuntos abordados foram:""",
        styles["Normal"],
        encoding="utf-8",
    )
    segundo.wrapOn(pdf, mm2pt(267), mm2pt(20))
    segundo.drawOn(pdf, mm2pt(12), mm2pt(140))

    styles["Normal"].fontName = "Helvetica"
    textObjetc = pdf.beginText(mm2pt(30), mm2pt(135))
    textObjetc.textLines(
        f"""
            Programas de segurança do Trabalho e saúde ocupacional
            Condições sobre o meio ambiente do trabalho;
            PAE - Plano de Atendimento à Emergência e procedimento de Comunicação em caso de emergência:
            Equipamento de proteção coletiva e individual;
            A importância do DSS – Diálogo Semanal de Segurança, Acidente do trabalho – aspecto legal e prevencionista;
            CIPA – Comissão Interna de Prevenção de Acidentes;
            Trabalho específicos, que citam documentos de referência:
            1. Espaço confinado – Placas de Sinalização;
            2. Câmara frigorificas
            3. Trabalho em Altura
            4. Solda
            Processo de lavagem de japona
            Riscos correspondentes à função de :     {dadosColab["cargo"]}   na Ordem de serviço.
            Limpeza, organização e higiene ocupacional;
            Ato inseguro e Condição insegura 
            Aspectos de seg. para trabalhos Forno;
            Segurança em instalações e serviços em eletricidade (habilitação, qualificação, capacitação e autorização dos trabalhadores);
            Noções básicas de combate a principio de Incêndio, Inflamáveis;
            Aspecto e impacto ambiental, Coleta seletiva;
            Manuseio e comportamento quando da execução próximo a cargas suspensas;                                                              
        """
    )
    pdf.drawText(textObjetc)


def add_assinatura(pdf):
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(mm2pt(40), mm2pt(10), "Assinatura do(a) funcionário(a): ")
    pdf.drawString(
        mm2pt(20),
        mm2pt(15),
        "________________________________________________",
    )
    pdf.drawString(mm2pt(190), mm2pt(10), "Assinatura do Tecnico em Segurança: ")
    pdf.drawString(
        mm2pt(170),
        mm2pt(15),
        "_______________________________________________",
    )
    pdf.drawString(mm2pt(130), mm2pt(7), f"São Paulo, {data_atual()}")


def nome_loja(numLoja):
    lojas = {
        1: "Matriz",
        2: "Isabel Dias",
        3: "Manaias",
        5: "José Zappi",
        6: "Heras",
        7: "Azevedo Soares",
        60: "Baia Grande",
    }
    return lojas[numLoja]


def data_atual():
    from datetime import datetime

    data = datetime.now()
    return data.strftime("%d/%m/%Y")
