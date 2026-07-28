import apiClient from '../lib/api';
import type {
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
} from '@/types';

export const aiService = {
  /**
   * Analyze a resume and extract structured information with ATS scoring
   * POST /ai/analyze-resume
   */
  async analyzeResume(data: ResumeAnalysisRequest): Promise<ResumeAnalysisResponse> {
    const response = await apiClient.post<ResumeAnalysisResponse>('/ai/analyze-resume', data);
    return response.data;
  },

  /**
   * Optimize a resume for a specific job description
   * POST /ai/optimize-resume
   */
  async optimizeResume(data: ResumeOptimizationRequest): Promise<ResumeOptimizationResponse> {
    const response = await apiClient.post<ResumeOptimizationResponse>('/ai/optimize-resume', data);
    return response.data;
  },

  /**
   * Calculate compatibility between a resume and job posting
   * POST /ai/match-job
   */
  async matchJobToResume(data: JobMatchRequest): Promise<JobMatchResponse> {
    const response = await apiClient.post<JobMatchResponse>('/ai/match-job', data);
    return response.data;
  },

  /**
   * Generate a personalized cover letter for a job application
   * POST /ai/generate-cover-letter
   */
  async generateCoverLetter(
    data: CoverLetterGenerationRequest
  ): Promise<CoverLetterGenerationResponse> {
    const response = await apiClient.post<CoverLetterGenerationResponse>(
      '/ai/generate-cover-letter',
      data
    );
    return response.data;
  },

  /**
   * Generate comprehensive interview preparation materials
   * POST /ai/prepare-interview
   */
  async prepareInterview(data: InterviewPrepRequest): Promise<InterviewPrepResponse> {
    const response = await apiClient.post<InterviewPrepResponse>('/ai/prepare-interview', data);
    return response.data;
  },

  /**
   * Generate an outreach message to a recruiter
   * POST /ai/generate-recruiter-message
   */
  async generateRecruiterMessage(
    data: RecruiterMessageRequest
  ): Promise<RecruiterMessageResponse> {
    const response = await apiClient.post<RecruiterMessageResponse>(
      '/ai/generate-recruiter-message',
      data
    );
    return response.data;
  },

  /**
   * Generate a follow-up message for a job application
   * POST /ai/generate-follow-up
   */
  async generateFollowUpMessage(data: FollowUpMessageRequest): Promise<FollowUpMessageResponse> {
    const response = await apiClient.post<FollowUpMessageResponse>('/ai/generate-follow-up', data);
    return response.data;
  },

  /**
   * Extract structured job details from a raw job posting
   * POST /ai/extract-job-details
   */
  async extractJobDetails(
    data: JobDetailsExtractionRequest
  ): Promise<JobDetailsExtractionResponse> {
    const response = await apiClient.post<JobDetailsExtractionResponse>(
      '/ai/extract-job-details',
      data
    );
    return response.data;
  },
};
