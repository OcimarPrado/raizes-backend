import random, uuid, json
from sqlalchemy.orm import Session
from app.domain.pedido import Pagamento, Pedido, StatusPedidoEnum
from app.application.schemas.pagamento import PagamentoCreate
from app.infrastructure.repositories.audit_log_repository import AuditLogRepository

METODOS_GARANTIDOS = {"PIX", "DINHEIRO"}
MOTIVOS_RECUSA = ["Saldo insuficiente", "Cartão bloqueado", "Limite diário atingido", "Não autorizada pelo banco"]
'''
Gerencia o processamento de pagamento, qualificando APROVADO e NÃO APROVADO, com alguns tratamentos de regras de negócio.
'''
class PagamentoService:
    @staticmethod
    def processar(db: Session, dados: PagamentoCreate, usuario_id: int, ip) -> Pagamento:
        dados.validate_metodo()
        pedido = db.query(Pedido).filter(Pedido.id == dados.pedido_id).first()
        if not pedido:
            raise ValueError(f"Pedido {dados.pedido_id} não encontrado.")
        if pedido.status == StatusPedidoEnum.CANCELADO:
            raise ValueError("Não é possível pagar um pedido cancelado.")
        if db.query(Pagamento).filter(Pagamento.pedido_id == dados.pedido_id, Pagamento.status == "APROVADO").first():
            raise ValueError("Este pedido já possui um pagamento aprovado.")

        aprovado = dados.metodo in METODOS_GARANTIDOS or random.random() > 0.20
        status = "APROVADO" if aprovado else "RECUSADO"
        resposta = str(uuid.uuid4()).replace("-","")[:20].upper() if aprovado else random.choice(MOTIVOS_RECUSA)

        pagamento = Pagamento(pedido_id=dados.pedido_id, metodo=dados.metodo,
                              status=status, valor=pedido.total, resposta_mock=resposta)
        db.add(pagamento)
        if aprovado:
            pedido.status = StatusPedidoEnum.CONFIRMADO
        db.flush()
        AuditLogRepository.registrar(db=db, acao="PAGAMENTO_PROCESSADO", entidade="pagamento",
            entidade_id=pagamento.id, usuario_id=usuario_id, ip=ip,
            detalhe=json.dumps({"pedido_id": dados.pedido_id, "metodo": dados.metodo,
                                "status": status, "valor": float(pedido.total)}, ensure_ascii=False))
        db.commit()
        db.refresh(pagamento)
        return pagamento
