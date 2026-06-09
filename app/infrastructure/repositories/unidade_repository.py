from sqlalchemy.orm import Session
from app.domain.unidade import Unidade

class UnidadeRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_todas(self):
        return self.db.query(Unidade).filter(Unidade.ativa == True).all()

    def buscar_por_id(self, unidade_id: int):
        return self.db.query(Unidade).filter(Unidade.id == unidade_id).first()
