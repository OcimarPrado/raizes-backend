from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.infrastructure.database.connection import get_db
from app.api.dependencies.auth import require_role
from app.application.schemas.audit_log import AuditLogResponse
from app.infrastructure.repositories.audit_log_repository import AuditLogRepository

# Cria um agrupamento de rotas responsável pelas funcionalidades
# relacionadas aos registros de auditoria do sistema.
#
# O prefixo "/audit-logs" será adicionado automaticamente a todas as rotas
# deste arquivo e a tag "Auditoria" será utilizada na documentação Swagger.
router = APIRouter(
    prefix="/audit-logs",
    tags=["Auditoria"]
)


@router.get(
    "/",
    response_model=list[AuditLogResponse],
    summary="Listar logs de auditoria (GERENTE)"
)
def listar_logs(
    entidade: Optional[str] = Query(None),
    usuario_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    _=Depends(require_role("GERENTE"))
):
    """
    Retorna os registros de auditoria armazenados no sistema.

    Esta rota permite que usuários com perfil GERENTE consultem
    o histórico de ações realizadas, auxiliando no controle,
    rastreabilidade e segurança das operações.

    Filtros opcionais:
    - entidade: retorna apenas logs relacionados a uma entidade específica.
    - usuario_id: retorna apenas logs gerados por determinado usuário.

    O retorno é uma lista contendo os registros encontrados.
    """

    # Consulta os logs de auditoria aplicando os filtros informados.
    # Caso nenhum filtro seja enviado, todos os registros serão retornados.
    return AuditLogRepository.listar(
        db=db,
        entidade=entidade,
        usuario_id=usuario_id
    )