from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class CargaCreate(BaseModel):
    nota_fiscal: str
    descricao: str
    peso_kg: float = Field(..., gt=0)
    valor_mercadoria: float = Field(0, ge=0)
    cidade_origem: str
    cidade_destino: str
    prazo_entrega: Optional[datetime] = None
    cliente_id: Optional[int] = None
    observacoes: Optional[str] = None


class CargaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nota_fiscal: str
    descricao: str
    peso_kg: float
    valor_mercadoria: float
    cidade_origem: str
    cidade_destino: str
    status: str
    cliente_id: Optional[int] = None
    caminhao_id: Optional[int] = None
    viagem_id: Optional[int] = None


class ReservaCargaPayload(BaseModel):
    carga_id: int
    viagem_id: int