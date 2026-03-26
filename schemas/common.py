from pydantic import BaseModel


class MessageOut(BaseModel):
    mensagem: str