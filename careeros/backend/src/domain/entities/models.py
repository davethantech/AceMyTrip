"""Domain Entities for CareerOS."""

from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from enum import Enum


class UserRole(str, Enum):
    """User role enumeration."""
    USER = "user"
    PREMIUM = "premium"
    ADMIN = "admin"


class ApplicationStatus(str, Enum):
    """Application status enumeration."""
    DRAFT = "draft"
    APPLIED = "applied"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class JobType(str, Enum):
    """Job type enumeration."""
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    FREELANCE = "freelance"
    INTERNSHIP = "internship"


class RemoteType(str, Enum):
    """Remote work type enumeration."""
    ONSITE = "onsite"
    REMOTE = "remote"
    HYBRID = "hybrid"


class User:
    """User entity representing a platform user."""

    def __init__(
        self,
        email: str,
        password_hash: str,
        full_name: str,
        role: UserRole = UserRole.USER,
        is_active: bool = True,
        is_verified: bool = False,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.email = email
        self.password_hash = password_hash
        self.full_name = full_name
        self.role = role
        self.is_active = is_active
        self.is_verified = is_verified
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def update(self, **kwargs) -> None:
        """Update user attributes."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()


class Resume:
    """Resume entity."""

    def __init__(
        self,
        user_id: UUID,
        title: str,
        content: str,
        file_path: Optional[str] = None,
        file_type: Optional[str] = None,
        ats_score: Optional[int] = None,
        is_primary: bool = False,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.user_id = user_id
        self.title = title
        self.content = content
        self.file_path = file_path
        self.file_type = file_type
        self.ats_score = ats_score
        self.is_primary = is_primary
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()


class ResumeVersion:
    """Resume version entity for tracking changes."""

    def __init__(
        self,
        resume_id: UUID,
        version_number: int,
        content: str,
        changes_summary: str,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.resume_id = resume_id
        self.version_number = version_number
        self.content = content
        self.changes_summary = changes_summary
        self.created_at = created_at or datetime.utcnow()


class Company:
    """Company entity."""

    def __init__(
        self,
        name: str,
        website: Optional[str] = None,
        industry: Optional[str] = None,
        size: Optional[str] = None,
        location: Optional[str] = None,
        description: Optional[str] = None,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.name = name
        self.website = website
        self.industry = industry
        self.size = size
        self.location = location
        self.description = description
        self.created_at = created_at or datetime.utcnow()


class Job:
    """Job entity."""

    def __init__(
        self,
        title: str,
        company_id: UUID,
        source: str,
        url: str,
        job_type: JobType = JobType.FULL_TIME,
        remote_type: RemoteType = RemoteType.REMOTE,
        salary_min: Optional[int] = None,
        salary_max: Optional[int] = None,
        currency: str = "USD",
        location: Optional[str] = None,
        description: Optional[str] = None,
        requirements: Optional[List[str]] = None,
        skills: Optional[List[str]] = None,
        benefits: Optional[List[str]] = None,
        visa_sponsorship: bool = False,
        application_deadline: Optional[datetime] = None,
        posted_date: Optional[datetime] = None,
        external_id: Optional[str] = None,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.title = title
        self.company_id = company_id
        self.source = source
        self.url = url
        self.job_type = job_type
        self.remote_type = remote_type
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.currency = currency
        self.location = location
        self.description = description
        self.requirements = requirements or []
        self.skills = skills or []
        self.benefits = benefits or []
        self.visa_sponsorship = visa_sponsorship
        self.application_deadline = application_deadline
        self.posted_date = posted_date or datetime.utcnow()
        self.external_id = external_id
        self.created_at = created_at or datetime.utcnow()


class Application:
    """Job application entity."""

    def __init__(
        self,
        user_id: UUID,
        job_id: UUID,
        resume_id: Optional[UUID],
        cover_letter_id: Optional[UUID],
        status: ApplicationStatus = ApplicationStatus.DRAFT,
        applied_date: Optional[datetime] = None,
        notes: Optional[str] = None,
        recruiter_id: Optional[UUID] = None,
        follow_up_date: Optional[datetime] = None,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.user_id = user_id
        self.job_id = job_id
        self.resume_id = resume_id
        self.cover_letter_id = cover_letter_id
        self.status = status
        self.applied_date = applied_date
        self.notes = notes
        self.recruiter_id = recruiter_id
        self.follow_up_date = follow_up_date
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()


class Recruiter:
    """Recruiter entity."""

    def __init__(
        self,
        name: str,
        email: Optional[str] = None,
        linkedin_url: Optional[str] = None,
        company_id: Optional[UUID] = None,
        title: Optional[str] = None,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.name = name
        self.email = email
        self.linkedin_url = linkedin_url
        self.company_id = company_id
        self.title = title
        self.created_at = created_at or datetime.utcnow()


class Skill:
    """Skill entity."""

    def __init__(
        self,
        name: str,
        category: str,
        proficiency_level: Optional[int] = None,
        years_experience: Optional[float] = None,
        id: Optional[UUID] = None,
    ):
        self.id = id or uuid4()
        self.name = name
        self.category = category
        self.proficiency_level = proficiency_level
        self.years_experience = years_experience


class Achievement:
    """Achievement entity."""

    def __init__(
        self,
        title: str,
        description: str,
        date: Optional[datetime] = None,
        issuer: Optional[str] = None,
        id: Optional[UUID] = None,
    ):
        self.id = id or uuid4()
        self.title = title
        self.description = description
        self.date = date
        self.issuer = issuer


class Project:
    """Project entity."""

    def __init__(
        self,
        name: str,
        description: str,
        url: Optional[str] = None,
        technologies: Optional[List[str]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        id: Optional[UUID] = None,
    ):
        self.id = id or uuid4()
        self.name = name
        self.description = description
        self.url = url
        self.technologies = technologies or []
        self.start_date = start_date
        self.end_date = end_date


class Certification:
    """Certification entity."""

    def __init__(
        self,
        name: str,
        issuer: str,
        issue_date: Optional[datetime] = None,
        expiry_date: Optional[datetime] = None,
        credential_url: Optional[str] = None,
        id: Optional[UUID] = None,
    ):
        self.id = id or uuid4()
        self.name = name
        self.issuer = issuer
        self.issue_date = issue_date
        self.expiry_date = expiry_date
        self.credential_url = credential_url


class Education:
    """Education entity."""

    def __init__(
        self,
        institution: str,
        degree: str,
        field_of_study: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        gpa: Optional[float] = None,
        id: Optional[UUID] = None,
    ):
        self.id = id or uuid4()
        self.institution = institution
        self.degree = degree
        self.field_of_study = field_of_study
        self.start_date = start_date
        self.end_date = end_date
        self.gpa = gpa


class CoverLetter:
    """Cover letter entity."""

    def __init__(
        self,
        user_id: UUID,
        job_id: Optional[UUID],
        title: str,
        content: str,
        style: str = "professional",
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.user_id = user_id
        self.job_id = job_id
        self.title = title
        self.content = content
        self.style = style
        self.created_at = created_at or datetime.utcnow()


class Message:
    """Message entity for recruiter communication."""

    def __init__(
        self,
        user_id: UUID,
        recruiter_id: UUID,
        subject: str,
        content: str,
        message_type: str = "email",
        status: str = "draft",
        sent_at: Optional[datetime] = None,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.user_id = user_id
        self.recruiter_id = recruiter_id
        self.subject = subject
        self.content = content
        self.message_type = message_type
        self.status = status
        self.sent_at = sent_at
        self.created_at = created_at or datetime.utcnow()


class Interview:
    """Interview entity."""

    def __init__(
        self,
        application_id: UUID,
        interview_type: str,
        scheduled_date: datetime,
        duration_minutes: int = 60,
        location: Optional[str] = None,
        meeting_link: Optional[str] = None,
        notes: Optional[str] = None,
        preparation_materials: Optional[List[str]] = None,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.application_id = application_id
        self.interview_type = interview_type
        self.scheduled_date = scheduled_date
        self.duration_minutes = duration_minutes
        self.location = location
        self.meeting_link = meeting_link
        self.notes = notes
        self.preparation_materials = preparation_materials or []
        self.created_at = created_at or datetime.utcnow()


class Task:
    """Task entity for reminders and follow-ups."""

    def __init__(
        self,
        user_id: UUID,
        title: str,
        description: Optional[str] = None,
        due_date: Optional[datetime] = None,
        task_type: str = "reminder",
        related_entity_type: Optional[str] = None,
        related_entity_id: Optional[UUID] = None,
        is_completed: bool = False,
        completed_at: Optional[datetime] = None,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.user_id = user_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.task_type = task_type
        self.related_entity_type = related_entity_type
        self.related_entity_id = related_entity_id
        self.is_completed = is_completed
        self.completed_at = completed_at
        self.created_at = created_at or datetime.utcnow()


class Notification:
    """Notification entity."""

    def __init__(
        self,
        user_id: UUID,
        title: str,
        message: str,
        notification_type: str = "info",
        is_read: bool = False,
        read_at: Optional[datetime] = None,
        action_url: Optional[str] = None,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.user_id = user_id
        self.title = title
        self.message = message
        self.notification_type = notification_type
        self.is_read = is_read
        self.read_at = read_at
        self.action_url = action_url
        self.created_at = created_at or datetime.utcnow()


class AuditLog:
    """Audit log entity for tracking system changes."""

    def __init__(
        self,
        user_id: Optional[UUID],
        action: str,
        entity_type: str,
        entity_id: Optional[UUID],
        old_values: Optional[dict] = None,
        new_values: Optional[dict] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.user_id = user_id
        self.action = action
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.old_values = old_values or {}
        self.new_values = new_values or {}
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.created_at = created_at or datetime.utcnow()


class Settings:
    """User settings entity."""

    def __init__(
        self,
        user_id: UUID,
        daily_job_limit: int = 50,
        auto_search_enabled: bool = True,
        email_notifications: bool = True,
        browser_notifications: bool = True,
        preferred_remote_type: RemoteType = RemoteType.REMOTE,
        preferred_job_types: Optional[List[JobType]] = None,
        min_salary: Optional[int] = None,
        locations: Optional[List[str]] = None,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.user_id = user_id
        self.daily_job_limit = daily_job_limit
        self.auto_search_enabled = auto_search_enabled
        self.email_notifications = email_notifications
        self.browser_notifications = browser_notifications
        self.preferred_remote_type = preferred_remote_type
        self.preferred_job_types = preferred_job_types or [JobType.FULL_TIME]
        self.min_salary = min_salary
        self.locations = locations or []
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
