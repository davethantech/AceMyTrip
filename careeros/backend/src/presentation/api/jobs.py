"""Jobs API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List, Optional
from uuid import UUID

from src.infrastructure.database.session import get_db
from src.infrastructure.repositories.sqlalchemy_repos import JobRepository, CompanyRepository
from src.infrastructure.database.models import Job, Company, JobType, RemoteType
from src.presentation.schemas.auth import JobResponse, JobCreate, JobFilter

router = APIRouter()


def get_job_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> JobRepository:
    """Get job repository instance."""
    return JobRepository(db)


def get_company_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> CompanyRepository:
    """Get company repository instance."""
    return CompanyRepository(db)


@router.get("/", response_model=List[JobResponse])
async def search_jobs(
    query: Optional[str] = None,
    remote_type: Optional[RemoteType] = None,
    job_type: Optional[JobType] = None,
    salary_min: Optional[int] = None,
    location: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    repo: Annotated[JobRepository, Depends(get_job_repo)] = None,
):
    """Search jobs with filters."""
    jobs = await repo.search(
        query=query,
        remote_type=remote_type.value if remote_type else None,
        salary_min=salary_min,
        location=location,
        skip=skip,
        limit=limit,
    )
    return [JobResponse.model_validate(j) for j in jobs]


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: UUID,
    repo: Annotated[JobRepository, Depends(get_job_repo)],
):
    """Get a specific job by ID."""
    job = await repo.get_by_id(job_id)
    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    return JobResponse.model_validate(job)


@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    data: JobCreate,
    company_repo: Annotated[CompanyRepository, Depends(get_company_repo)],
    job_repo: Annotated[JobRepository, Depends(get_job_repo)],
):
    """Create a new job (admin only)."""
    # Verify company exists
    company = await company_repo.get_by_id(data.company_id)
    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )

    # Check for duplicates
    duplicates = await job_repo.find_duplicates(data.url, data.title, data.company_id)
    if duplicates:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Duplicate job already exists",
        )

    job = Job(
        title=data.title,
        company_id=data.company_id,
        source=data.source,
        url=data.url,
        description=data.description,
        location=data.location,
        salary_min=data.salary_min,
        salary_max=data.salary_max,
        currency=data.currency,
        job_type=data.job_type,
        remote_type=data.remote_type,
        visa_sponsorship=data.visa_sponsorship,
        skills=data.skills,
        benefits=data.benefits,
    )
    await job_repo.create(job)
    return JobResponse.model_validate(job)
