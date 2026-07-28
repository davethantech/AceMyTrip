import apiClient from '../lib/api';
import type { JobResponse, JobFilter } from '@/types';

export const jobsService = {
  /**
   * Search jobs with filters
   * GET /jobs/
   */
  async searchJobs(params?: {
    query?: string;
    remote_type?: string;
    job_type?: string;
    salary_min?: number;
    location?: string;
    skip?: number;
    limit?: number;
  }): Promise<JobResponse[]> {
    const response = await apiClient.get<JobResponse[]>('/jobs/', { params });
    return response.data;
  },

  /**
   * Get a specific job by ID
   * GET /jobs/{job_id}
   */
  async getJob(jobId: string): Promise<JobResponse> {
    const response = await apiClient.get<JobResponse>(`/jobs/${jobId}`);
    return response.data;
  },
};
