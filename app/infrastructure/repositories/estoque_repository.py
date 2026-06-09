from sqlalchemy.orm import Session
from app.domain.estoque import Estoque, EstoqueMovimentacao, TipoMovimentacaoEnum

class EstoqueRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_por_unidade(self, unidade_id: int):
        return self.db.query(Estoque).filter(Estoque.unidade_id == unidade_id).all()

    def buscar_por_produto_e_unidade(self, produto_id: int, unidade_id: int):
        return self.db.query(Estoque).filter(
            Estoque.produto_id == produto_id,
            Estoque.unidade_id == unidade_id
        ).first()

    def movimentar(self, estoque: Estoque, tipo: TipoMovimentacaoEnum, quantidade: int, observacao: str = None):
        if tipo == TipoMovimentacaoEnum.ENTRADA:
            estoque.quantidade_disponivel += quantidade
        else:
            if estoque.quantidade_disponivel < quantidade:
                return None  # sinaliza estoque insuficiente
            estoque.quantidade_disponivel -= quantidade

        movimentacao = EstoqueMovimentacao(
            estoque_id=estoque.id,
            tipo=tipo,
            quantidade=quantidade,
            observacao=observacao
        )
        self.db.add(movimentacao)
        self.db.commit()
        self.db.refresh(estoque)
        return estoque
