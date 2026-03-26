from sqlalchemy.orm import Session
from aurora_tms_mvp import RelatorioService as LegacyRelatorioService

class RelatorioService:
    @staticmethod
    def gerar_relatorio(db: Session, tipo: str, parametros: dict):
        return LegacyRelatorioService.gerar_relatorio(db, tipo, parametros)
