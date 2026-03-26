from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ViagemCreate(BaseModel):
    origem: str
    destino: str
    distancia_km: float = Field(..., ge=0)
    caminhao_id: int
    motorista_id: int
    data_saida_prevista: Optional[datetime] = None
    data_chegada_prevista: Optional[datetime] = None
    observacoes: Optional[str] = None


class ViagemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    origem: str
    destino: str
    distancia_km: float
    status: str
    caminhao_id: int
    motorista_id: int
    data_saida_prevista: Optional[datetime] = None
    data_saida_real: Optional[datetime] = None
    data_chegada_prevista: Optional[datetime] = None
    data_chegada_real: Optional[datetime] = None
    observacoes: Optional[str] = None