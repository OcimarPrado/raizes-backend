
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.usuario_repository import UsuarioRepository
from app.application.usuario_service import UsuarioService

# Define o prefixo /auth para organizar as rotas de segurança
router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login")
def login(
    # O OAuth2PasswordRequestForm extrai automaticamente 'username' e 'password' da requisição
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """
    Endpoint para autenticar usuários. 
    Recebe as credenciais e retorna um Token JWT se forem válidas.
    """
    
    # 1. Instancia as camadas necessárias (Repository -> Service)
    repository = UsuarioRepository(db)
    service = UsuarioService(repository)
    
    # 2. Chama a lógica de autenticação que criamos no Service
    # Importante: O OAuth2PasswordRequestForm usa 'username' para o campo de login (seu e-mail)
    token_data = service.autenticar_usuario(
        email=form_data.username, 
        senha_pura=form_data.password
    )
    
    # 3. Retorna o token de acesso (Bearer Token)
    return token_data