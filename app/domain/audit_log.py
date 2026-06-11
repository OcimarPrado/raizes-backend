from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from app.infrastructure.database.connection import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    acao = Column(String(100), nullable=False)
    entidade = Column(String(50), nullable=False)
    entidade_id = Column(Integer, nullable=True)
    detalhe = Column(Text, nullable=True)
    ip = Column(String(45), nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
