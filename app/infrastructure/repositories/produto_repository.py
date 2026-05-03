from sqlalchemy.orm import Session
from app.domain.produto import Produto

class ProdutoRepository:
    """
    Esta classe é como um manual de instruções para mexer na tabela de produtos.
    Ela garante que a gente não precise escrever comandos complexos toda hora.
    """
    def __init__(self, db: Session):
        # Aqui a gente recebe a 'chave' do banco de dados (a sessão)
        self.db = db

    def salvar_no_banco(self, produto_dados: Produto):
        """
        Pega as informações do produto e guarda na prateleira do banco de dados.
        """
        # 1. Avisa ao banco que tem um item novo para guardar
        self.db.add(produto_dados)
        # 2. Confirma a gravação (como dar um 'Enter' ou salvar o arquivo)
        self.db.commit()
        # 3. Atualiza o item com as informações que o banco gerou (como o ID)
        self.db.refresh(produto_dados)
        # 4. Devolve o produto prontinho
        return produto_dados

    def listar_tudo(self):
        """
        Vai até a prateleira e traz a lista de todos os produtos cadastrados.
        """
        return self.db.query(Produto).all()
