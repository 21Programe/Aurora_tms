from sqlalchemy.orm import Session
from aurora_tms_mvp import CaminhaoService as LegacyCaminhaoService


class CaminhaoService:
    @staticmethod
    def criar(db: Session, placa: str, tipo: str, capacidade_max_kg: float, marca: str = "", modelo: str = "", ano=None):
        return LegacyCaminhaoService.criar(db, placa, tipo, capacidade_max_kg, marca, modelo, ano)

    @staticmethod
    def listar(db: Session):
        return LegacyCaminhaoService.listar(db)

    @staticmethod
    def buscar_por_id(db: Session, caminhao_id: int):
        return LegacyCaminhaoService.buscar_por_id(db, caminhao_id)

    @staticmethod
    def atualizar_status(db: Session, caminhao_id: int, novo_status: str):
        return LegacyCaminhaoService.atualizar_status(db, caminhao_id, novo_status)