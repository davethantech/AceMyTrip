"""Authentication service for user management."""

from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.models import User, UserRole
from src.infrastructure.security import get_password_hash, verify_password
from src.infrastructure.security import create_access_token, create_refresh_token
from src.presentation.schemas.auth import UserRegister, UserLogin


class AuthenticationService:
    """Service for handling authentication operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def register(self, data: UserRegister) -> User:
        """Register a new user."""
        # Check if user already exists
        from sqlalchemy import select

        result = await self.session.execute(
            select(User).where(User.email == data.email)
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise ValueError("User with this email already exists")

        # Create new user
        user = User(
            email=data.email,
            password_hash=get_password_hash(data.password),
            full_name=data.full_name,
            role=UserRole.USER,
            is_active=True,
            is_verified=False,
        )

        self.session.add(user)
        await self.session.flush()
        return user

    async def login(self, data: UserLogin) -> tuple[User, dict]:
        """Authenticate user and return tokens."""
        from sqlalchemy import select

        result = await self.session.execute(
            select(User).where(User.email == data.email)
        )
        user = result.scalar_one_or_none()

        if user is None or not user.password_hash:
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("User account is deactivated")

        if not verify_password(data.password, user.password_hash):
            raise ValueError("Invalid email or password")

        # Generate tokens
        access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})

        return user, {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def refresh_tokens(self, refresh_token: str) -> dict:
        """Refresh access token using refresh token."""
        from src.infrastructure.security import verify_token

        payload = verify_token(refresh_token, token_type="refresh")
        if payload is None:
            raise ValueError("Invalid or expired refresh token")

        user_id = payload.get("sub")
        if user_id is None:
            raise ValueError("Invalid token payload")

        from sqlalchemy import select

        result = await self.session.execute(select(User).where(User.id == UUID(user_id)))
        user = result.scalar_one_or_none()

        if user is None or not user.is_active:
            raise ValueError("User not found or inactive")

        # Generate new tokens
        new_access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
        new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        }

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        from sqlalchemy import select

        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        from sqlalchemy import select

        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def update_user(self, user_id: UUID, update_data: dict) -> User:
        """Update user information."""
        from sqlalchemy import select

        result = await self.session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if user is None:
            raise ValueError("User not found")

        for key, value in update_data.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)

        await self.session.flush()
        return user
