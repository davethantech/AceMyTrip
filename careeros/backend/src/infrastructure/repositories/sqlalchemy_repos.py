"""Repository implementations using SQLAlchemy."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_
from typing import Optional, List, Type, TypeVar, Generic
from uuid import UUID
from datetime import datetime

from src.domain.interfaces.repositories import (
    RepositoryInterface,
    UserRepositoryInterface,
    ResumeRepositoryInterface,
    JobRepositoryInterface,
    ApplicationRepositoryInterface,
)
from src.infrastructure.database.models import (
    Base,
    User,
    Resume,
    Job,
    Application,
    Company,
)

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """Base repository with common CRUD operations."""

    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def get_by_id(self, id: UUID) -> Optional[T]:
        """Get entity by ID."""
        result = await self.session.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all entities with pagination."""
        result = await self.session.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def create(self, entity: T) -> T:
        """Create a new entity."""
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def update(self, id: UUID, entity: T) -> T:
        """Update an existing entity."""
        existing = await self.get_by_id(id)
        if existing is None:
            raise ValueError(f"Entity with id {id} not found")

        for key, value in entity.__dict__.items():
            if key != "_sa_instance_state" and hasattr(existing, key):
                setattr(existing, key, value)

        await self.session.flush()
        return existing

    async def delete(self, id: UUID) -> bool:
        """Delete an entity."""
        entity = await self.get_by_id(id)
        if entity is None:
            return False

        await self.session.delete(entity)
        await self.session.flush()
        return True

    async def count(self) -> int:
        """Count total entities."""
        result = await self.session.execute(select(func.count()).select_from(self.model))
        return result.scalar() or 0


class UserRepository(BaseRepository[User], UserRepositoryInterface):
    """User repository implementation."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_oauth_id(self, provider: str, oauth_id: str) -> Optional[User]:
        """Get user by OAuth provider and ID."""
        if provider == "google":
            result = await self.session.execute(
                select(User).where(User.google_oauth_id == oauth_id)
            )
        elif provider == "github":
            result = await self.session.execute(
                select(User).where(User.github_oauth_id == oauth_id)
            )
        else:
            return None

        return result.scalar_one_or_none()


class ResumeRepository(BaseRepository[Resume], ResumeRepositoryInterface):
    """Resume repository implementation."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, Resume)

    async def get_by_user(self, user_id: UUID) -> List[Resume]:
        """Get all resumes for a user."""
        result = await self.session.execute(
            select(Resume).where(Resume.user_id == user_id).order_by(Resume.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_primary(self, user_id: UUID) -> Optional[Resume]:
        """Get primary resume for a user."""
        result = await self.session.execute(
            select(Resume).where(Resume.user_id == user_id, Resume.is_primary == True)
        )
        return result.scalar_one_or_none()

    async def set_primary(self, resume_id: UUID, user_id: UUID) -> None:
        """Set a resume as primary."""
        # Unset all other primary resumes
        await self.session.execute(
            update(Resume)
            .where(Resume.user_id == user_id, Resume.is_primary == True)
            .values(is_primary=False)
        )

        # Set the specified resume as primary
        result = await self.session.execute(
            select(Resume).where(Resume.id == resume_id, Resume.user_id == user_id)
        )
        resume = result.scalar_one_or_none()
        if resume:
            resume.is_primary = True
            await self.session.flush()

    async def update_ats_score(self, resume_id: UUID, ats_score: int) -> None:
        """Update ATS score for a resume."""
        result = await self.session.execute(
            select(Resume).where(Resume.id == resume_id)
        )
        resume = result.scalar_one_or_none()
        if resume:
            resume.ats_score = ats_score
            await self.session.flush()

    async def create_version(
        self, 
        resume_id: UUID, 
        content: str, 
        changes_summary: str
    ) -> None:
        """Create a new version of a resume."""
        from src.infrastructure.database.models import ResumeVersion
        
        # Get current max version number
        result = await self.session.execute(
            select(func.max(ResumeVersion.version_number))
            .where(ResumeVersion.resume_id == resume_id)
        )
        max_version = result.scalar_one_or_none() or 0
        
        version = ResumeVersion(
            resume_id=resume_id,
            version_number=max_version + 1,
            content=content,
            changes_summary=changes_summary,
        )
        self.session.add(version)
        await self.session.flush()


class CompanyRepository(BaseRepository[Company], RepositoryInterface):
    """Company repository implementation."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, Company)

    async def get_by_name(self, name: str) -> Optional[Company]:
        """Get company by name."""
        result = await self.session.execute(
            select(Company).where(func.lower(Company.name) == func.lower(name))
        )
        return result.scalar_one_or_none()

    async def search(self, query: str, skip: int = 0, limit: int = 100) -> List[Company]:
        """Search companies by name."""
        search_pattern = f"%{query.lower()}%"
        result = await self.session.execute(
            select(Company)
            .where(func.lower(Company.name).like(search_pattern))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())


class JobRepository(BaseRepository[Job], JobRepositoryInterface):
    """Job repository implementation."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, Job)

    async def search(
        self,
        query: Optional[str] = None,
        skills: Optional[List[str]] = None,
        remote_type: Optional[str] = None,
        salary_min: Optional[int] = None,
        location: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Job]:
        """Search jobs with filters."""
        filters = []

        if query:
            search_pattern = f"%{query.lower()}%"
            filters.append(
                or_(
                    func.lower(Job.title).like(search_pattern),
                    func.lower(Job.description).like(search_pattern),
                )
            )

        if remote_type:
            filters.append(Job.remote_type == remote_type)

        if salary_min:
            filters.append(
                or_(
                    Job.salary_min >= salary_min,
                    Job.salary_max >= salary_min,
                )
            )

        if location:
            search_pattern = f"%{location.lower()}%"
            filters.append(func.lower(Job.location).like(search_pattern))

        statement = select(Job).where(and_(*filters)) if filters else select(Job)
        statement = statement.offset(skip).limit(limit).order_by(Job.posted_date.desc())

        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def find_duplicates(self, url: str, title: str, company_id: UUID) -> List[Job]:
        """Find duplicate jobs by URL or title+company."""
        result = await self.session.execute(
            select(Job).where(
                or_(
                    Job.url == url,
                    and_(
                        func.lower(Job.title) == func.lower(title),
                        Job.company_id == company_id,
                    ),
                )
            )
        )
        return list(result.scalars().all())


class ApplicationRepository(BaseRepository[Application], ApplicationRepositoryInterface):
    """Application repository implementation."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, Application)

    async def get_by_user(self, user_id: UUID) -> List[Application]:
        """Get all applications for a user."""
        result = await self.session.execute(
            select(Application)
            .where(Application.user_id == user_id)
            .order_by(Application.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_status(self, user_id: UUID, status: str) -> List[Application]:
        """Get applications by status."""
        result = await self.session.execute(
            select(Application).where(
                Application.user_id == user_id,
                Application.status == status,
            ).order_by(Application.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_job(self, job_id: UUID) -> List[Application]:
        """Get applications for a job."""
        result = await self.session.execute(
            select(Application).where(Application.job_id == job_id)
        )
        return list(result.scalars().all())


class CoverLetterRepository(BaseRepository[CoverLetter]):
    """Cover letter repository implementation."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, CoverLetter)

    async def get_by_user(self, user_id: UUID) -> List[CoverLetter]:
        """Get all cover letters for a user."""
        result = await self.session.execute(
            select(CoverLetter)
            .where(CoverLetter.user_id == user_id)
            .order_by(CoverLetter.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_job(self, job_id: UUID) -> Optional[CoverLetter]:
        """Get cover letter for a specific job."""
        result = await self.session.execute(
            select(CoverLetter).where(CoverLetter.job_id == job_id)
        )
        return result.scalar_one_or_none()


# Import update here to avoid circular imports
from sqlalchemy import update
