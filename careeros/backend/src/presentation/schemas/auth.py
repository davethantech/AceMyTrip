"""Pydantic schemas for API request/response validation."""

from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    PREMIUM = "premium"
    ADMIN = "admin"


class ApplicationStatus(str, Enum):
    DRAFT = "draft"
    APPLIED = "applied"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class JobType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    FREELANCE = "freelance"
    INTERNSHIP = "internship"


class RemoteType(str, Enum):
    ONSITE = "onsite"
    REMOTE = "remote"
    HYBRID = "hybrid"


# Token schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)


class UserRegister(UserCreate):
    pass


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# OAuth schemas
class OAuthCallback(BaseModel):
    code: str
    state: Optional[str] = None


# Resume schemas
class ResumeBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str


class ResumeCreate(ResumeBase):
    file_type: Optional[str] = None
    is_primary: bool = False


class ResumeUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = None
    is_primary: Optional[bool] = None
    ats_score: Optional[int] = Field(None, ge=0, le=100)


class ResumeResponse(ResumeBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    ats_score: Optional[int] = None
    is_primary: bool
    created_at: datetime
    updated_at: datetime


# Job schemas
class JobBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    url: str = Field(..., max_length=1000)
    description: Optional[str] = None
    location: Optional[str] = None
    salary_min: Optional[int] = Field(None, ge=0)
    salary_max: Optional[int] = Field(None, ge=0)
    currency: str = "USD"
    job_type: JobType = JobType.FULL_TIME
    remote_type: RemoteType = RemoteType.REMOTE
    visa_sponsorship: bool = False
    skills: Optional[List[str]] = None
    benefits: Optional[List[str]] = None


class JobCreate(JobBase):
    company_id: UUID
    source: str


class JobFilter(BaseModel):
    query: Optional[str] = None
    skills: Optional[List[str]] = None
    remote_type: Optional[RemoteType] = None
    job_type: Optional[JobType] = None
    salary_min: Optional[int] = None
    location: Optional[str] = None
    skip: int = Field(0, ge=0)
    limit: int = Field(100, ge=1, le=500)


class JobResponse(JobBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    company_id: UUID
    source: str
    posted_date: datetime
    created_at: datetime


# Company schemas
class CompanyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    website: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyResponse(CompanyBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime


# Application schemas
class ApplicationBase(BaseModel):
    notes: Optional[str] = None
    follow_up_date: Optional[datetime] = None


class ApplicationCreate(ApplicationBase):
    job_id: UUID
    resume_id: Optional[UUID] = None
    cover_letter_id: Optional[UUID] = None


class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None
    notes: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    recruiter_id: Optional[UUID] = None


class ApplicationResponse(ApplicationBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    job_id: UUID
    resume_id: Optional[UUID] = None
    cover_letter_id: Optional[UUID] = None
    status: ApplicationStatus
    applied_date: Optional[datetime]
    recruiter_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime


# Cover Letter schemas
class CoverLetterBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str
    style: str = "professional"


class CoverLetterCreate(CoverLetterBase):
    job_id: Optional[UUID] = None


class CoverLetterResponse(CoverLetterBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    job_id: Optional[UUID] = None
    created_at: datetime


# Recruiter schemas
class RecruiterBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    linkedin_url: Optional[str] = None
    title: Optional[str] = None


class RecruiterCreate(RecruiterBase):
    company_id: Optional[UUID] = None


class RecruiterResponse(RecruiterBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    company_id: Optional[UUID] = None
    created_at: datetime


# Interview schemas
class InterviewBase(BaseModel):
    interview_type: str
    scheduled_date: datetime
    duration_minutes: int = 60
    location: Optional[str] = None
    meeting_link: Optional[str] = None
    notes: Optional[str] = None
    preparation_materials: Optional[List[str]] = None


class InterviewCreate(InterviewBase):
    application_id: UUID


class InterviewResponse(InterviewBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    application_id: UUID
    created_at: datetime


# Task schemas
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    task_type: str = "reminder"
    related_entity_type: Optional[str] = None
    related_entity_id: Optional[UUID] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    is_completed: Optional[bool] = None


class TaskResponse(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    is_completed: bool
    completed_at: Optional[datetime] = None
    created_at: datetime


# Notification schemas
class NotificationBase(BaseModel):
    title: str
    message: str
    notification_type: str = "info"
    action_url: Optional[str] = None


class NotificationCreate(NotificationBase):
    pass


class NotificationResponse(NotificationBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    is_read: bool
    read_at: Optional[datetime] = None
    created_at: datetime


# Settings schemas
class SettingsBase(BaseModel):
    daily_job_limit: int = Field(50, ge=1, le=500)
    auto_search_enabled: bool = True
    email_notifications: bool = True
    browser_notifications: bool = True
    preferred_remote_type: RemoteType = RemoteType.REMOTE
    preferred_job_types: Optional[List[JobType]] = None
    min_salary: Optional[int] = Field(None, ge=0)
    locations: Optional[List[str]] = None


class SettingsUpdate(SettingsBase):
    pass


class SettingsResponse(SettingsBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime


# Message schemas
class MessageBase(BaseModel):
    subject: str = Field(..., min_length=1, max_length=255)
    content: str
    message_type: str = "email"


class MessageCreate(MessageBase):
    recruiter_id: UUID


class MessageResponse(MessageBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    recruiter_id: UUID
    status: str
    sent_at: Optional[datetime] = None
    created_at: datetime


# Audit Log schemas
class AuditLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: Optional[UUID] = None
    action: str
    entity_type: str
    entity_id: Optional[UUID] = None
    old_values: Optional[dict] = None
    new_values: Optional[dict] = None
    ip_address: Optional[str] = None
    created_at: datetime


# Pagination
class PaginatedResponse(BaseModel):
    items: List
    total: int
    page: int
    page_size: int
    total_pages: int
