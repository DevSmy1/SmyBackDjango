import pandas as pd

import os
import django
from django.apps import apps


# Configurar o ambiente Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()
from project.setrab.models import SetrabCargoRel, SetrabEmpresaRel, SetrabSetorRel  # noqa: E402
from project.intranet.models import SmyUsuario  # noqa: E402


def sincronizar_empresa():
    usuario = SmyUsuario.objects.filter(login="gabriel.oliveira".upper()).first()
    user_data = {
        "usuario_criacao": usuario,
        "usuario_alteracao": usuario,
    }
    empresas = [
        {
            "id_empresa": 1,
            "id_empresa_setrab": 245,
        },
        {
            "id_empresa": 2,
            "id_empresa_setrab": 264,
        },
        {
            "id_empresa": 3,
            "id_empresa_setrab": 248,
        },
        {
            "id_empresa": 5,
            "id_empresa_setrab": 265,
        },
        {
            "id_empresa": 6,
            "id_empresa_setrab": 263,
        },
        {
            "id_empresa": 7,
            "id_empresa_setrab": 252,
        },
        {
            "id_empresa": 60,
            "id_empresa_setrab": 260,
        },
    ]

    for empresa in empresas:
        # print(empresa["id_empresa"])
        SetrabEmpresaRel.objects.update_or_create(
            id_empresa=empresa["id_empresa"],
            defaults={"id_empresa_setrab": empresa["id_empresa_setrab"], **user_data},
        )


sincronizar_empresa()
