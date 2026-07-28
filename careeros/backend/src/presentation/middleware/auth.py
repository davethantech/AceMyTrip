"""Authentication middleware and dependencies."""

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from uuid import UUID

from src.infrastructure.database.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.security import verify_token
from src.shared.utils.config import get_settings

settings = get_settings()
security = HTTPBearer(auto_error=False)


async def get_current_user_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Optional[UUID]:
    """Get current user ID from JWT token."""
    if credentials is None:
        return None

    token = credentials.credentials
    payload = verify_token(token, token_type="access")

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return UUID(user_id)


async def require_auth(
    user_id: Optional[UUID] = Depends(get_current_user_id),
) -> UUID:
    """Require authentication - raise exception if not authenticated."""
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id


async def get_optional_user_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Optional[UUID]:
    """Get user ID if authenticated, otherwise return None."""
    if credentials is None:
        return None

    try:
        return await get_current_user_id(credentials)
    except HTTPException:
        return None
