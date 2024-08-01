from django.contrib import admin
from django.urls import path

from .api import api, apiV2

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path("api/v2/", apiV2.urls),
]
