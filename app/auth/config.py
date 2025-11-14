"""
Configurações do módulo de autenticação.
Em produção, essas configurações devem vir de variáveis de ambiente.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env ANTES de ler as variáveis
load_dotenv()


class AuthConfig:
    """Configurações de autenticação"""

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    def __init__(self) -> None:
        self.SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
        self.ALGORITHM = os.getenv("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


class SupabaseConfig:
    """Configurações do Supabase"""

    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_SERVICE_KEY: Optional[str]

    def __init__(self) -> None:
        self.SUPABASE_URL = os.getenv("SUPABASE_URL", "")
        self.SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
        self.SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", None)


auth_config: AuthConfig = AuthConfig()
supabase_config: SupabaseConfig = SupabaseConfig()
