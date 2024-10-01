from ninja import NinjaAPI
from ninja.security import APIKeyHeader

# Router
from project.barcode.api import router as barcodeRouter
from project.controle_uni.route import routes as controleUniRoutes
from project.c5.route import routes as c5Routes
from project.setrab.route import routes as setrabRoutes

from project.intranet.models import SmyUsuario, TsmyIntranetusuario


class Unauthorized(Exception):
    pass


class GlobalAuth(APIKeyHeader):
    param_name = ".AuthCookie"

    def authenticate(self, request, key):
        if key is None:
            raise Unauthorized("Não foi possível auntenticar o usuário")
        # login = TsmyIntranetusuario.objects.filter(login=key).first()
        login = SmyUsuario.objects.filter(login=key.upper()).first()
        if login:
            return login


api = NinjaAPI(auth=GlobalAuth())

routes = []
routes += c5Routes
routes += controleUniRoutes
routes += setrabRoutes

for route in routes:
    api.add_router(route[0], route[1], tags=route[2])


@api.exception_handler(Unauthorized)
def nao_autorizado(request, exc):
    return api.create_response(request, {"message": str(exc)}, status=401)


# Api V2
apiV2 = NinjaAPI(version="2.0.0")
apiV2.add_router("/barcode", barcodeRouter, tags=["Barcode"])
