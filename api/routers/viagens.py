from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from api.deps import get_db
from schemas.viagem import ViagemCreate, ViagemOut
from services.viagem_service import ViagemService

router = APIRouter(prefix="/viagens", tags=["Viagens"])


@router.get("", response_model=List[ViagemOut])
def listar_viagens(db: Session = Depends(get_db)):
    return ViagemService.listar(db)


@router.post("", response_model=ViagemOut, status_code=201)
def criar_viagem(payload: ViagemCreate, db: Session = Depends(get_db)):
    try:
        return ViagemService.criar(
            db,
            payload.origem,
            payload.destino,
            payload.distancia_km,
            payload.caminhao_id,
            payload.motorista_id,
            payload.data_saida_prevista,
            payload.data_chegada_prevista,
            payload.observacoes or "",
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{viagem_id}/iniciar", response_model=ViagemOut)
def iniciar_viagem(viagem_id: int, db: Session = Depends(get_db)):
    try:
        return ViagemService.iniciar(db, viagem_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{viagem_id}/finalizar", response_model=ViagemOut)
def finalizar_viagem(viagem_id: int, db: Session = Depends(get_db)):
    try:
        return ViagemService.finalizar(db, viagem_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{viagem_id}/cancelar", response_model=ViagemOut)
def cancelar_viagem(
    viagem_id: int,
    motivo: str = Query(..., min_length=3),
    db: Session = Depends(get_db),
):
    try:
        return ViagemService.cancelar(db, viagem_id, motivo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))