from fastapi import APIRouter

router = APIRouter(tags=["Status"])


@router.get("/")
def status_sistema():
    return {
        "sistema": "Aurora TMS",
        "status": "Online",
        "mensagem": "Motor operando na frequência máxima.",
        "documentacao": "/docs",
    }