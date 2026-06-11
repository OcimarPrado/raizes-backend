import json
from sqlalchemy.orm import Session
from app.domain.fidelidade import Fidelidade, FidelidadeHistorico, TipoFidelidadeEnum
from app.infrastructure.repositories.audit_log_repository import AuditLogRepository

PEDIDOS_POR_CUPOM = 10


class FidelidadeService:

    @staticmethod
    def obter_ou_criar(db: Session, usuario_id: int) -> Fidelidade:
        fidelidade = db.query(Fidelidade).filter(Fidelidade.usuario_id == usuario_id).first()
        if not fidelidade:
            fidelidade = Fidelidade(usuario_id=usuario_id, cupons_disponiveis=0)
            db.add(fidelidade)
            db.commit()
            db.refresh(fidelidade)
        return fidelidade

    @staticmethod
    def registrar_pedido_entregue(db: Session, usuario_id: int, pedido_id: int, ip: str | None = None):
        fidelidade = FidelidadeService.obter_ou_criar(db, usuario_id)

        # Conta pedidos entregues do usuário
        from app.domain.pedido import Pedido, StatusPedidoEnum
        total_entregues = db.query(Pedido).filter(
            Pedido.usuario_id == usuario_id,
            Pedido.status == StatusPedidoEnum.ENTREGUE,
        ).count()

        # Gera cupom a cada 10 pedidos entregues
        cupons_devidos = total_entregues // PEDIDOS_POR_CUPOM
        cupons_ja_ganhos = db.query(FidelidadeHistorico).filter(
            FidelidadeHistorico.fidelidade_id == fidelidade.id,
            FidelidadeHistorico.tipo == TipoFidelidadeEnum.GANHO,
        ).count()

        novos_cupons = cupons_devidos - cupons_ja_ganhos
        if novos_cupons <= 0:
            return fidelidade

        fidelidade.cupons_disponiveis += novos_cupons
        historico = FidelidadeHistorico(
            fidelidade_id=fidelidade.id,
            usuario_id=usuario_id,
            pedido_id=pedido_id,
            tipo=TipoFidelidadeEnum.GANHO,
            cupons=novos_cupons,
        )
        db.add(historico)

        AuditLogRepository.registrar(
            db=db,
            acao="CUPOM_GERADO",
            entidade="fidelidade",
            entidade_id=fidelidade.id,
            usuario_id=usuario_id,
            ip=ip,
            detalhe=json.dumps({
                "pedido_id": pedido_id,
                "novos_cupons": novos_cupons,
                "total_cupons": fidelidade.cupons_disponiveis,
            }, ensure_ascii=False),
        )
        db.commit()
        db.refresh(fidelidade)
        return fidelidade

    @staticmethod
    def listar_historico(db: Session, usuario_id: int) -> list:
        fidelidade = db.query(Fidelidade).filter(Fidelidade.usuario_id == usuario_id).first()
        if not fidelidade:
            return []
        return db.query(FidelidadeHistorico).filter(
            FidelidadeHistorico.fidelidade_id == fidelidade.id
        ).order_by(FidelidadeHistorico.created_at.desc()).all()
