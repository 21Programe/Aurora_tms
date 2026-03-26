from sqlalchemy.orm import Session
from aurora_tms_mvp import ClienteService as LegacyClienteService


class ClienteService:
    @staticmethod
    def criar(db: Session, nome: str, documento: str, cidade: str = "", contato: str = "", email: str = ""):
        return LegacyClienteService.criar(db, nome, documento, cidade, contato, email)

    @staticmethod
    def listar(db: Session):
        return LegacyClienteService.listar(db)

    @staticmethod
    def buscar_por_id(db: Session, cliente_id: int):
        return LegacyClienteService.buscar_por_id(db, cliente_id)