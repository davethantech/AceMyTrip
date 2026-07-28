"""Repository interfaces for the domain layer."""

from abc import ABC, abstractmethod
from typing import Optional, List, Generic, TypeVar
from uuid import UUID

T = TypeVar("T")


class RepositoryInterface(ABC, Generic[T]):
    """Base repository interface."""

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[T]:
        """Get entity by ID."""
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all entities with pagination."""
        pass

    @abstractmethod
    async def create(self, entity: T) -> T:
        """Create a new entity."""
        pass

    @abstractmethod
    async def update(self, id: UUID, entity: T) -> T:
        """Update an existing entity."""
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """Delete an entity."""
        pass


class UserRepositoryInterface(RepositoryInterface):
    """User repository interface."""

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[T]:
        """Get user by email."""
        pass

    @abstractmethod
    async def get_by_oauth_id(self, provider: str, oauth_id: str) -> Optional[T]:
        """Get user by OAuth provider and ID."""
        pass


class ResumeRepositoryInterface(RepositoryInterface):
    """Resume repository interface."""

    @abstractmethod
    async def get_by_user(self, user_id: UUID) -> List[T]:
        """Get all resumes for a user."""
        pass

    @abstractmethod
    async def get_primary(self, user_id: UUID) -> Optional[T]:
        """Get primary resume for a user."""
        pass

    @abstractmethod
    async def set_primary(self, resume_id: UUID, user_id: UUID) -> None:
        """Set a resume as primary."""
        pass


class JobRepositoryInterface(RepositoryInterface):
    """Job repository interface."""

    @abstractmethod
    async def search(
        self,
        query: Optional[str] = None,
        skills: Optional[List[str]] = None,
        remote_type: Optional[str] = None,
        salary_min: Optional[int] = None,
        location: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[T]:
        """Search jobs with filters."""
        pass

    @abstractmethod
    async def find_duplicates(self, url: str, title: str, company_id: UUID) -> List[T]:
        """Find duplicate jobs."""
        pass


class ApplicationRepositoryInterface(RepositoryInterface):
    """Application repository interface."""

    @abstractmethod
    async def get_by_user(self, user_id: UUID) -> List[T]:
        """Get all applications for a user."""
        pass

    @abstractmethod
    async def get_by_status(
        self, user_id: UUID, status: str
    ) -> List[T]:
        """Get applications by status."""
        pass

    @abstractmethod
    async def get_by_job(self, job_id: UUID) -> List[T]:
        """Get applications for a job."""
        pass


class CompanyRepositoryInterface(RepositoryInterface):
    """Company repository interface."""

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[T]:
        """Get company by name."""
        pass

    @abstractmethod
    async def search(self, query: str, skip: int = 0, limit: int = 100) -> List[T]:
        """Search companies."""
        pass


class RecruiterRepositoryInterface(RepositoryInterface):
    """Recruiter repository interface."""

    @abstractmethod
    async def get_by_company(self, company_id: UUID) -> List[T]:
        """Get recruiters by company."""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[T]:
        """Get recruiter by email."""
        pass


class InterviewRepositoryInterface(RepositoryInterface):
    """Interview repository interface."""

    @abstractmethod
    async def get_by_application(self, application_id: UUID) -> List[T]:
        """Get interviews by application."""
        pass

    @abstractmethod
    async def get_upcoming(self, user_id: UUID) -> List[T]:
        """Get upcoming interviews for a user."""
        pass


class TaskRepositoryInterface(RepositoryInterface):
    """Task repository interface."""

    @abstractmethod
    async def get_by_user(self, user_id: UUID) -> List[T]:
        """Get tasks by user."""
        pass

    @abstractmethod
    async def get_pending(self, user_id: UUID) -> List[T]:
        """Get pending tasks for a user."""
        pass

    @abstractmethod
    async def mark_completed(self, task_id: UUID) -> None:
        """Mark task as completed."""
        pass


class NotificationRepositoryInterface(RepositoryInterface):
    """Notification repository interface."""

    @abstractmethod
    async def get_by_user(self, user_id: UUID, unread_only: bool = False) -> List[T]:
        """Get notifications by user."""
        pass

    @abstractmethod
    async def mark_read(self, notification_id: UUID) -> None:
        """Mark notification as read."""
        pass

    @abstractmethod
    async def mark_all_read(self, user_id: UUID) -> None:
        """Mark all notifications as read for a user."""
        pass


class AuditLogRepositoryInterface(RepositoryInterface):
    """Audit log repository interface."""

    @abstractmethod
    async def log(
        self,
        user_id: Optional[UUID],
        action: str,
        entity_type: str,
        entity_id: Optional[UUID],
        old_values: Optional[dict] = None,
        new_values: Optional[dict] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> T:
        """Create an audit log entry."""
        pass

    @abstractmethod
    async def get_by_entity(
        self, entity_type: str, entity_id: UUID
    ) -> List[T]:
        """Get audit logs for an entity."""
        pass


class SettingsRepositoryInterface(RepositoryInterface):
    """Settings repository interface."""

    @abstractmethod
    async def get_by_user(self, user_id: UUID) -> Optional[T]:
        """Get settings by user ID."""
        pass

    @abstractmethod
    async def upsert(self, user_id: UUID, settings_data: dict) -> T:
        """Create or update settings for a user."""
        pass
