# Caminho
from project.controle_uni.api.api_cargo import (
    CAMINHO_BASE as CAMINHO_BASE_CARGO,
)
from project.controle_uni.api.api_colab import (
    CAMINHO_BASE as CAMINHO_BASE_COLAB,
)
from project.controle_uni.api.api_agrupador import (
    CAMINHO_BASE as CAMINHO_BASE_AGRUPADOR,
)
from project.controle_uni.api.api_observação import (
    CAMINHO_BASE as CAMINHO_BASE_OBSERVACAO,
)
from project.controle_uni.api.api_ficha import (
    CAMINHO_BASE as CAMINHO_BASE_FICHA,
)
from project.controle_uni.api.api_termo import (
    CAMINHO_BASE as CAMINHO_BASE_TERMO,
)

# Router
from project.controle_uni.api.api_cargo import router as cargoRouter
from project.controle_uni.api.api_colab import router as colabRouter
from project.controle_uni.api.api_agrupador import router as agrupadorRouter
from project.controle_uni.api.api_observação import router as observacaoRouter
from project.controle_uni.api.api_ficha import router as fichaRouter
from project.controle_uni.api.api_ficha_cadastrada import (
    router as fichaCadastradaRouter,
)
from project.controle_uni.api.api_ficha_devolucao import router as fichaDevolucaoRouter
from project.controle_uni.api.api_termo import router as termoRouter

routes = [
    (CAMINHO_BASE_CARGO, cargoRouter, ["Cargo"]),
    (CAMINHO_BASE_COLAB, colabRouter, ["Colaborador"]),
    (CAMINHO_BASE_AGRUPADOR, agrupadorRouter, ["Agrupador"]),
    (CAMINHO_BASE_OBSERVACAO, observacaoRouter, ["Observação"]),
    (CAMINHO_BASE_FICHA, fichaRouter, ["Fichas"]),
    (CAMINHO_BASE_FICHA, fichaCadastradaRouter, ["Fichas Cadastradas"]),
    (CAMINHO_BASE_FICHA, fichaDevolucaoRouter, ["Fichas Devolução"]),
    (CAMINHO_BASE_TERMO, termoRouter, ["Termo"]),
]
