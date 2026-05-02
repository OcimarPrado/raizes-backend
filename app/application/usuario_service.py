
from passlib.context import CryptContext
from app.infrastructure.repositories.usuario_repository import UsuarioRepository
from app.application.schemas.usuario_schema import UsuarioCreate
from fastapi import HTTPException, status
from app.infrastructure.security import verificar_senha, criar_token_acesso

# Configuração do Hash
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UsuarioService:
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def criar_novo_usuario(self, usuario_in: UsuarioCreate):
        # 1. Regra de Negócio: Verificar se o e-mail já existe
        usuario_existente = self.repository.buscar_por_email(usuario_in.email)
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe um usuário cadastrado com este e-mail."
            )

        # 2. Segurança: Transformar senha em Hash
        senha_hash = pwd_context.hash(usuario_in.senha)

        # 3. Persistência: Chamar o repositório para salvar
        return self.repository.criar(usuario_in, senha_hash)
    
    def autenticar_usuario(self, email: str, senha_pura: str):
        usuario = self.repository.buscar_por_email(email)
        if not usuario or not verificar_senha(senha_pura, usuario.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha incorreta",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        token = criar_token_acesso(data={"sub": usuario.email, "role": usuario.role.value})
        return {"access_token": token, "token_type": "bearer"}

  