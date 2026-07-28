// Types derived from backend Pydantic schemas
// DO NOT modify - these must match the backend exactly

export type UserRole = 'user' | 'premium' | 'admin';

export type ApplicationStatus = 
  | 'draft' 
  | 'applied' 
  | 'interview' 
  | 'offer' 
  | 'rejected' 
  | 'withdrawn';

export type JobType = 
  | 'full_time' 
  | 'part_time' 
  | 'contract' 
  | 'freelance' 
  | 'internship';

export type RemoteType = 
  | 'onsite' 
  | 'remote' 
  | 'hybrid';

// Token schemas
export interface Token {
  access_token: string;
  refresh_token: string;
  token_type?: string;
}

export interface TokenData {
  user_id?: string;
  email?: string;
}

// User schemas
export interface UserBase {
  email: string;
  full_name: string;
}

export interface UserCreate extends UserBase {
  password: string;
}

export interface UserRegister extends UserCreate {}

export interface UserUpdate {
  full_name?: string;
  email?: string;
}

export interface UserResponse extends UserBase {
  id: string;
  role: UserRole;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

// OAuth schemas
export interface OAuthCallback {
  code: string;
  state?: string;
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
  file_path?: string;
  file_type?: string;
  ats_score?: number;
  is_primary: boolean;
  created_at: string;
  updated_at: string;
}

// Job schemas
export interface JobBase {
  title: string;
  url: string;
  description?: string;
  location?: string;
  salary_min?: number;
  salary_max?: number;
  currency?: string;
  job_type: JobType;
  remote_type: RemoteType;
  visa_sponsorship: boolean;
  skills?: string[];
  benefits?: string[];
}

export interface JobCreate extends JobBase {
  company_id: string;
  source: string;
}

export interface JobFilter {
  query?: string;
  skills?: string[];
  remote_type?: RemoteType;
  job_type?: JobType;
  salary_min?: number;
  location?: string;
  skip?: number;
  limit?: number;
}

export interface JobResponse extends JobBase {
  id: string;
  company_id: string;
  source: string;
  posted_date: string;
  created_at: string;
}

// Company schemas
export interface CompanyBase {
  name: string;
  website?: string;
  industry?: string;
  size?: string;
  location?: string;
  description?: string;
}

export interface CompanyCreate extends CompanyBase {}

export interface CompanyResponse extends CompanyBase {
  id: string;
  created_at: string;
}

// Application schemas
export interface ApplicationBase {
  notes?: string;
  follow_up_date?: string;
}

export interface ApplicationCreate extends ApplicationBase {
  job_id: string;
  resume_id?: string;
  cover_letter_id?: string;
}

export interface ApplicationUpdate {
  status?: ApplicationStatus;
  notes?: string;
  follow_up_date?: string;
  recruiter_id?: string;
}

export interface ApplicationResponse extends ApplicationBase {
  id: string;
  user_id: string;
  job_id: string;
  resume_id?: string;
  cover_letter_id?: string;
  status: ApplicationStatus;
  applied_date?: string;
  recruiter_id?: string;
  created_at: string;
  updated_at: string;
}

// Cover Letter schemas
export interface CoverLetterBase {
  title: string;
  content: string;
  style: string;
}

export interface CoverLetterCreate extends CoverLetterBase {
  job_id?: string;
}

export interface CoverLetterResponse extends CoverLetterBase {
  id: string;
  user_id: string;
  job_id?: string;
  created_at: string;
}

// Recruiter schemas
export interface RecruiterBase {
  name: string;
  email?: string;
  linkedin_url?: string;
  title?: string;
}

export interface RecruiterCreate extends RecruiterBase {
  company_id?: string;
}

export interface RecruiterResponse extends RecruiterBase {
  id: string;
  company_id?: string;
  created_at: string;
}

// Interview schemas
export interface InterviewBase {
  interview_type: string;
  scheduled_date: string;
  duration_minutes?: number;
  location?: string;
  meeting_link?: string;
  notes?: string;
  preparation_materials?: string[];
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
  description?: string;
  due_date?: string;
  task_type?: string;
  related_entity_type?: string;
  related_entity_id?: string;
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
  completed_at?: string;
  created_at: string;
}

// Notification schemas
export interface NotificationBase {
  title: string;
  message: string;
  notification_type?: string;
  action_url?: string;
}

export interface NotificationCreate extends NotificationBase {}

export interface NotificationResponse extends NotificationBase {
  id: string;
  user_id: string;
  is_read: boolean;
  read_at?: string;
  created_at: string;
}

// Settings schemas
export interface SettingsBase {
  daily_job_limit?: number;
  auto_search_enabled?: boolean;
  email_notifications?: boolean;
  browser_notifications?: boolean;
  preferred_remote_type?: RemoteType;
  preferred_job_types?: JobType[];
  min_salary?: number;
  locations?: string[];
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
  sent_at?: string;
  created_at: string;
}

// Audit Log schemas
export interface AuditLogResponse {
  id: string;
  user_id?: string;
  action: string;
  entity_type: string;
  entity_id?: string;
  old_values?: Record<string, any>;
  new_values?: Record<string, any>;
  ip_address?: string;
  created_at: string;
}

// Pagination
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

// AI Service schemas (from ai.py)
export interface ResumeAnalysisRequest {
  resume_content: string;
  resume_id?: string;
}

export interface ResumeAnalysisResponse {
  ats_score: number;
  extracted_skills: string[];
  extracted_experience: Record<string, any>[];
  extracted_education: Record<string, any>[];
  extracted_certifications: Record<string, any>[];
  keywords: string[];
  improvements: string[];
  formatting_issues: string[];
}

export interface ResumeOptimizationRequest {
  resume_content: string;
  job_description: string;
  preserve_facts?: boolean;
  resume_id?: string;
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
  resume_id?: string;
  job_id?: string;
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
  job_id?: string;
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
  job_id?: string;
}

export interface InterviewPrepResponse {
  technical_questions: Record<string, any>[];
  behavioral_questions: Record<string, any>[];
  star_answers: Record<string, any>[];
  company_research: Record<string, any>;
  system_design_topics: string[];
  coding_challenges: Record<string, any>[];
  salary_negotiation_tips: string[];
}

export interface RecruiterMessageRequest {
  recruiter_name: string;
  company_name: string;
  job_title: string;
  message_purpose: string;
  user_background: string;
  recruiter_id?: string;
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
  application_id?: string;
}

export interface FollowUpMessageResponse {
  message: string;
  suggested_channel: string;
}

export interface JobDetailsExtractionRequest {
  job_posting_html: string;
  source_url?: string;
}

export interface JobDetailsExtractionResponse {
  title?: string;
  company?: string;
  location?: string;
  remote_type?: string;
  job_type?: string;
  salary_min?: number;
  salary_max?: number;
  currency?: string;
  description?: string;
  requirements: string[];
  skills: string[];
  benefits: string[];
  experience_level?: string;
  education_requirements?: string;
  visa_sponsorship: boolean;
  application_url?: string;
}
