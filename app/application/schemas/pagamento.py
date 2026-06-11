from pydantic import BaseModel
from datetime import datetime
from typing import Optional

METODOS_VALIDOS = ["PIX", "CARTAO_CREDITO", "CARTAO_DEBITO", "DINHEIRO"]

class PagamentoCreate(BaseModel):
    pedido_id: int
    metodo: str

    def validate_metodo(self):
        if self.metodo not in METODOS_VALIDOS:
            raise ValueError(f"Método inválido. Use: {METODOS_VALIDOS}")

class PagamentoResponse(BaseModel):
    id: int
    pedido_id: int
    metodo: str
    status: str
    valor: float
    resposta_mock: Optional[str] = None
    created_at: datetime
    model_config = {"from_attributes": True}
