from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from decimal import Decimal

from app.infrastructure.repositories.pedido_repository import PedidoRepository
from app.infrastructure.repositories.estoque_repository import EstoqueRepository
from app.infrastructure.repositories.produto_repository import ProdutoRepository
from app.domain.pedido import Pedido, ItemPedido, StatusPedidoEnum
from app.domain.estoque import TipoMovimentacaoEnum
from app.domain.fidelidade import Fidelidade, FidelidadeHistorico, TipoFidelidadeEnum
from app.application.schemas.pedido_schema import PedidoCreate

# a cada 10 pedidos entregues o cliente ganha 1 cupom
PEDIDOS_POR_CUPOM = 10

class PedidoService:
    def __init__(self, db: Session):
        self.db = db
        self.pedido_repo   = PedidoRepository(db)
        self.estoque_repo  = EstoqueRepository(db)
        self.produto_repo  = ProdutoRepository(db)

    def criar_pedido(self, dados: PedidoCreate, usuario_id: int) -> Pedido:
        # 1. valida cada item: produto existe e tem estoque suficiente
        for item in dados.itens:
            produto = self.produto_repo.buscar_por_id(item.produto_id)
            if not produto or not produto.ativo:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Produto {item.produto_id} não encontrado ou inativo."
                )

            estoque = self.estoque_repo.buscar_por_produto_e_unidade(
                item.produto_id, dados.unidade_id
            )
            if not estoque or estoque.quantidade_disponivel < item.quantidade:
                disponivel = estoque.quantidade_disponivel if estoque else 0
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Estoque insuficiente para '{produto.nome}'. Disponível: {disponivel}."
                )

        # 2. cria o pedido
        pedido = Pedido(
            usuario_id=usuario_id,
            unidade_id=dados.unidade_id,
            canal_pedido=dados.canal_pedido,
            observacao=dados.observacao,
            status=StatusPedidoEnum.AGUARDANDO_PAGAMENTO,
            total=Decimal("0.00")
        )
        self.db.add(pedido)
        self.db.flush()  # gera o id sem commitar ainda

        # 3. cria os itens e desconta o estoque
        total = Decimal("0.00")
        for item in dados.itens:
            produto = self.produto_repo.buscar_por_id(item.produto_id)
            preco_unitario = Decimal(str(produto.preco))

            item_pedido = ItemPedido(
                pedido_id=pedido.id,
                produto_id=item.produto_id,
                quantidade=item.quantidade,
                preco_unitario=preco_unitario
            )
            self.db.add(item_pedido)

            # desconta estoque
            estoque = self.estoque_repo.buscar_por_produto_e_unidade(
                item.produto_id, dados.unidade_id
            )
            self.estoque_repo.movimentar(
                estoque=estoque,
                tipo=TipoMovimentacaoEnum.SAIDA,
                quantidade=item.quantidade,
                observacao=f"Pedido #{pedido.id}"
            )

            total += preco_unitario * item.quantidade

        # 4. atualiza o total e commita tudo
        pedido.total = total
        self.db.commit()
        self.db.refresh(pedido)
        return pedido

    def atualizar_status(self, pedido_id: int, novo_status: StatusPedidoEnum, usuario_id: int, role: str) -> Pedido:
        pedido = self.pedido_repo.buscar_por_id(pedido_id)
        if not pedido:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado.")

        # cliente só pode cancelar o próprio pedido
        if role == "CLIENTE":
            if pedido.usuario_id != usuario_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sem permissão.")
            if novo_status != StatusPedidoEnum.CANCELADO:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cliente só pode cancelar pedidos.")

        pedido = self.pedido_repo.atualizar_status(pedido, novo_status)

        # se pedido foi entregue, verifica fidelidade
        if novo_status == StatusPedidoEnum.ENTREGUE:
            self._processar_fidelidade(pedido)

        return pedido

    def _processar_fidelidade(self, pedido: Pedido):
        # conta pedidos entregues do cliente
        total_entregues = self.db.query(Pedido).filter(
            Pedido.usuario_id == pedido.usuario_id,
            Pedido.status == StatusPedidoEnum.ENTREGUE
        ).count()

        # ganha cupom a cada PEDIDOS_POR_CUPOM entregas
        if total_entregues % PEDIDOS_POR_CUPOM == 0:
            fidelidade = self.db.query(Fidelidade).filter(
                Fidelidade.usuario_id == pedido.usuario_id
            ).first()

            if not fidelidade:
                fidelidade = Fidelidade(usuario_id=pedido.usuario_id, cupons_disponiveis=0)
                self.db.add(fidelidade)
                self.db.flush()

            fidelidade.cupons_disponiveis += 1

            historico = FidelidadeHistorico(
                usuario_id=pedido.usuario_id,
                pedido_id=pedido.id,
                tipo=TipoFidelidadeEnum.GANHO,
                cupons=1
            )
            self.db.add(historico)
            self.db.commit()
