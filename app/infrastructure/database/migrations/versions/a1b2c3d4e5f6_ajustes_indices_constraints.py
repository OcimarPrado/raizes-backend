"""ajustes_indices_constraints_e_triggers

Revision ID: a1b2c3d4e5f6
Revises: 9fc249a2c79e
Create Date: 2026-06-08 10:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '9fc249a2c79e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_index('idx_pedidos_status',   'pedidos', ['status'],     unique=False)
    op.create_index('idx_pedidos_usuario',  'pedidos', ['usuario_id'], unique=False)
    op.create_index('idx_produtos_categoria', 'produtos', ['categoria'], unique=False)
    op.create_index('idx_produtos_ativo',     'produtos', ['ativo'],     unique=False)
    op.create_index('idx_fid_hist_usuario', 'fidelidade_historico', ['usuario_id'], unique=False)
    op.create_unique_constraint('uq_produto_unidade', 'estoques', ['produto_id', 'unidade_id'])

    op.execute("""
        CREATE OR REPLACE FUNCTION atualizar_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)
    op.execute("""
        CREATE TRIGGER trg_pedidos_updated_at
            BEFORE UPDATE ON pedidos
            FOR EACH ROW EXECUTE FUNCTION atualizar_updated_at();
    """)
    op.execute("""
        CREATE TRIGGER trg_estoques_updated_at
            BEFORE UPDATE ON estoques
            FOR EACH ROW EXECUTE FUNCTION atualizar_updated_at();
    """)
    op.execute("""
        CREATE TRIGGER trg_fidelidade_updated_at
            BEFORE UPDATE ON fidelidade
            FOR EACH ROW EXECUTE FUNCTION atualizar_updated_at();
    """)

    op.execute("""
        INSERT INTO unidades (nome, cidade, estado, endereco) VALUES
            ('Unidade Centro',  'Fortaleza', 'CE', 'Rua Floriano Peixoto, 500'),
            ('Unidade Aldeota', 'Fortaleza', 'CE', 'Av. Santos Dumont, 1200'),
            ('Unidade Recife',  'Recife',    'PE', 'Rua da Aurora, 300');
    """)

    op.execute("""
        INSERT INTO usuarios (nome, email, senha_hash, cpf, role) VALUES
            ('Admin', 'gerente@raizes.com',
             '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
             '00000000000', 'GERENTE');
    """)

    op.execute("""
        INSERT INTO usuarios (nome, email, senha_hash, cpf, telefone, role) VALUES
            ('João Silva', 'joao@email.com',
             '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
             '12345678901', '85999990001', 'CLIENTE');
    """)

    op.execute("""
        INSERT INTO produtos (nome, descricao, preco, categoria) VALUES
            ('Baião de Dois',      'Arroz, feijão-verde, queijo coalho e carne seca', 28.90, 'PRATOS_PRINCIPAIS'),
            ('Carne de Sol',       'Grelhada com manteiga de garrafa',                39.90, 'PRATOS_PRINCIPAIS'),
            ('Tapioca Recheada',   'Queijo e carne seca',                             18.50, 'LANCHES'),
            ('Macaxeira Cozida',   'Com manteiga',                                    12.00, 'COZIDOS'),
            ('Acarajé',            'Feijão-fradinho frito com vatapá',                15.00, 'FRITOS'),
            ('Dadinho de Tapioca', 'Com geleia de pimenta',                           22.00, 'PETISCOS'),
            ('Camarão Nordestino', 'Salteado com coco e coentro',                     52.00, 'FRUTOS_DO_MAR'),
            ('Suco de Cajá',       '400ml',                                            9.00, 'BEBIDAS'),
            ('Umbuzada',           '300ml',                                            8.00, 'BEBIDAS'),
            ('Cocada',             'Doce tradicional de coco',                         7.50, 'SOBREMESAS');
    """)

    op.execute("""
        INSERT INTO estoques (produto_id, unidade_id, quantidade_disponivel, quantidade_minima)
        SELECT id, 1, 50, 10 FROM produtos;
    """)

    op.execute("""
        INSERT INTO fidelidade (usuario_id, cupons_disponiveis)
        SELECT id, 0 FROM usuarios WHERE email = 'joao@email.com';
    """)

def downgrade() -> None:
    op.execute("DELETE FROM fidelidade;")
    op.execute("DELETE FROM estoques;")
    op.execute("DELETE FROM produtos;")
    op.execute("DELETE FROM usuarios WHERE email IN ('gerente@raizes.com', 'joao@email.com');")
    op.execute("DELETE FROM unidades;")
    op.execute("DROP TRIGGER IF EXISTS trg_fidelidade_updated_at ON fidelidade;")
    op.execute("DROP TRIGGER IF EXISTS trg_estoques_updated_at ON estoques;")
    op.execute("DROP TRIGGER IF EXISTS trg_pedidos_updated_at ON pedidos;")
    op.execute("DROP FUNCTION IF EXISTS atualizar_updated_at;")
    op.drop_constraint('uq_produto_unidade', 'estoques', type_='unique')
    op.drop_index('idx_fid_hist_usuario', table_name='fidelidade_historico')
    op.drop_index('idx_produtos_ativo',     table_name='produtos')
    op.drop_index('idx_produtos_categoria', table_name='produtos')
    op.drop_index('idx_pedidos_usuario',  table_name='pedidos')
    op.drop_index('idx_pedidos_status',   table_name='pedidos')
