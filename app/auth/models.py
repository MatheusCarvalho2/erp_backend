"""
Modelos de domínio para autenticação.
Representa a entidade User no sistema.
"""
from datetime import datetime
from typing import Optional


class User:
    """Modelo de domínio para usuário"""

    def __init__(
        self,
        id: int,
        email: str,
        name: str,
        hashed_password: str,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ) -> None:
        self.id: int = id
        self.email: str = email
        self.name: str = name
        self.hashed_password: str = hashed_password
        self.created_at: datetime = created_at or datetime.utcnow()
        self.updated_at: datetime = updated_at or datetime.utcnow()
