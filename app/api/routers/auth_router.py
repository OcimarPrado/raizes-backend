from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.usuario_repository import UsuarioRepository
from app.application.usuario_service import UsuarioService

# Agrupa todas as rotas relacionadas à autenticação e controle de acesso.
# O prefixo "/auth" será adicionado automaticamente a todas as rotas
# definidas neste arquivo.
router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)


@router.post("/login")
def login(
    # O FastAPI extrai automaticamente os campos "username" e "password"
    # enviados no formulário da requisição.
    # Neste projeto, o campo username representa o e-mail do usuário.
    form_data: OAuth2PasswordRequestForm = Depends(),

    # Disponibiliza uma sessão ativa com o banco de dados
    # durante a execução da requisição.
    db: Session = Depends(get_db)
):
    """
    Realiza a autenticação do usuário.

    Fluxo:
    1. Recebe o e-mail e a senha enviados pelo cliente.
    2. Encaminha os dados para a camada de serviço.
    3. Valida as credenciais informadas.
    4. Gera um Token JWT quando a autenticação é bem-sucedida.
    5. Retorna o token para ser utilizado nas rotas protegidas.

    Este endpoint é o ponto de entrada para acesso ao sistema.
    """

    # Instancia o repositório responsável pela comunicação
    # com a tabela de usuários.
    repository = UsuarioRepository(db)

    # Instancia a camada de serviço, onde ficam as regras
    # de negócio relacionadas aos usuários.
    service = UsuarioService(repository)

    # Executa o processo de autenticação.
    #
    # O OAuth2PasswordRequestForm utiliza o campo "username"
    # por padrão, porém neste sistema ele representa o e-mail
    # utilizado para login.
    token_data = service.autenticar_usuario(
        email=form_data.username,
        senha_pura=form_data.password
    )

    # Retorna o token JWT gerado após a validação das credenciais.
    # Esse token deverá ser enviado pelo cliente nas próximas
    # requisições para acessar recursos protegidos.
    return token_data