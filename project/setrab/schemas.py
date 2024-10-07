from datetime import date
from typing import List
from ninja import Schema


class ImportacaoSchema(Schema):
    id: int
    nome_arquivo: str
    mes: str
    usuario: str
    status: str
    resposta_servidor: str
    data_hora: str


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
    mes: str


class DemissaoSchema(BaseImportacaoSchema):
    data_demissao: date


class ConfirmarDemissaoSchema(Schema):
    dados: List[DemissaoSchema]
    nome_arquivo: str
    mes: str


class MudFuncaoSchema(BaseImportacaoSchema):
    id_cargo: int
    id_setor: int
    data_mud_func: date


class ConfirmarMudFuncaoSchema(Schema):
    dados: List[MudFuncaoSchema]
    nome_arquivo: str
    mes: str


class TransferenciaSchema(BaseImportacaoSchema):
    id_empresa_destino: int
    id_cargo: int
    id_setor: int
    data_transferencia: date


class ConfirmarTransferenciaSchema(Schema):
    dados: List[TransferenciaSchema]
    nome_arquivo: str
    mes: str
