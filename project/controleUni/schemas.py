from ninja import Field, Schema
from datetime import date, datetime


# Cargo
class SchemaCargo(Schema):
    cod_funcao: int
    funcao: str


# Colab
class SchemaColabOut(Schema):
    id_colab: int
    nroempresa: int
    matricula: int
    cpf: int
    nome: str
    dt_adm: date | None = None
    dt_desligamento: date | None = None
    dt_experiencia: date | None = None
    cod_funcao_id: int
    cod_funcao_nova_id: int | None = None
    cod_funcao_ant_id: int | None = None


class SchemaColabIn(Schema):
    nroempresa: int
    matricula: int
    cpf: int
    nome: str
    dt_adm: date | None
    dt_desligamento: date | None = None
    dt_experiencia: date | None = None
    cod_funcao_id: int
    cod_funcao_nova_id: int | None = None
    cod_funcao_ant_id: int | None = None


# Agrupador
class SchemaAgrupador(Schema):
    codigo: int
    descricao: str


# Rel Agrupador x Cargo
class SchemaRelAgrupadorCargoOut(Schema):
    cod_funcao: int = Field(alias="cod_funcao_id")
    valor: int | None = Field(None, alias="valor_id")
    quantidade: int


class SchemaRelAgrupadorCargoin(Schema):
    valor: int
    quantidade: int
