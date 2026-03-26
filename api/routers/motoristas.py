from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.deps import get_db
from schemas.motorista import MotoristaCreate, MotoristaOut
from services.motorista_service import MotoristaService

router = APIRouter(prefix="/motoristas", tags=["Motoristas"])


@router.get("", response_model=List[MotoristaOut])
def listar_motoristas(db: Session = Depends(get_db)):
    return MotoristaService.listar(db)


@router.post("", response_model=MotoristaOut, status_code=201)
def criar_motorista(payload: MotoristaCreate, db: Session = Depends(get_db)):
    try:
        return MotoristaService.criar(
            db,
            payload.nome,
            payload.cpf,
            payload.cnh,
            payload.categoria_cnh,
            payload.telefone or "",
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))