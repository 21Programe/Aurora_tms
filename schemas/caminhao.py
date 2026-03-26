from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class CaminhaoCreate(BaseModel):
    placa: str = Field(..., min_length=7, max_length=10)
    tipo: str
    capacidade_max_kg: float = Field(..., gt=0)
    marca: Optional[str] = None
    modelo: Optional[str] = None
    ano: Optional[int] = None


class CaminhaoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    placa: str
    tipo: str
    capacidade_max_kg: float
    marca: Optional[str] = None
    modelo: Optional[str] = None
    ano: Optional[int] = None
    status: str