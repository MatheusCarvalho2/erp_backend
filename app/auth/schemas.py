"""
Schemas para validação de dados de entrada e saída da API de autenticação.
Segue o princípio de Single Responsibility - apenas validação de dados.
"""
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema para criação de usuário"""
    email: EmailStr
    password: str = Field(
        ...,
        min_length=6,
        max_length=72,
        description="Senha deve ter entre 6 e 72 caracteres"
    )
    name: str = Field(..., min_length=2, max_length=100)


class UserLogin(BaseModel):
    """Schema para login de usuário"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Schema de resposta com token de acesso"""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Schema de resposta com dados do usuário"""
    id: int
    email: str
    name: str

    class Config:
        from_attributes = True
