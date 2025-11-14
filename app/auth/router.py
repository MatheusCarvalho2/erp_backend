"""
Rotas da API de autenticação.
Segue Single Responsibility - apenas definição de endpoints HTTP.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.schemas import UserCreate, UserLogin, TokenResponse, UserResponse
from app.auth.service import AuthService
from app.auth.dependencies import get_auth_service, get_current_user
from app.auth.models import User


router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
) -> UserResponse:
    """
    Endpoint para registro de novo usuário.
    """
    try:
        user: User = await auth_service.register_user(
            email=user_data.email,
            name=user_data.name,
            password=user_data.password
        )
        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.name
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
) -> TokenResponse:
    """
    Endpoint para login de usuário.
    Retorna token JWT para autenticação.
    """
    try:
        access_token: str = await auth_service.login(
            email=credentials.email,
            password=credentials.password
        )
        return TokenResponse(access_token=access_token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """
    Endpoint para obter informações do usuário autenticado.
    Requer token JWT válido.
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name
    )
