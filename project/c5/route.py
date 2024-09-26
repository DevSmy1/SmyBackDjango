from project.c5.api.api_map_fam_atributo import (
    CAMINHO_BASE as CAMINHO_BASE_ATRIBUTO_C5,
)
from project.c5.api.api_empresa import (
    CAMINHO_BASE as CAMINHO_BASE_EMPRESA_C5,
)
from project.c5.api.api_map_fam_atributo import router as mapFamAtributoRouter
from project.c5.api.api_empresa import router as empresaRouter

routes = [
    (CAMINHO_BASE_ATRIBUTO_C5, mapFamAtributoRouter, ["Agrupador"]),
    (CAMINHO_BASE_EMPRESA_C5, empresaRouter, ["Empresa"]),
]
