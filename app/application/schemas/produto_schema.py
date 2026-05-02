
from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import Optional
from app.domain.produto import CategoriaEnum

class ProdutoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    categoria: CategoriaEnum
    imagem_url: Optional[str] = None
    ativo: bool = True

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)