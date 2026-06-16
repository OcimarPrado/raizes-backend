from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.api.dependencies.auth import get_current_user
from app.application.schemas.produto_schema import ProdutoCreate, ProdutoResponse
from app.infrastructure.repositories.produto_repository import ProdutoRepository
from app.domain.produto import Produto
from app.domain.estoque import Estoque
from app.domain.unidade import Unidade
from app.infrastructure.repositories.usuario_repository import Usuario

router = APIRouter(prefix="/produtos", tags=["Produtos do Cardápio"])


@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto_novo(
    produto_que_chegou: ProdutoCreate,
    db: Session = Depends(get_db),
    usuario_logado=Depends(get_current_user)
):
    """
    Cria um produto e automaticamente registra estoque zerado em todas as unidades ativas.
    O gerente depois faz ENTRADA via painel de estoque para definir a quantidade.
    """
    repositorio = ProdutoRepository(db)
    novo_produto = Produto(**produto_que_chegou.model_dump())
    item_salvo = repositorio.salvar_no_banco(novo_produto)

    # Cria registro de estoque zerado em todas as unidades ativas
    unidades = db.query(Unidade).filter(Unidade.ativa == True).all()
    for unidade in unidades:
        estoque = Estoque(
            produto_id=item_salvo.id,
            unidade_id=unidade.id,
            quantidade_disponivel=0,
            quantidade_minima=10,
        )
        db.add(estoque)
    db.commit()
    db.refresh(item_salvo)

    return item_salvo


@router.get("/", response_model=list[ProdutoResponse])
def listar_todos_os_produtos(db: Session = Depends(get_db)):
    """
    Rota pública — lista todos os produtos ativos do cardápio.
    """
    repositorio = ProdutoRepository(db)
    return repositorio.buscar_todos()


@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(
    produto_id: int,
    produto_atualizado: ProdutoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Atualiza dados de um produto existente.
    """
    repositorio = ProdutoRepository(db)
    produto_existente = repositorio.buscar_por_id(produto_id)
    if not produto_existente:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    produto_existente.nome = produto_atualizado.nome
    produto_existente.descricao = produto_atualizado.descricao
    produto_existente.preco = produto_atualizado.preco
    produto_existente.categoria = produto_atualizado.categoria
    produto_existente.imagem_url = produto_atualizado.imagem_url if hasattr(produto_atualizado, 'imagem_url') else produto_existente.imagem_url

    return repositorio.atualizar(produto_existente)


@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Remove um produto do cardápio.
    """
    repositorio = ProdutoRepository(db)
    produto = repositorio.buscar_por_id(produto_id)
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com ID {produto_id} não encontrado."
        )
    repositorio.deletar(produto)
    return None
