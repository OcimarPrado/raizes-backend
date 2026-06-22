from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.usuario_repository import UsuarioRepository
from app.application.usuario_service import UsuarioService
from app.application.schemas.usuario_schema import (
    UsuarioCreate,
    UsuarioResponse
)
from app.api.dependencies.auth import get_current_user
from app.domain.usuario import Usuario

# Agrupa todas as rotas relacionadas ao gerenciamento
# e consulta de usuários do sistema.
router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


@router.post(
    "/",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED
)
def cadastrar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):
    """
    Realiza o cadastro de um novo usuário no sistema.

    Regras de negócio:
    - Os dados recebidos devem atender às validações definidas no schema.
    - A lógica de criação é executada pela camada de serviço.
    - O usuário recém-criado é retornado ao cliente.
    """

    # Cria uma instância do repositório responsável
    # pelo acesso aos dados dos usuários.
    repository = UsuarioRepository(db)

    # Cria a camada de serviço responsável pelas
    # regras de negócio relacionadas aos usuários.
    service = UsuarioService(repository)

    # Executa o processo de cadastro do usuário.
    return service.criar_novo_usuario(usuario)


@router.get(
    "/me",
    response_model=UsuarioResponse
)
def ler_meus_dados(
    current_user: Usuario = Depends(get_current_user)
):
    """
    Retorna os dados do usuário autenticado.

    Regras de negócio:
    - A rota exige autenticação válida.
    - O usuário acessa apenas seus próprios dados.
    - As informações retornadas são obtidas a partir
      do token enviado na requisição.

    Esta funcionalidade é normalmente utilizada para
    exibir informações do perfil do usuário logado.
    """

    # O objeto do usuário já foi validado e recuperado
    # pela dependência de autenticação.
    return current_user