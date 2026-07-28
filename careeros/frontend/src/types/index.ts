/**
 * Generated TypeScript types from FastAPI backend schemas.
 * DO NOT modify manually - these are derived from Pydantic models.
 */

// Enums from auth.py
export enum UserRole {
  USER = "user",
  PREMIUM = "premium",
  ADMIN = "admin",
}

export enum ApplicationStatus {
  DRAFT = "draft",
  APPLIED = "applied",
  INTERVIEW = "interview",
  OFFER = "offer",
  REJECTED = "rejected",
  WITHDRAWN = "withdrawn",
}

export enum JobType {
  FULL_TIME = "full_time",
  PART_TIME = "part_time",
  CONTRACT = "contract",
  FREELANCE = "freelance",
  INTERNSHIP = "internship",
}

export enum RemoteType {
  ONSITE = "onsite",
  REMOTE = "remote",
  HYBRID = "hybrid",
}

// Token schemas
export interface Token {
  access_token: string;
  refresh_token: string;
  token_type?: string;
}

// User schemas
export interface UserBase {
  email: string;
  full_name: string;
}

export interface UserResponse extends UserBase {
  id: string;
  role: UserRole;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
}

export interface UserUpdate {
  full_name?: string;
  email?: string;
}

// Resume schemas
export interface ResumeBase {
  title: string;
  content: string;
}

export interface ResumeCreate extends ResumeBase {
  file_type?: string;
  is_primary?: boolean;
}

export interface ResumeUpdate {
  title?: string;
  content?: string;
  is_primary?: boolean;
  ats_score?: number;
}

export interface ResumeResponse extends ResumeBase {
  id: string;
  user_id: string;
  file_path?: string | null;
  file_type?: string | null;
  ats_score?: number | null;
  is_primary: boolean;
  created_at: string;
  updated_at: string;
}

// Job schemas
export interface JobBase {
  title: string;
  url: string;
  description?: string | null;
  location?: string | null;
  salary_min?: number | null;
  salary_max?: number | null;
  currency?: string;
  job_type: JobType;
  remote_type: RemoteType;
  visa_sponsorship: boolean;
  skills?: string[] | null;
  benefits?: string[] | null;
}

export interface JobCreate extends JobBase {
  company_id: string;
  source: string;
}

export interface JobResponse extends JobBase {
  id: string;
  company_id: string;
  source: string;
  posted_date: string;
  created_at: string;
}

export interface JobFilter {
  query?: string | null;
  skills?: string[] | null;
  remote_type?: RemoteType | null;
  job_type?: JobType | null;
  salary_min?: number | null;
  location?: string | null;
  skip?: number;
  limit?: number;
}

// Company schemas
export interface CompanyBase {
  name: string;
  website?: string | null;
  industry?: string | null;
  size?: string | null;
  location?: string | null;
  description?: string | null;
}

export interface CompanyCreate extends CompanyBase {}

export interface CompanyResponse extends CompanyBase {
  id: string;
  created_at: string;
}

// Application schemas
export interface ApplicationBase {
  notes?: string | null;
  follow_up_date?: string | null;
}

export interface ApplicationCreate extends ApplicationBase {
  job_id: string;
  resume_id?: string | null;
  cover_letter_id?: string | null;
}

export interface ApplicationUpdate {
  status?: ApplicationStatus | null;
  notes?: string | null;
  follow_up_date?: string | null;
  recruiter_id?: string | null;
}

export interface ApplicationResponse extends ApplicationBase {
  id: string;
  user_id: string;
  job_id: string;
  resume_id?: string | null;
  cover_letter_id?: string | null;
  status: ApplicationStatus;
  applied_date?: string | null;
  recruiter_id?: string | null;
  created_at: string;
  updated_at: string;
}

// Cover Letter schemas
export interface CoverLetterBase {
  title: string;
  content: string;
  style?: string;
}

export interface CoverLetterCreate extends CoverLetterBase {
  job_id?: string | null;
}

export interface CoverLetterResponse extends CoverLetterBase {
  id: string;
  user_id: string;
  job_id?: string | null;
  created_at: string;
}

// Recruiter schemas
export interface RecruiterBase {
  name: string;
  email?: string | null;
  linkedin_url?: string | null;
  title?: string | null;
}

export interface RecruiterCreate extends RecruiterBase {
  company_id?: string | null;
}

export interface RecruiterResponse extends RecruiterBase {
  id: string;
  company_id?: string | null;
  created_at: string;
}

// Interview schemas
export interface InterviewBase {
  interview_type: string;
  scheduled_date: string;
  duration_minutes?: number;
  location?: string | null;
  meeting_link?: string | null;
  notes?: string | null;
  preparation_materials?: string[] | null;
}

export interface InterviewCreate extends InterviewBase {
  application_id: string;
}

export interface InterviewResponse extends InterviewBase {
  id: string;
  application_id: string;
  created_at: string;
}

// Task schemas
export interface TaskBase {
  title: string;
  description?: string | null;
  due_date?: string | null;
  task_type?: string;
  related_entity_type?: string | null;
  related_entity_id?: string | null;
}

export interface TaskCreate extends TaskBase {}

export interface TaskUpdate {
  title?: string;
  description?: string;
  due_date?: string;
  is_completed?: boolean;
}

export interface TaskResponse extends TaskBase {
  id: string;
  user_id: string;
  is_completed: boolean;
  completed_at?: string | null;
  created_at: string;
}

// Notification schemas
export interface NotificationBase {
  title: string;
  message: string;
  notification_type?: string;
  action_url?: string | null;
}

export interface NotificationCreate extends NotificationBase {}

export interface NotificationResponse extends NotificationBase {
  id: string;
  user_id: string;
  is_read: boolean;
  read_at?: string | null;
  created_at: string;
}

// Settings schemas
export interface SettingsBase {
  daily_job_limit?: number;
  auto_search_enabled?: boolean;
  email_notifications?: boolean;
  browser_notifications?: boolean;
  preferred_remote_type?: RemoteType;
  preferred_job_types?: JobType[] | null;
  min_salary?: number | null;
  locations?: string[] | null;
}

export interface SettingsUpdate extends SettingsBase {}

export interface SettingsResponse extends SettingsBase {
  id: string;
  user_id: string;
  created_at: string;
  updated_at: string;
}

// Message schemas
export interface MessageBase {
  subject: string;
  content: string;
  message_type?: string;
}

export interface MessageCreate extends MessageBase {
  recruiter_id: string;
}

export interface MessageResponse extends MessageBase {
  id: string;
  user_id: string;
  recruiter_id: string;
  status: string;
  sent_at?: string | null;
  created_at: string;
}

// AI Service schemas (from ai.py)
export interface ResumeAnalysisRequest {
  resume_content: string;
  resume_id?: string | null;
}

export interface ResumeAnalysisResponse {
  ats_score: number;
  extracted_skills: string[];
  extracted_experience: Record<string, unknown>[];
  extracted_education: Record<string, unknown>[];
  extracted_certifications: Record<string, unknown>[];
  keywords: string[];
  improvements: string[];
  formatting_issues: string[];
}

export interface ResumeOptimizationRequest {
  resume_content: string;
  job_description: string;
  preserve_facts?: boolean;
  resume_id?: string | null;
}

export interface ResumeOptimizationResponse {
  optimized_content: string;
  changes_summary: string;
  keyword_improvements: string[];
}

export interface JobMatchRequest {
  resume_content: string;
  job_description: string;
  job_requirements: string[];
  job_skills: string[];
  resume_id?: string | null;
  job_id?: string | null;
}

export interface JobMatchResponse {
  match_percentage: number;
  strengths: string[];
  weaknesses: string[];
  missing_skills: string[];
  learning_recommendations: string[];
  ats_score: number;
}

export interface CoverLetterGenerationRequest {
  resume_content: string;
  job_description: string;
  company_name: string;
  style?: string;
  job_id?: string | null;
}

export interface CoverLetterGenerationResponse {
  content: string;
  style: string;
  word_count: number;
  key_highlights: string[];
}

export interface InterviewPrepRequest {
  job_description: string;
  company_name: string;
  role_level?: string;
  job_id?: string | null;
}

export interface InterviewPrepResponse {
  technical_questions: Record<string, unknown>[];
  behavioral_questions: Record<string, unknown>[];
  star_answers: Record<string, unknown>[];
  company_research: Record<string, unknown>;
  system_design_topics: string[];
  coding_challenges: Record<string, unknown>[];
  salary_negotiation_tips: string[];
}

export interface RecruiterMessageRequest {
  recruiter_name: string;
  company_name: string;
  job_title: string;
  message_purpose: string;
  user_background: string;
  recruiter_id?: string | null;
}

export interface RecruiterMessageResponse {
  subject: string;
  content: string;
  message_type: string;
  follow_up_suggestions: string[];
}

export interface FollowUpMessageRequest {
  application_status: string;
  days_since_application: number;
  company_name: string;
  application_id?: string | null;
}

export interface FollowUpMessageResponse {
  message: string;
  suggested_channel: string;
}

export interface JobDetailsExtractionRequest {
  job_posting_html: string;
  source_url?: string | null;
}

export interface JobDetailsExtractionResponse {
  title?: string | null;
  company?: string | null;
  location?: string | null;
  remote_type?: string | null;
  job_type?: string | null;
  salary_min?: number | null;
  salary_max?: number | null;
  currency?: string;
  description?: string | null;
  requirements: string[];
  skills: string[];
  benefits: string[];
  experience_level?: string | null;
  education_requirements?: string | null;
  visa_sponsorship: boolean;
  application_url?: string | null;
}

// Pagination
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

// Auth request types
export interface UserRegister {
  email: string;
  full_name: string;
  password: string;
}

export interface UserLogin {
  email: string;
  password: string;
}
