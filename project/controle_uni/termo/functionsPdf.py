import re

def mm2pt(mm):
    return mm * 2.83464567

def pt2mm(pt):
    return pt * 0.352778

def formatarDinheiro(valor):
    try:
        valor = float(valor)
        valor_formatado = f"R$ {valor:.2f}".replace(".", ",")
        valor_formatado = re.sub(r'(\d{3})(?=\d)', r'\1.', valor_formatado[::-1])
        return valor_formatado[::-1]
    except Exception as erro:
        print(f"Erro: {erro}")
        return None