import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric
from sqlalchemy.sql import func
from app.infrastructure.database.connection import Base

# Definindo as categorias como um Enum Python para garantir consistência em todo o sistema
class CategoriaEnum(str, enum.Enum):
    PRATOS_PRINCIPAIS = "PRATOS_PRINCIPAIS"
    FRITOS = "FRITOS"
    COZIDOS = "COZIDOS"
    PETISCOS = "PETISCOS"
    FRUTOS_DO_MAR = "FRUTOS_DO_MAR"
    BEBIDAS = "BEBIDAS"
    SOBREMESAS = "SOBREMESAS"
    LANCHES = "LANCHES"



   # Representa a entidade Produto no banco de dados.
   # Utilizada para gerenciar o cardápio ou estoque do sistema Raízes do Nordeste.

class Produto(Base):
    __tablename__ = "produtos"

    # Identificador único (Chave Primária) com indexação para buscas rápidas.
    id = Column(Integer, primary_key=True, index=True)

    # Nome do produto (obrigatório)
    nome = Column(String, nullable=False)

    # Detalhes do produto (opcional).
    descricao = Column(String, nullable=True)

    # Preço usando Numeric para precisão decimal (10 dígitos no total, 2 decimais).
    preco = Column(Numeric(10, 2), nullable=False)

    # Ajuste: Usando explicitamente o Enum para que o banco valide as categorias permitidas.
    categoria = Column(String, nullable=False)

    # Link para a foto do produto (opcional).
    imagem_url = Column(String, nullable=True)

    # Controle lógico de exclusão (soft delete) e disponibilidade.
    ativo = Column(Boolean, default=True)

    # Registro automático de data e hora de criação com fuso horário.
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# --- NOTA PARA O TCC / ADS ---
    # No futuro, para o modelo Multitenant, adicionaremos aqui:
    # empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)