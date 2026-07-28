"""AI Service interfaces for CareerOS."""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from uuid import UUID


class JobMatchResult:
    """Result of job matching analysis."""
    
    def __init__(
        self,
        match_percentage: float,
        strengths: List[str],
        weaknesses: List[str],
        missing_skills: List[str],
        learning_recommendations: List[str],
        ats_score: Optional[int] = None,
    ):
        self.match_percentage = match_percentage
        self.strengths = strengths
        self.weaknesses = weaknesses
        self.missing_skills = missing_skills
        self.learning_recommendations = learning_recommendations
        self.ats_score = ats_score


class ResumeAnalysisResult:
    """Result of resume analysis."""
    
    def __init__(
        self,
        ats_score: int,
        extracted_skills: List[str],
        extracted_experience: List[Dict[str, Any]],
        extracted_education: List[Dict[str, Any]],
        extracted_certifications: List[Dict[str, Any]],
        keywords: List[str],
        improvements: List[str],
        formatting_issues: List[str],
    ):
        self.ats_score = ats_score
        self.extracted_skills = extracted_skills
        self.extracted_experience = extracted_experience
        self.extracted_education = extracted_education
        self.extracted_certifications = extracted_certifications
        self.keywords = keywords
        self.improvements = improvements
        self.formatting_issues = formatting_issues


class CoverLetterGenerationResult:
    """Result of cover letter generation."""
    
    def __init__(
        self,
        content: str,
        style: str,
        word_count: int,
        key_highlights: List[str],
    ):
        self.content = content
        self.style = style
        self.word_count = word_count
        self.key_highlights = key_highlights


class InterviewPreparationResult:
    """Result of interview preparation generation."""
    
    def __init__(
        self,
        technical_questions: List[Dict[str, Any]],
        behavioral_questions: List[Dict[str, Any]],
        star_answers: List[Dict[str, Any]],
        company_research: Dict[str, Any],
        system_design_topics: List[str],
        coding_challenges: List[Dict[str, Any]],
        salary_negotiation_tips: List[str],
    ):
        self.technical_questions = technical_questions
        self.behavioral_questions = behavioral_questions
        self.star_answers = star_answers
        self.company_research = company_research
        self.system_design_topics = system_design_topics
        self.coding_challenges = coding_challenges
        self.salary_negotiation_tips = salary_negotiation_tips


class RecruiterMessageResult:
    """Result of recruiter message generation."""
    
    def __init__(
        self,
        subject: str,
        content: str,
        message_type: str,
        follow_up_suggestions: List[str],
    ):
        self.subject = subject
        self.content = content
        self.message_type = message_type
        self.follow_up_suggestions = follow_up_suggestions


class AIServiceInterface(ABC):
    """Interface for AI service operations."""
    
    @abstractmethod
    async def analyze_resume(self, resume_content: str) -> ResumeAnalysisResult:
        """Analyze a resume and extract information."""
        pass
    
    @abstractmethod
    async def optimize_resume(
        self, 
        resume_content: str, 
        job_description: str,
        preserve_facts: bool = True
    ) -> str:
        """Optimize resume for a specific job description."""
        pass
    
    @abstractmethod
    async def match_job_to_resume(
        self,
        resume_content: str,
        job_description: str,
        job_requirements: List[str],
        job_skills: List[str],
    ) -> JobMatchResult:
        """Calculate compatibility between resume and job."""
        pass
    
    @abstractmethod
    async def generate_cover_letter(
        self,
        resume_content: str,
        job_description: str,
        company_name: str,
        style: str = "professional",
    ) -> CoverLetterGenerationResult:
        """Generate a personalized cover letter."""
        pass
    
    @abstractmethod
    async def prepare_interview(
        self,
        job_description: str,
        company_name: str,
        role_level: str,
    ) -> InterviewPreparationResult:
        """Generate interview preparation materials."""
        pass
    
    @abstractmethod
    async def generate_recruiter_message(
        self,
        recruiter_name: str,
        company_name: str,
        job_title: str,
        message_purpose: str,
        user_background: str,
    ) -> RecruiterMessageResult:
        """Generate outreach message to recruiter."""
        pass
    
    @abstractmethod
    async def extract_job_details(self, job_posting_html: str) -> Dict[str, Any]:
        """Extract structured job details from raw posting."""
        pass
    
    @abstractmethod
    async def generate_follow_up_message(
        self,
        application_status: str,
        days_since_application: int,
        company_name: str,
    ) -> str:
        """Generate follow-up message for applications."""
        pass
