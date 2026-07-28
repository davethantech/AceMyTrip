"""Authentication API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.infrastructure.database.session import get_db
from src.application.services.auth_service import AuthenticationService
from src.presentation.schemas.auth import (
    UserRegister,
    UserLogin,
    UserResponse,
    Token,
)
from src.presentation.middleware.auth import require_auth, get_current_user_id
from uuid import UUID

router = APIRouter()


def get_auth_service(db: Annotated[AsyncSession, Depends(get_db)]) -> AuthenticationService:
    """Get authentication service instance."""
    return AuthenticationService(db)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    data: UserRegister,
    auth_service: Annotated[AuthenticationService, Depends(get_auth_service)],
):
    """Register a new user."""
    try:
        user = await auth_service.register(data)
        return UserResponse.model_validate(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/login", response_model=Token)
async def login(
    data: UserLogin,
    auth_service: Annotated[AuthenticationService, Depends(get_auth_service)],
):
    """Login and get access/refresh tokens."""
    try:
        _, tokens = await auth_service.login(data)
        return Token(**tokens)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    auth_service: Annotated[AuthenticationService, Depends(get_auth_service)],
):
    """Refresh access token using refresh token."""
    try:
        tokens = await auth_service.refresh_tokens(refresh_token)
        return Token(**tokens)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    user_id: Annotated[UUID, Depends(require_auth)],
    auth_service: Annotated[AuthenticationService, Depends(get_auth_service)],
):
    """Get current authenticated user."""
    user = await auth_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return UserResponse.model_validate(user)
