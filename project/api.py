from ninja import NinjaAPI
from ninja.security import APIKeyHeader

# Base paths imports
from project.controleUni.api.apiCargo import (
    CAMINHO_BASE as CAMINHO_BASE_CARGO,
)
from project.controleUni.api.apiColab import (
    CAMINHO_BASE as CAMINHO_BASE_COLAB,
)
from project.controleUni.api.apiAgrupador import (
    CAMINHO_BASE as CAMINHO_BASE_AGRUPADOR,
)
from project.c5.api.apiMapFamAtributo import (
    CAMINHO_BASE as CAMINHO_BASE_ATRIBUTO_C5,
)
from project.c5.api.apiEmpresa import (
    CAMINHO_BASE as CAMINHO_BASE_EMPRESA_C5,
)
from project.controleUni.api.apiObservação import (
    CAMINHO_BASE as CAMINHO_BASE_OBSERVACAO,
)
from project.controleUni.api.apiFicha import (
    CAMINHO_BASE as CAMINHO_BASE_FICHA,
)

# Router imports
from project.barcode.api import router as barcodeRouter
from project.controleUni.api.apiCargo import router as cargoRouter
from project.controleUni.api.apiColab import router as colabRouter
from project.c5.api.apiMapFamAtributo import router as mapFamAtributoRouter
from project.c5.api.apiEmpresa import router as empresaRouter
from project.controleUni.api.apiAgrupador import router as agrupadorRouter
from project.controleUni.api.apiObservação import router as observacaoRouter
from project.controleUni.api.apiFicha import router as fichaRouter

from project.intranet.models import TsmyIntranetusuario


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
api.add_router(CAMINHO_BASE_COLAB, colabRouter, tags=["Colaborador"])
api.add_router(CAMINHO_BASE_AGRUPADOR, agrupadorRouter, tags=["Agrupador"])
api.add_router(CAMINHO_BASE_ATRIBUTO_C5, mapFamAtributoRouter, tags=["Agrupador"])
api.add_router(CAMINHO_BASE_OBSERVACAO, observacaoRouter, tags=["Observação"])
api.add_router(CAMINHO_BASE_EMPRESA_C5, empresaRouter, tags=["Empresa"])
api.add_router(CAMINHO_BASE_FICHA, fichaRouter, tags=["Fichas"])


@api.exception_handler(Unauthorized)
def nao_autorizado(request, exc):
    return api.create_response(request, {"message": str(exc)}, status=401)


# Api V2
apiV2 = NinjaAPI(version="2.0.0")
apiV2.add_router("/barcode", barcodeRouter, tags=["Barcode"])
