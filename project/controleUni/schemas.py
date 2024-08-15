from ninja import Field, Schema
from datetime import date, datetime

from project.controleUni.models import TsmyEuCargoAgrup


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
    genero: str
    dt_adm: date | None = None
    dt_desligamento: date | None = None
    dt_experiencia: date | None = None
    cod_funcao_id: int
    nome_funcao: str = Field(alias="cod_funcao.funcao")
    cod_funcao_nova_id: int | None = None
    nome_funcao_nova: str | None = Field(None, alias="cod_funcao_nova.funcao")
    cod_funcao_ant_id: int | None = None
    nome_funcao_ant: str | None = Field(None, alias="cod_funcao_ant.funcao")


class SchemaColabOutMin(Schema):
    id_colab: int
    matricula: int
    nome: str
    nroempresa: int
    cod_funcao: int | None = Field(None, alias="cod_funcao_id")


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
    descricao: str | None = Field(None, alias="valor.descricao")
    quantidade: int


class SchemaRelAgrupadorCargoin(Schema):
    valor: int
    quantidade: int


# Produtos
class SchemaProdutoOut(Schema):
    seqproduto: int
    descreduzida: str


# Observação
class SchemaObservaçãoOut(Schema):
    id_observacao: int
    observacao: str


class SchemaObservaçãoIn(Schema):
    observacao: str


# Ficha
class SchemaFichaOut(Schema):
    id_ficha: int
    id_troca: int | None = None
    seq_produto: int = Field(alias="seqproduto_id")
    agrupador: int | None = Field(
        None, alias="seqproduto.seqfamilia.mapfamatributo.valor"
    )
    nome_produto: str = Field(alias="seqproduto.descreduzida")
    sit_produto: str
    recibo_uni: int | None = Field(None, alias="reciboUni_id")
    recibo_epi: int | None = Field(None, alias="reciboEpi_id")


class SchemaFichaIn(Schema):
    seqproduto: int
    matricula: int | None = None
    cpf: int | None = None
    nro_ca: int | None = None
    dt_validade: date | None = None
    id_observacao: int | None = None
    sit_produto: str
    nro_empresa_orig: int
    nro_empresa_dest: int
