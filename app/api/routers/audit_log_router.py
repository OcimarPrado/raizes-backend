from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.infrastructure.database.connection import get_db
from app.api.dependencies.auth import require_role
from app.application.schemas.audit_log import AuditLogResponse
from app.infrastructure.repositories.audit_log_repository import AuditLogRepository

router = APIRouter(prefix="/audit-logs", tags=["Auditoria"])

@router.get("/", response_model=list[AuditLogResponse], summary="Listar logs de auditoria (GERENTE)")
def listar_logs(
    entidade: Optional[str] = Query(None),
    usuario_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    _=Depends(require_role("GERENTE"))):
    return AuditLogRepository.listar(db=db, entidade=entidade, usuario_id=usuario_id)
