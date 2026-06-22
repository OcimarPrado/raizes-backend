from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.api.dependencies.auth import get_current_user
from app.application.fidelidade_service import FidelidadeService
from app.application.schemas.fidelidade_schema import (
    FidelidadeResponse,
    FidelidadeHistoricoResponse
)

# Agrupa as rotas relacionadas ao programa de fidelidade.
# Todas as URLs deste módulo iniciarão com "/fidelidade".
router = APIRouter(
    prefix="/fidelidade",
    tags=["Fidelidade"]
)


@router.get(
    "/me",
    response_model=FidelidadeResponse,
    summary="Saldo de cupons do usuário logado",
)
def meu_saldo(
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user),
):
    """
    Retorna o saldo atual de cupons do usuário autenticado.

    Regra de negócio:
    - O usuário só pode consultar seus próprios cupons.
    - Caso ainda não exista um registro de fidelidade,
      ele será criado automaticamente.
    - O retorno inclui a quantidade atual de cupons
      disponíveis para utilização.
    """

    # Busca o cadastro de fidelidade do usuário.
    # Caso ele ainda não exista, o sistema cria
    # automaticamente um novo registro.
    return FidelidadeService.obter_ou_criar(
        db,
        usuario_atual.id
    )


@router.get(
    "/me/historico",
    response_model=list[FidelidadeHistoricoResponse],
    summary="Histórico de cupons do usuário logado",
)
def meu_historico(
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user),
):
    """
    Retorna o histórico completo de movimentações
    do programa de fidelidade do usuário autenticado.

    Regra de negócio:
    - O usuário visualiza apenas suas próprias movimentações.
    - O histórico permite acompanhar ganhos,
      utilizações e ajustes de cupons.
    - Serve como mecanismo de transparência
      para o programa de fidelidade.
    """

    # Recupera todas as movimentações registradas
    # para o usuário autenticado.
    return FidelidadeService.listar_historico(
        db,
        usuario_atual.id
    )