from ninja import Field, Schema


class SchemaMapFamatributo(Schema):
    seqfamilia: int
    nomefamilia: str = Field(None, alias="seqfamilia__familia")
    valor: str

    @staticmethod
    def resolve_seqfamilia__familia(obj):
        return obj["seqfamilia__familia"].replace("(CONS) ", "")
