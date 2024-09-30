# Caminho
from project.setrab.api.api_setrab import CAMINHO_BASE as CAMINHO_BASE_SETRAB

# Router
from project.setrab.api.api_setrab import router as setrabRouter


routes = [
    (CAMINHO_BASE_SETRAB, setrabRouter, ["Importações"]),
]
