with open('app/application/pedido_service.py', 'r') as f:
    content = f.read()

old = '''    def _processar_fidelidade(self, pedido: Pedido):
        # conta pedidos entregues do cliente
        total_entregues = self.db.query(Pedido).filter(
            Pedido.usuario_id == pedido.usuario_id,
            Pedido.status == StatusPedidoEnum.ENTREGUE
        ).count()

        # ganha cupom a cada PEDIDOS_POR_CUPOM entregas (nunca no zero)
        if total_entregues > 0 and total_entregues % PEDIDOS_POR_CUPOM == 0:
            fidelidade = self.db.query(Fidelidade).filter(
                Fidelidade.usuario_id == pedido.usuario_id
            ).first()

            if not fidelidade:
                fidelidade = Fidelidade(usuario_id=pedido.usuario_id, cupons_disponiveis=0)
                self.db.add(fidelidade)
                self.db.flush()

            fidelidade.cupons_disponiveis += 1

            historico = FidelidadeHistorico(
                fidelidade_id=fidelidade.id,
                usuario_id=pedido.usuario_id,
                pedido_id=pedido.id,
                tipo=TipoFidelidadeEnum.GANHO,
                cupons=1
            )
            self.db.add(historico)
            self.db.commit()'''

new = '''    def _processar_fidelidade(self, pedido: Pedido):
        # Conta pedidos entregues do cliente
        total_entregues = self.db.query(Pedido).filter(
            Pedido.usuario_id == pedido.usuario_id,
            Pedido.status == StatusPedidoEnum.ENTREGUE
        ).count()

        if total_entregues == 0:
            return

        # Obtém ou cria registro de fidelidade
        fidelidade = self.db.query(Fidelidade).filter(
            Fidelidade.usuario_id == pedido.usuario_id
        ).first()

        if not fidelidade:
            fidelidade = Fidelidade(usuario_id=pedido.usuario_id, cupons_disponiveis=0)
            self.db.add(fidelidade)
            self.db.flush()

        # Calcula cupons devidos vs cupons já ganhos
        cupons_devidos = total_entregues // PEDIDOS_POR_CUPOM
        cupons_ganhos = self.db.query(FidelidadeHistorico).filter(
            FidelidadeHistorico.fidelidade_id == fidelidade.id,
            FidelidadeHistorico.tipo == TipoFidelidadeEnum.GANHO
        ).count()

        novos_cupons = cupons_devidos - cupons_ganhos
        if novos_cupons <= 0:
            return

        # Registra os cupons novos
        fidelidade.cupons_disponiveis += novos_cupons

        historico = FidelidadeHistorico(
            fidelidade_id=fidelidade.id,
            usuario_id=pedido.usuario_id,
            pedido_id=pedido.id,
            tipo=TipoFidelidadeEnum.GANHO,
            cupons=novos_cupons
        )
        self.db.add(historico)
        self.db.commit()'''

if old in content:
    content = content.replace(old, new)
    with open('app/application/pedido_service.py', 'w') as f:
        f.write(content)
    print("Patch aplicado com sucesso.")
else:
    print("ERRO: trecho não encontrado. Verifique o arquivo manualmente.")
