from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database.connection import get_db
from app.api.dependencies.auth import get_current_user
from app.application.fidelidade_service import FidelidadeService
from app.application.schemas.fidelidade_schema import FidelidadeResponse, FidelidadeHistoricoResponse

router = APIRouter(prefix="/fidelidade", tags=["Fidelidade"])


@router.get(
    "/me",
    response_model=FidelidadeResponse,
    summary="Saldo de cupons do usuário logado",
)
def meu_saldo(
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user),
):
    return FidelidadeService.obter_ou_criar(db, usuario_atual.id)


@router.get(
    "/me/historico",
    response_model=list[FidelidadeHistoricoResponse],
    summary="Histórico de cupons do usuário logado",
)
def meu_historico(
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user),
):
    return FidelidadeService.listar_historico(db, usuario_atual.id)
