from typing import Optional
from pydantic import BaseModel, ConfigDict


class ClienteCreate(BaseModel):
    nome: str
    documento: str
    cidade: Optional[str] = None
    contato: Optional[str] = None
    email: Optional[str] = None


class ClienteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    documento: str
    cidade: Optional[str] = None
    contato: Optional[str] = None
    email: Optional[str] = None