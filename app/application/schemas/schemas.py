
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional
from app.domain.usuario import RoleEnum

# Schema base com campos comuns
class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    cpf: str = Field(..., min_length=11, max_length=11)
    telefone: Optional[str] = None
    role: RoleEnum = RoleEnum.CLIENTE

# Schema para criação (Recebe a senha pura)
class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., min_length=6)

# Schema para resposta (Não envia a senha, envia o ID e datas)
class UsuarioResponse(UsuarioBase):
    id: int
    ativo: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True) # Permite ler do SQLAlchemy