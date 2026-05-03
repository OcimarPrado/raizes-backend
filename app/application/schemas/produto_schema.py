from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import Optional
from app.domain.produto import CategoriaEnum

class ProdutoBase(BaseModel):
    """
    Schema base para a entidade Produto.
    Define os campos comuns e as regras de validação de dados para o Raízes do Nordeste.
    """
    # Nome do produto com validação de tamanho para evitar strings vazias
    nome: str = Field(..., min_length=3, max_length=100, description="Nome identificador do produto")
    
    # Descrição opcional, limitada para não sobrecarregar o banco de dados
    descricao: Optional[str] = Field(None, max_length=500, description="Detalhes sobre o produto")
    
    # Preço utilizando Decimal para precisão financeira, garantindo que seja sempre positivo
    preco: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2, description="Preço de venda")
    
    # Categoria validada automaticamente contra o CategoriaEnum definido no domínio
    categoria: CategoriaEnum = Field(..., description="Categoria de classificação do item")
    
    # URL da imagem (opcional). Pode ser validado como string ou HttpUrl futuramente.
    imagem_url: Optional[str] = Field(None, description="Link para a imagem do produto")
    
    # Status de disponibilidade do produto no sistema
    ativo: bool = Field(default=True, description="Indica se o produto está visível para venda")

class ProdutoCreate(ProdutoBase):
    """
    Schema utilizado para a criação de novos produtos.
    Herda todas as validações do ProdutoBase.
    """
    pass

class ProdutoResponse(ProdutoBase):
    """
    Schema de resposta (Output) que inclui o ID gerado pelo banco de dados.
    Utilizado para retornar dados de forma segura e formatada.
    """
    id: int
    
    # Configuração para permitir que o Pydantic converta objetos do SQLAlchemy (ORM) automaticamente
    model_config = ConfigDict(from_attributes=True)