/**
 * Users Service - matches FastAPI users endpoints
 */

import { api } from "../lib/api-client";
import { ENDPOINTS } from "../lib/api-config";
import type { UserResponse, UserUpdate } from "../types";

export const userService = {
  /**
   * Get current user profile
   * GET /api/v1/users/me
   */
  getProfile: async (): Promise<UserResponse> => {
    const response = await api.get<UserResponse>(ENDPOINTS.USERS.ME);
    return response.data;
  },

  /**
   * Update current user profile
   * PATCH /api/v1/users/me
   */
  updateProfile: async (data: UserUpdate): Promise<UserResponse> => {
    const response = await api.patch<UserResponse>(ENDPOINTS.USERS.UPDATE, data);
    return response.data;
  },
};
