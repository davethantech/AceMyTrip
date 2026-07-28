"""SQLAlchemy ORM Models for CareerOS Database."""

from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from enum import Enum as PyEnum

from sqlalchemy import (
    String,
    Text,
    Integer,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    Enum,
    Index,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ARRAY, JSONB
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    validates,
)


def generate_uuid() -> str:
    """Generate a UUID string."""
    return str(uuid4())


class Base(DeclarativeBase):
    """Base class for all models."""

    id: Mapped[str] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=generate_uuid
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), default=datetime.utcnow, nullable=False
    )

    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }


# Enums
class UserRole(PyEnum):
    USER = "user"
    PREMIUM = "premium"
    ADMIN = "admin"


class ApplicationStatus(PyEnum):
    DRAFT = "draft"
    APPLIED = "applied"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class JobType(PyEnum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    FREELANCE = "freelance"
    INTERNSHIP = "internship"


class RemoteType(PyEnum):
    ONSITE = "onsite"
    REMOTE = "remote"
    HYBRID = "hybrid"


# Auth & Users
class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # OAuth
    google_oauth_id: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True)
    github_oauth_id: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True)

    # Relationships
    resumes: Mapped[List["Resume"]] = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    applications: Mapped[List["Application"]] = relationship("Application", back_populates="user", cascade="all, delete-orphan")
    cover_letters: Mapped[List["CoverLetter"]] = relationship("CoverLetter", back_populates="user", cascade="all, delete-orphan")
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="user", cascade="all, delete-orphan")
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    notifications: Mapped[List["Notification"]] = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    settings: Mapped["Settings"] = relationship("Settings", back_populates="user", uselist=False, cascade="all, delete-orphan")
    audit_logs: Mapped[List["AuditLog"]] = relationship("AuditLog", back_populates="user")

    __table_args__ = (
        Index("ix_users_email", "email"),
        Index("ix_users_google_oauth", "google_oauth_id"),
        Index("ix_users_github_oauth", "github_oauth_id"),
    )


class OAuthAccount(Base):
    __tablename__ = "oauth_accounts"

    user_id: Mapped[str] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    oauth_id: Mapped[str] = mapped_column(String(255), nullable=False)
    access_token: Mapped[str] = mapped_column(Text, nullable=False)
    refresh_token: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        UniqueConstraint("provider", "oauth_id", name="uq_oauth_provider_id"),
        Index("ix_oauth_user_id", "user_id"),
    )


# Resumes
class Resume(Base):
    __tablename__ = "resumes"

    user_id: Mapped[str] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    file_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    file_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    ats_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="resumes")
    versions: Mapped[List["ResumeVersion"]] = relationship("ResumeVersion", back_populates="resume", cascade="all, delete-orphan")
    applications: Mapped[List["Application"]] = relationship("Application", back_populates="resume")

    __table_args__ = (
        Index("ix_resumes_user_id", "user_id"),
        Index("ix_resumes_primary", "user_id", "is_primary"),
    )


class ResumeVersion(Base):
    __tablename__ = "resume_versions"

    resume_id: Mapped[str] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    changes_summary: Mapped[str] = mapped_column(Text, nullable=False)

    # Relationships
    resume: Mapped["Resume"] = relationship("Resume", back_populates="versions")

    __table_args__ = (
        Index("ix_resume_versions_resume_id", "resume_id"),
        Index("ix_resume_versions_number", "resume_id", "version_number"),
    )


# Companies & Jobs
class Company(Base):
    __tablename__ = "companies"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    website: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    industry: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    size: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    jobs: Mapped[List["Job"]] = relationship("Job", back_populates="company", cascade="all, delete-orphan")
    recruiters: Mapped[List["Recruiter"]] = relationship("Recruiter", back_populates="company")

    __table_args__ = (
        UniqueConstraint("name", "website", name="uq_company_name_website"),
        Index("ix_companies_name", "name"),
    )


class Job(Base):
    __tablename__ = "jobs"

    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    company_id: Mapped[str] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    url: Mapped[str] = mapped_column(String(1000), nullable=False)
    job_type: Mapped[JobType] = mapped_column(Enum(JobType), default=JobType.FULL_TIME, nullable=False)
    remote_type: Mapped[RemoteType] = mapped_column(Enum(RemoteType), default=RemoteType.REMOTE, nullable=False)
    salary_min: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    currency: Mapped[str] = mapped_column(String(10), default="USD", nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    requirements: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    skills: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    benefits: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    visa_sponsorship: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    application_deadline: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    posted_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    external_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Relationships
    company: Mapped["Company"] = relationship("Company", back_populates="jobs")
    applications: Mapped[List["Application"]] = relationship("Application", back_populates="job", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("external_id", "source", name="uq_job_external_source"),
        Index("ix_jobs_title", "title"),
        Index("ix_jobs_company", "company_id"),
        Index("ix_jobs_remote", "remote_type"),
        Index("ix_jobs_salary", "salary_min", "salary_max"),
    )


# Applications
class Application(Base):
    __tablename__ = "applications"

    user_id: Mapped[str] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id: Mapped[str] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    resume_id: Mapped[Optional[str]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("resumes.id", ondelete="SET NULL"), nullable=True)
    cover_letter_id: Mapped[Optional[str]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("cover_letters.id", ondelete="SET NULL"), nullable=True)
    status: Mapped[ApplicationStatus] = mapped_column(Enum(ApplicationStatus), default=ApplicationStatus.DRAFT, nullable=False)
    applied_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recruiter_id: Mapped[Optional[str]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("recruiters.id", ondelete="SET NULL"), nullable=True)
    follow_up_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="applications")
    job: Mapped["Job"] = relationship("Job", back_populates="applications")
    resume: Mapped["Resume"] = relationship("Resume", back_populates="applications")
    cover_letter: Mapped["CoverLetter"] = relationship("CoverLetter", back_populates="application")
    recruiter: Mapped["Recruiter"] = relationship("Recruiter", back_populates="applications")
    interviews: Mapped[List["Interview"]] = relationship("Interview", back_populates="application", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("user_id", "job_id", name="uq_application_user_job"),
        Index("ix_applications_user", "user_id"),
        Index("ix_applications_job", "job_id"),
        Index("ix_applications_status", "status"),
    )


# Recruiters
class Recruiter(Base):
    __tablename__ = "recruiters"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    linkedin_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    company_id: Mapped[Optional[str]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True)
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Relationships
    company: Mapped["Company"] = relationship("Company", back_populates="recruiters")
    applications: Mapped[List["Application"]] = relationship("Application", back_populates="recruiter")
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="recruiter", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_recruiters_email", "email"),
        Index("ix_recruiters_company", "company_id"),
    )


# User Profile
class Skill(Base):
    __tablename__ = "skills"

    user_id: Mapped[str] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    proficiency_level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    years_experience: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    __table_args__ = (
        Index("ix_skills_user", "user_id"),
        Index("ix_skills_name", "name"),
    )


class Achievement(Base):
    __tablename__ = "achievements"

    user_id: Mapped[str] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    issuer: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    __table_args__ = (
        Index("ix_achievements_user", "user_id"),
    )


class Project(Base):
    __tablename__ = "projects"

    user_id: Mapped[str] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    technologies: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        Index("ix_projects_user", "user_id"),
    )


class Certification(Base):
    __tablename__ = "certifications"

    user_id: Mapped[str] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    issuer: Mapped[str] = mapped_column(String(255), nullable=False)
    issue_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    expiry_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    credential_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)

    __table_args__ = (
        Index("ix_certifications_user", "user_id"),
    )


class Education(Base):
    __tablename__ = "education"

    user_id: Mapped[str] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    institution: Mapped[str] = mapped_column(String(255), nullable=False)
    degree: Mapped[str] = mapped_column(String(255), nullable=False)
    field_of_study: Mapped[str] = mapped_column(String(255), nullable=False)
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    gpa: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    __table_args__ = (
        Index("ix_education_user", "user_id"),
    )


# Cover Letters
class CoverLetter(Base):
    __tablename__ = "cover_letters"

    user_id: Mapped[str] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id: Mapped[Optional[str]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    style: Mapped[str] = mapped_column(String(50), default="professional", nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="cover_letters")
    application: Mapped["Application"] = relationship("Application", back_populates="cover_letter")

    __table_args__ = (
        Index("ix_cover_letters_user", "user_id"),
    )


# Messages
class Message(Base):
    __tablename__ = "messages"

    user_id: Mapped[str] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    recruiter_id: Mapped[str] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("recruiters.id", ondelete="CASCADE"), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    message_type: Mapped[str] = mapped_column(String(50), default="email", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False)
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="messages")
    recruiter: Mapped["Recruiter"] = relationship("Recruiter", back_populates="messages")

    __table_args__ = (
        Index("ix_messages_user", "user_id"),
        Index("ix_messages_recruiter", "recruiter_id"),
    )


# Interviews
class Interview(Base):
    __tablename__ = "interviews"

    application_id: Mapped[str] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("applications.id", ondelete="CASCADE"), nullable=False)
    interview_type: Mapped[str] = mapped_column(String(100), nullable=False)
    scheduled_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    meeting_link: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    preparation_materials: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)

    # Relationships
    application: Mapped["Application"] = relationship("Application", back_populates="interviews")

    __table_args__ = (
        Index("ix_interviews_application", "application_id"),
        Index("ix_interviews_scheduled", "scheduled_date"),
    )


# Tasks
class Task(Base):
    __tablename__ = "tasks"

    user_id: Mapped[str] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, index=True)
    task_type: Mapped[str] = mapped_column(String(50), default="reminder", nullable=False)
    related_entity_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    related_entity_id: Mapped[Optional[str]] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="tasks")

    __table_args__ = (
        Index("ix_tasks_user", "user_id"),
        Index("ix_tasks_completed", "is_completed"),
    )


# Notifications
class Notification(Base):
    __tablename__ = "notifications"

    user_id: Mapped[str] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    notification_type: Mapped[str] = mapped_column(String(50), default="info", nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    read_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    action_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="notifications")

    __table_args__ = (
        Index("ix_notifications_user", "user_id"),
        Index("ix_notifications_read", "is_read"),
        Index("ix_notifications_created", "created_at"),
    )


# Settings
class Settings(Base):
    __tablename__ = "settings"

    user_id: Mapped[str] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    daily_job_limit: Mapped[int] = mapped_column(Integer, default=50, nullable=False)
    auto_search_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    email_notifications: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    browser_notifications: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    preferred_remote_type: Mapped[RemoteType] = mapped_column(Enum(RemoteType), default=RemoteType.REMOTE, nullable=False)
    preferred_job_types: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    min_salary: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    locations: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="settings")


# Audit Logs
class AuditLog(Base):
    __tablename__ = "audit_logs"

    user_id: Mapped[Optional[str]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_id: Mapped[Optional[str]] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    old_values: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    new_values: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="audit_logs")

    __table_args__ = (
        Index("ix_audit_logs_user", "user_id"),
        Index("ix_audit_logs_entity", "entity_type", "entity_id"),
        Index("ix_audit_logs_action", "action"),
        Index("ix_audit_logs_created", "created_at"),
    )
