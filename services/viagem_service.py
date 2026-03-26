from sqlalchemy.orm import Session
from aurora_tms_mvp import ViagemService as LegacyViagemService


class ViagemService:
    @staticmethod
    def criar(
        db: Session,
        origem: str,
        destino: str,
        distancia_km: float,
        caminhao_id: int,
        motorista_id: int,
        data_saida_prevista=None,
        data_chegada_prevista=None,
        observacoes: str = "",
    ):
        return LegacyViagemService.criar(
            db,
            origem,
            destino,
            distancia_km,
            caminhao_id,
            motorista_id,
            data_saida_prevista,
            data_chegada_prevista,
            observacoes,
        )

    @staticmethod
    def listar(db: Session):
        return LegacyViagemService.listar(db)

    @staticmethod
    def buscar_por_id(db: Session, viagem_id: int):
        return LegacyViagemService.buscar_por_id(db, viagem_id)

    @staticmethod
    def iniciar(db: Session, viagem_id: int):
        return LegacyViagemService.iniciar(db, viagem_id)

    @staticmethod
    def finalizar(db: Session, viagem_id: int):
        return LegacyViagemService.finalizar(db, viagem_id)

    @staticmethod
    def cancelar(db: Session, viagem_id: int, motivo: str):
        return LegacyViagemService.cancelar(db, viagem_id, motivo)