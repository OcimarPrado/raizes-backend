import os
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
from pathlib import Path

# Carrega as variáveis de ambiente do arquivo .env na raiz do projeto.
# Em produção, essas variáveis devem ser configuradas diretamente
# no servidor, nunca expostas no código-fonte.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

# Chave secreta utilizada para assinar os tokens JWT.
# Lida do ambiente para evitar exposição de dados sensíveis no código.
SECRET_KEY = os.getenv("SECRET_KEY", "chave_padrao_apenas_para_desenvolvimento")

# Algoritmo de assinatura do JWT.
# HS256 é o padrão mais utilizado para APIs REST.
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Tempo de expiração do token em minutos.
# Após esse período, o usuário precisará fazer login novamente.
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# Contexto de hash de senha utilizando bcrypt.
# O bcrypt é recomendado pela LGPD e pelas boas práticas de segurança
# pois é resistente a ataques de força bruta e rainbow tables.
# A opção "deprecated=auto" garante que hashes antigos sejam atualizados
# automaticamente quando o usuário fizer login.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verificar_senha(senha_pura: str, senha_hash: str) -> bool:
    """
    Compara a senha digitada pelo usuário com o hash armazenado no banco.

    Nunca comparamos senhas em texto puro — o bcrypt faz isso de forma
    segura, sem precisar descriptografar o hash.
    """
    return pwd_context.verify(senha_pura, senha_hash)


def criar_token_acesso(data: dict) -> str:
    """
    Gera um Token JWT assinado com as informações do usuário autenticado.

    O token carrega o e-mail e o perfil (role) do usuário, permitindo
    que as rotas protegidas identifiquem quem está fazendo a requisição
    sem precisar consultar o banco a cada chamada.

    O token expira automaticamente após o tempo configurado no .env,
    forçando o usuário a se autenticar novamente após esse período.
    """
    dados = data.copy()

    # Define o momento exato em que o token deixará de ser válido.
    expiracao = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados.update({"exp": expiracao})

    # Assina e codifica o token com a chave secreta da aplicação.
    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)
