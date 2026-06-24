import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.connection import Base


# Definimos os tipos de movimentação como Enum para garantir que
# apenas valores válidos sejam registrados no banco.
# ENTRADA = produtos chegando ao estoque
# SAIDA = produtos saindo (venda, descarte, etc.)
class TipoMovimentacaoEnum(str, enum.Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"


class Estoque(Base):
    """
    Representa o saldo de um produto em uma unidade específica da rede.

    Cada unidade da rede Raízes do Nordeste mantém seu próprio controle
    de estoque por produto. Isso significa que o mesmo produto pode ter
    quantidades diferentes em cada loja.

    Exemplo: Baião de Dois pode ter 50 unidades no Centro e 30 na Aldeota.
    """

    __tablename__ = "estoques"

    # Identificador único deste registro de estoque.
    id = Column(Integer, primary_key=True, index=True)

    # Qual produto estamos controlando neste registro.
    produto_id = Column(
        Integer,
        ForeignKey("produtos.id"),
        nullable=False
    )

    # Em qual unidade da rede esse estoque pertence.
    unidade_id = Column(
        Integer,
        ForeignKey("unidades.id"),
        nullable=False
    )

    # Quantidade atual disponível para venda nesta unidade.
    # Esse valor é atualizado a cada entrada ou saída registrada.
    quantidade_disponivel = Column(Integer, nullable=False, default=0)

    # Quantidade mínima de alerta. Quando o estoque ficar abaixo
    # desse valor, o gerente deve ser notificado para repor.
    quantidade_minima = Column(Integer, nullable=False, default=5)

    # Data da última atualização deste registro de estoque.
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relacionamentos para facilitar consultas no ORM
    produto = relationship("Produto")
    unidade = relationship("Unidade")
    movimentacoes = relationship("EstoqueMovimentacao", back_populates="estoque")


class EstoqueMovimentacao(Base):
    """
    Registra cada entrada ou saída de produtos no estoque.

    Toda vez que um produto entra ou sai do estoque de uma unidade,
    um registro é criado aqui. Isso permite rastrear o histórico
    completo de movimentações e auditar qualquer divergência.

    Exemplos de uso:
    - Recebimento de mercadoria: ENTRADA de 100 unidades de Baião de Dois
    - Venda realizada: SAIDA de 2 unidades ao criar um pedido
    - Descarte por vencimento: SAIDA com observação explicando o motivo
    """

    __tablename__ = "estoque_movimentacoes"

    # Identificador único da movimentação.
    id = Column(Integer, primary_key=True, index=True)

    # Qual registro de estoque foi afetado por esta movimentação.
    estoque_id = Column(
        Integer,
        ForeignKey("estoques.id"),
        nullable=False
    )

    # Tipo da movimentação: entrada (acréscimo) ou saída (decréscimo).
    tipo = Column(
        Enum(TipoMovimentacaoEnum),
        nullable=False
    )

    # Quantidade de unidades movimentadas nesta operação.
    quantidade = Column(Integer, nullable=False)

    # Campo opcional para registrar o motivo ou contexto da movimentação.
    # Exemplos: "Pedido #42", "Recebimento NF 1234", "Descarte - vencimento"
    observacao = Column(String, nullable=True)

    # Data e hora em que a movimentação foi registrada.
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relacionamento com o registro de estoque pai.
    estoque = relationship("Estoque", back_populates="movimentacoes")
