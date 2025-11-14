"""
Implementação do repositório de usuários usando Supabase.
Segue Liskov Substitution Principle - pode substituir IUserRepository.
"""
from typing import Optional, Any
from datetime import datetime
from supabase import create_client, Client
from app.auth.models import User
from app.auth.repository import IUserRepository
from app.auth.config import supabase_config


class SupabaseUserRepository(IUserRepository):
    """
    Implementação do repositório usando Supabase.
    Segue Dependency Inversion Principle - implementa IUserRepository.
    """

    def __init__(self) -> None:
        """Inicializa o cliente Supabase"""
        if not supabase_config.SUPABASE_URL:
            raise ValueError("SUPABASE_URL deve estar configurado nas variáveis de ambiente")

        # Usa Service Key se disponível (bypassa RLS), senão usa anon key
        api_key: Optional[str] = supabase_config.SUPABASE_SERVICE_KEY or supabase_config.SUPABASE_KEY
        if not api_key:
            raise ValueError(
                "SUPABASE_KEY ou SUPABASE_SERVICE_KEY deve estar configurado nas variáveis de ambiente"
            )

        self.client: Client = create_client(
            supabase_config.SUPABASE_URL,
            api_key
        )
        self.table_name: str = "users"
        print(f"🔑 Usando {'Service Key' if supabase_config.SUPABASE_SERVICE_KEY else 'Anon Key'} para Supabase")

    async def create(self, email: str, name: str, hashed_password: str) -> User:
        """Cria um novo usuário no Supabase"""
        # Verifica se usuário já existe
        existing_user = await self.get_by_email(email)
        if existing_user:
            raise ValueError("Email já está cadastrado")

        try:
            print(f"📝 Tentando inserir usuário no Supabase: {email}")
            print(f"📋 Tabela: {self.table_name}")
            print(f"🔑 Usando Service Key: {bool(supabase_config.SUPABASE_SERVICE_KEY)}")

            # Insere novo usuário
            response = self.client.table(self.table_name).insert({
                "email": email,
                "name": name,
                "hashed_password": hashed_password
            }).execute()

            # Log detalhado da resposta
            print(f"📦 Resposta do Supabase:")
            print(f"   - data: {response.data}")
            print(f"   - data type: {type(response.data)}")
            print(f"   - data length: {len(response.data) if response.data else 0}")
            print(f"   - error: {getattr(response, 'error', None)}")
            print(f"   - status_code: {getattr(response, 'status_code', 'N/A')}")

            # Verifica se há erro na resposta
            if hasattr(response, 'error') and response.error:
                error_msg = f"Erro do Supabase: {response.error}"
                print(f"❌ {error_msg}")
                raise ValueError(error_msg)

            if not response.data or len(response.data) == 0:
                error_msg = "Erro ao criar usuário no banco de dados: resposta vazia do Supabase"
                print(f"❌ {error_msg}")
                print(f"⚠️  Possíveis causas:")
                print(f"   1. RLS (Row Level Security) está habilitado - mas você disse que está desabilitado")
                print(f"   2. A tabela 'users' não existe no Supabase")
                print(f"   3. Problema com permissões da API key")
                print(f"   4. Problema com a estrutura da tabela (campos faltando)")
                # Tenta obter mais informações sobre o erro
                if hasattr(response, 'status_code'):
                    error_msg += f" (Status: {response.status_code})"
                # Verifica se há mensagem de erro em outros atributos
                response_dict = response.__dict__ if hasattr(response, '__dict__') else {}
                if response_dict:
                    print(f"   Resposta completa: {response_dict}")
                raise ValueError(error_msg)

            user_data: dict[str, Any] = response.data[0]
            print(f"✅ Usuário criado no Supabase: {email} (ID: {user_data.get('id')})")
            return self._map_to_user(user_data)
        except ValueError:
            # Re-raise ValueError para manter o comportamento esperado
            raise
        except Exception as e:
            error_msg = f"Erro ao criar usuário no Supabase: {type(e).__name__}: {str(e)}"
            print(f"❌ {error_msg}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            raise ValueError(error_msg) from e

    async def get_by_email(self, email: str) -> Optional[User]:
        """Busca usuário por email no Supabase"""
        response = self.client.table(self.table_name)\
            .select("*")\
            .eq("email", email)\
            .limit(1)\
            .execute()

        if not response.data or len(response.data) == 0:
            return None

        user_data: dict[str, Any] = response.data[0]
        return self._map_to_user(user_data)

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Busca usuário por ID no Supabase"""
        response = self.client.table(self.table_name)\
            .select("*")\
            .eq("id", user_id)\
            .limit(1)\
            .execute()

        if not response.data or len(response.data) == 0:
            return None

        user_data: dict[str, Any] = response.data[0]
        return self._map_to_user(user_data)

    def _map_to_user(self, data: dict[str, Any]) -> User:
        """Mapeia dados do banco para o modelo User"""
        def parse_datetime(dt_str: Optional[str]) -> datetime:
            """Converte string de data do Supabase para datetime"""
            if not dt_str:
                return datetime.utcnow()
            try:
                # Remove timezone se presente e converte
                dt_str = dt_str.replace("Z", "+00:00")
                if "+" in dt_str or dt_str.endswith("+00:00"):
                    return datetime.fromisoformat(dt_str)
                return datetime.fromisoformat(dt_str)
            except Exception:
                return datetime.utcnow()

        return User(
            id=data["id"],
            email=data["email"],
            name=data["name"],
            hashed_password=data["hashed_password"],
            created_at=parse_datetime(data.get("created_at")) if data.get("created_at") else None,
            updated_at=parse_datetime(data.get("updated_at")) if data.get("updated_at") else None
        )
