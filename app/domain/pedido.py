import enum
from sqlalchemy.orm import column, Integer, Dtring, ForeignKey, DateTime, Enum
import enum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.connection import Base

class CanalPedidoEnum(str, enum.Enum):
    APP = "APP"
    TOTEM = "TOTEM"
    BALCAO = "BALCAO"
    PICKUP = "PICKUP"
    WEB = "WEB"

class StatusPedidoEnum(str, enum.Enum):
    AGUARDANDO_PAGAMENTO = "AGUARDANDO_PAGAMENTO"
    CONFIRMADO = "CONFIRMADO"
    PREPARANDO = "PREPARANDO"
    PRONTO = "PRONTO"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)
    canal_pedido = Column(Enum(CanalPedidoEnum), nullable=False)
    status = Column(Enum(StatusPedidoEnum), nullable=False, default=StatusPedidoEnum.AGUARDANDO_PAGAMENTO)
    total = Column(Numeric(10, 2), nullable=False, default=0)
    observacao = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    usuario = relationship("Usuario")
    unidade = relationship("Unidade")
    itens = relationship("ItemPedido", back_populates="pedido")
    pagamentos = relationship("Pagamento", back_populates="pedido")
# O preço unitário é armazenado em ItemPedido no momento da criação do pedido,
# garantindo que o histórico financeiro guarde informações de compra
# corretamente, independente de atualizações futuras no cadastro de produtos


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto")

class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    metodo = Column(String, nullable=False)
    status = Column(String, nullable=False)
    resposta_mock = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    pedido = relationship("Pedido", back_populates="pagamentos")
