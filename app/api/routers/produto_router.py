
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

# Importamos as ferramentas que a gente já construiu antes
from app.infrastructure.database.connection import get_db
from app.api.dependencies.auth import get_current_user
from app.application.schemas.produto_schema import ProdutoCreate, ProdutoResponse
from app.infrastructure.repositories.produto_repository import ProdutoRepository
from app.domain.produto import Produto
from app.infrastructure.repositories.usuario_repository import Usuario

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

@router.get("/", response_model=list[ProdutoResponse])
def listar_todos_os_produtos(db: Session = Depends(get_db)):
    """
    Rota lista  todos os produtos. Visto que o cardápio é público, não usamos 'get_current_user'.
    """
    # 1. Chamada do estoque.
    repositorio = ProdutoRepository(db)

    # 2. Busca de produtos em estoque.
    produtos = repositorio.buscar_todos()

    # 3. Lista todos os produtos
    return produtos 

@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(
    produto_id: int,
    produto_atualizado: ProdutoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # Exige login
):
    """
    Endpoint para atualizar dados de um produto.
    Verifica se o ID existe antes de fazer alteração.
    """

    repositorio = ProdutoRepository(db)

    # 1. Busca o produto original no banco.
    produto_existente = repositorio.buscar_por_id(produto_id)

    # 2. Se n~so existir retorna ERRO 404 - Not Found
    if not produto_existente:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # 3. Mapeando novos dados para o objeto do banco.
    produto_existente.nome = produto_atualizado.nome
    produto_existente.descricao = produto_atualizado.descricao
    produto_existente.preco = produto_atualizado.preco
    produto_existente.categoria = produto_atualizado.categoria

    # 4. Salva e retorna o produto modificado.
    return repositorio.atualizar(produto_existente)

# Rota para remover um produto (DELETE)
@router.delete("/{produto_id}", status_code=204)
def deletar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # Exige login
):
    
    """
    Endpoint para deletar um produto.
    Retorna 204 quando a exclusão é bem sucedida.
    """

    repositorio = ProdutoRepository(db)

    # 1. Tenta localizar o item
    produto = repositorio.buscar_por_id(produto_id)

    # 2. Se não achar o ID, avisa que não existe.
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    
    # 3. Executa remoção do item 
    repositorio.deletar(produto)

    # 4. Retorna vazio
    return None