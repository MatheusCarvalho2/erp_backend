"""
Serviço de autenticação contendo a lógica de negócio.
Segue Single Responsibility Principle - apenas lógica de autenticação.
Segue Dependency Inversion Principle - depende da abstração IUserRepository.
"""
from datetime import datetime, timedelta
from typing import Optional, Any
from jose import JWTError, jwt
import bcrypt
from app.auth.models import User
from app.auth.repository import IUserRepository
from app.auth.config import auth_config


def _truncate_password(password: str) -> bytes:
    """
    Trunca a senha para 72 bytes (limitação do bcrypt).
    Retorna os bytes da senha truncada.
    """
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        return password_bytes[:72]
    return password_bytes


class AuthService:
    """
    Serviço de autenticação.
    Contém toda a lógica de negócio relacionada a autenticação.
    """

    def __init__(self, user_repository: IUserRepository) -> None:
        """
        Injeção de dependência do repositório.
        Segue Dependency Inversion Principle.
        """
        self.user_repository: IUserRepository = user_repository

    def _hash_password(self, password: str) -> str:
        """
        Gera hash da senha usando bcrypt.
        Bcrypt tem limitação de 72 bytes, então truncamos se necessário.
        """
        # Trunca a senha para 72 bytes antes de fazer o hash
        password_bytes = _truncate_password(password)

        # Gera o salt e faz o hash usando bcrypt diretamente
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)

        # Retorna como string (formato bcrypt)
        return hashed.decode('utf-8')

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica se a senha está correta usando bcrypt.
        Trunca a senha se necessário para compatibilidade com bcrypt.
        """
        # Trunca a senha para 72 bytes antes de verificar
        password_bytes = _truncate_password(plain_password)
        hashed_bytes = hashed_password.encode('utf-8')

        # Verifica usando bcrypt diretamente
        return bcrypt.checkpw(password_bytes, hashed_bytes)

    def _create_access_token(self, data: dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Cria token JWT"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=auth_config.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, auth_config.SECRET_KEY, algorithm=auth_config.ALGORITHM)
        return encoded_jwt

    async def register_user(self, email: str, name: str, password: str) -> User:
        """
        Registra um novo usuário.
        Lógica de negócio: valida, hash da senha e cria usuário.
        """
        # Verifica se usuário já existe
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError("Email já está cadastrado")

        # Hash da senha
        hashed_password = self._hash_password(password)

        # Cria usuário
        user = await self.user_repository.create(
            email=email,
            name=name,
            hashed_password=hashed_password
        )

        return user

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Autentica um usuário.
        Lógica de negócio: verifica credenciais e retorna usuário se válido.
        """
        user = await self.user_repository.get_by_email(email)
        if not user:
            return None

        if not self._verify_password(password, user.hashed_password):
            return None

        return user

    async def login(self, email: str, password: str) -> str:
        """
        Realiza login e retorna token JWT.
        Combina autenticação e geração de token.
        """
        user = await self.authenticate_user(email, password)
        if not user:
            raise ValueError("Email ou senha incorretos")

        access_token_expires = timedelta(minutes=auth_config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self._create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )

        return access_token

    def verify_token(self, token: str) -> Optional[dict[str, Any]]:
        """
        Verifica e decodifica token JWT.
        Retorna payload se válido, None caso contrário.
        """
        try:
            payload: dict[str, Any] = jwt.decode(token, auth_config.SECRET_KEY, algorithms=[auth_config.ALGORITHM])
            return payload
        except JWTError:
            return None

    async def get_current_user(self, token: str) -> Optional[User]:
        """
        Obtém usuário atual a partir do token.
        Combina verificação de token e busca de usuário.
        """
        payload = self.verify_token(token)
        if payload is None:
            return None

        user_id: Any = payload.get("sub")
        if user_id is None:
            return None

        user: Optional[User] = await self.user_repository.get_by_id(int(str(user_id)))
        return user
