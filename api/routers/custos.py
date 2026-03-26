from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.deps import get_db
from schemas.custo import CustoViagemCreate, CustoViagemOut
from services.custo_viagem_service import CustoViagemService

router = APIRouter(prefix="/custos", tags=["Custos"])


@router.get("/viagem/{viagem_id}", response_model=List[CustoViagemOut])
def listar_custos_viagem(viagem_id: int, db: Session = Depends(get_db)):
    try:
        return CustoViagemService.listar_por_viagem(db, viagem_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("", response_model=CustoViagemOut, status_code=201)
def adicionar_custo(payload: CustoViagemCreate, db: Session = Depends(get_db)):
    try:
        return CustoViagemService.adicionar(
            db,
            payload.viagem_id,
            payload.tipo,
            payload.descricao,
            payload.valor,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))