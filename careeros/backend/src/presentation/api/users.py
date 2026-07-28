"""Users API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from uuid import UUID

from src.infrastructure.database.session import get_db
from src.application.services.auth_service import AuthenticationService
from src.presentation.schemas.auth import UserResponse, UserUpdate
from src.presentation.middleware.auth import require_auth

router = APIRouter()


def get_auth_service(db: Annotated[AsyncSession, Depends(get_db)]) -> AuthenticationService:
    """Get authentication service instance."""
    return AuthenticationService(db)


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    user_id: Annotated[UUID, Depends(require_auth)],
    auth_service: Annotated[AuthenticationService, Depends(get_auth_service)],
):
    """Get current authenticated user profile."""
    user = await auth_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return UserResponse.model_validate(user)


@router.patch("/me", response_model=UserResponse)
async def update_current_user(
    data: UserUpdate,
    user_id: Annotated[UUID, Depends(require_auth)],
    auth_service: Annotated[AuthenticationService, Depends(get_auth_service)],
):
    """Update current user profile."""
    update_data = data.model_dump(exclude_unset=True)
    try:
        user = await auth_service.update_user(user_id, update_data)
        return UserResponse.model_validate(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
