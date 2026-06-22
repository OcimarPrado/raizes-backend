from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.api.dependencies.auth import get_current_user
from app.infrastructure.repositories.estoque_repository import EstoqueRepository
from app.application.schemas.estoque_schema import (
    EstoqueResponse,
    MovimentacaoCreate
)
from app.domain.usuario import RoleEnum

# Agrupa as rotas responsáveis pelo controle e movimentação de estoque.
# Todas as rotas deste módulo serão acessadas através do prefixo "/estoque".
router = APIRouter(
    prefix="/estoque",
    tags=["Estoque"]
)


def exigir_gerente(usuario=Depends(get_current_user)):
    """
    Dependência responsável por validar se o usuário autenticado
    possui perfil de GERENTE.

    Essa verificação garante que apenas usuários autorizados
    possam consultar e movimentar estoques.
    """

    if usuario.role != RoleEnum.GERENTE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito ao gerente."
        )

    return usuario


@router.get(
    "/unidade/{unidade_id}",
    response_model=list[EstoqueResponse]
)
def consultar_estoque_por_unidade(
    unidade_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_gerente)
):
    """
    Retorna a posição atual de estoque de todos os produtos
    pertencentes a uma determinada unidade.

    Regra de negócio:
    - Somente usuários com perfil GERENTE podem realizar a consulta.
    - A consulta exibe a quantidade disponível de cada produto
      cadastrada para a unidade informada.
    """

    # Cria uma instância do repositório responsável pelas
    # operações de acesso aos dados de estoque.
    repositorio = EstoqueRepository(db)

    # Recupera todos os registros de estoque vinculados
    # à unidade informada.
    return repositorio.buscar_por_unidade(unidade_id)


@router.post(
    "/unidade/{unidade_id}/produto/{produto_id}",
    response_model=EstoqueResponse
)
def movimentar_estoque(
    unidade_id: int,
    produto_id: int,
    movimentacao: MovimentacaoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_gerente)
):
    """
    Registra movimentações de entrada ou saída de estoque.

    Regra de negócio:
    - Apenas GERENTES podem movimentar estoque.
    - Entradas aumentam o saldo disponível.
    - Saídas reduzem o saldo disponível.
    - Não é permitido gerar saldo negativo.
    """

    # Instancia o repositório responsável pelas operações
    # relacionadas ao estoque.
    repositorio = EstoqueRepository(db)

    # Localiza o registro de estoque correspondente ao produto
    # e à unidade informados na requisição.
    estoque = repositorio.buscar_por_produto_e_unidade(
        produto_id,
        unidade_id
    )

    # Caso não exista vínculo entre o produto e a unidade,
    # a operação é interrompida.
    if not estoque:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de estoque não encontrado para este produto e unidade."
        )

    # Executa a movimentação solicitada (entrada ou saída),
    # aplicando as validações definidas na camada de repositório.
    resultado = repositorio.movimentar(
        estoque=estoque,
        tipo=movimentacao.tipo,
        quantidade=movimentacao.quantidade,
        observacao=movimentacao.observacao
    )

    # Quando o método retorna None significa que a operação
    # de saída deixaria o estoque com saldo negativo.
    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Estoque insuficiente. "
                f"Disponível: {estoque.quantidade_disponivel} unidade(s)."
            )
        )

    # Retorna o estado atualizado do estoque após a movimentação.
    return resultado