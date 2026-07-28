/**
 * AI Services - matches FastAPI ai_services endpoints
 */

import { api } from "../lib/api-client";
import { ENDPOINTS } from "../lib/api-config";
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
} from "../types";

export const aiService = {
  /**
   * Analyze a resume and extract structured information with ATS scoring
   * POST /api/v1/ai/analyze-resume
   */
  analyzeResume: async (
    request: ResumeAnalysisRequest
  ): Promise<ResumeAnalysisResponse> => {
    const response = await api.post<ResumeAnalysisResponse>(
      ENDPOINTS.AI.ANALYZE_RESUME,
      request
    );
    return response.data;
  },

  /**
   * Optimize a resume for a specific job description
   * POST /api/v1/ai/optimize-resume
   */
  optimizeResume: async (
    request: ResumeOptimizationRequest
  ): Promise<ResumeOptimizationResponse> => {
    const response = await api.post<ResumeOptimizationResponse>(
      ENDPOINTS.AI.OPTIMIZE_RESUME,
      request
    );
    return response.data;
  },

  /**
   * Calculate compatibility between a resume and job posting
   * POST /api/v1/ai/match-job
   */
  matchJobToResume: async (request: JobMatchRequest): Promise<JobMatchResponse> => {
    const response = await api.post<JobMatchResponse>(
      ENDPOINTS.AI.MATCH_JOB,
      request
    );
    return response.data;
  },

  /**
   * Generate a personalized cover letter for a job application
   * POST /api/v1/ai/generate-cover-letter
   */
  generateCoverLetter: async (
    request: CoverLetterGenerationRequest
  ): Promise<CoverLetterGenerationResponse> => {
    const response = await api.post<CoverLetterGenerationResponse>(
      ENDPOINTS.AI.GENERATE_COVER_LETTER,
      request
    );
    return response.data;
  },

  /**
   * Generate comprehensive interview preparation materials
   * POST /api/v1/ai/prepare-interview
   */
  prepareInterview: async (
    request: InterviewPrepRequest
  ): Promise<InterviewPrepResponse> => {
    const response = await api.post<InterviewPrepResponse>(
      ENDPOINTS.AI.PREPARE_INTERVIEW,
      request
    );
    return response.data;
  },

  /**
   * Generate an outreach message to a recruiter
   * POST /api/v1/ai/generate-recruiter-message
   */
  generateRecruiterMessage: async (
    request: RecruiterMessageRequest
  ): Promise<RecruiterMessageResponse> => {
    const response = await api.post<RecruiterMessageResponse>(
      ENDPOINTS.AI.GENERATE_RECRUITER_MESSAGE,
      request
    );
    return response.data;
  },

  /**
   * Generate a follow-up message for a job application
   * POST /api/v1/ai/generate-follow-up
   */
  generateFollowUp: async (
    request: FollowUpMessageRequest
  ): Promise<FollowUpMessageResponse> => {
    const response = await api.post<FollowUpMessageResponse>(
      ENDPOINTS.AI.GENERATE_FOLLOW_UP,
      request
    );
    return response.data;
  },

  /**
   * Extract structured job details from a raw job posting
   * POST /api/v1/ai/extract-job-details
   */
  extractJobDetails: async (
    request: JobDetailsExtractionRequest
  ): Promise<JobDetailsExtractionResponse> => {
    const response = await api.post<JobDetailsExtractionResponse>(
      ENDPOINTS.AI.EXTRACT_JOB_DETAILS,
      request
    );
    return response.data;
  },
};
