"""
Repositório de usuários seguindo o padrão Repository e Dependency Inversion Principle.
Define uma interface abstrata que pode ser implementada por diferentes fontes de dados.
"""
from abc import ABC, abstractmethod
from typing import Optional
from app.auth.models import User


class IUserRepository(ABC):
    """
    Interface do repositório de usuários.
    Segue Interface Segregation Principle - interface específica e focada.
    """

    @abstractmethod
    async def create(self, email: str, name: str, hashed_password: str) -> User:
        """Cria um novo usuário"""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Busca usuário por email"""
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Busca usuário por ID"""
        pass


class InMemoryUserRepository(IUserRepository):
    """
    Implementação em memória do repositório.
    Segue Liskov Substitution Principle - pode substituir IUserRepository.
    Em produção, seria substituído por uma implementação com banco de dados.
    """

    def __init__(self) -> None:
        self._users: dict[int, User] = {}
        self._users_by_email: dict[str, User] = {}
        self._next_id: int = 1

    async def create(self, email: str, name: str, hashed_password: str) -> User:
        """Cria um novo usuário em memória"""
        print("⚠️  ATENÇÃO: Usando InMemoryUserRepository - dados NÃO serão persistidos!")
        print(f"📝 Criando usuário em memória: {email}")
        if email in self._users_by_email:
            raise ValueError("Email já está em uso")

        user: User = User(
            id=self._next_id,
            email=email,
            name=name,
            hashed_password=hashed_password
        )

        self._users[self._next_id] = user
        self._users_by_email[email] = user
        self._next_id += 1

        print(f"✅ Usuário criado em memória (NÃO persistido): {email} (ID: {user.id})")
        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        """Busca usuário por email"""
        return self._users_by_email.get(email)

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Busca usuário por ID"""
        return self._users.get(user_id)
