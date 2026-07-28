"""AI Services API routes for CareerOS."""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from uuid import UUID
import structlog

from src.infrastructure.database.session import get_db
from src.infrastructure.repositories.sqlalchemy_repos import ResumeRepository, JobRepository, CoverLetterRepository
from src.infrastructure.external_services.ai_service import AIService
from src.presentation.schemas.auth import CoverLetterCreate, CoverLetterResponse
from src.presentation.schemas.ai import (
    ResumeAnalysisRequest,
    ResumeAnalysisResponse,
    ResumeOptimizationRequest,
    ResumeOptimizationResponse,
    JobMatchRequest,
    JobMatchResponse,
    CoverLetterGenerationRequest,
    CoverLetterGenerationResponse,
    InterviewPrepRequest,
    InterviewPrepResponse,
    RecruiterMessageRequest,
    RecruiterMessageResponse,
    FollowUpMessageRequest,
    FollowUpMessageResponse,
    JobDetailsExtractionRequest,
    JobDetailsExtractionResponse,
)
from src.presentation.middleware.auth import require_auth
from src.infrastructure.database.models import CoverLetter

logger = structlog.get_logger()

router = APIRouter()


def get_ai_service() -> AIService:
    """Get AI service instance."""
    return AIService()


def get_resume_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> ResumeRepository:
    """Get resume repository instance."""
    return ResumeRepository(db)


def get_job_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> JobRepository:
    """Get job repository instance."""
    return JobRepository(db)


def get_cover_letter_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> CoverLetterRepository:
    """Get cover letter repository instance."""
    return CoverLetterRepository(db)


@router.post("/analyze-resume", response_model=ResumeAnalysisResponse)
async def analyze_resume(
    request: ResumeAnalysisRequest,
    user_id: Annotated[UUID, Depends(require_auth)],
    ai_service: Annotated[AIService, Depends(get_ai_service)],
    resume_repo: Annotated[ResumeRepository, Depends(get_resume_repo)],
):
    """Analyze a resume and extract structured information with ATS scoring."""
    try:
        result = await ai_service.analyze_resume(request.resume_content)
        
        # Optionally update the resume in database with ATS score
        if request.resume_id:
            resume = await resume_repo.get_by_id(UUID(request.resume_id))
            if resume and resume.user_id == user_id:
                await resume_repo.update_ats_score(UUID(request.resume_id), result.ats_score)
        
        logger.info("Resume analysis completed", user_id=user_id, ats_score=result.ats_score)
        
        return ResumeAnalysisResponse(
            ats_score=result.ats_score,
            extracted_skills=result.extracted_skills,
            extracted_experience=result.extracted_experience,
            extracted_education=result.extracted_education,
            extracted_certifications=result.extracted_certifications,
            keywords=result.keywords,
            improvements=result.improvements,
            formatting_issues=result.formatting_issues,
        )
    except Exception as e:
        logger.error("Resume analysis failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze resume: {str(e)}",
        )


@router.post("/optimize-resume", response_model=ResumeOptimizationResponse)
async def optimize_resume(
    request: ResumeOptimizationRequest,
    user_id: Annotated[UUID, Depends(require_auth)],
    ai_service: Annotated[AIService, Depends(get_ai_service)],
    resume_repo: Annotated[ResumeRepository, Depends(get_resume_repo)],
):
    """Optimize a resume for a specific job description without inventing experience."""
    try:
        optimized_content = await ai_service.optimize_resume(
            resume_content=request.resume_content,
            job_description=request.job_description,
            preserve_facts=request.preserve_facts,
        )
        
        # Generate a summary of changes
        changes_summary = "Resume optimized for target job description with improved keyword alignment."
        keyword_improvements = ["Enhanced action verbs", "Added relevant keywords from job description"]
        
        # Optionally save as new version
        if request.resume_id:
            resume = await resume_repo.get_by_id(UUID(request.resume_id))
            if resume and resume.user_id == user_id:
                await resume_repo.create_version(
                    UUID(request.resume_id),
                    optimized_content,
                    "Optimized for specific job posting",
                )
        
        logger.info("Resume optimization completed", user_id=user_id)
        
        return ResumeOptimizationResponse(
            optimized_content=optimized_content,
            changes_summary=changes_summary,
            keyword_improvements=keyword_improvements,
        )
    except Exception as e:
        logger.error("Resume optimization failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to optimize resume: {str(e)}",
        )


@router.post("/match-job", response_model=JobMatchResponse)
async def match_job_to_resume(
    request: JobMatchRequest,
    user_id: Annotated[UUID, Depends(require_auth)],
    ai_service: Annotated[AIService, Depends(get_ai_service)],
):
    """Calculate compatibility between a resume and job posting."""
    try:
        result = await ai_service.match_job_to_resume(
            resume_content=request.resume_content,
            job_description=request.job_description,
            job_requirements=request.job_requirements,
            job_skills=request.job_skills,
        )
        
        logger.info(
            "Job matching completed",
            user_id=user_id,
            match_percentage=result.match_percentage,
        )
        
        return JobMatchResponse(
            match_percentage=result.match_percentage,
            strengths=result.strengths,
            weaknesses=result.weaknesses,
            missing_skills=result.missing_skills,
            learning_recommendations=result.learning_recommendations,
            ats_score=result.ats_score,
        )
    except Exception as e:
        logger.error("Job matching failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to match job: {str(e)}",
        )


@router.post("/generate-cover-letter", response_model=CoverLetterGenerationResponse)
async def generate_cover_letter(
    request: CoverLetterGenerationRequest,
    user_id: Annotated[UUID, Depends(require_auth)],
    ai_service: Annotated[AIService, Depends(get_ai_service)],
    cover_letter_repo: Annotated[CoverLetterRepository, Depends(get_cover_letter_repo)],
):
    """Generate a personalized cover letter for a job application."""
    try:
        result = await ai_service.generate_cover_letter(
            resume_content=request.resume_content,
            job_description=request.job_description,
            company_name=request.company_name,
            style=request.style,
        )
        
        # Optionally save cover letter to database
        if request.job_id:
            cover_letter = CoverLetter(
                user_id=user_id,
                job_id=UUID(request.job_id),
                title=f"Cover Letter - {request.company_name}",
                content=result.content,
                style=request.style,
            )
            await cover_letter_repo.create(cover_letter)
        
        logger.info(
            "Cover letter generated",
            user_id=user_id,
            style=request.style,
            word_count=result.word_count,
        )
        
        return CoverLetterGenerationResponse(
            content=result.content,
            style=result.style,
            word_count=result.word_count,
            key_highlights=result.key_highlights,
        )
    except Exception as e:
        logger.error("Cover letter generation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate cover letter: {str(e)}",
        )


@router.post("/prepare-interview", response_model=InterviewPrepResponse)
async def prepare_interview(
    request: InterviewPrepRequest,
    user_id: Annotated[UUID, Depends(require_auth)],
    ai_service: Annotated[AIService, Depends(get_ai_service)],
):
    """Generate comprehensive interview preparation materials."""
    try:
        result = await ai_service.prepare_interview(
            job_description=request.job_description,
            company_name=request.company_name,
            role_level=request.role_level,
        )
        
        logger.info(
            "Interview preparation generated",
            user_id=user_id,
            company=request.company_name,
        )
        
        return InterviewPrepResponse(
            technical_questions=result.technical_questions,
            behavioral_questions=result.behavioral_questions,
            star_answers=result.star_answers,
            company_research=result.company_research,
            system_design_topics=result.system_design_topics,
            coding_challenges=result.coding_challenges,
            salary_negotiation_tips=result.salary_negotiation_tips,
        )
    except Exception as e:
        logger.error("Interview preparation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to prepare interview: {str(e)}",
        )


@router.post("/generate-recruiter-message", response_model=RecruiterMessageResponse)
async def generate_recruiter_message(
    request: RecruiterMessageRequest,
    user_id: Annotated[UUID, Depends(require_auth)],
    ai_service: Annotated[AIService, Depends(get_ai_service)],
):
    """Generate an outreach message to a recruiter."""
    try:
        result = await ai_service.generate_recruiter_message(
            recruiter_name=request.recruiter_name,
            company_name=request.company_name,
            job_title=request.job_title,
            message_purpose=request.message_purpose,
            user_background=request.user_background,
        )
        
        logger.info(
            "Recruiter message generated",
            user_id=user_id,
            purpose=request.message_purpose,
        )
        
        return RecruiterMessageResponse(
            subject=result.subject,
            content=result.content,
            message_type=result.message_type,
            follow_up_suggestions=result.follow_up_suggestions,
        )
    except Exception as e:
        logger.error("Recruiter message generation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate message: {str(e)}",
        )


@router.post("/generate-follow-up", response_model=FollowUpMessageResponse)
async def generate_follow_up_message(
    request: FollowUpMessageRequest,
    user_id: Annotated[UUID, Depends(require_auth)],
    ai_service: Annotated[AIService, Depends(get_ai_service)],
):
    """Generate a follow-up message for a job application."""
    try:
        message = await ai_service.generate_follow_up_message(
            application_status=request.application_status,
            days_since_application=request.days_since_application,
            company_name=request.company_name,
        )
        
        suggested_channel = "email" if request.days_since_application > 7 else "linkedin"
        
        logger.info(
            "Follow-up message generated",
            user_id=user_id,
            days=request.days_since_application,
        )
        
        return FollowUpMessageResponse(
            message=message,
            suggested_channel=suggested_channel,
        )
    except Exception as e:
        logger.error("Follow-up message generation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate follow-up: {str(e)}",
        )


@router.post("/extract-job-details", response_model=JobDetailsExtractionResponse)
async def extract_job_details(
    request: JobDetailsExtractionRequest,
    user_id: Annotated[UUID, Depends(require_auth)],
    ai_service: Annotated[AIService, Depends(get_ai_service)],
):
    """Extract structured job details from a raw job posting."""
    try:
        result = await ai_service.extract_job_details(request.job_posting_html)
        
        logger.info(
            "Job details extracted",
            user_id=user_id,
            title=result.get("title"),
            company=result.get("company"),
        )
        
        return JobDetailsExtractionResponse(
            title=result.get("title"),
            company=result.get("company"),
            location=result.get("location"),
            remote_type=result.get("remote_type"),
            job_type=result.get("job_type"),
            salary_min=result.get("salary_min"),
            salary_max=result.get("salary_max"),
            currency=result.get("currency", "USD"),
            description=result.get("description"),
            requirements=result.get("requirements", []),
            skills=result.get("skills", []),
            benefits=result.get("benefits", []),
            experience_level=result.get("experience_level"),
            education_requirements=result.get("education_requirements"),
            visa_sponsorship=result.get("visa_sponsorship", False),
            application_url=result.get("application_url") or request.source_url,
        )
    except Exception as e:
        logger.error("Job details extraction failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to extract job details: {str(e)}",
        )
