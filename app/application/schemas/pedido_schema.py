
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
from app.domain.pedido import StatusPedidoEnum, CanalPedidoEnum

class ItemPedidoSchema(BaseModel):
    produto_id: int
    quantidade: int = Field(..., gt=0)
    preco_unitario: Decimal

class PedidoBase(BaseModel):
    unidade_id: int
    canal_pedido: CanalPedidoEnum
    observacao: Optional[str] = None

class PedidoCreate(PedidoBase):
    usuario_id: int
    itens: List[ItemPedidoSchema]

class PedidoResponse(PedidoBase):
    id: int
    usuario_id: int
    status: StatusPedidoEnum
    total: Decimal
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)