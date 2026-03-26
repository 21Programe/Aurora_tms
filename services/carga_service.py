from sqlalchemy.orm import Session
from aurora_tms_mvp import CargaService as LegacyCargaService

class CargaService:
    @staticmethod
    def criar(db: Session, descricao: str, peso_kg: float, valor_nf: float, cliente_id: int):
        return LegacyCargaService.criar(db, descricao, peso_kg, valor_nf, cliente_id)

    @staticmethod
    def listar(db: Session):
        return LegacyCargaService.listar(db)

    @staticmethod
    def buscar_por_id(db: Session, carga_id: int):
        return LegacyCargaService.buscar_por_id(db, carga_id)

    @staticmethod
    def embarcar(db: Session, carga_id: int, viagem_id: int, caminhao_id: int):
        return LegacyCargaService.embarcar(db, carga_id, viagem_id, caminhao_id)

    @staticmethod
    def registrar_entrega(db: Session, carga_id: int):
        return LegacyCargaService.registrar_entrega(db, carga_id)
