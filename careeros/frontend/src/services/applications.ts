/**
 * Applications Service - matches FastAPI applications endpoints
 */

import { api } from "../lib/api-client";
import { ENDPOINTS } from "../lib/api-config";
import type {
  ApplicationResponse,
  ApplicationCreate,
  ApplicationUpdate,
  ApplicationStatus,
} from "../types";

export const applicationService = {
  /**
   * Get all applications for current user
   * GET /api/v1/applications
   */
  getApplications: async (): Promise<ApplicationResponse[]> => {
    const response = await api.get<ApplicationResponse[]>(ENDPOINTS.APPLICATIONS.LIST);
    return response.data;
  },

  /**
   * Get applications by status
   * GET /api/v1/applications/status/:status
   */
  getApplicationsByStatus: async (
    status: ApplicationStatus
  ): Promise<ApplicationResponse[]> => {
    const response = await api.get<ApplicationResponse[]>(
      ENDPOINTS.APPLICATIONS.BY_STATUS(status)
    );
    return response.data;
  },

  /**
   * Create a new job application
   * POST /api/v1/applications
   */
  createApplication: async (
    data: ApplicationCreate
  ): Promise<ApplicationResponse> => {
    const response = await api.post<ApplicationResponse>(
      ENDPOINTS.APPLICATIONS.CREATE,
      data
    );
    return response.data;
  },

  /**
   * Get a specific application by ID
   * GET /api/v1/applications/:id
   */
  getApplication: async (id: string): Promise<ApplicationResponse> => {
    const response = await api.get<ApplicationResponse>(
      ENDPOINTS.APPLICATIONS.DETAIL(id)
    );
    return response.data;
  },

  /**
   * Update an application
   * PATCH /api/v1/applications/:id
   */
  updateApplication: async (
    id: string,
    data: ApplicationUpdate
  ): Promise<ApplicationResponse> => {
    const response = await api.patch<ApplicationResponse>(
      ENDPOINTS.APPLICATIONS.UPDATE(id),
      data
    );
    return response.data;
  },

  /**
   * Delete an application
   * DELETE /api/v1/applications/:id
   */
  deleteApplication: async (id: string): Promise<void> => {
    await api.delete(ENDPOINTS.APPLICATIONS.DELETE(id));
  },
};
