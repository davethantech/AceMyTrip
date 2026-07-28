import apiClient from '../lib/api';
import type { UserResponse, UserUpdate } from '@/types';

export const usersService = {
  /**
   * Get current user profile
   * GET /users/me
   */
  async getCurrentUser(): Promise<UserResponse> {
    const response = await apiClient.get<UserResponse>('/users/me');
    return response.data;
  },

  /**
   * Update current user profile
   * PATCH /users/me
   */
  async updateCurrentUser(data: UserUpdate): Promise<UserResponse> {
    const response = await apiClient.patch<UserResponse>('/users/me', data);
    return response.data;
  },
};
