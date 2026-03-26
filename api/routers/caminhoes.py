from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.deps import get_db
from schemas.caminhao import CaminhaoCreate, CaminhaoOut
from services.caminhao_service import CaminhaoService

router = APIRouter(prefix="/caminhoes", tags=["Frota"])


@router.get("", response_model=List[CaminhaoOut])
def listar_caminhoes(db: Session = Depends(get_db)):
    return CaminhaoService.listar(db)


@router.post("", response_model=CaminhaoOut, status_code=201)
def criar_caminhao(payload: CaminhaoCreate, db: Session = Depends(get_db)):
    try:
        return CaminhaoService.criar(
            db,
            payload.placa,
            payload.tipo,
            payload.capacidade_max_kg,
            payload.marca or "",
            payload.modelo or "",
            payload.ano,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))