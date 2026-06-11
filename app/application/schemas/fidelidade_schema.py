from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional
from app.domain.fidelidade import TipoFidelidadeEnum


class FidelidadeResponse(BaseModel):
    id: int
    usuario_id: int
    cupons_disponiveis: int
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FidelidadeHistoricoResponse(BaseModel):
    id: int
    tipo: TipoFidelidadeEnum
    cupons: int
    pedido_id: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
