
from sqlalchemy.orm import Session
from app.domain.usuario import Usuario
from app.application.usuario_schema import UsuarioCreate

class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar(self, usuario_in: UsuarioCreate, senha_hash: str) -> Usuario:
        db_usuario = Usuario(
            nome=usuario_in.nome,
            email=usuario_in.email,
            cpf=usuario_in.cpf,
            telefone=usuario_in.telefone,
            senha_hash=senha_hash,
            role=usuario_in.role
        )
        self.db.add(db_usuario)
        self.db.commit()
        self.db.refresh(db_usuario)
        return db_usuario

    def buscar_por_email(self, email: str) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.email == email).first()

    def buscar_por_id(self, usuario_id: int) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()