from datetime import date, datetime
from typing import List
from ninja import Field, Schema


class ImportacaoSchema(Schema):
    nome_arquivo: str
    mes: str
    usuario_criacao: str = Field(alias="usuario_criacao.nome")
    status: str
    resposta_servidor: str
    data_criacao: datetime


class BaseImportacaoSchema(Schema):
    id_empresa: int
    id_funcionario: str
    nome: str
    id_empresa_rh: int
    erro_sistema: str | None = None  # type: ignore


class AdmissaoSchema(BaseImportacaoSchema):
    data_admissao: date
    data_nascimento: date
    sexo: str
    id_cargo: int
    id_setor: int
    possui_vinculo: str


class ConfirmarAdmissaoSchema(Schema):
    dados: List[AdmissaoSchema]
    nome_arquivo: str
    mes: date


class DemissaoSchema(BaseImportacaoSchema):
    data_demissao: date


class ConfirmarDemissaoSchema(Schema):
    dados: List[DemissaoSchema]
    nome_arquivo: str
    mes: date


class MudFuncaoSchema(BaseImportacaoSchema):
    id_cargo: int
    id_setor: int
    data_mud_func: date


class ConfirmarMudFuncaoSchema(Schema):
    dados: List[MudFuncaoSchema]
    nome_arquivo: str
    mes: date


class TransferenciaSchema(BaseImportacaoSchema):
    id_empresa_destino: int
    id_cargo: int
    id_setor: int
    data_transferencia: date


class ConfirmarTransferenciaSchema(Schema):
    dados: List[TransferenciaSchema]
    nome_arquivo: str
    mes: date
