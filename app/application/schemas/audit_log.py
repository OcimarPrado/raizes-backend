from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AuditLogResponse(BaseModel):
    id: int
    usuario_id: Optional[int] = None
    acao: str
    entidade: str
    entidade_id: Optional[int] = None
    detalhe: Optional[str] = None
    ip: Optional[str] = None
    criado_em: datetime
    model_config = {"from_attributes": True}
