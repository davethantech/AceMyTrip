"""Applications API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from uuid import UUID

from src.infrastructure.database.session import get_db
from src.infrastructure.repositories.sqlalchemy_repos import ApplicationRepository, JobRepository
from src.infrastructure.database.models import Application, ApplicationStatus
from src.presentation.schemas.auth import ApplicationResponse, ApplicationCreate, ApplicationUpdate
from src.presentation.middleware.auth import require_auth

router = APIRouter()


def get_app_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> ApplicationRepository:
    """Get application repository instance."""
    return ApplicationRepository(db)


def get_job_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> JobRepository:
    """Get job repository instance."""
    return JobRepository(db)


@router.get("/", response_model=List[ApplicationResponse])
async def get_applications(
    user_id: Annotated[UUID, Depends(require_auth)],
    repo: Annotated[ApplicationRepository, Depends(get_app_repo)],
):
    """Get all applications for current user."""
    applications = await repo.get_by_user(user_id)
    return [ApplicationResponse.model_validate(a) for a in applications]


@router.get("/status/{status}", response_model=List[ApplicationResponse])
async def get_applications_by_status(
    status: str,
    user_id: Annotated[UUID, Depends(require_auth)],
    repo: Annotated[ApplicationRepository, Depends(get_app_repo)],
):
    """Get applications by status."""
    try:
        app_status = ApplicationStatus(status)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Valid values: {[s.value for s in ApplicationStatus]}",
        )

    applications = await repo.get_by_status(user_id, app_status)
    return [ApplicationResponse.model_validate(a) for a in applications]


@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def create_application(
    data: ApplicationCreate,
    user_id: Annotated[UUID, Depends(require_auth)],
    app_repo: Annotated[ApplicationRepository, Depends(get_app_repo)],
    job_repo: Annotated[JobRepository, Depends(get_job_repo)],
):
    """Create a new job application."""
    # Verify job exists
    job = await job_repo.get_by_id(data.job_id)
    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    application = Application(
        user_id=user_id,
        job_id=data.job_id,
        resume_id=data.resume_id,
        cover_letter_id=data.cover_letter_id,
        status=ApplicationStatus.DRAFT,
        notes=data.notes,
        follow_up_date=data.follow_up_date,
    )
    await app_repo.create(application)
    return ApplicationResponse.model_validate(application)


@router.get("/{app_id}", response_model=ApplicationResponse)
async def get_application(
    app_id: UUID,
    user_id: Annotated[UUID, Depends(require_auth)],
    repo: Annotated[ApplicationRepository, Depends(get_app_repo)],
):
    """Get a specific application by ID."""
    application = await repo.get_by_id(app_id)
    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    if application.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this application",
        )

    return ApplicationResponse.model_validate(application)


@router.patch("/{app_id}", response_model=ApplicationResponse)
async def update_application(
    app_id: UUID,
    data: ApplicationUpdate,
    user_id: Annotated[UUID, Depends(require_auth)],
    repo: Annotated[ApplicationRepository, Depends(get_app_repo)],
):
    """Update an application."""
    application = await repo.get_by_id(app_id)
    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    if application.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this application",
        )

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(application, key, value)

    await repo.update(app_id, application)
    return ApplicationResponse.model_validate(application)


@router.delete("/{app_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(
    app_id: UUID,
    user_id: Annotated[UUID, Depends(require_auth)],
    repo: Annotated[ApplicationRepository, Depends(get_app_repo)],
):
    """Delete an application."""
    application = await repo.get_by_id(app_id)
    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    if application.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this application",
        )

    await repo.delete(app_id)
