
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.usuario_repository import UsuarioRepository
from app.application.usuario_service import UsuarioService
from app.application.schemas.usuario_schema import UsuarioCreate, UsuarioResponse
from app.api.dependencies.auth import get_current_user
from app.domain.usuario import Usuario

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    repository = UsuarioRepository(db)
    service = UsuarioService(repository)
    return service.criar_novo_usuario(usuario)

@router.get("/me", response_model=UsuarioResponse)
def ler_meus_dados(current_user: Usuario = Depends(get_current_user)):
    """
    Retorna os dados do usuário que está atualmente logado.
    Note que esta rota só funciona se um Token válido for enviado.
    """
    return current_user