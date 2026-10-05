from sqlalchemy.orm import Session

from legacy.aurora_tms_mvp import RelatorioService as LegacyRelatorioService


class RelatorioService:
    """Facade dos relatórios para a API modular."""

    @staticmethod
    def dashboard_operacional(db: Session):
        return LegacyRelatorioService.dashboard_operacional(db)

    @staticmethod
    def ocupacao_frota(db: Session):
        return LegacyRelatorioService.ocupacao_frota(db)

    @staticmethod
    def rentabilidade_viagem(db: Session, viagem_id: int):
        return LegacyRelatorioService.rentabilidade_viagem(db, viagem_id)

    @staticmethod
    def alertas_prazo(db: Session):
        return LegacyRelatorioService.alertas_prazo(db)

    @staticmethod
    def ultimos_eventos(db: Session, limite: int = 20):
        return LegacyRelatorioService.ultimos_eventos(db, limite)