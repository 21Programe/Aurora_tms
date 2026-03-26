from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.deps import get_db
from schemas.carga import CargaCreate, CargaOut, ReservaCargaPayload
from services.carga_service import CargaService

router = APIRouter(prefix="/cargas", tags=["Cargas"])


@router.get("", response_model=List[CargaOut])
def listar_cargas(db: Session = Depends(get_db)):
    return CargaService.listar(db)


@router.post("", response_model=CargaOut, status_code=201)
def criar_carga(payload: CargaCreate, db: Session = Depends(get_db)):
    try:
        return CargaService.criar(
            db,
            payload.nota_fiscal,
            payload.descricao,
            payload.peso_kg,
            payload.valor_mercadoria,
            payload.cidade_origem,
            payload.cidade_destino,
            payload.prazo_entrega,
            payload.cliente_id,
            payload.observacoes or "",
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/reservar", response_model=CargaOut)
def reservar_carga(payload: ReservaCargaPayload, db: Session = Depends(get_db)):
    try:
        return CargaService.reservar_para_viagem(db, payload.carga_id, payload.viagem_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{carga_id}/embarcar", response_model=CargaOut)
def embarcar_carga(carga_id: int, db: Session = Depends(get_db)):
    try:
        return CargaService.embarcar_carga(db, carga_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{carga_id}/entregar", response_model=CargaOut)
def entregar_carga(carga_id: int, db: Session = Depends(get_db)):
    try:
        return CargaService.entregar_carga(db, carga_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))