/**
 * Jobs Service - matches FastAPI jobs endpoints
 */

import { api } from "../lib/api-client";
import { ENDPOINTS } from "../lib/api-config";
import type { JobResponse, JobFilter, JobCreate, RemoteType, JobType } from "../types";

export const jobService = {
  /**
   * Search jobs with filters
   * GET /api/v1/jobs
   */
  searchJobs: async (filters?: {
    query?: string;
    remote_type?: RemoteType;
    job_type?: JobType;
    salary_min?: number;
    location?: string;
    skip?: number;
    limit?: number;
  }): Promise<JobResponse[]> => {
    const params = new URLSearchParams();
    if (filters?.query) params.append("query", filters.query);
    if (filters?.remote_type) params.append("remote_type", filters.remote_type);
    if (filters?.job_type) params.append("job_type", filters.job_type);
    if (filters?.salary_min) params.append("salary_min", filters.salary_min.toString());
    if (filters?.location) params.append("location", filters.location);
    if (filters?.skip !== undefined) params.append("skip", filters.skip.toString());
    if (filters?.limit !== undefined) params.append("limit", filters.limit.toString());

    const response = await api.get<JobResponse[]>(`${ENDPOINTS.JOBS.LIST}?${params.toString()}`);
    return response.data;
  },

  /**
   * Get a specific job by ID
   * GET /api/v1/jobs/:id
   */
  getJob: async (id: string): Promise<JobResponse> => {
    const response = await api.get<JobResponse>(ENDPOINTS.JOBS.DETAIL(id));
    return response.data;
  },

  /**
   * Create a new job (admin only)
   * POST /api/v1/jobs
   */
  createJob: async (data: JobCreate): Promise<JobResponse> => {
    const response = await api.post<JobResponse>(ENDPOINTS.JOBS.CREATE, data);
    return response.data;
  },
};
