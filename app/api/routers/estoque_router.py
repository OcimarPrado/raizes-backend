from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.database.connection import get_db
from app.api.dependencies.auth import get_current_user
from app.infrastructure.repositories.estoque_repository import EstoqueRepository
from app.application.schemas.estoque_schema import EstoqueResponse, MovimentacaoCreate
from app.domain.usuario import RoleEnum

router = APIRouter(prefix="/estoque", tags=["Estoque"])

def exigir_gerente(usuario=Depends(get_current_user)):
    if usuario.role != RoleEnum.GERENTE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito ao gerente."
        )
    return usuario

@router.get("/unidade/{unidade_id}", response_model=list[EstoqueResponse])
def consultar_estoque_por_unidade(
    unidade_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_gerente)
):
    """
    Lista o saldo de estoque de todos os produtos de uma unidade.
    Acesso restrito: GERENTE.
    """
    repositorio = EstoqueRepository(db)
    return repositorio.buscar_por_unidade(unidade_id)

@router.post("/unidade/{unidade_id}/produto/{produto_id}", response_model=EstoqueResponse)
def movimentar_estoque(
    unidade_id: int,
    produto_id: int,
    movimentacao: MovimentacaoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_gerente)
):
    """
    Registra entrada ou saída de estoque para um produto em uma unidade.
    Acesso restrito: GERENTE.
    """
    repositorio = EstoqueRepository(db)

    estoque = repositorio.buscar_por_produto_e_unidade(produto_id, unidade_id)
    if not estoque:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de estoque não encontrado para este produto e unidade."
        )

    resultado = repositorio.movimentar(
        estoque=estoque,
        tipo=movimentacao.tipo,
        quantidade=movimentacao.quantidade,
        observacao=movimentacao.observacao
    )

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Estoque insuficiente. Disponível: {estoque.quantidade_disponivel} unidade(s)."
        )

    return resultado
