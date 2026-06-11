from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.infrastructure.database.connection import get_db
from app.api.dependencies.auth import get_current_user
from app.application.schemas.pagamento import PagamentoCreate, PagamentoResponse
from app.application.pagamento_service import PagamentoService

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])

@router.post("/", response_model=PagamentoResponse, status_code=status.HTTP_201_CREATED,
    summary="Processar pagamento de um pedido",
    description="PIX e DINHEIRO sempre aprovados. CARTAO tem 20% de recusa (mock).")
def processar_pagamento(dados: PagamentoCreate, request: Request,
    db: Session = Depends(get_db), usuario_atual=Depends(get_current_user)):
    ip = request.client.host if request.client else None
    try:
        return PagamentoService.processar(db=db, dados=dados, usuario_id=usuario_atual.id, ip=ip)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
