"""Resumes API routes."""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from uuid import UUID

from src.infrastructure.database.session import get_db
from src.infrastructure.repositories.sqlalchemy_repos import ResumeRepository
from src.infrastructure.database.models import Resume
from src.presentation.schemas.auth import ResumeResponse, ResumeCreate, ResumeUpdate
from src.presentation.middleware.auth import require_auth

router = APIRouter()


def get_resume_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> ResumeRepository:
    """Get resume repository instance."""
    return ResumeRepository(db)


@router.get("/", response_model=List[ResumeResponse])
async def get_resumes(
    user_id: Annotated[UUID, Depends(require_auth)],
    repo: Annotated[ResumeRepository, Depends(get_resume_repo)],
):
    """Get all resumes for current user."""
    resumes = await repo.get_by_user(user_id)
    return [ResumeResponse.model_validate(r) for r in resumes]


@router.get("/primary", response_model=ResumeResponse)
async def get_primary_resume(
    user_id: Annotated[UUID, Depends(require_auth)],
    repo: Annotated[ResumeRepository, Depends(get_resume_repo)],
):
    """Get primary resume for current user."""
    resume = await repo.get_primary(user_id)
    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No primary resume found",
        )
    return ResumeResponse.model_validate(resume)


@router.post("/", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def create_resume(
    data: ResumeCreate,
    user_id: Annotated[UUID, Depends(require_auth)],
    repo: Annotated[ResumeRepository, Depends(get_resume_repo)],
):
    """Create a new resume."""
    resume = Resume(
        user_id=user_id,
        title=data.title,
        content=data.content,
        file_type=data.file_type,
        is_primary=data.is_primary,
    )
    await repo.create(resume)
    return ResumeResponse.model_validate(resume)


@router.put("/{resume_id}", response_model=ResumeResponse)
async def update_resume(
    resume_id: UUID,
    data: ResumeUpdate,
    user_id: Annotated[UUID, Depends(require_auth)],
    repo: Annotated[ResumeRepository, Depends(get_resume_repo)],
):
    """Update a resume."""
    existing = await repo.get_by_id(resume_id)
    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    if existing.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this resume",
        )

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing, key, value)

    await repo.update(resume_id, existing)
    return ResumeResponse.model_validate(existing)


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: UUID,
    user_id: Annotated[UUID, Depends(require_auth)],
    repo: Annotated[ResumeRepository, Depends(get_resume_repo)],
):
    """Delete a resume."""
    existing = await repo.get_by_id(resume_id)
    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    if existing.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this resume",
        )

    await repo.delete(resume_id)


@router.post("/{resume_id}/set-primary", response_model=ResumeResponse)
async def set_primary_resume(
    resume_id: UUID,
    user_id: Annotated[UUID, Depends(require_auth)],
    repo: Annotated[ResumeRepository, Depends(get_resume_repo)],
):
    """Set a resume as primary."""
    existing = await repo.get_by_id(resume_id)
    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    if existing.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this resume",
        )

    await repo.set_primary(resume_id, user_id)
    updated = await repo.get_by_id(resume_id)
    return ResumeResponse.model_validate(updated)
