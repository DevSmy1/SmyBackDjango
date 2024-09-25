import os
import django
from django.apps import apps

# Configurar o ambiente Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from project.intranet.models import (  # noqa: E402
    SmyUsuario as Usuario,
)  # Importar o modelo de usuário do projeto

from project.controle_uni.models import (  # noqa: E402
    TsmyEuColaboradores,
)


def migrar_usuarios():
    models = apps.get_models()
    for model in models:
        if "controle_uni" in model.__module__:
            model_records = model.objects.all()
            for record in model_records:
                if hasattr(record, "usuarioincl"):
                    if record.usuarioincl:
                        user_create = Usuario.objects.filter(
                            login=record.usuarioincl.login.upper()
                        ).first()
                        record.usuario_criacao = user_create

                if hasattr(record, "usuarioalt"):
                    if record.usuarioalt:
                        user_update = Usuario.objects.filter(
                            login=record.usuarioalt.login.upper()
                        ).first()
                        record.usuario_alteracao = user_update

                if hasattr(record, "dt_inclusao"):
                    if record.dt_inclusao:
                        record.data_criacao = record.dt_inclusao

                if hasattr(record, "dt_alteracao"):
                    if record.dt_alteracao:
                        record.data_alteracao = record.dt_alteracao
                record.save()
            print(f"Modelo {model.__name__} migrado com sucesso!")


def migrar_usuarios_colab():
    colabs = TsmyEuColaboradores.objects.all()
    for colab in colabs:
        user_create = Usuario.objects.filter(
            login=colab.usuarioincl.login.upper()
        ).first()
        if colab.usuarioalt:
            user_update = Usuario.objects.filter(
                login=colab.usuarioalt.login.upper()
            ).first()
        colab.usuario_criacao = user_create
        colab.usuario_alteracao = user_update
        colab.save()


if __name__ == "__main__":
    migrar_usuarios()
