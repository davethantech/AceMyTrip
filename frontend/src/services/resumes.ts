import apiClient from '../lib/api';
import type { ResumeResponse, ResumeCreate, ResumeUpdate } from '@/types';

export const resumesService = {
  /**
   * Get all resumes for current user
   * GET /resumes/
   */
  async getResumes(): Promise<ResumeResponse[]> {
    const response = await apiClient.get<ResumeResponse[]>('/resumes/');
    return response.data;
  },

  /**
   * Get primary resume for current user
   * GET /resumes/primary
   */
  async getPrimaryResume(): Promise<ResumeResponse> {
    const response = await apiClient.get<ResumeResponse>('/resumes/primary');
    return response.data;
  },

  /**
   * Create a new resume
   * POST /resumes/
   */
  async createResume(data: ResumeCreate): Promise<ResumeResponse> {
    const response = await apiClient.post<ResumeResponse>('/resumes/', data);
    return response.data;
  },

  /**
   * Update a resume
   * PUT /resumes/{resume_id}
   */
  async updateResume(
    resumeId: string,
    data: ResumeUpdate
  ): Promise<ResumeResponse> {
    const response = await apiClient.put<ResumeResponse>(`/resumes/${resumeId}`, data);
    return response.data;
  },

  /**
   * Delete a resume
   * DELETE /resumes/{resume_id}
   */
  async deleteResume(resumeId: string): Promise<void> {
    await apiClient.delete(`/resumes/${resumeId}`);
  },

  /**
   * Set a resume as primary
   * POST /resumes/{resume_id}/set-primary
   */
  async setPrimaryResume(resumeId: string): Promise<ResumeResponse> {
    const response = await apiClient.post<ResumeResponse>(`/resumes/${resumeId}/set-primary`);
    return response.data;
  },
};
