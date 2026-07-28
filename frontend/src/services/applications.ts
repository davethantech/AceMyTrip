import apiClient from '../lib/api';
import type { ApplicationResponse, ApplicationCreate, ApplicationUpdate } from '@/types';

export const applicationsService = {
  /**
   * Get all applications for current user
   * GET /applications/
   */
  async getApplications(): Promise<ApplicationResponse[]> {
    const response = await apiClient.get<ApplicationResponse[]>('/applications/');
    return response.data;
  },

  /**
   * Get applications by status
   * GET /applications/status/{status}
   */
  async getApplicationsByStatus(status: string): Promise<ApplicationResponse[]> {
    const response = await apiClient.get<ApplicationResponse[]>(`/applications/status/${status}`);
    return response.data;
  },

  /**
   * Create a new job application
   * POST /applications/
   */
  async createApplication(data: ApplicationCreate): Promise<ApplicationResponse> {
    const response = await apiClient.post<ApplicationResponse>('/applications/', data);
    return response.data;
  },

  /**
   * Get a specific application by ID
   * GET /applications/{app_id}
   */
  async getApplication(appId: string): Promise<ApplicationResponse> {
    const response = await apiClient.get<ApplicationResponse>(`/applications/${appId}`);
    return response.data;
  },

  /**
   * Update an application
   * PATCH /applications/{app_id}
   */
  async updateApplication(
    appId: string,
    data: ApplicationUpdate
  ): Promise<ApplicationResponse> {
    const response = await apiClient.patch<ApplicationResponse>(`/applications/${appId}`, data);
    return response.data;
  },

  /**
   * Delete an application
   * DELETE /applications/{app_id}
   */
  async deleteApplication(appId: string): Promise<void> {
    await apiClient.delete(`/applications/${appId}`);
  },
};
