from pydantic import BaseModel, ConfigDict, Field
from app.domain.estoque import TipoMovimentacaoEnum

class EstoqueResponse(BaseModel):
    id: int
    produto_id: int
    unidade_id: int
    quantidade_disponivel: int
    quantidade_minima: int

    model_config = ConfigDict(from_attributes=True)

class MovimentacaoCreate(BaseModel):
    tipo: TipoMovimentacaoEnum
    quantidade: int = Field(..., gt=0, description="Quantidade deve ser maior que zero")
    observacao: str | None = None
