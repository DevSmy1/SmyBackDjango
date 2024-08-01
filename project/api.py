# Django Imports
from django.contrib import admin
from django.urls import path


from ninja import NinjaAPI
from ninja.security import APIKeyHeader

from project.barcode.api import router as barcodeRouter

# class Unauthorized(Exception):
#     pass

# class GlobalAuth(APIKeyHeader):
#     param_name = ".AuthCookie"

#     def authenticate(self, request, key):
#         if key is None:
#             raise Unauthorized("Não foi possível auntenticar o usuário")
#         login = TsmyIntranetusuario.objects.filter(login=key).first()
#         if login:
#             return login

# api = NinjaAPI(auth=GlobalAuth(), version="2.0.0")
apiV2 = NinjaAPI(version="2.0.0")

apiV2.add_router("/barcode", barcodeRouter, tags=["Barcode"])


api = NinjaAPI()
