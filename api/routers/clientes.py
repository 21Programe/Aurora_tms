from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.deps import get_db
from schemas.cliente import ClienteCreate, ClienteOut
from services.cliente_service import ClienteService

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("", response_model=List[ClienteOut])
def listar_clientes(db: Session = Depends(get_db)):
    return ClienteService.listar(db)


@router.post("", response_model=ClienteOut, status_code=201)
def criar_cliente(payload: ClienteCreate, db: Session = Depends(get_db)):
    try:
        return ClienteService.criar(
            db,
            payload.nome,
            payload.documento,
            payload.cidade or "",
            payload.contato or "",
            payload.email or "",
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))