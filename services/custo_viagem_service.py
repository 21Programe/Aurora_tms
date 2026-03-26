from sqlalchemy.orm import Session
from aurora_tms_mvp import CustoViagemService as LegacyCustoViagemService


class CustoViagemService:
    @staticmethod
    def adicionar(db: Session, viagem_id: int, tipo: str, descricao: str, valor: float):
        return LegacyCustoViagemService.adicionar(db, viagem_id, tipo, descricao, valor)

    @staticmethod
    def listar_por_viagem(db: Session, viagem_id: int):
        return LegacyCustoViagemService.listar_por_viagem(db, viagem_id)