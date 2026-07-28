/**
 * Authentication Service - matches FastAPI auth endpoints
 */

import { api, tokenStorage } from "../lib/api-client";
import { ENDPOINTS } from "../lib/api-config";
import type {
  UserRegister,
  UserLogin,
  UserResponse,
  Token,
} from "../types";

export const authService = {
  /**
   * Register a new user
   * POST /api/v1/auth/register
   */
  register: async (data: UserRegister): Promise<UserResponse> => {
    const response = await api.post<UserResponse>(ENDPOINTS.AUTH.REGISTER, data);
    return response.data;
  },

  /**
   * Login and get access/refresh tokens
   * POST /api/v1/auth/login
   */
  login: async (data: UserLogin): Promise<Token> => {
    const response = await api.post<Token>(ENDPOINTS.AUTH.LOGIN, data);
    // Store tokens
    tokenStorage.setTokens(response.data);
    return response.data;
  },

  /**
   * Refresh access token using refresh token
   * POST /api/v1/auth/refresh
   */
  refreshToken: async (refreshToken: string): Promise<Token> => {
    const response = await api.post<Token>(ENDPOINTS.AUTH.REFRESH, {
      refresh_token: refreshToken,
    });
    // Store new tokens
    tokenStorage.setTokens(response.data);
    return response.data;
  },

  /**
   * Get current authenticated user
   * GET /api/v1/auth/me
   */
  getCurrentUser: async (): Promise<UserResponse> => {
    const response = await api.get<UserResponse>(ENDPOINTS.AUTH.ME);
    return response.data;
  },

  /**
   * Logout - clear tokens
   */
  logout: (): void => {
    tokenStorage.clearTokens();
    if (typeof window !== "undefined") {
      window.dispatchEvent(new CustomEvent("auth:logout"));
    }
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated: (): boolean => {
    return tokenStorage.getAccessToken() !== null;
  },

  /**
   * Get stored access token
   */
  getToken: (): string | null => {
    return tokenStorage.getAccessToken();
  },
};
