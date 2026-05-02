import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric
from sqlalchemy.sql import func
from app.infrastructure.database.connection import Base


class CategoriaEnum(str, enum.Enum):
    PRATOS_PRINCIPAIS = "PRATOS_PRINCIPAIS"
    FRITOS = "FRITOS"
    COZIDOS = "COZIDOS"
    PETISCOS = "PETISCOS"
    FRUTOS_DO_MAR = "FRUTOS_DO_MAR"
    BEBIDAS = "BEBIDAS"
    SOBREMESAS = "SOBREMESAS"

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    preco = Column(Numeric(10, 2), nullable=False)
    categoria = Column(String, nullable=False)
    imagem_url = Column(String, nullable=True)
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
