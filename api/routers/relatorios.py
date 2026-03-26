from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from api.deps import get_db
from services.relatorio_service import RelatorioService

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])


@router.get("/dashboard")
def obter_dashboard(db: Session = Depends(get_db)):
    try:
        return RelatorioService.dashboard_operacional(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/frota/ocupacao")
def ocupacao_frota(db: Session = Depends(get_db)):
    try:
        dados = RelatorioService.ocupacao_frota(db)
        return [
            {
                "placa": placa,
                "capacidade_max_kg": capacidade,
                "peso_atual_kg": peso_total,
                "ocupacao_pct": ocupacao_pct,
            }
            for placa, capacidade, peso_total, ocupacao_pct in dados
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/viagens/{viagem_id}/rentabilidade")
def rentabilidade_viagem(viagem_id: int, db: Session = Depends(get_db)):
    try:
        return RelatorioService.rentabilidade_viagem(db, viagem_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/cargas/alertas")
def alertas_prazo(db: Session = Depends(get_db)):
    try:
        alertas = RelatorioService.alertas_prazo(db)
        return [
            {
                "id": c.id,
                "nf": c.nota_fiscal,
                "descricao": c.descricao,
                "destino": c.cidade_destino,
                "status": c.status,
                "prazo_entrega": c.prazo_entrega,
            }
            for c in alertas
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/eventos")
def listar_eventos(
    limite: int = Query(20, ge=1, le=200),
    db: Session = Depends(get_db),
):
    try:
        eventos = RelatorioService.ultimos_eventos(db, limite)
        return [
            {
                "id": e.id,
                "tipo": e.tipo,
                "entidade": e.entidade,
                "entidade_id": e.entidade_id,
                "mensagem": e.mensagem,
                "criado_em": e.criado_em,
            }
            for e in eventos
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))