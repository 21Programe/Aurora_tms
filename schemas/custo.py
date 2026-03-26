from pydantic import BaseModel, ConfigDict, Field


class CustoViagemCreate(BaseModel):
    viagem_id: int
    tipo: str
    descricao: str
    valor: float = Field(..., ge=0)


class CustoViagemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    viagem_id: int
    tipo: str
    descricao: str
    valor: float