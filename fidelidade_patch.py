with open('app/application/pedido_service.py', 'r') as f:
    content = f.read()

content = content.replace(
    'if total_entregues % PEDIDOS_POR_CUPOM == 0:',
    'if total_entregues > 0 and total_entregues % PEDIDOS_POR_CUPOM == 0:'
)
content = content.replace(
    '''            historico = FidelidadeHistorico(
                usuario_id=pedido.usuario_id,
                pedido_id=pedido.id,
                tipo=TipoFidelidadeEnum.GANHO,
                cupons=1
            )''',
    '''            historico = FidelidadeHistorico(
                fidelidade_id=fidelidade.id,
                usuario_id=pedido.usuario_id,
                pedido_id=pedido.id,
                tipo=TipoFidelidadeEnum.GANHO,
                cupons=1
            )'''
)

with open('app/application/pedido_service.py', 'w') as f:
    f.write(content)
print("Patch aplicado.")
