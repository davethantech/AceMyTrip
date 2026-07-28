"""AI Service implementation using LangChain and multiple LLM providers."""

import structlog
from typing import Optional, List, Dict, Any
from uuid import UUID

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

from src.domain.interfaces.ai_service import (
    AIServiceInterface,
    JobMatchResult,
    ResumeAnalysisResult,
    CoverLetterGenerationResult,
    InterviewPreparationResult,
    RecruiterMessageResult,
)
from src.shared.utils.config import get_settings

logger = structlog.get_logger()
settings = get_settings()


class JobMatchSchema(BaseModel):
    """Schema for job matching results."""
    match_percentage: float = Field(description="Overall match percentage 0-100")
    strengths: List[str] = Field(description="Candidate strengths for this role")
    weaknesses: List[str] = Field(description="Areas where candidate lacks experience")
    missing_skills: List[str] = Field(description="Skills mentioned in job but not in resume")
    learning_recommendations: List[str] = Field(description="Recommended learning resources")
    ats_score: int = Field(description="ATS compatibility score 0-100")


class ResumeAnalysisSchema(BaseModel):
    """Schema for resume analysis results."""
    ats_score: int = Field(description="ATS compatibility score 0-100")
    extracted_skills: List[str] = Field(description="List of skills found in resume")
    extracted_experience: List[Dict[str, Any]] = Field(description="Work experience entries")
    extracted_education: List[Dict[str, Any]] = Field(description="Education entries")
    extracted_certifications: List[Dict[str, Any]] = Field(description="Certification entries")
    keywords: List[str] = Field(description="Important keywords from resume")
    improvements: List[str] = Field(description="Suggested improvements")
    formatting_issues: List[str] = Field(description="Formatting issues detected")


class CoverLetterSchema(BaseModel):
    """Schema for cover letter generation."""
    content: str = Field(description="Full cover letter content")
    style: str = Field(description="Writing style used")
    word_count: int = Field(description="Number of words in cover letter")
    key_highlights: List[str] = Field(description="Key highlights emphasized")


class InterviewPrepSchema(BaseModel):
    """Schema for interview preparation."""
    technical_questions: List[Dict[str, Any]] = Field(description="Technical questions with answers")
    behavioral_questions: List[Dict[str, Any]] = Field(description="Behavioral questions with STAR answers")
    star_answers: List[Dict[str, Any]] = Field(description="STAR method answer examples")
    company_research: Dict[str, Any] = Field(description="Company research summary")
    system_design_topics: List[str] = Field(description="System design topics to study")
    coding_challenges: List[Dict[str, Any]] = Field(description="Coding challenge suggestions")
    salary_negotiation_tips: List[str] = Field(description="Salary negotiation advice")


class RecruiterMessageSchema(BaseModel):
    """Schema for recruiter message generation."""
    subject: str = Field(description="Email/message subject line")
    content: str = Field(description="Full message content")
    message_type: str = Field(description="Type of message: email, linkedin, etc.")
    follow_up_suggestions: List[str] = Field(description="Follow-up message suggestions")


class AIService(AIServiceInterface):
    """AI Service implementation using LangChain with multiple LLM providers."""
    
    def __init__(self, provider: Optional[str] = None):
        self.provider = provider or settings.AI_PROVIDER
        self.llm = self._get_llm()
        logger.info("AIService initialized", provider=self.provider)
    
    def _get_llm(self):
        """Get the appropriate LLM based on provider setting."""
        if self.provider == "openai":
            return ChatOpenAI(
                model=settings.OPENAI_MODEL,
                temperature=0.3,
                api_key=settings.OPENAI_API_KEY,
            )
        elif self.provider == "anthropic":
            return ChatAnthropic(
                model=settings.ANTHROPIC_MODEL,
                temperature=0.3,
                api_key=settings.ANTHROPIC_API_KEY,
            )
        elif self.provider == "google":
            return ChatGoogleGenerativeAI(
                model=settings.GOOGLE_MODEL,
                temperature=0.3,
                api_key=settings.GOOGLE_API_KEY,
            )
        else:
            # Default to OpenAI-compatible endpoint (OpenRouter, etc.)
            return ChatOpenAI(
                base_url=settings.OPENROUTER_BASE_URL,
                api_key=settings.OPENROUTER_API_KEY,
                model=settings.OPENROUTER_DEFAULT_MODEL,
                temperature=0.3,
            )
    
    async def analyze_resume(self, resume_content: str) -> ResumeAnalysisResult:
        """Analyze a resume and extract structured information."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert resume analyst and ATS (Applicant Tracking System) specialist.
Analyze the provided resume and extract all relevant information. Be thorough and accurate.
Never invent information - only extract what is explicitly present in the resume.

Return your analysis in valid JSON format matching the schema."""),
            ("human", """Please analyze this resume:

{resume}

Extract:
1. ATS compatibility score (0-100) based on formatting, keywords, and structure
2. All skills mentioned (technical, soft, tools, frameworks)
3. Work experience entries with company, title, dates, and achievements
4. Education entries with institution, degree, dates, and GPA if available
5. Certifications with issuer, date, and credential URL if available
6. Important keywords that would match job descriptions
7. Specific improvements to increase ATS score
8. Any formatting issues that might cause ATS parsing problems"""),
        ])
        
        chain = prompt | self.llm.with_structured_output(ResumeAnalysisSchema)
        
        try:
            result = await chain.ainvoke({"resume": resume_content})
            logger.info("Resume analysis completed", ats_score=result.ats_score)
            
            return ResumeAnalysisResult(
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
            raise
    
    async def optimize_resume(
        self, 
        resume_content: str, 
        job_description: str,
        preserve_facts: bool = True
    ) -> str:
        """Optimize resume for a specific job description without inventing experience."""
        preservation_instruction = (
            "CRITICAL: Never invent or fabricate experience, skills, or qualifications. "
            "Only rephrase and reorder existing content to better match the job description. "
            "Highlight relevant experience that already exists. Do not add false information."
        ) if preserve_facts else ""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"""You are an expert resume writer specializing in ATS optimization.
Your task is to optimize the given resume to better match a specific job description.

{preservation_instruction}

Focus on:
1. Reordering sections to highlight most relevant experience first
2. Using keywords from the job description naturally
3. Rewriting bullet points to emphasize relevant achievements
4. Adjusting the professional summary to align with the role
5. Ensuring proper formatting for ATS systems

Return only the optimized resume content in markdown format."""),
            ("human", """JOB DESCRIPTION:
{job_description}

CURRENT RESUME:
{resume}

Please optimize this resume for the job description while maintaining factual accuracy."""),
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        
        try:
            optimized_resume = await chain.ainvoke({
                "job_description": job_description,
                "resume": resume_content,
            })
            logger.info("Resume optimization completed")
            return optimized_resume
        except Exception as e:
            logger.error("Resume optimization failed", error=str(e))
            raise
    
    async def match_job_to_resume(
        self,
        resume_content: str,
        job_description: str,
        job_requirements: List[str],
        job_skills: List[str],
    ) -> JobMatchResult:
        """Calculate compatibility between resume and job posting."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert career matcher. Analyze how well a candidate's resume matches a job posting.
Be objective and honest about both strengths and gaps.
Return your analysis in valid JSON format matching the schema."""),
            ("human", """RESUME:
{resume}

JOB DESCRIPTION:
{job_description}

REQUIRED SKILLS: {required_skills}
PREFERRED SKILLS: {preferred_skills}

Provide:
1. Overall match percentage (0-100)
2. Candidate's strengths for this specific role
3. Weaknesses or areas lacking experience
4. Missing skills that are in the job but not the resume
5. Specific learning recommendations to fill gaps
6. Estimated ATS score"""),
        ])
        
        chain = prompt | self.llm.with_structured_output(JobMatchSchema)
        
        try:
            result = await chain.ainvoke({
                "resume": resume_content,
                "job_description": job_description,
                "required_skills": job_requirements,
                "preferred_skills": job_skills,
            })
            logger.info("Job matching completed", match_percentage=result.match_percentage)
            
            return JobMatchResult(
                match_percentage=result.match_percentage,
                strengths=result.strengths,
                weaknesses=result.weaknesses,
                missing_skills=result.missing_skills,
                learning_recommendations=result.learning_recommendations,
                ats_score=result.ats_score,
            )
        except Exception as e:
            logger.error("Job matching failed", error=str(e))
            raise
    
    async def generate_cover_letter(
        self,
        resume_content: str,
        job_description: str,
        company_name: str,
        style: str = "professional",
    ) -> CoverLetterGenerationResult:
        """Generate a personalized cover letter."""
        style_instructions = {
            "professional": "Write in a formal, professional tone suitable for corporate environments.",
            "friendly": "Write in a warm, approachable tone while maintaining professionalism.",
            "creative": "Write in an engaging, creative tone that shows personality.",
            "concise": "Write in a brief, direct style focusing on key points only.",
            "storytelling": "Write as a narrative story connecting your journey to this role.",
        }
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"""You are an expert cover letter writer. Create compelling, personalized cover letters.
Style guidance: {style_instructions.get(style, style_instructions['professional'])}

The cover letter should:
1. Start with a strong opening that mentions the specific role and company
2. Highlight 2-3 most relevant achievements from the resume
3. Show genuine interest in the company and role
4. Connect past experience to future potential contributions
5. End with a confident call to action

Return your output in valid JSON format matching the schema."""),
            ("human", """RESUME:
{resume}

JOB DESCRIPTION:
{job_description}

COMPANY: {company}
STYLE: {style}

Generate a personalized cover letter for this application."""),
        ])
        
        chain = prompt | self.llm.with_structured_output(CoverLetterSchema)
        
        try:
            result = await chain.ainvoke({
                "resume": resume_content,
                "job_description": job_description,
                "company": company_name,
                "style": style,
            })
            logger.info("Cover letter generated", style=style, word_count=result.word_count)
            
            return CoverLetterGenerationResult(
                content=result.content,
                style=style,
                word_count=result.word_count,
                key_highlights=result.key_highlights,
            )
        except Exception as e:
            logger.error("Cover letter generation failed", error=str(e))
            raise
    
    async def prepare_interview(
        self,
        job_description: str,
        company_name: str,
        role_level: str,
    ) -> InterviewPreparationResult:
        """Generate comprehensive interview preparation materials."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert interview coach. Generate comprehensive interview preparation materials.
Include realistic questions that candidates actually face at top companies.
For behavioral questions, provide complete STAR (Situation, Task, Action, Result) answers.
Return your output in valid JSON format matching the schema."""),
            ("human", """JOB DESCRIPTION:
{job_description}

COMPANY: {company}
ROLE LEVEL: {role_level}

Generate:
1. 8-10 technical questions likely to be asked for this role with model answers
2. 5-7 behavioral questions with complete STAR method answers
3. 3 detailed STAR answer examples the candidate can adapt
4. Company research summary including culture, recent news, products
5. System design topics relevant to this role
6. 3-5 coding challenges similar to what this company asks
7. Salary negotiation tips specific to this company and role level"""),
        ])
        
        chain = prompt | self.llm.with_structured_output(InterviewPrepSchema)
        
        try:
            result = await chain.ainvoke({
                "job_description": job_description,
                "company": company_name,
                "role_level": role_level,
            })
            logger.info("Interview preparation generated", company=company_name)
            
            return InterviewPreparationResult(
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
            raise
    
    async def generate_recruiter_message(
        self,
        recruiter_name: str,
        company_name: str,
        job_title: str,
        message_purpose: str,
        user_background: str,
    ) -> RecruiterMessageResult:
        """Generate outreach message to recruiter."""
        purpose_templates = {
            "initial_outreach": "Initial connection and expressing interest in opportunities",
            "follow_up": "Following up on a submitted application",
            "networking": "Building relationship for future opportunities",
            "referral_request": "Requesting a referral for a specific position",
            "thank_you": "Thank you after an interview or conversation",
        }
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert at crafting recruiter outreach messages.
Create personalized, concise messages that get responses.
Messages should be professional but personable, showing genuine interest.
Return your output in valid JSON format matching the schema."""),
            ("human", """RECRUITER: {recruiter_name}
COMPANY: {company}
JOB TITLE: {job_title}
PURPOSE: {purpose} ({purpose_desc})

CANDIDATE BACKGROUND:
{background}

Generate a compelling outreach message for this scenario."""),
        ])
        
        chain = prompt | self.llm.with_structured_output(RecruiterMessageSchema)
        
        try:
            result = await chain.ainvoke({
                "recruiter_name": recruiter_name,
                "company": company_name,
                "job_title": job_title,
                "purpose": message_purpose,
                "purpose_desc": purpose_templates.get(message_purpose, message_purpose),
                "background": user_background,
            })
            logger.info("Recruiter message generated", purpose=message_purpose)
            
            return RecruiterMessageResult(
                subject=result.subject,
                content=result.content,
                message_type=result.message_type,
                follow_up_suggestions=result.follow_up_suggestions,
            )
        except Exception as e:
            logger.error("Recruiter message generation failed", error=str(e))
            raise
    
    async def extract_job_details(self, job_posting_html: str) -> Dict[str, Any]:
        """Extract structured job details from raw job posting."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert at extracting structured data from job postings.
Parse the job posting and extract all relevant information accurately.
Return ONLY valid JSON with the following structure:
{
    "title": string,
    "company": string,
    "location": string,
    "remote_type": "remote" | "hybrid" | "onsite",
    "job_type": "full_time" | "part_time" | "contract" | "freelance" | "internship",
    "salary_min": number | null,
    "salary_max": number | null,
    "currency": string,
    "description": string,
    "requirements": array of strings,
    "skills": array of strings,
    "benefits": array of strings,
    "experience_level": string,
    "education_requirements": string,
    "visa_sponsorship": boolean,
    "application_url": string | null
}"""),
            ("human", """Extract job details from this posting:

{posting}"""),
        ])
        
        chain = prompt | self.llm | JsonOutputParser()
        
        try:
            result = await chain.ainvoke({"posting": job_posting_html})
            logger.info("Job details extracted", title=result.get("title"))
            return result
        except Exception as e:
            logger.error("Job details extraction failed", error=str(e))
            return {}
    
    async def generate_follow_up_message(
        self,
        application_status: str,
        days_since_application: int,
        company_name: str,
    ) -> str:
        """Generate follow-up message for applications."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert at writing polite, effective follow-up messages.
Create a concise follow-up message that shows continued interest without being pushy.
The message should be appropriate for the time elapsed since application."""),
            ("human", """APPLICATION STATUS: {status}
DAYS SINCE APPLICATION: {days}
COMPANY: {company}

Write a professional follow-up message for this situation.
Keep it under 150 words. Focus on enthusiasm and value proposition."""),
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        
        try:
            message = await chain.ainvoke({
                "status": application_status,
                "days": days_since_application,
                "company": company_name,
            })
            logger.info("Follow-up message generated", days=days_since_application)
            return message
        except Exception as e:
            logger.error("Follow-up message generation failed", error=str(e))
            raise
