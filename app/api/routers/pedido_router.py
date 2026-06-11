from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.infrastructure.database.connection import get_db
from app.api.dependencies.auth import get_current_user
from app.application.pedido_service import PedidoService
from app.infrastructure.repositories.pedido_repository import PedidoRepository
from app.application.fidelidade_service import FidelidadeService
from app.application.schemas.pedido_schema import PedidoCreate, PedidoResponse, StatusUpdate
from app.domain.pedido import StatusPedidoEnum, CanalPedidoEnum
from app.domain.usuario import RoleEnum

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def criar_pedido(
    dados: PedidoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    """
    Cria um novo pedido validando estoque e calculando o total automaticamente.
    O campo canalPedido é obrigatório (APP, TOTEM, BALCAO, PICKUP, WEB).
    """
    service = PedidoService(db)
    return service.criar_pedido(dados, usuario_id=usuario.id)

@router.get("/", response_model=list[PedidoResponse])
def listar_pedidos(
    canal_pedido: Optional[CanalPedidoEnum] = Query(None, description="Filtrar por canal"),
    status_pedido: Optional[StatusPedidoEnum] = Query(None, alias="status", description="Filtrar por status"),
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    """
    Lista pedidos com filtros opcionais por canal e status.
    GERENTE vê todos os pedidos. CLIENTE vê apenas os seus.
    """
    repositorio = PedidoRepository(db)

    usuario_id = None if usuario.role == RoleEnum.GERENTE else usuario.id

    return repositorio.listar(
        usuario_id=usuario_id,
        status=status_pedido,
        canal=canal_pedido
    )

@router.get("/{pedido_id}", response_model=PedidoResponse)
def buscar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    """
    Retorna os detalhes de um pedido específico.
    """
    repositorio = PedidoRepository(db)
    pedido = repositorio.buscar_por_id(pedido_id)

    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado.")

    # cliente só vê o próprio pedido
    if usuario.role == RoleEnum.CLIENTE and pedido.usuario_id != usuario.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sem permissão.")

    return pedido

@router.patch("/{pedido_id}/status", response_model=PedidoResponse)
def atualizar_status(
    pedido_id: int,
    dados: StatusUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    """
    Atualiza o status de um pedido.
    GERENTE pode mover para qualquer status.
    CLIENTE só pode cancelar o próprio pedido.
    """
    service = PedidoService(db)
    return service.atualizar_status(
        pedido_id=pedido_id,
        novo_status=dados.status,
        usuario_id=usuario.id,
        role=usuario.role.value
    )
