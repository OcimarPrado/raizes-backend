from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.unidade_repository import UnidadeRepository
from app.application.schemas.unidade_schema import UnidadeResponse

router = APIRouter(prefix="/unidades", tags=["Unidades"])

@router.get("/", response_model=list[UnidadeResponse])
def listar_unidades(db: Session = Depends(get_db)):
    """
    Lista todas as unidades ativas da rede Raízes do Nordeste.
    Rota pública — usada pelo cliente para escolher onde retirar o pedido.
    """
    repositorio = UnidadeRepository(db)
    return repositorio.buscar_todas()

@router.get("/{unidade_id}", response_model=UnidadeResponse)
def buscar_unidade(unidade_id: int, db: Session = Depends(get_db)):
    """
    Retorna os dados de uma unidade específica pelo ID.
    """
    repositorio = UnidadeRepository(db)
    unidade = repositorio.buscar_por_id(unidade_id)
    if not unidade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unidade {unidade_id} não encontrada."
        )
    return unidade
