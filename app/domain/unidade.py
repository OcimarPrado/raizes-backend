from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.connection import Base

class Unidade(Base):
    __tablename__ = "unidades"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    estado = Column(String(2), nullable=False)
    endereco = Column(String, nullable=False)
    ativa = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Ponto importante aqui é o campo 'ativa',
# que serve para desativar uma unidade sem perder o histórico vinculados a ela.
