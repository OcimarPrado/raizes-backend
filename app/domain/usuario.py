import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum 
from sqlalchemy.sql import func
from app.infrastructure.database.connection import Base

# Os perfis de acesso são controlados via Enum no domínio da aplicação,
# impedindo valores arbitrários e garantindo consistência no controle de autorização. 
class RoleEnum (str, enum.Enum):
	CLIENTE = "CLIENTE"
	ATENDENTE = "ATENDENTE"
	GERENTE = "GERENTE"

class Usuario(Base):
	__tablename__="usuarios"

	id = Column(Integer, primary_key=True, index=True)
	nome = Column(String, nullable=False)
	email = Column(String, unique=True, nullable=False, index=True)
	senha_hash = Column(String, nullable=False) 
	cpf = Column(String(11), unique=True, nullable=False)
	telefone = Column(String(15), nullable=True)
	role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.CLIENTE)
	ativo = Column(Boolean, default=True)
	created_at = Column(DateTime(timezone=True), server_default=func.now())
# As senhas dos usuários são armazenadas exclusivamente em formato hash bc>
# garantindo que nem a equipe técnica tenha acesso à senha original,
# em conformidade com o princípio de segurança da LGPD.
# Index no  ID e EMAIL para facilitar as buscas no login
# Deixei o telefone como opcional,
# entendendo que esse quesito não se faz obrigatório
# para o pleno funcionamento do nosso software.
