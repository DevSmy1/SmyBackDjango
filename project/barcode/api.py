import os

from icecream import ic  # noqa
from ninja import Router, UploadedFile
from pyzbar.pyzbar import decode, ZBarSymbol
from PIL import Image, ImageEnhance

from .schemas import Error, Success

router = Router()


@router.post(
    "/readBarcode",
    response={200: Success, 404: Error},
)
def readBarcode(request, barcode: UploadedFile):
    try:
        # salvar imagem
        with open("barcode.jpg", "wb") as f:
            f.write(barcode.read())
        # ler imagem
        imagem = Image.open("barcode.jpg")
        detectedBarcodes = getBarcodeInImage(imagem)
        if detectedBarcodes is None:
            return 404, {"message": "Nenhum código de barras detectado"}
        result = getDataDecodeBar(detectedBarcodes)
        if result is None or result == "":
            return 404, {"message": "Nenhum código de barras detectado"}
        # deletar imagem
        os.remove("barcode.jpg")
        return 200, {"message": result}
    except Exception as e:
        return 404, {"message": str(e)}


def getBarcodeInImage(imagem):
    try:
        MAX_TRIES = 3  # Defina o número máximo de tentativas aqui
        tries = 0
        detectedBarcodes = decode(imagem, symbols=[ZBarSymbol.CODE128])
        while not detectedBarcodes and tries < MAX_TRIES:
            # Redimensionar a imagem
            imagem = imagem.resize((imagem.width * 2, imagem.height * 2), Image.LANCZOS)  # type: ignore

            # Converter para escala de cinza
            imagem = imagem.convert("L")

            # Ajustar o contraste
            enhancer = ImageEnhance.Contrast(imagem)
            imagem = enhancer.enhance(1.5)

            detectedBarcodes = decode(imagem, symbols=[ZBarSymbol.CODE128])
            tries += 1
        if not detectedBarcodes:
            return None
        return detectedBarcodes
    except Exception as e:
        return None


def getDataDecodeBar(detectedBarcodes):
    data = ""
    for barcode in detectedBarcodes:
        if barcode.data != "":
            data = barcode.data.decode("utf-8")
        if barcode.data == "":
            data = None
    return data
