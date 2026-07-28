/**
 * Resumes Service - matches FastAPI resumes endpoints
 */

import { api } from "../lib/api-client";
import { ENDPOINTS } from "../lib/api-config";
import type {
  ResumeResponse,
  ResumeCreate,
  ResumeUpdate,
} from "../types";

export const resumeService = {
  /**
   * Get all resumes for current user
   * GET /api/v1/resumes
   */
  getResumes: async (): Promise<ResumeResponse[]> => {
    const response = await api.get<ResumeResponse[]>(ENDPOINTS.RESUMES.LIST);
    return response.data;
  },

  /**
   * Get primary resume for current user
   * GET /api/v1/resumes/primary
   */
  getPrimaryResume: async (): Promise<ResumeResponse> => {
    const response = await api.get<ResumeResponse>(ENDPOINTS.RESUMES.PRIMARY);
    return response.data;
  },

  /**
   * Create a new resume
   * POST /api/v1/resumes
   */
  createResume: async (data: ResumeCreate): Promise<ResumeResponse> => {
    const response = await api.post<ResumeResponse>(ENDPOINTS.RESUMES.CREATE, data);
    return response.data;
  },

  /**
   * Update a resume
   * PUT /api/v1/resumes/:id
   */
  updateResume: async (
    id: string,
    data: ResumeUpdate
  ): Promise<ResumeResponse> => {
    const response = await api.put<ResumeResponse>(
      ENDPOINTS.RESUMES.UPDATE(id),
      data
    );
    return response.data;
  },

  /**
   * Delete a resume
   * DELETE /api/v1/resumes/:id
   */
  deleteResume: async (id: string): Promise<void> => {
    await api.delete(ENDPOINTS.RESUMES.DELETE(id));
  },

  /**
   * Set a resume as primary
   * POST /api/v1/resumes/:id/set-primary
   */
  setPrimaryResume: async (id: string): Promise<ResumeResponse> => {
    const response = await api.post<ResumeResponse>(
      ENDPOINTS.RESUMES.SET_PRIMARY(id)
    );
    return response.data;
  },
};
