
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.usuario_repository import UsuarioRepository
from app.infrastructure.security import SECRET_KEY, ALGORITHM

# Define onde o FastAPI deve procurar o token (no endpoint /auth/login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Decodifica o token JWT, verifica se é válido e retorna o usuário do banco.
    Esta função será usada como dependência em rotas protegidas.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 1. Tenta decodificar o token usando sua chave secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # 2. Busca o usuário no banco de dados para confirmar que ele ainda existe
    repository = UsuarioRepository(db)
    usuario = repository.buscar_por_email(email)
    
    if usuario is None:
        raise credentials_exception
        
    return usuario