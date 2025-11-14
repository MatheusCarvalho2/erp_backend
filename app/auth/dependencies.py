"""
Dependências do FastAPI para autenticação.
Segue Single Responsibility - apenas extração e validação de tokens.
"""
from typing import TYPE_CHECKING, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.service import AuthService
from app.auth.models import User
from app.auth.repository import IUserRepository

if TYPE_CHECKING:
    from app.auth.repository_supabase import SupabaseUserRepository

security: HTTPBearer = HTTPBearer()


def get_user_repository() -> IUserRepository:
    """
    Factory function para criar instância do repositório.
    Usa Supabase se configurado, caso contrário usa InMemoryUserRepository.
    Segue Open/Closed Principle - pode ser estendido sem modificar código existente.
    """
    from app.auth.config import supabase_config
    from app.auth.repository import InMemoryUserRepository

    # Verifica se Supabase está configurado
    if supabase_config.SUPABASE_URL and supabase_config.SUPABASE_KEY:
        try:
            from app.auth.repository_supabase import SupabaseUserRepository
            repo: SupabaseUserRepository = SupabaseUserRepository()
            print("✅ Conectado ao Supabase com sucesso!")
            print(f"📊 Repositório: SupabaseUserRepository")
            return repo
        except Exception as e:
            # Se houver erro ao conectar, usa repositório em memória como fallback
            import traceback
            print(f"❌ Erro ao conectar com Supabase: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            print("⚠️  ATENÇÃO: Usando repositório em memória como fallback.")
            print("⚠️  Os dados NÃO serão persistidos no Supabase!")
            print(f"📊 Repositório: InMemoryUserRepository (FALLBACK)")
            return InMemoryUserRepository()

    # Fallback para repositório em memória
    print("⚠️  Supabase não configurado. Usando repositório em memória.")
    print("⚠️  Os dados NÃO serão persistidos!")
    print(f"📊 Repositório: InMemoryUserRepository")
    return InMemoryUserRepository()


def get_auth_service(
    user_repository: IUserRepository = Depends(get_user_repository)
) -> AuthService:
    """
    Factory function para criar instância do AuthService.
    Segue Dependency Inversion Principle.
    """
    return AuthService(user_repository)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> User:
    """
    Dependency que extrai e valida o token JWT da requisição.
    Retorna o usuário autenticado ou levanta exceção HTTP.
    """
    token: str = credentials.credentials
    user: Optional[User] = await auth_service.get_current_user(token)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
