import enum
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.connection import Base

class TipoMovimentacaoEnum(str, enum.Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"

class Estoque(Base):
    __tablename__ = "estoques"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)
    quantidade_disponivel = Column(Integer, nullable=False, default=0)
    quantidade_minima = Column(Integer, nullable=False, default=5)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    produto = relationship("Produto")
    unidade = relationship("Unidade")

class EstoqueMovimentacao(Base):
    __tablename__ = "estoque_movimentacoes"

    id = Column(Integer, primary_key=True, index=True)
    estoque_id = Column(Integer, ForeignKey("estoques.id"), nullable=False)
    tipo = Column(Enum(TipoMovimentacaoEnum), nullable=False)
    quantidade = Column(Integer, nullable=False)
    observacao = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    estoque = relationship("Estoque")
