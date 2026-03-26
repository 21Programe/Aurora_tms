from pydantic import BaseModel


class ExecutarPlanoPayload(BaseModel):
    origem_padrao: str = "Pátio Central"
    iniciar_viagens: bool = False