
from fastapi import APIRouter, Depends, UploadFile, File, status, HTTPException
from sqlalchemy.orm import Session
import os
import uuid

from app.infrastructure.database.connection import get_db
from app.api.dependencies.auth import get_current_user
from app.application.schemas.produto_schema import ProdutoCreate, ProdutoResponse
from app.infrastructure.repositories.produto_repository import ProdutoRepository
from app.domain.produto import Produto
from app.domain.estoque import Estoque, EstoqueMovimentacao
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

    # Cria registro de estoque zerado em todas as unidades ativas.
    # Isso garante que o produto já aparece no painel de estoque
    # de cada unidade, pronto para receber entrada de quantidade.
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
    Rota pública — lista todos os produtos do cardápio.
    """
    repositorio = ProdutoRepository(db)
    return repositorio.buscar_todos()


@router.post("/upload-imagem")
def upload_imagem(file: UploadFile = File(...)):
    """
    Recebe um arquivo de imagem e salva em /uploads, retornando a URL pública.
    """
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(upload_dir, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return {"url": f"/uploads/{filename}"}


@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(
    produto_id: int,
    produto_atualizado: ProdutoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Atualiza dados de um produto existente, incluindo imagem.
    """
    repositorio = ProdutoRepository(db)
    produto_existente = repositorio.buscar_por_id(produto_id)
    if not produto_existente:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    produto_existente.nome = produto_atualizado.nome
    produto_existente.descricao = produto_atualizado.descricao
    produto_existente.preco = produto_atualizado.preco
    produto_existente.categoria = produto_atualizado.categoria
    if hasattr(produto_atualizado, "imagem_url"):
        produto_existente.imagem_url = produto_atualizado.imagem_url

    return repositorio.atualizar(produto_existente)


@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Remove um produto do cardápio.

    Antes de excluir o produto, remove também os registros de estoque
    e movimentações vinculados a ele. Produtos que já foram incluídos
    em pedidos não podem ser excluídos — nesses casos, use a opção
    de desativar o produto (campo 'ativo = false').
    """
    repositorio = ProdutoRepository(db)
    produto = repositorio.buscar_por_id(produto_id)

    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com ID {produto_id} não encontrado no cardápio."
        )

    # Verifica se o produto já foi usado em algum pedido.
    # Se sim, não permite exclusão para preservar o histórico financeiro.
    from app.domain.pedido import ItemPedido
    if db.query(ItemPedido).filter(ItemPedido.produto_id == produto_id).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este produto já foi utilizado em pedidos e não pode ser excluído. Desative-o alterando o campo 'ativo' para false."
        )

    # Remove as movimentações de estoque vinculadas antes de remover o estoque.
    estoques = db.query(Estoque).filter(Estoque.produto_id == produto_id).all()
    for e in estoques:
        db.query(EstoqueMovimentacao).filter(
            EstoqueMovimentacao.estoque_id == e.id
        ).delete()
    db.query(Estoque).filter(Estoque.produto_id == produto_id).delete()
    db.flush()

    repositorio.deletar(produto)
    return None
