from __future__ import annotations
from api.app import app
from typing import Generator, List, Optional
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from aurora_tms_mvp import (
    Base,
    engine,
    SessionLocal,
    CaminhaoService,
    MotoristaService,
    ClienteService,
    CargaService,
    ViagemService,
    CustoViagemService,
    RelatorioService,
)
from oraculo_ia import PastorSalmo23


app = FastAPI(
    title="Aurora TMS - API Tática",
    description="Motor logístico de alta performance para gestão de transportes.",
    version="1.3.0",
)


@app.on_event("startup")
def startup_event() -> None:
    Base.metadata.create_all(bind=engine)


def get_db_web() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


class CaminhaoCreate(BaseModel):
    placa: str = Field(..., min_length=7, max_length=10)
    tipo: str
    capacidade_max_kg: float = Field(..., gt=0)
    marca: Optional[str] = None
    modelo: Optional[str] = None
    ano: Optional[int] = None


class CaminhaoOut(BaseModel):
    id: int
    placa: str
    tipo: str
    capacidade_max_kg: float
    marca: Optional[str] = None
    modelo: Optional[str] = None
    ano: Optional[int] = None
    status: str

    class Config:
        from_attributes = True


class MotoristaCreate(BaseModel):
    nome: str
    cpf: str
    cnh: str
    categoria_cnh: str
    telefone: Optional[str] = None


class MotoristaOut(BaseModel):
    id: int
    nome: str
    cpf: str
    cnh: str
    categoria_cnh: str
    telefone: Optional[str] = None
    status: str

    class Config:
        from_attributes = True


class ClienteCreate(BaseModel):
    nome: str
    documento: str
    cidade: Optional[str] = None
    contato: Optional[str] = None
    email: Optional[str] = None


class ClienteOut(BaseModel):
    id: int
    nome: str
    documento: str
    cidade: Optional[str] = None
    contato: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True


class CargaCreate(BaseModel):
    nota_fiscal: str
    descricao: str
    peso_kg: float = Field(..., gt=0)
    valor_mercadoria: float = Field(0, ge=0)
    cidade_origem: str
    cidade_destino: str
    prazo_entrega: Optional[datetime] = None
    cliente_id: Optional[int] = None
    observacoes: Optional[str] = None


class CargaOut(BaseModel):
    id: int
    nota_fiscal: str
    descricao: str
    peso_kg: float
    valor_mercadoria: float
    cidade_origem: str
    cidade_destino: str
    status: str
    cliente_id: Optional[int] = None
    caminhao_id: Optional[int] = None
    viagem_id: Optional[int] = None

    class Config:
        from_attributes = True


class ViagemCreate(BaseModel):
    origem: str
    destino: str
    distancia_km: float = Field(..., ge=0)
    caminhao_id: int
    motorista_id: int
    data_saida_prevista: Optional[datetime] = None
    data_chegada_prevista: Optional[datetime] = None
    observacoes: Optional[str] = None


class ViagemOut(BaseModel):
    id: int
    codigo: str
    origem: str
    destino: str
    distancia_km: float
    status: str
    caminhao_id: int
    motorista_id: int
    data_saida_prevista: Optional[datetime] = None
    data_saida_real: Optional[datetime] = None
    data_chegada_prevista: Optional[datetime] = None
    data_chegada_real: Optional[datetime] = None
    observacoes: Optional[str] = None

    class Config:
        from_attributes = True


class ReservaCargaPayload(BaseModel):
    carga_id: int
    viagem_id: int


class CustoViagemCreate(BaseModel):
    viagem_id: int
    tipo: str
    descricao: str
    valor: float = Field(..., ge=0)


class CustoViagemOut(BaseModel):
    id: int
    viagem_id: int
    tipo: str
    descricao: str
    valor: float

    class Config:
        from_attributes = True


def tratar_erro_regra(e: Exception) -> None:
    raise HTTPException(status_code=400, detail=str(e))


@app.get("/", tags=["Status"])
def status_sistema():
    return {
        "sistema": "Aurora TMS",
        "status": "Online",
        "mensagem": "Motor operando na frequência máxima.",
        "documentacao": "/docs",
    }


@app.get("/dashboard", tags=["Relatórios"])
def obter_dashboard(db: Session = Depends(get_db_web)):
    return RelatorioService.dashboard_operacional(db)


@app.get("/relatorios/frota/ocupacao", tags=["Relatórios"])
def relatorio_ocupacao_frota(db: Session = Depends(get_db_web)):
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


@app.get("/relatorios/viagens/{viagem_id}/rentabilidade", tags=["Relatórios"])
def relatorio_rentabilidade(viagem_id: int, db: Session = Depends(get_db_web)):
    try:
        return RelatorioService.rentabilidade_viagem(db, viagem_id)
    except Exception as e:
        tratar_erro_regra(e)


@app.get("/cargas/alertas", tags=["Operação"])
def alertas_de_prazo(db: Session = Depends(get_db_web)):
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


@app.get("/eventos", tags=["Auditoria"])
def listar_eventos(
    limite: int = Query(20, ge=1, le=200),
    db: Session = Depends(get_db_web),
):
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


@app.get("/caminhoes", response_model=List[CaminhaoOut], tags=["Frota"])
def listar_caminhoes(db: Session = Depends(get_db_web)):
    return CaminhaoService.listar(db)


@app.post("/caminhoes", response_model=CaminhaoOut, tags=["Frota"], status_code=201)
def criar_caminhao(payload: CaminhaoCreate, db: Session = Depends(get_db_web)):
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
        tratar_erro_regra(e)


@app.get("/motoristas", response_model=List[MotoristaOut], tags=["Motoristas"])
def listar_motoristas(db: Session = Depends(get_db_web)):
    return MotoristaService.listar(db)


@app.post("/motoristas", response_model=MotoristaOut, tags=["Motoristas"], status_code=201)
def criar_motorista(payload: MotoristaCreate, db: Session = Depends(get_db_web)):
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
        tratar_erro_regra(e)


@app.get("/clientes", response_model=List[ClienteOut], tags=["Clientes"])
def listar_clientes(db: Session = Depends(get_db_web)):
    return ClienteService.listar(db)


@app.post("/clientes", response_model=ClienteOut, tags=["Clientes"], status_code=201)
def criar_cliente(payload: ClienteCreate, db: Session = Depends(get_db_web)):
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
        tratar_erro_regra(e)


@app.get("/cargas", response_model=List[CargaOut], tags=["Cargas"])
def listar_cargas(db: Session = Depends(get_db_web)):
    return CargaService.listar(db)


@app.post("/cargas", response_model=CargaOut, tags=["Cargas"], status_code=201)
def criar_carga(payload: CargaCreate, db: Session = Depends(get_db_web)):
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
        tratar_erro_regra(e)


@app.post("/cargas/reservar", response_model=CargaOut, tags=["Cargas"])
def reservar_carga(payload: ReservaCargaPayload, db: Session = Depends(get_db_web)):
    try:
        return CargaService.reservar_para_viagem(db, payload.carga_id, payload.viagem_id)
    except Exception as e:
        tratar_erro_regra(e)


@app.post("/cargas/{carga_id}/embarcar", response_model=CargaOut, tags=["Cargas"])
def embarcar_carga(carga_id: int, db: Session = Depends(get_db_web)):
    try:
        return CargaService.embarcar_carga(db, carga_id)
    except Exception as e:
        tratar_erro_regra(e)


@app.post("/cargas/{carga_id}/entregar", response_model=CargaOut, tags=["Cargas"])
def entregar_carga(carga_id: int, db: Session = Depends(get_db_web)):
    try:
        return CargaService.entregar_carga(db, carga_id)
    except Exception as e:
        tratar_erro_regra(e)


@app.get("/viagens", response_model=List[ViagemOut], tags=["Viagens"])
def listar_viagens(db: Session = Depends(get_db_web)):
    return ViagemService.listar(db)


@app.post("/viagens", response_model=ViagemOut, tags=["Viagens"], status_code=201)
def criar_viagem(payload: ViagemCreate, db: Session = Depends(get_db_web)):
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
        tratar_erro_regra(e)


@app.post("/viagens/{viagem_id}/iniciar", response_model=ViagemOut, tags=["Viagens"])
def iniciar_viagem(viagem_id: int, db: Session = Depends(get_db_web)):
    try:
        return ViagemService.iniciar(db, viagem_id)
    except Exception as e:
        tratar_erro_regra(e)


@app.post("/viagens/{viagem_id}/finalizar", response_model=ViagemOut, tags=["Viagens"])
def finalizar_viagem(viagem_id: int, db: Session = Depends(get_db_web)):
    try:
        return ViagemService.finalizar(db, viagem_id)
    except Exception as e:
        tratar_erro_regra(e)


@app.post("/viagens/{viagem_id}/cancelar", response_model=ViagemOut, tags=["Viagens"])
def cancelar_viagem(
    viagem_id: int,
    motivo: str = Query(..., min_length=3),
    db: Session = Depends(get_db_web),
):
    try:
        return ViagemService.cancelar(db, viagem_id, motivo)
    except Exception as e:
        tratar_erro_regra(e)


@app.get("/viagens/{viagem_id}/custos", response_model=List[CustoViagemOut], tags=["Custos"])
def listar_custos_viagem(viagem_id: int, db: Session = Depends(get_db_web)):
    try:
        return CustoViagemService.listar_por_viagem(db, viagem_id)
    except Exception as e:
        tratar_erro_regra(e)


@app.post("/custos", response_model=CustoViagemOut, tags=["Custos"], status_code=201)
def adicionar_custo(payload: CustoViagemCreate, db: Session = Depends(get_db_web)):
    try:
        return CustoViagemService.adicionar(
            db,
            payload.viagem_id,
            payload.tipo,
            payload.descricao,
            payload.valor,
        )
    except Exception as e:
        tratar_erro_regra(e)


@app.get("/oraculo/plano-tatico", tags=["Inteligência Artificial"])
def gerar_plano_tatico(db: Session = Depends(get_db_web)):
    try:
        resultado = PastorSalmo23.gerar_plano_tatico(db)
        if resultado.get("status") == "erro":
            raise HTTPException(status_code=400, detail=resultado.get("mensagem"))
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        tratar_erro_regra(e)