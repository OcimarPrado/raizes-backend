
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.usuario_repository import UsuarioRepository
from app.application.usuario_service import UsuarioService
from app.application.schemas.usuario_schema import UsuarioCreate, UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    repository = UsuarioRepository(db)
    service = UsuarioService(repository)
    return service.criar_novo_usuario(usuario)