from ninja import NinjaAPI
from ninja.security import APIKeyHeader

from project.barcode.api import router as barcodeRouter
from project.intranet.models import TsmyIntranetusuario
from project.controleUni.api.apiCargo import (
    router as cargoRouter,
    CAMINHO_BASE as CAMINHO_BASE_CARGO,
)


class Unauthorized(Exception):
    pass


class GlobalAuth(APIKeyHeader):
    param_name = ".AuthCookie"

    def authenticate(self, request, key):
        if key is None:
            raise Unauthorized("Não foi possível auntenticar o usuário")
        login = TsmyIntranetusuario.objects.filter(login=key).first()
        if login:
            return login


api = NinjaAPI(auth=GlobalAuth())
api.add_router(CAMINHO_BASE_CARGO, cargoRouter, tags=["Cargo"])


@api.exception_handler(Unauthorized)
def nao_autorizado(request, exc):
    return api.create_response(request, {"message": str(exc)}, status=401)


# Api V2
apiV2 = NinjaAPI(version="2.0.0")
apiV2.add_router("/barcode", barcodeRouter, tags=["Barcode"])
