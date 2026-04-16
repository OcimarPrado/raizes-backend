import enum
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.connection import Base

class TipoFidelidadeEnum(str, enum.Enum):
    GANHO = "GANHO"
    RESGATE = "RESGATE"

class Fidelidade(Base):
    __tablename__ = "fidelidade"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, unique=True) # Cada cliente tem apenas um registro de saldo, de modo que o banco rejeita dois registros no mesmo cliente. 
    cupons_disponiveis = Column(Integer, nullable=False, default=0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    usuario = relationship("Usuario")
    historico = relationship("FidelidadeHistorico", back_populates="fidelidade")

class FidelidadeHistorico(Base):
    __tablename__ = "fidelidade_historico"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=True)
    tipo = Column(Enum(TipoFidelidadeEnum), nullable=False)
    cupons = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    usuario = relationship("Usuario")
    pedido = relationship("Pedido")
    fidelidade = relationship("Fidelidade", back_populates="historico")
