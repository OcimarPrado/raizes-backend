
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

# Importamos as ferramentas que a gente já construiu antes
from app.infrastructure.database.connection import get_db
from app.api.dependencies.auth import get_current_user
from app.application.schemas.produto_schema import ProdutoCreate, ProdutoResponse
from app.infrastructure.repositories.produto_repository import ProdutoRepository
from app.domain.produto import Produto

# Criamos a rota com o nome 'produtos'
router = APIRouter(prefix="/produtos", tags=["Produtos do Cardápio"])

@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto_novo(
    produto_que_chegou: ProdutoCreate, 
    db: Session = Depends(get_db),
    usuario_logado = Depends(get_current_user) # O CADEADO: Só passa se tiver o Token!
):
    """
    Este é o processo de receber um produto novo no sistema.
    """
    # 1. Chamamos o 'Funcionário do Estoque' (Repository)
    repositorio = ProdutoRepository(db)
    
    # 2. Transformamos os dados que chegaram no formato que o banco entende
    novo_produto = Produto(**produto_que_chegou.model_dump())
    
    # 3. Mandamos o funcionário salvar e nos devolver o resultado
    item_salvo = repositorio.salvar_no_banco(novo_produto)
    
    # 4. Entregamos o produto cadastrado para quem pediu
    return item_salvo