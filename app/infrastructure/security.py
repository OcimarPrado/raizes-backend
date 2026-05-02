
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# CHAVE_MESTRA: Em produção, isso deve vir de uma variável de ambiente (.env)
SECRET_KEY = "sua_chave_secreta_super_segura_nordestina"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_senha(senha_pura, senha_hash):
    return pwd_context.verify(senha_pura, senha_hash)

def criar_token_acesso(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)