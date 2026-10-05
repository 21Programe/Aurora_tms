from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from legacy.aurora_tms_mvp import CargaService as LegacyCargaService


class CargaService:
    """Facade da camada de domínio legada para a API modular."""

    @staticmethod
    def criar(
        db: Session,
        nota_fiscal: str,
        descricao: str,
        peso_kg: float,
        valor_mercadoria: float,
        cidade_origem: str,
        cidade_destino: str,
        prazo_entrega: Optional[datetime] = None,
        cliente_id: Optional[int] = None,
        observacoes: str = "",
    ):
        return LegacyCargaService.criar(
            db,
            nota_fiscal,
            descricao,
            peso_kg,
            valor_mercadoria,
            cidade_origem,
            cidade_destino,
            prazo_entrega,
            cliente_id,
            observacoes,
        )

    @staticmethod
    def listar(db: Session):
        return LegacyCargaService.listar(db)

    @staticmethod
    def buscar_por_id(db: Session, carga_id: int):
        return LegacyCargaService.buscar_por_id(db, carga_id)

    @staticmethod
    def reservar_para_viagem(db: Session, carga_id: int, viagem_id: int):
        return LegacyCargaService.reservar_para_viagem(db, carga_id, viagem_id)

    @staticmethod
    def embarcar_carga(db: Session, carga_id: int):
        return LegacyCargaService.embarcar_carga(db, carga_id)

    @staticmethod
    def entregar_carga(db: Session, carga_id: int):
        return LegacyCargaService.entregar_carga(db, carga_id)

    @staticmethod
    def peso_total_por_caminhao(db: Session, caminhao_id: int):
        return LegacyCargaService.peso_total_por_caminhao(db, caminhao_id)
