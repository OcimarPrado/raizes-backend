from sqlalchemy.orm import Session
from app.domain.audit_log import AuditLog

class AuditLogRepository:
    @staticmethod
    def registrar(db, acao, entidade, entidade_id=None, usuario_id=None, ip=None, detalhe=None):
        log = AuditLog(acao=acao, entidade=entidade, entidade_id=entidade_id,
                       usuario_id=usuario_id, ip=ip, detalhe=detalhe)
        db.add(log)
        return log

    @staticmethod
    def listar(db, entidade=None, usuario_id=None):
        q = db.query(AuditLog)
        if entidade:
            q = q.filter(AuditLog.entidade == entidade)
        if usuario_id:
            q = q.filter(AuditLog.usuario_id == usuario_id)
        return q.order_by(AuditLog.criado_em.desc()).all()
