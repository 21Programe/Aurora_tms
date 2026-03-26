from sqlalchemy.orm import Session
from oraculo_ia import PastorSalmo23


class OraculoService:
    @staticmethod
    def gerar_plano_tatico(db: Session):
        return PastorSalmo23.gerar_plano_tatico(db)

    @staticmethod
    def executar_plano_tatico(db: Session, origem_padrao: str = "Pátio Central", iniciar_viagens: bool = False):
        return PastorSalmo23.executar_plano_tatico(
            db=db,
            origem_padrao=origem_padrao,
            iniciar_viagens=iniciar_viagens,
        )