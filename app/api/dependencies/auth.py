from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.usuario_repository import UsuarioRepository
from app.infrastructure.security import SECRET_KEY, ALGORITHM

# Configura o mecanismo de autenticação baseado em Bearer Token.
# O FastAPI utilizará o endpoint "/auth/login" como referência
# para obtenção do token durante a documentação interativa (Swagger).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Responsável por identificar o usuário autenticado.

    Fluxo:
    1. Recebe o token JWT enviado na requisição.
    2. Valida e decodifica o token.
    3. Recupera o e-mail armazenado no campo 'sub'.
    4. Busca o usuário no banco de dados.
    5. Retorna o usuário autenticado para utilização na rota.

    Caso qualquer etapa falhe, o acesso é negado.
    """

    # Exceção padrão utilizada quando o token é inválido,
    # expirado ou quando o usuário não pode ser identificado.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodifica o JWT utilizando a chave secreta da aplicação.
        # Se o token tiver sido alterado ou estiver inválido,
        # uma exceção será lançada.
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Recupera o e-mail armazenado como assunto (subject)
        # do token JWT. Esse valor identifica o usuário.
        email: str = payload.get("sub")

        # Se o token não possuir o identificador do usuário,
        # ele é considerado inválido.
        if email is None:
            raise credentials_exception

    except JWTError:
        # Captura qualquer erro relacionado ao JWT,
        # como assinatura inválida ou token expirado.
        raise credentials_exception

    # Após validar o token, confirma se o usuário ainda existe
    # no banco de dados. Isso evita acesso com tokens válidos
    # de usuários removidos ou desativados.
    repository = UsuarioRepository(db)
    usuario = repository.buscar_por_email(email)

    if usuario is None:
        raise credentials_exception

    # Retorna o objeto do usuário autenticado para ser utilizado
    # pelas rotas protegidas.
    return usuario


def require_role(role: str):
    """
    Cria uma dependência para controle de autorização baseado em perfil.

    Exemplo:
        Depends(require_role("admin"))

    Somente usuários com o perfil informado poderão acessar a rota.
    """

    def dependency(current_user=Depends(get_current_user)):

        # Verifica se o perfil do usuário autenticado corresponde
        # ao perfil exigido pela rota.
        if current_user.role.value != role:

            from fastapi import HTTPException, status

            # O usuário está autenticado, porém não possui
            # permissão suficiente para executar a ação.
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso restrito a {role}."
            )

        return current_user

    return dependency