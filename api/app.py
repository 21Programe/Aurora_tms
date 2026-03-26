from fastapi import FastAPI
from core.database import Base, engine

from api.routers.status import router as status_router
from api.routers.relatorios import router as relatorios_router
from api.routers.caminhoes import router as caminhoes_router
from api.routers.motoristas import router as motoristas_router
from api.routers.clientes import router as clientes_router
from api.routers.cargas import router as cargas_router
from api.routers.viagens import router as viagens_router
from api.routers.custos import router as custos_router
from api.routers.oraculo import router as oraculo_router

app = FastAPI(
    title="Aurora TMS - API Tática",
    description="Motor logístico de alta performance para gestão de transportes.",
    version="2.0.0",
)


@app.on_event("startup")
def startup_event() -> None:
    Base.metadata.create_all(bind=engine)


app.include_router(status_router)
app.include_router(relatorios_router)
app.include_router(caminhoes_router)
app.include_router(motoristas_router)
app.include_router(clientes_router)
app.include_router(cargas_router)
app.include_router(viagens_router)
app.include_router(custos_router)
app.include_router(oraculo_router)