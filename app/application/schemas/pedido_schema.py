from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
from app.domain.pedido import StatusPedidoEnum, CanalPedidoEnum

class ItemPedidoCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(..., gt=0, description="Quantidade deve ser maior que zero")

class ItemPedidoResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    preco_unitario: Decimal

    model_config = ConfigDict(from_attributes=True)

class PedidoCreate(BaseModel):
    unidade_id: int
    canal_pedido: CanalPedidoEnum
    observacao: Optional[str] = None
    itens: List[ItemPedidoCreate]

class StatusUpdate(BaseModel):
    status: StatusPedidoEnum

class PedidoResponse(BaseModel):
    id: int
    usuario_id: int
    unidade_id: int
    canal_pedido: CanalPedidoEnum
    status: StatusPedidoEnum
    total: Decimal
    observacao: Optional[str] = None
    created_at: datetime
    itens: List[ItemPedidoResponse] = []

    model_config = ConfigDict(from_attributes=True)
