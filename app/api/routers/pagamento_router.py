from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.api.dependencies.auth import get_current_user
from app.application.schemas.pagamento import (
    PagamentoCreate,
    PagamentoResponse
)
from app.application.pagamento_service import PagamentoService

# Agrupa todas as rotas relacionadas ao processamento
# e gerenciamento de pagamentos realizados no sistema.
router = APIRouter(
    prefix="/pagamentos",
    tags=["Pagamentos"]
)


@router.post(
    "/",
    response_model=PagamentoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Processar pagamento de um pedido",
    description=(
        "PIX e DINHEIRO sempre aprovados. "
        "CARTAO tem 20% de recusa (mock)."
    )
)
def processar_pagamento(
    dados: PagamentoCreate,
    request: Request,
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user)
):
    """
    Processa o pagamento de um pedido realizado pelo usuário autenticado.

    Regras de negócio:
    - Apenas usuários autenticados podem efetuar pagamentos.
    - Pagamentos via PIX são aprovados automaticamente.
    - Pagamentos em dinheiro são aprovados automaticamente.
    - Pagamentos com cartão utilizam uma simulação (mock),
      possuindo 20% de chance de recusa.
    - Toda tentativa de pagamento fica vinculada ao usuário
      que realizou a operação.
    """

    # Obtém o endereço IP de origem da requisição.
    # Essa informação pode ser utilizada para auditoria,
    # rastreamento de operações ou análise de segurança.
    ip = request.client.host if request.client else None

    try:
        # Encaminha a solicitação para a camada de serviço,
        # responsável por validar as regras de negócio,
        # registrar a transação e definir seu resultado.
        return PagamentoService.processar(
            db=db,
            dados=dados,
            usuario_id=usuario_atual.id,
            ip=ip
        )

    except ValueError as e:
        # Captura erros de validação gerados pela camada
        # de serviço e os converte para uma resposta HTTP
        # adequada ao cliente da API.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )