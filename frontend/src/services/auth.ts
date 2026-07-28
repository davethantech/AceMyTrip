import apiClient from '../lib/api';
import type {
  UserRegister,
  UserLogin,
  UserResponse,
  Token,
  UserUpdate,
} from '@/types';

export const authService = {
  /**
   * Register a new user
   * POST /auth/register
   */
  async register(data: UserRegister): Promise<UserResponse> {
    const response = await apiClient.post<UserResponse>('/auth/register', data);
    return response.data;
  },

  /**
   * Login user and get tokens
   * POST /auth/login
   */
  async login(data: UserLogin): Promise<Token> {
    const response = await apiClient.post<Token>('/auth/login', data);
    if (response.data.access_token && response.data.refresh_token) {
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('refresh_token', response.data.refresh_token);
    }
    return response.data;
  },

  /**
   * Refresh access token
   * POST /auth/refresh
   */
  async refreshToken(refreshToken: string): Promise<Token> {
    const response = await apiClient.post<Token>('/auth/refresh', { refresh_token: refreshToken });
    if (response.data.access_token && response.data.refresh_token) {
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('refresh_token', response.data.refresh_token);
    }
    return response.data;
  },

  /**
   * Get current authenticated user
   * GET /auth/me
   */
  async getCurrentUser(): Promise<UserResponse> {
    const response = await apiClient.get<UserResponse>('/auth/me');
    return response.data;
  },

  /**
   * Logout user (client-side only - clear tokens)
   */
  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token');
  },
};
