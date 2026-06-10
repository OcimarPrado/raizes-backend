from sqlalchemy.orm import Session
from app.domain.pedido import Pedido, ItemPedido, StatusPedidoEnum, CanalPedidoEnum

class PedidoRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar(self, pedido: Pedido) -> Pedido:
        self.db.add(pedido)
        self.db.commit()
        self.db.refresh(pedido)
        return pedido

    def adicionar_item(self, item: ItemPedido) -> ItemPedido:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def buscar_por_id(self, pedido_id: int) -> Pedido | None:
        return self.db.query(Pedido).filter(Pedido.id == pedido_id).first()

    def listar(self, usuario_id: int | None = None, status: StatusPedidoEnum | None = None, canal: CanalPedidoEnum | None = None):
        query = self.db.query(Pedido)
        if usuario_id:
            query = query.filter(Pedido.usuario_id == usuario_id)
        if status:
            query = query.filter(Pedido.status == status)
        if canal:
            query = query.filter(Pedido.canal_pedido == canal)
        return query.order_by(Pedido.created_at.desc()).all()

    def atualizar_status(self, pedido: Pedido, novo_status: StatusPedidoEnum) -> Pedido:
        pedido.status = novo_status
        self.db.commit()
        self.db.refresh(pedido)
        return pedido

    def atualizar_total(self, pedido: Pedido, total: float) -> Pedido:
        pedido.total = total
        self.db.commit()
        self.db.refresh(pedido)
        return pedido
