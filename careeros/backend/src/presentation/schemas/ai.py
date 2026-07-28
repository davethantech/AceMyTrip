"""Pydantic schemas for AI service operations."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# Resume Analysis schemas
class ResumeAnalysisRequest(BaseModel):
    """Request schema for resume analysis."""
    resume_content: str = Field(..., description="The resume content to analyze")
    resume_id: Optional[str] = Field(None, description="Optional resume ID for database update")


class ResumeAnalysisResponse(BaseModel):
    """Response schema for resume analysis."""
    ats_score: int = Field(..., ge=0, le=100, description="ATS compatibility score")
    extracted_skills: List[str] = Field(..., description="Skills found in resume")
    extracted_experience: List[Dict[str, Any]] = Field(..., description="Work experience entries")
    extracted_education: List[Dict[str, Any]] = Field(..., description="Education entries")
    extracted_certifications: List[Dict[str, Any]] = Field(..., description="Certification entries")
    keywords: List[str] = Field(..., description="Important keywords")
    improvements: List[str] = Field(..., description="Suggested improvements")
    formatting_issues: List[str] = Field(..., description="Formatting issues detected")


# Resume Optimization schemas
class ResumeOptimizationRequest(BaseModel):
    """Request schema for resume optimization."""
    resume_content: str = Field(..., description="Current resume content")
    job_description: str = Field(..., description="Target job description")
    preserve_facts: bool = Field(True, description="Whether to preserve factual accuracy")
    resume_id: Optional[str] = Field(None, description="Optional resume ID for database update")


class ResumeOptimizationResponse(BaseModel):
    """Response schema for resume optimization."""
    optimized_content: str = Field(..., description="Optimized resume content")
    changes_summary: str = Field(..., description="Summary of changes made")
    keyword_improvements: List[str] = Field(..., description="Keywords added or emphasized")


# Job Matching schemas
class JobMatchRequest(BaseModel):
    """Request schema for job-resume matching."""
    resume_content: str = Field(..., description="Resume content")
    job_description: str = Field(..., description="Full job description")
    job_requirements: List[str] = Field(..., description="Required skills/qualifications")
    job_skills: List[str] = Field(..., description="Preferred skills")
    resume_id: Optional[str] = Field(None, description="Resume ID")
    job_id: Optional[str] = Field(None, description="Job ID")


class JobMatchResponse(BaseModel):
    """Response schema for job matching results."""
    match_percentage: float = Field(..., ge=0, le=100, description="Overall match percentage")
    strengths: List[str] = Field(..., description="Candidate strengths for this role")
    weaknesses: List[str] = Field(..., description="Areas lacking experience")
    missing_skills: List[str] = Field(..., description="Skills in job but not in resume")
    learning_recommendations: List[str] = Field(..., description="Learning recommendations")
    ats_score: int = Field(..., ge=0, le=100, description="Estimated ATS score")


# Cover Letter schemas
class CoverLetterGenerationRequest(BaseModel):
    """Request schema for cover letter generation."""
    resume_content: str = Field(..., description="Resume content")
    job_description: str = Field(..., description="Job description")
    company_name: str = Field(..., description="Target company name")
    style: str = Field("professional", description="Writing style: professional, friendly, creative, concise, storytelling")
    job_id: Optional[str] = Field(None, description="Optional job ID for saving")


class CoverLetterGenerationResponse(BaseModel):
    """Response schema for cover letter generation."""
    content: str = Field(..., description="Generated cover letter content")
    style: str = Field(..., description="Writing style used")
    word_count: int = Field(..., description="Number of words")
    key_highlights: List[str] = Field(..., description="Key highlights emphasized")


# Interview Preparation schemas
class InterviewPrepRequest(BaseModel):
    """Request schema for interview preparation."""
    job_description: str = Field(..., description="Job description")
    company_name: str = Field(..., description="Company name")
    role_level: str = Field("mid", description="Role level: junior, mid, senior, staff, principal")
    job_id: Optional[str] = Field(None, description="Optional job ID")


class InterviewPrepResponse(BaseModel):
    """Response schema for interview preparation results."""
    technical_questions: List[Dict[str, Any]] = Field(..., description="Technical Q&A pairs")
    behavioral_questions: List[Dict[str, Any]] = Field(..., description="Behavioral Q&A with STAR")
    star_answers: List[Dict[str, Any]] = Field(..., description="STAR answer examples")
    company_research: Dict[str, Any] = Field(..., description="Company research summary")
    system_design_topics: List[str] = Field(..., description="System design topics")
    coding_challenges: List[Dict[str, Any]] = Field(..., description="Coding challenge suggestions")
    salary_negotiation_tips: List[str] = Field(..., description="Salary negotiation advice")


# Recruiter Message schemas
class RecruiterMessageRequest(BaseModel):
    """Request schema for recruiter message generation."""
    recruiter_name: str = Field(..., description="Recruiter's name")
    company_name: str = Field(..., description="Company name")
    job_title: str = Field(..., description="Job title")
    message_purpose: str = Field(..., description="Purpose: initial_outreach, follow_up, networking, referral_request, thank_you")
    user_background: str = Field(..., description="User's professional background summary")
    recruiter_id: Optional[str] = Field(None, description="Optional recruiter ID")


class RecruiterMessageResponse(BaseModel):
    """Response schema for recruiter message generation."""
    subject: str = Field(..., description="Message subject line")
    content: str = Field(..., description="Full message content")
    message_type: str = Field(..., description="Type: email, linkedin")
    follow_up_suggestions: List[str] = Field(..., description="Follow-up suggestions")


# Follow-up Message schemas
class FollowUpMessageRequest(BaseModel):
    """Request schema for follow-up message generation."""
    application_status: str = Field(..., description="Current application status")
    days_since_application: int = Field(..., ge=0, description="Days since application")
    company_name: str = Field(..., description="Company name")
    application_id: Optional[str] = Field(None, description="Optional application ID")


class FollowUpMessageResponse(BaseModel):
    """Response schema for follow-up message."""
    message: str = Field(..., description="Generated follow-up message")
    suggested_channel: str = Field("email", description="Suggested communication channel")


# Job Details Extraction schemas
class JobDetailsExtractionRequest(BaseModel):
    """Request schema for job details extraction."""
    job_posting_html: str = Field(..., description="Raw HTML or text of job posting")
    source_url: Optional[str] = Field(None, description="URL of the job posting")


class JobDetailsExtractionResponse(BaseModel):
    """Response schema for extracted job details."""
    title: Optional[str] = Field(None, description="Job title")
    company: Optional[str] = Field(None, description="Company name")
    location: Optional[str] = Field(None, description="Job location")
    remote_type: Optional[str] = Field(None, description="remote, hybrid, or onsite")
    job_type: Optional[str] = Field(None, description="full_time, part_time, contract, etc.")
    salary_min: Optional[int] = Field(None, description="Minimum salary")
    salary_max: Optional[int] = Field(None, description="Maximum salary")
    currency: str = Field("USD", description="Currency code")
    description: Optional[str] = Field(None, description="Job description")
    requirements: List[str] = Field(default_factory=list, description="Requirements list")
    skills: List[str] = Field(default_factory=list, description="Skills list")
    benefits: List[str] = Field(default_factory=list, description="Benefits list")
    experience_level: Optional[str] = Field(None, description="Experience level required")
    education_requirements: Optional[str] = Field(None, description="Education requirements")
    visa_sponsorship: bool = Field(False, description="Visa sponsorship available")
    application_url: Optional[str] = Field(None, description="Application URL")
