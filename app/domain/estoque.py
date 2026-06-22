from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text
)

from app.infrastructure.database.connection import Base


class AuditLog(Base):
    """
    Entidade responsável por armazenar os registros de auditoria do sistema.

    O objetivo desta tabela é manter um histórico das ações realizadas
    pelos usuários, permitindo rastreabilidade, controle operacional
    e apoio em processos de auditoria e segurança.

    Cada registro representa um evento importante ocorrido no sistema.
    """

    # Nome da tabela que será criada no banco de dados.
    __tablename__ = "audit_logs"

    # Identificador único do registro de auditoria.
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Usuário responsável pela ação registrada.
    # Pode ser nulo em situações onde a ação foi executada
    # automaticamente pelo sistema.
    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=True
    )

    # Descreve a ação executada.
    # Exemplos:
    # - CRIAR
    # - EDITAR
    # - EXCLUIR
    # - LOGIN
    # - PAGAMENTO_APROVADO
    acao = Column(
        String(100),
        nullable=False
    )

    # Identifica qual entidade do sistema foi afetada.
    # Exemplos:
    # - Usuario
    # - Pedido
    # - Produto
    # - Pagamento
    entidade = Column(
        String(50),
        nullable=False
    )

    # Identificador do registro afetado pela operação.
    # Permite localizar exatamente qual objeto sofreu alteração.
    entidade_id = Column(
        Integer,
        nullable=True
    )

    # Campo livre para armazenar informações adicionais
    # sobre o evento ocorrido.
    #
    # Exemplos:
    # - Valores alterados
    # - Motivo da operação
    # - Dados relevantes para investigação futura
    detalhe = Column(
        Text,
        nullable=True
    )

    # Endereço IP de origem da ação.
    # Auxilia em auditorias, monitoramento e rastreamento
    # de operações realizadas pelos usuários.
    ip = Column(
        String(45),
        nullable=True
    )

    # Data e horário em que o evento foi registrado.
    # O horário é armazenado em UTC para manter
    # consistência entre diferentes regiões e servidores.
    criado_em = Column(
        DateTime,
        default=datetime.utcnow)