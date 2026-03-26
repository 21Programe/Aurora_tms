from sqlalchemy.orm import Session
from aurora_tms_mvp import MotoristaService as LegacyMotoristaService


class MotoristaService:
    @staticmethod
    def criar(db: Session, nome: str, cpf: str, cnh: str, categoria_cnh: str, telefone: str = ""):
        return LegacyMotoristaService.criar(db, nome, cpf, cnh, categoria_cnh, telefone)

    @staticmethod
    def listar(db: Session):
        return LegacyMotoristaService.listar(db)

    @staticmethod
    def buscar_por_id(db: Session, motorista_id: int):
        return LegacyMotoristaService.buscar_por_id(db, motorista_id)

    @staticmethod
    def atualizar_status(db: Session, motorista_id: int, novo_status: str):
        return LegacyMotoristaService.atualizar_status(db, motorista_id, novo_status)