from typing import Optional
from pydantic import BaseModel, ConfigDict


class MotoristaCreate(BaseModel):
    nome: str
    cpf: str
    cnh: str
    categoria_cnh: str
    telefone: Optional[str] = None


class MotoristaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    cpf: str
    cnh: str
    categoria_cnh: str
    telefone: Optional[str] = None
    status: str