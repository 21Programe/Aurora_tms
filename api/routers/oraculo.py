from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.deps import get_db
from schemas.oraculo import ExecutarPlanoPayload
from services.oraculo_service import OraculoService

router = APIRouter(prefix="/oraculo", tags=["Inteligência Artificial"])


@router.get("/plano-tatico")
def gerar_plano_tatico(db: Session = Depends(get_db)):
    try:
        resultado = OraculoService.gerar_plano_tatico(db)
        if resultado.get("status") == "erro":
            raise HTTPException(status_code=400, detail=resultado.get("mensagem"))
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/executar-plano")
def executar_plano(payload: ExecutarPlanoPayload, db: Session = Depends(get_db)):
    try:
        resultado = OraculoService.executar_plano_tatico(
            db=db,
            origem_padrao=payload.origem_padrao,
            iniciar_viagens=payload.iniciar_viagens,
        )
        if resultado.get("status") == "erro":
            raise HTTPException(status_code=400, detail=resultado.get("mensagem"))
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))